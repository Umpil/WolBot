(* ::Package:: *)

(* ::Input:: *)
(*ClearAll["Notebook`*"]*)


(* ::Input:: *)
(*l=0.01;*)


(* ::Input:: *)
(*r=2.25*106*)


(* ::Input:: *)
(*aq2=RandomReal[{10^-8,10^-6}]*)


(* ::Input:: *)
(*cm2=RandomReal[{0.1,0.7}]*)


(* ::Input:: *)
(*\[Epsilon]2=0.9*)


(* ::Input:: *)
(*aq1 = 1.15*10^-6*)


(* ::Input:: *)
(*Subscript[a, 1,2]=aq1/aq2;*)


(* ::Input:: *)
(*ap=1.15*10^-6*)


(* ::Input:: *)
(*\[Rho]m2=1050*)


(* ::Input:: *)
(*Subscript[Lu, p]=ap/aq2;*)


(* ::Input:: *)
(*Subscript[\[Theta], 0]=188;*)


(* ::Input:: *)
(*Subscript[\[Theta], s]=10;*)


(* ::Input:: *)
(*Subscript[\[Theta], v]=Subscript[\[Theta], s];*)


(* ::Input:: *)
(*Subscript[t, v]=270;*)


(* ::Input:: *)
(*Subscript[t, 0]=-20+273;*)


(* ::Input:: *)
(*Subscript[t, s]=45+273;*)


(* ::Input:: *)
(*cq2=1600;*)
(*am2=8*10^-6;*)
(*\[Delta]2=0.02;*)
(*k1=0.027;*)
(*k2=2.4;*)


(* ::Input:: *)
(*Subscript[Ko, 2]=r*cm2/cq2*(Subscript[\[Theta], 0]-Subscript[\[Theta], s])/(Subscript[t, s]-Subscript[t, 0])*)


(* ::Input:: *)
(*Subscript[Lu, 2]=am2/aq2*)


(* ::Input:: *)
(*Subscript[Pn, 2]=\[Delta]2*(Subscript[t, s]-Subscript[t, 0])/(Subscript[\[Theta], 0]-Subscript[\[Theta], s])*)


(* ::Input:: *)
(*Subscript[k, 2,1]=1*)


(* ::Input:: *)
(*Subscript[k, 2,2]=k2/k1*)


(* ::Input:: *)
(*Subscript[\[Nu], t]=(r*(1-\[Epsilon]2)*\[Rho]m2*aq2)/(k1*(Subscript[t, s]-Subscript[t, 0]))*)


(* ::Input:: *)
(*kp=9/10000*)


(* ::Input:: *)
(*ps=100*)


(* ::Input:: *)
(*Subscript[\[Nu], p]=((1-\[Epsilon]2)*\[Rho]m2*aq2)/(kp*ps)*)


(* ::Input:: *)
(*Tv=(Subscript[t, v]-Subscript[t, 0])/(Subscript[t, s]-Subscript[t, 0])*)


(* ::Input:: *)
(*\[CapitalTheta]1[X_,F0_]:=1*)


(* ::Input:: *)
(*T1[X_,F0_]:=Subscript[A, 1,1]+Subscript[B, 1,1]*Erf[X/(2*Sqrt[Subscript[a, 1,2]*F0])]*)


(* ::Input:: *)
(*P[X_,F0_]:=Subscript[A, 2,1]+Subscript[B, 2,1]*Erf[X/(2*Sqrt[Subscript[Lu, p]*F0])]*)


(* ::Text:: *)
(*\:0414\:043b\:044f i=2*)


(* ::Input:: *)
(*by[X_,F0_]:={Subscript[T, 2][X,F0],Subscript[\[CapitalTheta], 2][X,F0]}*)
(*leftpart= {{1,\[Epsilon]2*Subscript[Ko, 2]},{0,1/Subscript[Lu, 2]}};*)
(*rightpart= {{1,0},{-Subscript[Pn, 2],1}};*)


(* ::Text:: *)
(*\:041d\:043e\:0440\:043c\:0430\:043b\:044c\:043d\:0430\:044f \:0416\:043e\:0440\:0434\:0430\:043d\:043e\:0432\:0430 \:0444\:043e\:0440\:043c\:0430*)


