const MODE='mouth';
const L=ship.len,B=ship.beam,c=ship.view;evRoot.visible=false;PIR.visible=false;
const E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)};const DY=1.71;
if(!window.CH1){
 const mk=(f)=>{const V=[];f(V);return vmesh(V)};
 // 1 = le capitaine : manteau bleu marine, grosse barbe blanche, casquette
 const cap=mk(V=>{addBox(V,.42,1.0,.42,-.28,.5,0,'#1B2440');addBox(V,.42,1.0,.42,.28,.5,0,'#1B2440');addBox(V,.5,.2,.6,-.28,.05,.08,'#111');addBox(V,.5,.2,.6,.28,.05,.08,'#111');
  addBox(V,1.35,1.4,.9,0,1.7,0,'#22315E');addBox(V,.12,.12,.06,0,1.95,.47,'#FFD24B');addBox(V,.12,.12,.06,0,1.6,.47,'#FFD24B');addBox(V,.12,.12,.06,0,1.25,.47,'#FFD24B');
  addBox(V,.36,1.15,.4,-.88,1.85,0,'#22315E');addBox(V,.36,1.15,.4,.88,1.85,0,'#22315E');addBox(V,.34,.3,.34,-.88,1.15,0,'#F2C49B');addBox(V,.34,.3,.34,.88,1.15,0,'#F2C49B');
  addBox(V,1.0,1.0,1.0,0,2.9,0,'#F2C49B');addBox(V,1.15,.75,.35,0,2.45,.45,'#FFFFFF');addBox(V,.8,.4,.3,0,2.15,.42,'#FFFFFF');
  addBox(V,.16,.16,.06,-.22,3.05,.51,'#111');addBox(V,.16,.16,.06,.22,3.05,.51,'#111');addBox(V,.24,.2,.12,0,2.85,.55,'#E89A7A');
  addBox(V,1.2,.32,1.2,0,3.56,0,'#FFFFFF');addBox(V,1.25,.12,.5,0,3.38,.55,'#111');addBox(V,.3,.2,.06,0,3.56,.61,'#FFD24B')});
 // 2 = le cuisinier : gros, toque géante, moustache, ÉNORME gâteau rose
 const chef=mk(V=>{addBox(V,.5,.9,.5,-.4,.45,0,'#333');addBox(V,.5,.9,.5,.4,.45,0,'#333');
  addBox(V,1.9,1.6,1.4,0,1.7,0,'#FAFAFA');addBox(V,1.95,.3,1.45,0,1.1,0,'#E5484D');addBox(V,.5,.5,.1,0,2.2,.72,'#E5484D');
  addBox(V,1.05,1.0,1.0,0,3.0,0,'#F5C9A0');addBox(V,.16,.16,.06,-.22,3.15,.51,'#111');addBox(V,.16,.16,.06,.22,3.15,.51,'#111');
  addBox(V,.7,.16,.1,0,2.85,.53,'#2A1A0E');addBox(V,.2,.2,.1,-.42,2.78,.53,'#2A1A0E');addBox(V,.2,.2,.1,.42,2.78,.53,'#2A1A0E');
  addBox(V,1.0,.25,1.0,0,3.6,0,'#FFFFFF');addBox(V,1.15,1.1,1.15,0,4.25,0,'#FFFFFF');addBox(V,1.35,.45,1.35,0,4.95,0,'#FFFFFF');
  addBox(V,.36,.36,.9,-.95,1.5,.5,'#FAFAFA');addBox(V,.36,.36,.9,.95,1.5,.5,'#FAFAFA');
  // gâteau
  addBox(V,1.9,.55,1.1,0,1.20,1.35,'#FF8FB8');addBox(V,1.95,.12,1.15,0,1.50,1.35,'#FFFFFF');addBox(V,1.45,.45,.85,0,1.78,1.35,'#FF6FA3');addBox(V,1.5,.1,.9,0,2.03,1.35,'#FFFFFF');
  addBox(V,.9,.4,.55,0,2.25,1.35,'#FF8FB8');addBox(V,.12,.4,.12,0,2.65,1.35,'#8FD3FF');addBox(V,.14,.18,.14,0,2.93,1.35,'#FFB020');
  for(const x of [-.7,-.25,.25,.7])addBox(V,.18,.18,.18,x,1.60,1.95,'#E5484D')});
 window.CH1=new THREE.Group();CH1.add(cap);window.CH2=new THREE.Group();CH2.add(chef);
 // canot de sauvetage avec UNE place
 const lb=mk(V=>{addBox(V,5,.9,2.2,0,0,0,'#FF6A00');addBox(V,5.3,.3,.3,0,.55,1.1,'#FF8A2A');addBox(V,5.3,.3,.3,0,.55,-1.1,'#FF8A2A');addBox(V,.3,.3,2.5,2.6,.55,0,'#FF8A2A');addBox(V,.3,.3,2.5,-2.6,.55,0,'#FF8A2A');addBox(V,4.6,.1,1.8,0,.5,0,'#F4F4F4');addBox(V,.9,.35,1.8,.3,.7,0,'#C0392B');for(const x of [-2,-.8,1.4,2.2])addBox(V,.3,.3,.08,x,.25,1.12,'#FFFFFF')});
 window.LB=new THREE.Group();LB.add(lb);sea.add(LB);
 // vague géante
 const wv=mk(V=>{for(let i=0;i<26;i++){const x=(i-12.5)*2.6,hh=1+.12*Math.sin(i*1.7);
   for(let j=0;j<12;j++){const y=j*1.6*hh,z=Math.pow(j/11,2.2)*7;addBox(V,2.7,1.7,2.6,x,y,z,j>9?'#BFE8FF':(j%2?'#2E7FC0':'#2672B0'))}
   addBox(V,2.7,1.0,3.4,x,12*1.6*hh+.2,8.2,'#FFFFFF');addBox(V,2.7,1.2,2.2,x,11*1.6*hh-.6,9.6,'#E6F6FF')}});
 window.WAV=new THREE.Group();WAV.add(wv);sea.add(WAV);
 window.SPL2=[];for(let i=0;i<34;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(1,8,6),new THREE.MeshBasicMaterial({color:i%3?0xDDF3FF:0xFFFFFF,transparent:true,opacity:.92}));sea.add(s);SPL2.push(s)}
 ship.group.add(CH1);ship.group.add(CH2);
}
if(!window.WHL){const V=[];const C1='#2D5B8F',C2='#244A75',W='#E8F0F7';
 for(let k=0;k<9;k++){const s=1-Math.pow(Math.abs(k-2.5)/7,1.4);addBox(V,1.25,2.4*s+.5,2.6*s+.5,k*1.2,0,0,k%2?C1:C2);addBox(V,1.25,.5,1.8*s+.3,k*1.2,-(1.2*s+.25),0,W)}
 addBox(V,1.4,.6,4.4,10.8,.2,0,C1);addBox(V,.9,.5,1.6,10.0,.1,0,C2);
 addBox(V,2.6,.35,1.2,2.2,-.9,1.9,C2);addBox(V,2.6,.35,1.2,2.2,-.9,-1.9,C2);
 for(const s of [1,-1]){addBox(V,.95,.95,.2,-.1,.45,s*1.42,'#FFFFFF');addBox(V,.5,.55,.24,-.25,.4,s*1.46,'#101010');addBox(V,.18,.18,.26,-.35,.55,s*1.48,'#FFFFFF')}
 addBox(V,.2,.18,2.4,-.62,-.35,0,'#101010');addBox(V,.6,.25,.6,1.0,1.42,0,'#1B3A5E');for(const s of [1,-1])addBox(V,1.2,.22,.24,-.15,1.05,s*1.47,'#0d1a2b');
 const m=vmesh(V);m.position.x=-4.6;window.WHI=new THREE.Group();WHI.add(m);window.WHL=new THREE.Group();WHL.add(WHI);sea.add(WHL);
 window.SPL=[];for(let i=0;i<26;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(1,8,6),new THREE.MeshBasicMaterial({color:i%3?0xDDF3FF:0xFFFFFF,transparent:true,opacity:.92}));sea.add(s);SPL.push(s)}}

