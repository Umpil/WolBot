
ClearAll["Notebook`*"]


l=0.01;


r=2.25*106


aq2=RandomReal[{10^-8,10^-6}]


cm2=RandomReal[{0.1,0.7}]


\[Epsilon]2=0.9


aq1 = 1.15*10^-6


Subscript[a, 1,2]=aq1/aq2;


ap=1.15*10^-6


\[Rho]m2=1050


Subscript[Lu, p]=ap/aq2;


Subscript[\[Theta], 0]=188;


Subscript[\[Theta], s]=10;


Subscript[\[Theta], v]=Subscript[\[Theta], s];


Subscript[t, v]=270;


Subscript[t, 0]=-20+273;


Subscript[t, s]=45+273;


cq2=1600;
am2=8*10^-6;
\[Delta]2=0.02;
k1=0.027;
k2=2.4;


Subscript[Ko, 2]=r*cm2/cq2*(Subscript[\[Theta], 0]-Subscript[\[Theta], s])/(Subscript[t, s]-Subscript[t, 0])


Subscript[Lu, 2]=am2/aq2


Subscript[Pn, 2]=\[Delta]2*(Subscript[t, s]-Subscript[t, 0])/(Subscript[\[Theta], 0]-Subscript[\[Theta], s])


Subscript[k, 2,1]=1


Subscript[k, 2,2]=k2/k1


Subscript[\[Nu], t]=(r*(1-\[Epsilon]2)*\[Rho]m2*aq2)/(k1*(Subscript[t, s]-Subscript[t, 0]))


kp=9/10000


ps=100


Subscript[\[Nu], p]=((1-\[Epsilon]2)*\[Rho]m2*aq2)/(kp*ps)


Tv=(Subscript[t, v]-Subscript[t, 0])/(Subscript[t, s]-Subscript[t, 0])


\[CapitalTheta]1[X_,F0_]:=1


T1[X_,F0_]:=Subscript[A, 1,1]+Subscript[B, 1,1]*Erf[X/(2*Sqrt[Subscript[a, 1,2]*F0])]


P[X_,F0_]:=Subscript[A, 2,1]+Subscript[B, 2,1]*Erf[X/(2*Sqrt[Subscript[Lu, p]*F0])]


by[X_,F0_]:={Subscript[T, 2][X,F0],Subscript[\[CapitalTheta], 2][X,F0]}
leftpart= {{1,\[Epsilon]2*Subscript[Ko, 2]},{0,1/Subscript[Lu, 2]}};
rightpart= {{1,0},{-Subscript[Pn, 2],1}};


JJ=JordanDecomposition[Inverse[leftpart] . rightpart];


JJ[[1]] . JJ[[2]] . Inverse[JJ[[1]]]//FullSimplify//MatrixForm


Z12[X_,F0_]:=Inverse[JJ[[1]]][[1]] . by[X,F0]


Z22[X_,F0_]:=Inverse[JJ[[1]]][[2]] . by[X,F0]


solr1 = Solve[Z12[X,F0]==Subscript[Z, 12][X,F0]&&Z22[X,F0]==Subscript[Z, 22][X,F0],{Subscript[T, 2][X,F0],Subscript[\[CapitalTheta], 2][X,F0]}][[1]];


Z12sol[X_,F0_]:=Subscript[A, 1,2]+Subscript[B, 1,2]*Erf[X/(2*Sqrt[JJ[[2,1,1]]*F0])]


Z22sol[X_,F0_]:=Subscript[A, 2,2]+Subscript[B, 2,2]*Erf[X/(2*Sqrt[JJ[[2,2,2]]*F0])]


T2[X_,F0_]:=Evaluate[Subscript[T, 2][X,F0]/.solr1/.{Subscript[Z, 12][X,F0]->Z12sol[X,F0],Subscript[Z, 22][X,F0]->Z22sol[X,F0]}]


\[CapitalTheta]2[X_,F0_]:=Evaluate[Subscript[\[CapitalTheta], 2][X,F0]/.solr1/.{Subscript[Z, 12][X,F0]->Z12sol[X,F0],Subscript[Z, 22][X,F0]->Z22sol[X,F0]}]