(* ::Input:: *)
(*JJ=JordanDecomposition[Inverse[leftpart] . rightpart];*)


(* ::Input:: *)
(*JJ[[1]] . JJ[[2]] . Inverse[JJ[[1]]]//FullSimplify//MatrixForm*)


(* ::Input:: *)
(*Z12[X_,F0_]:=Inverse[JJ[[1]]][[1]] . by[X,F0]*)


(* ::Input:: *)
(*Z22[X_,F0_]:=Inverse[JJ[[1]]][[2]] . by[X,F0]*)


(* ::Input:: *)
(*solr1 = Solve[Z12[X,F0]==Subscript[Z, 12][X,F0]&&Z22[X,F0]==Subscript[Z, 22][X,F0],{Subscript[T, 2][X,F0],Subscript[\[CapitalTheta], 2][X,F0]}][[1]];*)


(* ::Input:: *)
(*Z12sol[X_,F0_]:=Subscript[A, 1,2]+Subscript[B, 1,2]*Erf[X/(2*Sqrt[JJ[[2,1,1]]*F0])]*)


(* ::Input:: *)
(*Z22sol[X_,F0_]:=Subscript[A, 2,2]+Subscript[B, 2,2]*Erf[X/(2*Sqrt[JJ[[2,2,2]]*F0])]*)


(* ::Input:: *)
(*T2[X_,F0_]:=Evaluate[Subscript[T, 2][X,F0]/.solr1/.{Subscript[Z, 12][X,F0]->Z12sol[X,F0],Subscript[Z, 22][X,F0]->Z22sol[X,F0]}]*)


(* ::Input:: *)
(*\[CapitalTheta]2[X_,F0_]:=Evaluate[Subscript[\[CapitalTheta], 2][X,F0]/.solr1/.{Subscript[Z, 12][X,F0]->Z12sol[X,F0],Subscript[Z, 22][X,F0]->Z22sol[X,F0]}]*)


(* ::Text:: *)
(*\:0412\:044b\:0447\:0438\:0441\:043b\:0438\:043c \:043a\:043e\:044d\:0444\:0444\:0438\:0446\:0438\:0435\:043d\:0442\:044b Subscript[A, j,i] \:0438 Subscript[B, j,i]*)


(* ::Text:: *)
(*Subscript[T, 2](x,0)=0, Subscript[\[CapitalTheta], 2](x,0)=0*)


(* ::Input:: *)
(*conrule1=Solve[T2[X,0]==0&&\[CapitalTheta]2[X,0]==0/.{ComplexInfinity->\[Infinity]},{Subscript[B, 1,2],Subscript[B, 2,2]}][[1]]//FullSimplify;*)


(* ::Text:: *)
(*Subscript[T, 1](0,t)=1,P(0,t)=0*)


(* ::Input:: *)
(*conrule2=Solve[T1[0,F0]==1][[1]];*)


(* ::Input:: *)
(*conrule3=Solve[P[0,F0]==0][[1]];*)


(* ::Text:: *)
(*\!\( *)
(*\*SubscriptBox[\(\[PartialD]\), \(x\)]\(P(s, t)\)\)=Subscript[\[Nu], p]\!\( *)
(*\*SubscriptBox[\(\[PartialD]\), \(t\)]S\)*)


(* ::Input:: *)
(*S[F0_]:=2*\[Lambda]*Sqrt[F0]*)


(* ::Input:: *)
(*T = {0,3000,6000,12600,16800,22200,27600,34800}(*\:0441\:0435\:043a\:0443\:043d\:0434\:044b*);*)
(*\!\(\*OverscriptBox[\(s\), \(^\)]\)={0,0.2,0.3,0.47,0.57,0.67,0.75,0.8}/100(*\:043c\:0435\:0442\:0440\:044b*)*)
(*pairs=Thread[{T,\!\(\*OverscriptBox[\(s\), \(^\)]\)}];*)


(* ::Input:: *)
(*lst = {};*)


(* ::Input:: *)
(*conrule4=Solve[D[P[X,F0],X]==Subscript[\[Nu], p]*D[S[F0],F0]//.{X->S,S->2*\[Lambda]*Sqrt[F0]},Subscript[B, 2,1]][[1]];*)


(* ::Text:: *)
(*\!\( *)
(*\*UnderoverscriptBox[\(\[Sum]\), \(i = 1\), \(2\)]\( *)
(*\*SuperscriptBox[\((\(-1\))\), \(i\)] *)
(*\*SubscriptBox[\(k\), \(2  i\)] *)
(*\*SubscriptBox[\(\[PartialD]\), \(x\)]*)
(*\*SubscriptBox[\(T\), \(i\)] \((s, t)\)\)\)=Subscript[\[Nu], t]\!\( *)
(*\*SubscriptBox[\(\[PartialD]\), \(t\)]s\)*)


(* ::Input:: *)
(*conrule5=Solve[T1[S,F0]==Tv&&T2[S,F0]==Tv&&\[CapitalTheta]2[S,F0]==1//.{S->2*\[Lambda]*Sqrt[F0]}//.conrule1//.conrule2//.conrule3//.conrule4,{Subscript[B, 1,1],Subscript[A, 1,2],Subscript[A, 2,2]}][[1]];*)


(* ::Input:: *)
(*allrules = Flatten[{conrule1,conrule2,conrule3,conrule4,conrule5}];*)


(* ::Input:: *)
(*allrules*)


(* ::Input:: *)
(*rllamb=FindRoot[-Subscript[k, 2,1]*D[T1[X,F0],X]+Subscript[k, 2,2]*D[T2[X,F0],X]==Subscript[\[Nu], t]*D[S[F0],F0]//.allrules//.{X->S,S->2*\[Lambda]*Sqrt[F0],F0->1},{\[Lambda],0.00000001},PrecisionGoal->100]*)


(* ::Input:: *)
(*s[\[Tau]_]=l*S[(aq2*\[Tau])/l^2]//.rllamb*)


(* ::Input:: *)
(*Subscript[\[Theta], 1][x_,\[Tau]_]=(Subscript[\[Theta], 0]-\[CapitalTheta]1[x/l,(aq2*\[Tau])/l^2](Subscript[\[Theta], 0]-Subscript[\[Theta], s]))//.allrules//.rllamb*)


(* ::Input:: *)
(*Subscript[\[Theta], 2][x_,\[Tau]_]=(Subscript[\[Theta], 0]-\[CapitalTheta]2[x/l,(aq2*\[Tau])/l^2](Subscript[\[Theta], 0]-Subscript[\[Theta], s]))//.allrules//.rllamb*)


(* ::Input:: *)
(*Subscript[t, 1][x_,\[Tau]_]=(Subscript[t, 0]-T1[x/l,(aq2*\[Tau])/l^2](Subscript[t, 0]-Subscript[t, s]))//.allrules//.rllamb*)


(* ::Input:: *)
(*Subscript[t, 2][x_,\[Tau]_]=(Subscript[t, 0]-T2[x/l,(aq2*\[Tau])/l^2](Subscript[t, 0]-Subscript[t, s]))//.allrules//.rllamb*)


(* ::Input:: *)
(*x0=0.015*)


(* ::Input:: *)
(**)


(* ::Input:: *)
(*\[Theta][x_,\[Tau]_]:=Piecewise[{{Subscript[\[Theta], 1][x,\[Tau]],x<=s[\[Tau]]},{Subscript[\[Theta], 2][x,\[Tau]],x>=s[\[Tau]]}}]//.{ComplexInfinity->\[Infinity]}*)


(* ::Input:: *)
(*t[x_,\[Tau]_]:=Piecewise[{{Subscript[t, 1][x,\[Tau]],x<=s[\[Tau]]},{Subscript[t, 2][x,\[Tau]],x>=s[\[Tau]]}}]//.{ComplexInfinity->\[Infinity]}*)


(* ::Input:: *)
(*Plot[t[x0,\[Tau]],{\[Tau],0,34800}]*)


(* ::Input:: *)
(**)


(* ::Input:: *)
(*valTemp=Table[t[x0,i],{i,1,100,1}];*)


(* ::Input:: *)
(*aq2*)


(* ::Input:: *)
(*{aq2,cm2,valTemp}*)
