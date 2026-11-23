const L=ship.len,B=ship.beam,c=ship.view;evRoot.visible=false;PIR.visible=false;
if(window.__ship!==4){setShip(4);window.__ship=4;window.__n=-1;}
const E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)};const T=arguments[0];
const N=(n)=>{if(window.__n!==n){R.reset(n);rebuild();window.__n=n}};
// scène avec 3 héros (chef / paille / lunettes) + foule : handles techniques, jamais affichés
const HER=()=>{if(window.__n!==99){P.length=0;byH.clear();const now=Date.now();
 const rows=[{handle:'hero_a',style:{hat:'chef',color:'#E5484D'}},{handle:'hero_b',style:{hat:'straw',color:'#2FBF71'}},{handle:'hero_c',style:{hat:'cap',glasses:true,color:'#2F7DE1'}}]
  .map((r,i)=>({...r,vip:false,joined_ship:4,refs:0,streak:0,best_streak:0,created_at:new Date(now-1e9+i*1e3).toISOString()}));
 ingest(rows);ingest(demoData(12).map((r,i)=>({...r,vip:false,refs:0,streak:0,created_at:new Date(now-1e3+i).toISOString()})));rebuild();
 for(let k=0;k<3;k++){P[k].look.yaw=[.5,-.4,.2][k]}window.__n=99}
 if(!window.PRP){const g=new THREE.Group();
  const mk=(f)=>{const V=[];f(V);return vmesh(V)};
  const stack=mk(V=>{for(let i=0;i<14;i++)addBox(V,.55,.07,.55,0,.04+i*.075,0,i%2?'#FFFFFF':'#E9EEF5');addBox(V,.7,.05,.7,0,0,0,'#8A5A33')});
  const stack2=mk(V=>{for(let i=0;i<9;i++)addBox(V,.5,.07,.5,0,.04+i*.075,0,i%2?'#FFFFFF':'#E9EEF5');addBox(V,.62,.05,.62,0,0,0,'#8A5A33')});
  const lounger=mk(V=>{addBox(V,1.5,.14,.7,0,.12,0,'#EDEDED');addBox(V,.5,.5,.7,-.9,.35,0,'#EDEDED');addBox(V,1.1,.05,.6,.1,.21,0,'#FF4D6D');addBox(V,.3,.05,.6,-.85,.5,0,'#FF4D6D')});
  const stick=mk(V=>{addBox(V,.06,1.0,.06,0,.5,0,'#222222');addBox(V,.34,.55,.05,0,1.28,0,'#111111');addBox(V,.28,.45,.06,0,1.28,0,'#7FD6FF')});
  g.add(stack,stack2,lounger,stick);window.PRP={g,stack,stack2,lounger,stick};ship.group.add(g)}
 {const P0=WP(0),f0=FACE(0),P1=WP(1),f1=FACE(1),P2=WP(2),f2=FACE(2),{stack,stack2,lounger,stick}=window.PRP;
  const sc=.9;[stack,stack2,lounger,stick].forEach(m=>m.scale.setScalar(sc));
  const yb=ship.group.position.y;
  stack.position.set(P0.x+(-f0.z)*.9,P0.y-yb-.05,P0.z+(f0.x)*.9);stack2.position.set(P0.x+(f0.z)*.9,P0.y-yb-.05,P0.z+(-f0.x)*.9);
  lounger.position.set(P1.x+f1.x*.35,P1.y-yb-.05,P1.z+f1.z*.1);lounger.rotation.y=Math.atan2(f1.x,f1.z)+Math.PI/2;
  stick.position.set(P2.x+f2.x*.55,P2.y-yb+.35,P2.z+f2.z*.7);stick.rotation.y=Math.atan2(f2.x,f2.z)}
};
const WP=k=>{const p=P[k],s=p.slot;return new THREE.Vector3(s.x,s.y+ship.group.position.y,s.z)};
const FACE=k=>{const y=P[k].look.yaw;return new THREE.Vector3(-Math.sin(y),0,-Math.cos(y))};
SNK2=0;ROTZ=0;ROTX=0;
const HERO=(k,t,dur,d0,d1)=>{HER();const w=WP(k),f=FACE(k),u=E(t/dur),d=d0+(d1-d0)*u;R.cam(w.x+f.x*d,w.y+1.5+.05*u,w.z+f.z*d,w.x,w.y+.78,w.z)};
if(MODE==='wide'){HER();const k=E(T/2.6);R.cam(L*(.62-.25*k),c.h*(.25+.35*k),B*(1.25+.55*k),L*(.1-.1*k),c.h*(1.3-.2*k),0)}
if(MODE==='ha'){HERO(0,T,2.4,6.4,5)}
if(MODE==='hb'){HERO(1,T,2.4,6.4,5)}
if(MODE==='hc'){HERO(2,T,2.4,6.4,5)}
if(MODE==='trio'){HER();const w=WP(1),k=E(T/2.2);R.cam(w.x+1.2-1.2*k,w.y+1.5+.3*k,w.z+5.2-.8*k,w.x,w.y+.8,w.z)}
if(MODE==='demo'){N(T<1.58?1:(T<3.5?4:14));const k=E(T/4.8);R.cam(L*(.38-.12*k),c.h*(2.1+.2*k),B*(1.4+.25*k),L*.08,c.h*.62,0)}
if(MODE==='end'){N(0);const k=E(T/3.9);const a=.55+1.0*k;R.cam(Math.cos(a)*L*1.15,L*(.22-.13*k),Math.sin(a)*L*1.15,L*.05*(1-k),c.h*.8,0)}
window.__i={mode:MODE,n:P.length,s:P[0]&&P[0].slot};