if(!window.MTH){const C1='#2D5B8F',C2='#244A75',IN='#8B1E2E',TH='#3A0A12';
 const lo=[],up=[];
 addBox(lo,6,1.2,7,0,0,3.5,C2);addBox(lo,5.2,.2,6.4,0,.65,3.6,IN);addBox(lo,3.4,.5,4.2,0,.9,3.2,'#D9576B');addBox(lo,6.1,.5,7.1,0,-.6,3.5,'#E8F0F7');
 for(let i=0;i<7;i++){addBox(lo,.45,.9,.45,2.6,1.15,.8+i*.95,'#FFFFFF');addBox(lo,.45,.9,.45,-2.6,1.15,.8+i*.95,'#FFFFFF')}
 for(let i=0;i<5;i++)addBox(lo,.45,.9,.45,-2+i,1.15,6.75,'#FFFFFF');
 addBox(up,6,1.4,7,0,0,3.5,C1);addBox(up,5.2,.2,6.4,0,-.75,3.6,IN);addBox(up,6.2,1.2,2.5,0,.2,-.8,C1);
 for(let i=0;i<7;i++){addBox(up,.45,.9,.45,2.6,-1.2,.8+i*.95,'#FFFFFF');addBox(up,.45,.9,.45,-2.6,-1.2,.8+i*.95,'#FFFFFF')}
 for(let i=0;i<5;i++)addBox(up,.45,.9,.45,-2+i,-1.2,6.75,'#FFFFFF');
 for(const s of [1,-1]){addBox(up,.2,1.3,1.3,s*3.05,.75,1.2,'#FFFFFF');addBox(up,.24,.75,.75,s*3.1,.7,1.3,'#101010');addBox(up,.26,.25,.25,s*3.12,.95,1.45,'#FFFFFF');addBox(up,.3,.3,1.6,s*3.1,1.5,1.2,'#0d1a2b')}
 const th=[];addBox(th,5.6,7,.6,0,2.5,-.2,TH);addBox(th,6.2,9,4,0,-3,-1.8,C2);
 window.MLO=vmesh(lo);window.MUP=new THREE.Group();const mu=vmesh(up);MUP.add(mu);MUP.position.set(0,1.3,0);
 window.MTH=new THREE.Group();MTH.add(MLO);MTH.add(MUP);MTH.add(vmesh(th));sea.add(MTH)}
