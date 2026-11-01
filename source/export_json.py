import sys, json; sys.path.insert(0,"data")
from model import JUR, COMP, F, FEAT, FEAT_EVID, BUDGET, FX_DEFAULT, FEAS, DIMS
from sources import S
from graph import G
ids=set(S)
for j,(n,e) in G.items():
    nid={x[0] for x in n}
    for a,b,r,s in e: assert a in nid and b in nid and s in ids,(j,a,b,s)
d={
 "jur":[dict(code=c,name=n,group=g,inst=i,est=e) for c,n,g,i,e in JUR],
 "dims":DIMS,
 "facts":[dict(j=j,dim=d,text=t,src=s) for j,d,t,s in F],
 "features":[dict(code=c,label=l,defn=df,codes=m,evid=FEAT_EVID.get(c,"")) for c,l,df,m in FEAT],
 "comp":COMP,
 "budget":[dict(j=j,label=l,amt=a,cur=c,usd=round(a*FX_DEFAULT[c]),basis=b,src=s[0]) for j,l,a,c,b,s in BUDGET],
 "fx":FX_DEFAULT,
 "feas":[dict(factor=f,text=t,reading=r,src=s.split(";")) for f,t,r,s in FEAS],
 "sources":{k:dict(title=v[0],pub=v[1],date=v[2],tier=v[3],url=v[4]) for k,v in S.items()},
 "graph":{j:dict(nodes=[dict(id=a,label=b,kind=c) for a,b,c in n],edges=[dict(a=a,b=b,rel=r,src=s) for a,b,r,s in e]) for j,(n,e) in G.items()},
}
json.dump(d,open("app/src/data.json","w"),ensure_ascii=False)
print("ok",len(d["facts"]))