conrule1=Solve[T2[X,0]==0&&\[CapitalTheta]2[X,0]==0/.{ComplexInfinity->\[Infinity]},{Subscript[B, 1,2],Subscript[B, 2,2]}][[1]]//FullSimplify;


conrule2=Solve[T1[0,F0]==1][[1]];


conrule3=Solve[P[0,F0]==0][[1]];


S[F0_]:=2*\[Lambda]*Sqrt[F0]


T = {0,3000,6000,12600,16800,22200,27600,34800}(*\:0441\:0435\:043a\:0443\:043d\:0434\:044b*);
\!\(\*OverscriptBox[\(s\), \(^\)]\)={0,0.2,0.3,0.47,0.57,0.67,0.75,0.8}/100(*\:043c\:0435\:0442\:0440\:044b*)
pairs=Thread[{T,\!\(\*OverscriptBox[\(s\), \(^\)]\)}];


lst = {};


conrule4=Solve[D[P[X,F0],X]==Subscript[\[Nu], p]*D[S[F0],F0]//.{X->S,S->2*\[Lambda]*Sqrt[F0]},Subscript[B, 2,1]][[1]];


conrule5=Solve[T1[S,F0]==Tv&&T2[S,F0]==Tv&&\[CapitalTheta]2[S,F0]==1//.{S->2*\[Lambda]*Sqrt[F0]}//.conrule1//.conrule2//.conrule3//.conrule4,{Subscript[B, 1,1],Subscript[A, 1,2],Subscript[A, 2,2]}][[1]];


allrules = Flatten[{conrule1,conrule2,conrule3,conrule4,conrule5}];


allrules


rllamb=FindRoot[-Subscript[k, 2,1]*D[T1[X,F0],X]+Subscript[k, 2,2]*D[T2[X,F0],X]==Subscript[\[Nu], t]*D[S[F0],F0]//.allrules//.{X->S,S->2*\[Lambda]*Sqrt[F0],F0->1},{\[Lambda],0.00000001},PrecisionGoal->100]


s[\[Tau]_]=l*S[(aq2*\[Tau])/l^2]//.rllamb


Subscript[\[Theta], 1][x_,\[Tau]_]=(Subscript[\[Theta], 0]-\[CapitalTheta]1[x/l,(aq2*\[Tau])/l^2](Subscript[\[Theta], 0]-Subscript[\[Theta], s]))//.allrules//.rllamb


Subscript[\[Theta], 2][x_,\[Tau]_]=(Subscript[\[Theta], 0]-\[CapitalTheta]2[x/l,(aq2*\[Tau])/l^2](Subscript[\[Theta], 0]-Subscript[\[Theta], s]))//.allrules//.rllamb


Subscript[t, 1][x_,\[Tau]_]=(Subscript[t, 0]-T1[x/l,(aq2*\[Tau])/l^2](Subscript[t, 0]-Subscript[t, s]))//.allrules//.rllamb


Subscript[t, 2][x_,\[Tau]_]=(Subscript[t, 0]-T2[x/l,(aq2*\[Tau])/l^2](Subscript[t, 0]-Subscript[t, s]))//.allrules//.rllamb


x0=0.015





\[Theta][x_,\[Tau]_]:=Piecewise[{{Subscript[\[Theta], 1][x,\[Tau]],x<=s[\[Tau]]},{Subscript[\[Theta], 2][x,\[Tau]],x>=s[\[Tau]]}}]//.{ComplexInfinity->\[Infinity]}


t[x_,\[Tau]_]:=Piecewise[{{Subscript[t, 1][x,\[Tau]],x<=s[\[Tau]]},{Subscript[t, 2][x,\[Tau]],x>=s[\[Tau]]}}]//.{ComplexInfinity->\[Infinity]}


Plot[t[x0,\[Tau]],{\[Tau],0,34800}]





valTemp=Table[t[x0,i],{i,1,100,1}];


aq2


{aq2,cm2,valTemp}
