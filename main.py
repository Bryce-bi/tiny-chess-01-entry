d='NKBRQ'
c=range
Q=False
P='abcdefgh'
O='Q'
N='R'
M='B'
I='K'
L='e'
K='w'
H='P'
F=True
B='.'
A=None
import json as R,os,sys,urllib.request,urllib.error
b=os.environ.get('MAKEFUN_ENV_URL')or sys.exit(1)
D={'N':[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)],I:[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)],M:[(1,1),(1,-1),(-1,1),(-1,-1)],N:[(1,0),(-1,0),(0,1),(0,-1)]}
D[O]=D[M]+D[N]
S='BRQ'
C={H:100,'N':320,M:330,N:500,O:900,I:0}
T=[0,1,2,3,3,2,1,0]
U=7500
E=0
G=A
def J(f,r):return 0<=f<8 and 0<=r<8
def V(p,w):return p!=B and p.isupper()==w
def e(p,w):return p!=B and p.isupper()!=w
def f(fen):
	F,G,L,A=fen.split()[:4];E=[B]*64
	for(H,I)in enumerate(F.split('/')):
		J=7-H;C=0
		for D in I:
			if D.isdigit():C+=int(D)
			else:E[J*8+C]=D;C+=1
	K=-1 if A=='-'else P.index(A[0])+(int(A[1])-1)*8;return E,G,K
def g(b,sq,w,t):
	I,K=sq%8,sq//8;F=[]
	for(G,H)in D[t]:
		A,C=I+G,K+H
		while J(A,C):
			E=C*8+A
			if V(b[E],w):break
			F.append(E)
			if b[E]!=B or t not in S:break
			A+=G;C+=H
	return F
def h(b,side,ep):
	U='QRBN';H=side==K;E=[]
	for C in c(64):
		M=b[C]
		if M==B or not V(M,H):continue
		P=M.upper()
		if P in d:
			for D in g(b,C,H,P):E.append((C,D,A,A))
		else:
			I,N=C%8,C//8;Q=1 if H else-1;W=1 if H else 6;R=7 if H else 0;G=N+Q
			if J(I,G)and b[G*8+I]==B:
				D=G*8+I
				if G==R:
					for O in U:E.append((C,D,O,A))
				else:E.append((C,D,A,A))
				if N==W:
					S=N+2*Q
					if b[S*8+I]==B:E.append((C,S*8+I,A,F))
			for X in(-1,1):
				T=I+X
				if not J(T,G):continue
				D=G*8+T
				if e(b[D],H):
					if G==R:
						for O in U:E.append((C,D,O,A))
					else:E.append((C,D,A,A))
				elif D==ep:E.append((C,D,A,L))
	return E
def W(b,sq,bw):
	K,L=sq%8,sq//8;P=-1 if bw else 1
	for E in(-1,1):
		A,C=K+E,L+P
		if J(A,C)and b[C*8+A]==(H if bw else'p'):return F
	for G in d:
		for(E,M)in D[G]:
			A,C=K+E,L+M
			while J(A,C):
				I=b[C*8+A]
				if I!=B:
					N=I.upper()
					if I.isupper()==bw and(N==G or G in'BR'and N==O):return F
					break
				if G not in S:break
				A+=E;C+=M
	return Q
def i(b,side,ep,m):
	D,C,E,H=m;G=side==K;A=b[:];I=A[D];A[D]=B;J=-1
	if H==L:A[C]=I;M=C+(-8 if G else 8);A[M]=B
	elif E:A[C]=E if G else E.lower()
	else:A[C]=I
	if H is F:J=(D+C)//2
	return A,'b'if G else K,J
def X(b,w):return b.index(I if w else'k')
def Y(b):
	G=0
	for D in c(64):
		A=b[D]
		if A==B:continue
		J,E=D%8,D//8;I=A.upper();F=C[I]+4*(T[J]+T[E])
		if I==H:F+=6*(E-1)if A==H else 6*(6-E)
		G+=F if A.isupper()else-F
	return G
def j(b,m):A=b[m[1]];D=C[A.upper()]if A!=B else C[H]if m[3]==L else 0;E=b[m[0]];return-(D*10-C[E.upper()])-(40 if m[2]else 0)
def k(b,side,ep):
	A=side;C=A==K;D=h(b,A,ep);D.sort(key=lambda m:j(b,m))
	for E in D:
		B,F,G=i(b,A,ep,E)
		if W(B,X(B,C),not C):continue
		yield(E,B,F,G)
def Z(b,side,ep,depth,alpha,beta,root=Q):
	I=depth;H=beta;A=alpha;global E,G;E+=1;J=side==K
	if E>U:return Y(b)*(1 if J else-1)
	M=I<=0 and not root
	if M:
		N=Y(b)*(1 if J else-1)
		if N>=H:return H
		if N>A:A=N
		if I<=-4:return A
	P=Q;C=-10**9
	for(O,R,S,T)in k(b,side,ep):
		if M and b[O[1]]==B and O[3]!=L:continue
		P=F;D=-Z(R,S,T,I-1,-H,-A)
		if root:
			if D>C:C=D;G=O
			if C>A:A=C
		elif M:
			if D>=H:return H
			if D>A:A=D
		else:
			if D>C:C=D
			if C>A:A=C
			if A>=H:break
	if M:return A
	if not P:
		if W(b,X(b,J),not J):return-100000+(10-I)
		return 0
	return C
def l(b,side,ep):
	global E,G;E=0;C=A;B=1
	while B<=10 and E<U:
		G=A;Z(b,side,ep,B,-10**9,10**9,F)
		if G is not A:C=G
		B+=1
	return C
def m(m):A,B,C=m[0],m[1],m[2];D=P[A%8]+str(A//8+1)+P[B%8]+str(B//8+1);return D+C.lower()if C else D
def a(path,body):
	A=urllib.request.Request(b+path,data=R.dumps(body).encode(),headers={'content-type':'application/json'})
	try:
		with urllib.request.urlopen(A)as B:return R.load(B)
	except urllib.error.HTTPError:sys.exit(1)
def n():
	G='game';E='status';C='legal_moves'
	while F:
		A=a('/game',{})
		if A[E]=='done':break
		while A[E]=='your_move':
			H,I,J=f(A['fen']);D=l(H,I,J);B=m(D)if D else A[C][0]
			if B not in A[C]:B=A[C][0]
			A=a('/move',{G:A[G],'move':B})
if __name__=='__main__':n()