if(CH2.parent!==LB)LB.add(CH2);if(CH1.parent!==sea)sea.add(CH1);
const sc=1.25;CH1.scale.setScalar(sc);CH2.scale.setScalar(.85);
WAV.visible=false;SPL2.forEach(s=>s.visible=false);SPL.forEach(s=>s.visible=false);LB.visible=true;MTH.visible=false;WHL.visible=false;
const ws=L/15;WHL.scale.setScalar(ws);MTH.scale.setScalar(ws*.9);
const LX=0,LZ=-B/2-10;
LB.position.set(LX,.55+Math.sin(t*2)*.15,LZ);LB.rotation.set(Math.sin(t*1.7)*.06,0,Math.sin(t*2.3)*.05);
CH2.position.set(.3,.55,0);CH2.rotation.set(0,0,Math.sin(t*5)*.05);
CH1.position.set(LX+6.5,-2.2+Math.sin(t*3)*.25,LZ+3);CH1.rotation.set(Math.sin(t*4)*.15,-0.6,Math.sin(t*5)*.18);
ROTX=-.22+.03*Math.sin(t*1.3);ROTZ=.06;SNK2=.38;
const splash=(arr,cx,cy,cz,k,R,H)=>{arr.forEach((s,i)=>{const kk=k-i*.015;s.visible=kk>0&&kk<1.4;if(s.visible){const a=i*2.39,uu=kk/1.4;s.position.set(cx+Math.cos(a)*R*(.4+uu),cy+H*(uu*1.6-uu*uu*1.7),cz+Math.sin(a)*R*(.4+uu));s.scale.setScalar(R*.18*(1+(i%3)*.5));s.material.opacity=Math.max(0,.95-uu*.7)}})};
let sh=0;const m=WHI.children[0];
if(MODE==='leap'){WHL.visible=true;const T=2.3,u=(t+.6)/T;WHL.rotation.set(0,Math.PI,0);
 const wx=LX+lerp(-ws*8,ws*5,u),wy=-ws*2.2+ws*6.2*Math.sin(Math.min(1,u)*Math.PI);WHL.position.set(wx,wy,LZ-ws*4.5);WHI.rotation.z=lerp(-.6,.65,u);
 splash(SPL,LX-ws*4.2,0,LZ-ws*4.5,t+.5,ws*1.3,ws*2.2);if(t>1.1)splash(SPL2,LX+ws*3,0,LZ-ws*4.5,t-1.15,ws*1.8,ws*3);
 sh=t<.6?(.6-t)*1.2:(t>1.3&&t<1.8?(1.8-t)*1.6:0);CH2.rotation.set(0,-.4,Math.sin(t*14)*.12);
 R.cam(LX+4+Math.sin(t*61)*sh,3.6+Math.cos(t*47)*sh,LZ+26-t*1.2,LX-1,ws*2.1,LZ-ws*3)}
