import json,os,sys,urllib.request,urllib.error
EU=os.environ.get("MAKEFUN_ENV_URL")or sys.exit(1)
Z={"N":[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)],"K":[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)],"B":[(1,1),(1,-1),(-1,1),(-1,-1)],"R":[(1,0),(-1,0),(0,1),(0,-1)]}
Z["Q"]=Z["B"]+Z["R"]
X="BRQ"
V={"P":100,"N":320,"B":330,"R":500,"Q":900,"K":0}
Y=[0,1,2,3,3,2,1,0]
O=7200
N=0
J=None
W=J
U="."
AB="abcdefgh"
LM="legal_moves"
def B(f,r):return 0<=f<8 and 0<=r<8
def M(p,w):return p!=U and p.isupper()==w
def F(p,w):return p!=U and p.isupper()!=w
def P(fen):
 pl,side,_,ep=fen.split()[:4]
 bd=[U]*64
 for i,row in enumerate(pl.split("/")):
  rk=7-i;fl=0
  for ch in row:
   if ch.isdigit():fl+=int(ch)
   else:bd[rk*8+fl]=ch;fl+=1
 e=-1 if ep=="-" else AB.index(ep[0])+(int(ep[1])-1)*8
 return bd,side,e
def R(bd,sq,w,t):
 f0,r0=sq%8,sq//8;out=[]
 for df,dr in Z[t]:
  f,r=f0+df,r0+dr
  while B(f,r):
   if M(bd[to:=r*8+f],w):break
   out.append(to)
   if bd[to]!=U or t not in X:break
   f+=df;r+=dr
 return out
def PZ(ms,sq,to,r,pr):
 if r==pr:
  for q in"QRBN":ms.append((sq,to,q,J))
 else:ms.append((sq,to,J,J))
def G(bd,side,ep):
 w=side=="w";ms=[]
 for sq in range(64):
  if(p:=bd[sq])==U or not M(p,w):continue
  t=p.upper()
  if t in "NKBRQ":
   for to in R(bd,sq,w,t):ms.append((sq,to,J,J))
  else:
   f0,r0=sq%8,sq//8;d=1 if w else-1;sr=1 if w else 6;pr=7 if w else 0;r=r0+d
   if B(f0,r) and bd[r*8+f0]==U:
    to=r*8+f0
    PZ(ms,sq,to,r,pr)
    if r0==sr:
     r2=r0+2*d
     if bd[r2*8+f0]==U:ms.append((sq,r2*8+f0,J,True))
   for df in(-1,1):
    f=f0+df
    if not B(f,r):continue
    to=r*8+f
    if F(bd[to],w):PZ(ms,sq,to,r,pr)
    elif to==ep:ms.append((sq,to,J,"e"))
 return ms
def A(bd,sq,bw):
 f0,r0=sq%8,sq//8;d=-1 if bw else 1
 for df in(-1,1):
  f,r=f0+df,r0+d
  if B(f,r) and bd[r*8+f]==("P" if bw else "p"):return True
 for t in "NKBRQ":
  for df,dr in Z[t]:
   f,r=f0+df,r0+dr
   while B(f,r):
    if(p:=bd[r*8+f])!=U:
     if p.isupper()==bw and((pu:=p.upper())==t or(t in "BR" and pu=="Q")):return True
     break
    if t not in X:break
    f+=df;r+=dr
 return False
def D(bd,side,ep,m):
 frm,to,promo,fl=m;w=side=="w";b2=bd[:]
 p=b2[frm];b2[frm]=U
 if fl=="e":
  b2[to]=p;cap=to+(-8 if w else 8);b2[cap]=U
 elif promo:b2[to]=promo if w else promo.lower()
 else:b2[to]=p
 return b2,("b" if w else "w"),(frm+to)//2 if fl is True else-1
def K(bd,w):return bd.index("K" if w else "k")
def E(bd):
 s=0
 for sq in range(64):
  if(p:=bd[sq])==U:continue
  f,r=sq%8,sq//8;t=p.upper();v=V[t]+4*(Y[f]+Y[r])
  if t=="P":v+=6*(r-1) if p=="P" else 6*(6-r)
  s+=v if p.isupper() else-v
 return s
def Q(bd,m):
 vv=V[t.upper()] if(t:=bd[m[1]])!=U else(V["P"] if m[3]=="e" else 0)
 return-(vv*10-V[bd[m[0]].upper()])-(40 if m[2] else 0)
def L(bd,side,ep):
 w=side=="w"
 pm=G(bd,side,ep)
 pm.sort(key=lambda m:Q(bd,m))
 for m in pm:
  b2,s2,e2=D(bd,side,ep,m)
  if A(b2,K(b2,w),not w):continue
  yield m,b2,s2,e2
def S(bd,side,ep,depth,alpha,beta,root=False):
 global N,W
 N+=1
 w=side=="w"
 if N>O or depth==0:return E(bd)*(1 if w else-1)
 best=-10**9
 for m,b2,s2,e2 in L(bd,side,ep):
  sc=-S(b2,s2,e2,depth-1,-beta,-alpha)
  if sc>best:
   best=sc
   if root:W=m
  if best>alpha:alpha=best
  if alpha>=beta and not root:break
 if best==-(10**9):
  if A(bd,K(bd,w),not w):return-100000+(10-depth)
  return 0
 return best
def T(m):
 fr,to,pr=m[:3]
 s=AB[fr%8]+str(fr//8+1)+AB[to%8]+str(to//8+1)
 return s+pr.lower() if pr else s
def H(path,body):
 rq=urllib.request.Request(EU+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(rq)as rs:return json.load(rs)
 except urllib.error.HTTPError:sys.exit(1)
def I():
 global N,W
 while True:
  g=H("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":
   bd,side,ep=P(g["fen"])
   N=0;m=J;d=1
   while d<=10 and N<O:
    W=J
    S(bd,side,ep,d,-10**9,10**9,True)
    if W is not J:m=W
    d+=1
   if(mv:=T(m)if m else g[LM][0])not in g[LM]:mv=g[LM][0]
   g=H("/move",{"game":g["game"],"move":mv})
if __name__=="__main__":I()
