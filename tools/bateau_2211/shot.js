const L=ship.len,B=ship.beam,c=ship.view;evRoot.visible=false;PIR.visible=false;
if(window.__ship!==4){setShip(4);window.__ship=4;window.__n=-1;}
const E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)};const T=arguments[0];
const N=(n)=>{if(window.__n!==n){R.reset(n);rebuild();window.__n=n}};
SNK2=0;ROTZ=0;ROTX=0;
if(MODE==='wide'){N(0);const k=E(T/2.6);R.cam(L*(.62-.25*k),c.h*(.25+.35*k),B*(1.25+.55*k),L*(.1-.1*k),c.h*(1.3-.2*k),0)}
if(MODE==='sink'){N(0);const k=E(T/3.7);SNK2=.15+.75*k;ROTX=-.06*k;ROTZ=.05*k;R.cam(L*(.15-.1*k),L*.18,L*(1.25-.15*k),0,c.h*.35,0)}
if(MODE==='empty'){N(0);const k=T/1.1;R.cam(L*(.42-.04*k),c.h*2.1,B*(1.5-.1*k),L*.1,c.h*.6,0)}
if(MODE==='demo'){N(T<1.58?1:(T<3.5?4:14));const k=E(T/4.8);R.cam(L*(.38-.12*k),c.h*(2.1+.2*k),B*(1.4+.25*k),L*.08,c.h*.62,0)}
if(MODE==='spots'){N(0);const k=E(T/1.7);R.cam(L*(.1+.05*k),c.h*(3.4+.4*k),B*(.9+.1*k),L*.05,c.h*.55,0)}
if(MODE==='end'){N(0);const k=E(T/3.9);const a=.55+1.0*k;R.cam(Math.cos(a)*L*1.15,L*(.22-.13*k),Math.sin(a)*L*1.15,L*.05*(1-k),c.h*.8,0)}
window.__i={mode:MODE,n:P.length};
