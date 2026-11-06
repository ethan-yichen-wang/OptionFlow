"""Explicit weighted FWL/CGM estimator with full-rank CRV1 and FE recovery."""
import numpy as np
import pandas as pd
from scipy import stats
import pyhdfe

def grouped(values,ids,size=None):
    values=np.asarray(values);size=int(ids.max())+1 if size is None else size
    out=np.zeros((size,)+values.shape[1:],dtype=float)
    np.add.at(out,ids,values)
    return out

def singletons(frame,effects):
    d=frame.copy();rounds=[]
    while len(d):
        bad=pd.Series(False,index=d.index)
        for col in effects:bad|=d.groupby(col)[col].transform('size').eq(1)
        if not bad.any():break
        rounds.append(int(bad.sum()));d=d.loc[~bad].copy()
    return d.reset_index(drop=True),rounds

def holm(pvalues):
    p=np.asarray(pvalues,dtype=float);p=np.where(np.isfinite(p),p,1.)
    order=np.argsort(p,kind='stable');out=np.empty(len(p))
    out[order]=np.minimum(1.,np.maximum.accumulate((len(p)-np.arange(len(p)))*p[order]))
    return out

def fit(frame,x,target='y',time='outcome_date',two_way=True,weight=None):
    effects=['commodity']+([time] if two_way else [])
    finite=np.isfinite(frame[x+[target]].to_numpy(dtype=float)).all(axis=1)
    if weight:finite&=frame[weight].gt(0).to_numpy()&np.isfinite(frame[weight].to_numpy(dtype=float))
    d,rounds=singletons(frame.loc[finite],effects)
    if not len(d):raise ValueError('No estimable observations')
    # Month weights are defined on the final (post-singleton) product-day keys.
    if weight=='month_weight':d[weight]=1./d.groupby(['commodity','date']).date.transform('size')
    w=d[weight].to_numpy(dtype=float) if weight else np.ones(len(d))
    ids=np.column_stack([pd.factorize(d[col],sort=True)[0] for col in effects])
    algorithm=pyhdfe.create(ids,drop_singletons=False,compute_degrees=True,degrees_method='pairwise' if two_way else None,options={'tol':1e-12} if two_way else None)
    z=algorithm.residualize(d[[target]+x].to_numpy(dtype=float),weights=w[:,None] if weight else None)
    Y=z[:,0];X=z[:,1:]
    if np.linalg.matrix_rank(X*np.sqrt(w[:,None]))!=len(x):raise ValueError('Nonidentified slopes: '+str(x))
    bread=np.linalg.inv(X.T@(w[:,None]*X))
    beta=np.linalg.lstsq(X*np.sqrt(w[:,None]),Y*np.sqrt(w),rcond=None)[0];u=Y-X@beta
    n=len(d);rank_fe=int(algorithm.degrees);k_full=rank_fe+len(x);k_diag=1+len(x)
    correction=(n-1)/(n-k_full)
    scores=w[:,None]*X*u[:,None]
    groups=[ids[:,0]]
    if two_way:
        groups+=[ids[:,1],pd.factorize(pd.MultiIndex.from_frame(d[['commodity',time]]),sort=True)[0]]
    meats=[];counts=[]
    for group in groups:
        score=grouped(scores,group);g=len(score);counts.append(g)
        meats.append((score.T@score)*g/(g-1)*correction)
    cov1=bread@meats[0]@bread
    cov=bread@(meats[0]+meats[1]-meats[2])@bread if two_way else cov1
    cov=(cov+cov.T)/2
    diag=np.diag(cov);se=np.sqrt(np.where(diag>=0,diag,np.nan))
    dof=min(counts[:2])-1 if two_way else counts[0]-1
    t=np.divide(beta,se,out=np.full_like(beta,np.nan),where=se>0)
    p=2*stats.t.sf(np.abs(t),dof);critical=stats.t.ppf(.975,dof)
    sst=float(Y@(w*Y));sse=float(u@(w*u))
    meta={'N_before':len(frame),'N_finite':int(finite.sum()),'N':n,'singleton_removed':sum(rounds),
          'singleton_rounds':rounds,'G':counts[0],'T':d[time].nunique(),'clusters':counts,'K_full':k_full,
          'rank_FE':rank_fe,'K_diag':k_diag,'df_test':dof,'CRV1_full_factor':correction,
          'CRV1_diag_factor':(n-1)/(n-k_diag),'cov_min_eigenvalue':float(np.linalg.eigvalsh(cov).min()),
          'cov_PSD':bool(np.linalg.eigvalsh(cov).min()>=-1e-12*max(float(np.linalg.norm(cov)),1e-30)),
          'within_R2':1-sse/sst if sst>0 else None,'weighted':weight is not None,'target':target,'time_FE':time if two_way else None,
          'estimable_slopes':len(x),'weighted_SSE':sse}
    table=pd.DataFrame({'term':x,'b':beta,'se':se,'t':t,'p_unadjusted':p,'ci95_lower':beta-critical*se,'ci95_upper':beta+critical*se,
                        'se_oneway':np.sqrt(np.maximum(np.diag(cov1),0))})
    return {'frame':d,'x':x,'beta':beta,'cov':cov,'cov_oneway':cov1,'meta':meta,'table':table,
            'algorithm':algorithm,'X':X,'Y':Y,'u':u,'w':w,'bread':bread,'ids':ids,'target':target,'time':time,'two_way':two_way}

