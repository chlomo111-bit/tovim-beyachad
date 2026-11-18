const L=ship.len,B=ship.beam,c=ship.view;evRoot.visible=false;PIR.visible=false;
const E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)};
const DY=1.71; // pont (local)
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
const sc=1.25;CH1.scale.setScalar(sc);CH2.scale.setScalar(sc);
WAV.visible=false;SPL2.forEach(s=>s.visible=false);LB.visible=true;
const zr=B/2-1.2; // près du bastingage côté +z
const bob=a=>Math.abs(Math.sin(t*6+a))*.25;
CH1.position.set(2.5,DY+bob(0),zr);CH2.position.set(7.5,DY+bob(1),zr);CH1.rotation.set(0,0,Math.sin(t*5)*.08);CH2.rotation.set(0,0,Math.sin(t*4+1)*.06);
LB.position.set(5,.55+Math.sin(t*2)*.15,B/2+5.5);LB.rotation.set(Math.sin(t*1.7)*.06,0,Math.sin(t*2.3)*.05);
ROTX=.10*Math.sin(t*1.6);ROTZ=.03*Math.sin(t*1.1);SNK2=.15;
let sh=0;
if(MODE==='wave'){LB.visible=false;WAV.visible=true;const TI=.9,k=t-TI;
 const zW=lerp(-B/2-24,-B/2-12,E(t/TI)),hs=lerp(.95,1.15,E(t/TI));
 WAV.position.set(0,-2,k<0?zW:-B/2-12+k*6);WAV.scale.set(1,k<0?hs:hs*(1-E(k/1.2)*.7),1);
 if(k>0){const tk=E(k/.8);ROTX=-.32*tk+.06*Math.sin(k*4);ROTZ=.05*tk;SNK2=.15+.25*tk;sh=k<.9?(.9-k)*1.6:0;
  SPL2.forEach((s,i)=>{const kk=k-i*.015;s.visible=kk>0&&kk<1.6;if(s.visible){const a=i*2.39,uu=kk/1.6;s.position.set(Math.cos(a)*L*.45,4+L*.5*(uu*1.6-uu*uu*1.7),-B/2+Math.sin(a*1.7)*3+uu*8);s.scale.setScalar(1.6+(i%3));s.material.opacity=Math.max(0,.95-uu*.7)}})}
 R.cam(L*.18+Math.sin(t*61)*sh,4.5+t*.3+Math.cos(t*47)*sh,B/2+L*.85-t*1.5,L*.05,9,-B/2-6);}
else if(MODE==='boat'){const a=t*.04;R.cam(5+L*.25,8+t*.3,B/2+L*.55-t*1.2,5,1.5,B/2+1)}
else if(MODE==='c1'){const g=new THREE.Vector3();CH1.getWorldPosition(g);R.cam(g.x+1.2,g.y+4.6,g.z+7.5-t*1.0,g.x,g.y+3.4,g.z)}
else if(MODE==='c2'){const g=new THREE.Vector3();CH2.getWorldPosition(g);R.cam(g.x-1.2,g.y+5.6,g.z+9.0-t*.9,g.x,g.y+4.3,g.z)}
else if(MODE==='jump'){const j=t<1.0?E(t/1.25):.896+.035*E((t-1.0)/4.5);
 CH1.position.set(2.5+j*1.2,DY+j*3.5*(1.2-j)+j*.6,zr+j*4.0);CH2.position.set(7.5-j*1.2,DY+j*3.5*(1.2-j)+j*.6,zr+j*4.0);
 CH1.rotation.set(-.4*j,0,.35*j);CH2.rotation.set(-.4*j,0,-.35*j);
 R.cam(5,7.5-Math.min(t,5)*.25,B/2+L*.42-Math.min(t,1.2)*.8-Math.max(0,t-1.2)*.3,5,3.2+Math.max(0,t-1.2)*.1,B/2+2)}
window.__i={L,B};