else if(MODE==='land'){const k=Math.min(1,t/.55);CH2.position.set(.3,lerp(6.5,.55,k*k),0);CH2.rotation.set(-.3*(1-k),0,.25*(1-k));
 const d=t>.55?Math.exp(-(t-.55)*3)*Math.cos((t-.55)*12)*.45:0;LB.position.y-=d+(t>.55?.12:0);
 splash(SPL2.slice(0,16),LX,0,LZ,t-.55,1.6,2.2);sh=t>.55&&t<1?(1-t)*1.5:0;
 R.cam(LX+5.5+Math.sin(t*61)*sh,4.6+Math.cos(t*47)*sh,LZ+9.5-t*.5,LX,2.2,LZ)}
else if(MODE==='cap'){CH1.rotation.set(Math.sin(t*4)*.15,Math.PI+.25,Math.sin(t*5)*.2);const g=new THREE.Vector3();CH1.getWorldPosition(g);
 R.cam(g.x+1.5,g.y+4.6+t*.2,g.z-7+t*.6,g.x,g.y+3.4,g.z)}
else if(MODE==='eye'){WHL.visible=true;WHL.rotation.set(0,Math.PI*.5,0);WHI.rotation.z=.05+.04*Math.sin(t*2);
 WHL.position.set(LX-ws*1,ws*.15+ws*.12*Math.sin(t*2),LZ-ws*15+t*ws*1.6);WHL.updateMatrixWorld(true);
 const e=m.localToWorld(new THREE.Vector3(-.3,.5,1.46)),cp=m.localToWorld(new THREE.Vector3(-2.6+t*.25,1.6,5.2-t*.5));R.cam(cp.x,cp.y,cp.z,e.x,e.y,e.z)}
else if(MODE==='mouth'){MTH.visible=true;const r=E((t+.15)/.8),o=E((t-.15)/1.3)*1.1+Math.max(0,t-1.45)*.02;
 MTH.position.set(LX,lerp(-ws*5.5,-ws*.35,r),LZ-24);MTH.rotation.set(.08,0,0);MUP.rotation.x=-o;
 splash(SPL,LX,0,LZ-14,t+.1,ws*2.2,ws*3);sh=t>.2&&t<1.2?(1.2-t)*.8:0;CH2.rotation.set(0,Math.sin(t*9)*.15,Math.sin(t*14)*.1);
 const pi=Math.min(t,2)*1.2+Math.max(0,t-2)*.3;
 R.cam(LX+3.2+Math.sin(t*61)*sh,6.8+Math.cos(t*47)*sh,LZ+15-pi,LX-.3,3.2+r*2.5,LZ-12)}
window.__i={L,B,ws,whl:WHL.position.toArray().map(v=>+v.toFixed(1))};