def recover_fixed_effects(result):
    d=result['frame'];w=result['w'];ids=result['ids'];x=result['x']
    v=d[result['target']].to_numpy(dtype=float)-d[x].to_numpy(dtype=float)@result['beta']
    g=int(ids[:,0].max())+1;a=np.zeros(g)
    h=int(ids[:,1].max())+1 if result['two_way'] else 1;b=np.zeros(h)
    wg=np.bincount(ids[:,0],weights=w,minlength=g)
    wh=np.bincount(ids[:,1],weights=w,minlength=h) if result['two_way'] else None
    for iteration in range(100000):
        new_a=np.bincount(ids[:,0],weights=w*(v-(b[ids[:,1]] if result['two_way'] else 0)),minlength=g)/wg
        if result['two_way']:
            new_b=np.bincount(ids[:,1],weights=w*(v-new_a[ids[:,0]]),minlength=h)/wh
            shift=np.average(new_b,weights=wh);new_b-=shift;new_a+=shift
        else:new_b=b
        change=max(np.max(np.abs(new_a-a)),np.max(np.abs(new_b-b)))
        a,b=new_a,new_b
        if change<1e-13:break
    else:raise RuntimeError('FE recovery did not converge')
    reconstructed=v-a[ids[:,0]]-(b[ids[:,1]] if result['two_way'] else 0)
    assert np.max(np.abs(reconstructed-result['u']))<1e-9,'Recovered FE mismatch'
    commodities=sorted(d.commodity.unique())
    return {'slopes':dict(zip(x,map(float,result['beta']))),'commodity_intercepts':dict(zip(commodities,map(float,a))),
            'date_effects':dict(zip([pd.Timestamp(t).isoformat() for t in sorted(d[result['time']].unique())],map(float,b))) if result['two_way'] else {},
            'normalization':'weighted_mean_date_effect_zero; intercept_in_commodity_effect',
            'recovery_iterations':iteration+1,'training_commodity_counts':d.groupby('commodity').size().to_dict(),
            'metadata':result['meta']}

def raw_prediction(model,features):
    alpha=features.commodity.map(model['commodity_intercepts']).to_numpy(dtype=float)
    out=alpha.copy()
    for name,beta in model['slopes'].items():out+=features[name].to_numpy(dtype=float)*beta
    assert np.isfinite(out).all(),'Unknown commodity or nonfinite prediction'
    return out

def wild_cluster_restricted(result,term,reps=10000,seed=20261106):
    """Exact linear WCR-t via precomputed projected residual/group matrices.

    Each draw equals refitting the full FE model to restricted fit + cluster
    sign * restricted residual. All FE are reprojected, not held fixed.
    """
    assert np.all(result['w']==1),'Core WCR is unweighted only'
    j=result['x'].index(term);X=result['X'];Y=result['Y'];gids=result['ids'][:,0]
    n,k=X.shape;G=int(gids.max())+1
    keep=[q for q in range(k) if q!=j]
    restricted=Y-X[:,keep]@np.linalg.lstsq(X[:,keep],Y,rcond=None)[0]
    instruments=np.zeros((n,G));instruments[np.arange(n),gids]=restricted
    projected=result['algorithm'].residualize(instruments)
    shifts=result['bread']@(X.T@projected)
    residual_matrix=projected-X@shifts
    influence=X@result['bread'][:,j]
    A=grouped(influence[:,None]*residual_matrix,gids)
    factor=G/(G-1)*result['meta']['CRV1_full_factor']
    rng=np.random.default_rng(seed)
    signs=rng.choice(np.array([-1.,1.]),size=(G,reps))
    numerators=shifts[j]@signs
    variances=factor*np.sum((A@signs)**2,axis=0)
    assert np.all(variances>0)
    tstar=numerators/np.sqrt(variances)
    observed=float(result['beta'][j]/np.sqrt(result['cov_oneway'][j,j]))
    count=int((np.abs(tstar)>=abs(observed)).sum())
    return {'term':term,'p_wild_unadjusted':(count+1)/(reps+1),'t_oneway_observed':observed,
            'extreme_draws':count,'reps':reps,'seed':seed,'weights':'Rademacher','rng':'numpy PCG64',
            'null_imposed':True,'p_rule':'(exceedances+1)/(B+1)','scope':'descriptive_supplement_not_two_way_inference',
            '_tstar':tstar,'_signs':signs}
