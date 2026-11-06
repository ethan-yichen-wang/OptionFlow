"""Pure scoring operations. No data loading, fitting, tuning or model selection."""
import hashlib
import numpy as np
import pandas as pd

PREDICTIONS={
 'absolute':{'baseline':'p_O0','C':'p_OC','G':'p_OG'},
 'relative':{'baseline':'p_B_FE','C':'p_C','G':'p_G'},
}
LABELS={'absolute':{'baseline':'O0','C':'OC','G':'OG'},'relative':{'baseline':'R0','C':'RC','G':'RG'}}

def circular_blocks(dates,block_length,repetitions,seed):
    if dates<1 or block_length<1 or repetitions<1:raise ValueError('Invalid bootstrap sizes')
    rng=np.random.default_rng(seed)
    starts=rng.integers(0,dates,size=(repetitions,(dates+block_length-1)//block_length),dtype=np.int64)
    indices=((starts[:,:,None]+np.arange(block_length))%dates).reshape(repetitions,-1)[:,:dates]
    return starts.astype(np.int32),indices.astype(np.int32)

def index_digest(indices):return hashlib.sha256(np.asarray(indices).tobytes(order='C')).hexdigest()

def r2_os(model_mse,baseline_mse):
    model=np.asarray(model_mse,dtype=float);base=np.asarray(baseline_mse,dtype=float)
    shape=np.broadcast_shapes(model.shape,base.shape)
    ratio=np.full(shape,np.nan,dtype=float)
    np.divide(model,base,out=ratio,where=base>0)
    return 1-ratio

def prepare_cells(joined):
    """Apply one explicit scoring operator per universe/target on common dates."""
    if joined.duplicated(['commodity','outcome_date']).any():raise ValueError('Duplicate scoring key')
    universes={u:joined.loc[joined[u]].copy() for u in ['U_all','U_120']}
    date_sets=[]
    for frame in universes.values():
        size=frame.groupby('outcome_date').commodity.nunique()
        date_sets.append(set(size[size.ge(2)].index))
    dates=sorted(date_sets[0]&date_sets[1])
    if not dates:raise ValueError('No common dates with at least two commodities')
    cells={};means=[]
    for universe,frame in universes.items():
        frame=frame[frame.outcome_date.isin(dates)].copy().sort_values(['outcome_date','commodity']).reset_index(drop=True)
        for target in ['absolute','relative']:
            cols=[c for c in ['entity','commodity','exchange','product','date','outcome_date','training_rows'] if c in frame]
            t=frame[cols].copy();t['universe']=universe;t['target']=target
            mapping=PREDICTIONS[target]
            if target=='relative':
                source=['y']+list(mapping.values())
                group_means=frame.groupby('outcome_date')[source].transform('mean')
                t['target_value']=frame.y-group_means.y
                for key,col in mapping.items():t['pred_'+key]=frame[col]-group_means[col]
                center=frame.groupby('outcome_date')[source].mean().reset_index()
                center=center.rename(columns={v:'mean_'+v for v in source})
                center['universe']=universe;means.append(center)
            else:
                t['target_value']=frame.y
                for key,col in mapping.items():t['pred_'+key]=frame[col]
                t['pred_training_mean']=frame.p_training_mean
            t['pred_zero']=0.
            required=['target_value','pred_baseline','pred_C','pred_G']
            if not np.isfinite(t[required]).all().all():raise ValueError('Nonfinite scored target or sealed prediction')
            cells[(target,universe)]=t
    return cells,pd.concat(means,ignore_index=True),pd.DatetimeIndex(dates)

def daily_losses(frame):
    pieces=[]
    target=frame.target.iloc[0];universe=frame.universe.iloc[0]
    for col in [c for c in frame if c.startswith('pred_')]:
        predictor=col[5:]
        errors=frame.target_value.to_numpy()-frame[col].to_numpy()
        loss=pd.DataFrame({'outcome_date':frame.outcome_date.to_numpy(),'sq':errors**2,'absolute':np.abs(errors)})
        daily=loss.groupby('outcome_date',sort=True).agg(n=('sq','size'),MSE=('sq','mean'),MAE=('absolute','mean')).reset_index()
        daily['target']=target;daily['universe']=universe;daily['predictor']=predictor
        pieces.append(daily)
    return pd.concat(pieces,ignore_index=True)

def statistics(frame,model='C',baseline='baseline',weighting='equal_day'):
    em=frame.target_value.to_numpy()-frame['pred_'+model].to_numpy()
    eb=frame.target_value.to_numpy()-frame['pred_'+baseline].to_numpy()
    losses=pd.DataFrame({'outcome_date':frame.outcome_date.to_numpy(),'mse_m':em**2,'mse_b':eb**2,'mae_m':np.abs(em),'mae_b':np.abs(eb)})
    per_day=losses.groupby('outcome_date',sort=True).mean()
    result=per_day.mean() if weighting=='equal_day' else losses.drop(columns='outcome_date').mean()
    if weighting not in {'equal_day','equal_row'}:raise ValueError('Unknown weighting')
    return {
      'model_MSE':float(result.mse_m),'baseline_MSE':float(result.mse_b),
      'model_RMSE':float(np.sqrt(result.mse_m)),'baseline_RMSE':float(np.sqrt(result.mse_b)),
      'model_MAE':float(result.mae_m),'baseline_MAE':float(result.mae_b),
      'Delta_MSE':float(result.mse_b-result.mse_m),
      'R2_OS':float(r2_os(result.mse_m,result.mse_b)),
      'rows':len(frame),'products':frame.commodity.nunique(),'dates':frame.outcome_date.nunique(),
    },per_day

def percentile_interval(values):
    values=np.asarray(values,dtype=float)
    # Do not silently drop bootstrap draws with zero baseline MSE.
    if not np.isfinite(values).all():return np.nan,np.nan
    lo,hi=np.quantile(values,[.025,.975],method='linear')
    return float(lo),float(hi)

def bootstrap_statistics(per_day,indices):
    if indices.shape[1]!=len(per_day):raise ValueError('Index/date count mismatch')
    mb=per_day.mse_b.to_numpy()[indices].mean(axis=1)
    mm=per_day.mse_m.to_numpy()[indices].mean(axis=1)
    return {'Delta_MSE':mb-mm,'R2_OS':r2_os(mm,mb),'index_digest':index_digest(indices)}

def primary_scores(cells,indices):
    rows=[];draws=[];comparisons=[]
    for (target,universe),frame in cells.items():
        for model in ['C','G']:
            summary,daily=statistics(frame,model)
            boots=bootstrap_statistics(daily,indices)
            cid=target+'__'+universe+'__'+LABELS[target][model]
            row={'comparison':cid,'target':target,'universe':universe,'model':LABELS[target][model],
                 'baseline':LABELS[target]['baseline'],'weighting':'equal_day_then_equal_product',**summary,
                 'Delta_MSE_ci95_lower':percentile_interval(boots['Delta_MSE'])[0],
                 'Delta_MSE_ci95_upper':percentile_interval(boots['Delta_MSE'])[1],
                 'R2_OS_ci95_lower':percentile_interval(boots['R2_OS'])[0],
                 'R2_OS_ci95_upper':percentile_interval(boots['R2_OS'])[1],
                 'shared_index_digest':boots['index_digest'],'bootstrap_repetitions':len(indices),
                 'interval_scope':'pointwise_conditional_percentile_not_familywise','confirmatory_pvalue':False}
            rows.append(row)
            draws.append(pd.DataFrame({'comparison':cid,'replicate':np.arange(len(indices)),
                                       'Delta_MSE':boots['Delta_MSE'],'R2_OS':boots['R2_OS']}))
            z=daily.reset_index();z['comparison']=cid;z['target']=target;z['universe']=universe
            z['model']=LABELS[target][model];z['baseline']=LABELS[target]['baseline'];z['Delta_MSE']=z.mse_b-z.mse_m
            comparisons.append(z)
    return pd.DataFrame(rows),pd.concat(draws,ignore_index=True),pd.concat(comparisons,ignore_index=True)

def secondary_scores(cells):
    rows=[]
    for (target,universe),frame in cells.items():
        variants=[('equal_row_primary_benchmark','baseline','equal_row')]
        if target=='absolute':variants += [('absolute_zero_benchmark','zero','equal_day'),('absolute_training_product_mean_benchmark','training_mean','equal_day')]
        else:variants += [('relative_zero_benchmark','zero','equal_day')]
        for variant,baseline,weighting in variants:
            for model in ['C','G']:
                summary,_=statistics(frame,model,baseline,weighting)
                rows.append({'target':target,'universe':universe,'model':LABELS[target][model],
                    'variant':variant,'baseline':baseline,'weighting':weighting,**summary,
                    'role':'prespecified_secondary_descriptive_no_additional_tests'})
    return pd.DataFrame(rows)
