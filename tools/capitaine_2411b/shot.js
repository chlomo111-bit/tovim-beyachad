// Plateau « הקפטן מספר » : הקפטן parle (bouche sur l'amplitude de la voix), caméra qui bouge, Endurance qui remonte, banquise, navire de guerre qui coule (teaser).
const T=t, E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)}, L_=(a,b,k)=>a+(b-a)*k;
const A=(window.AMP&&window.AMP.length)?(window.AMP[Math.max(0,Math.min(window.AMP.length-1,Math.floor((window.TS!==undefined?window.TS:T)*30)))]||0):0;
if(!window.__S){
 const S=window.__S={};S.old=sea.children.filter(c=>c.type==='Group'&&c.position.lengthSq()<1);
 const mk=f=>{const V=[];f(V);return vmesh(V)};
 window.__dbg=1;S.bgA=new THREE.Color('#CFE3F0');S.bgB=new THREE.Color('#0B2A47');sea.background=S.bgA.clone();sea.fog=new THREE.Fog(new THREE.Color('#CFE3F0'),50,260);
 // plateforme
 S.stg=new THREE.Group();
 S.stg.add(mk(V=>{addBox(V,10,1.3,7.4,0,.4,0,'#6B4426');addBox(V,10.2,.16,7.6,0,1.08,0,'#8E6A3F');for(let i=-4;i<=4;i++)addBox(V,.06,.02,7.2,i*1.1,1.17,0,'#5B3A20');
  for(const x of [-4.8,4.8])for(const z of [-3.5,0,3.5])addBox(V,.22,1.2,.22,x,1.8,z,'#4A2E18');
  addBox(V,.14,.14,7.4,-4.8,2.35,0,'#4A2E18');addBox(V,.14,.14,7.4,4.8,2.35,0,'#4A2E18');addBox(V,10,.14,.14,0,2.35,-3.5,'#4A2E18');
  addBox(V,.9,.9,.9,3.6,1.65,-1.8,'#B5702B');addBox(V,.9,.9,.9,3.6,2.5,-1.8,'#C98235');addBox(V,.2,1.2,.2,-3.4,1.7,-2,'#4A2E18');addBox(V,1.2,.14,.14,-3.4,2.3,-2,'#C9A24B');addBox(V,.14,1.2,.14,-3.4,2.3,-2,'#C9A24B')}));
 sea.add(S.stg);
 // capitaine
 const cg=S.cap=new THREE.Group();S.stg.add(cg);cg.position.set(0,1.16,0);
 cg.add(mk(V=>{addBox(V,.5,1.2,.5,-.32,.6,0,'#1B2440');addBox(V,.5,1.2,.5,.32,.6,0,'#1B2440');addBox(V,.56,.3,.75,-.32,.15,.12,'#111');addBox(V,.56,.3,.75,.32,.15,.12,'#111');
  addBox(V,1.45,1.6,.85,0,1.95,0,'#22315E');addBox(V,.14,.14,.06,.4,2.4,.45,'#FFD24B');addBox(V,.14,.14,.06,.4,2.0,.45,'#FFD24B');addBox(V,.14,.14,.06,.4,1.6,.45,'#FFD24B');addBox(V,.5,.7,.06,-.35,2.0,.44,'#FFFFFF');addBox(V,1.5,.18,.9,0,1.25,0,'#111')}));
 S.armR=new THREE.Group();S.armL=new THREE.Group();
 for(const [g,s] of [[S.armR,1],[S.armL,-1]]){g.position.set(s*1.0,2.65,0);cg.add(g);g.add(mk(V=>{addBox(V,.42,1.4,.42,0,-.7,0,'#22315E');addBox(V,.36,.34,.36,0,-1.5,0,'#F2C49B');addBox(V,.46,.12,.46,0,-1.25,0,'#FFD24B')}))}
 S.head=new THREE.Group();S.head.position.set(0,3.72,0);cg.add(S.head);
 S.head.add(mk(V=>{addBox(V,1.05,1.05,1.0,0,0,0,'#F2C49B');
  addBox(V,1.12,.2,.9,0,-.5,.08,'#FFFFFF');addBox(V,1.08,.7,.38,0,-.62,.52,'#FFFFFF');addBox(V,.22,.8,.8,-.58,-.35,.15,'#FFFFFF');addBox(V,.22,.8,.8,.58,-.35,.15,'#FFFFFF');
  addBox(V,.9,.2,.2,0,-.1,.58,'#FFFFFF');addBox(V,.22,.22,.16,0,.0,.58,'#E5A07E');
  addBox(V,.26,.07,.06,-.24,.32,.51,'#FFFFFF');addBox(V,.26,.07,.06,.24,.32,.51,'#FFFFFF');
  addBox(V,1.25,.34,1.25,0,.7,0,'#FFFFFF');addBox(V,1.3,.14,1.3,0,.5,0,'#22315E');addBox(V,1.28,.1,.6,0,.45,.7,'#111');addBox(V,.34,.22,.06,0,.72,.64,'#FFD24B')}));
 S.mouth=mk(V=>addBox(V,.38,.12,.08,0,0,0,'#7A1020'));S.mouth.position.set(0,-.27,.55);S.head.add(S.mouth);
 S.eyes=mk(V=>{addBox(V,.14,.16,.06,-.24,.12,.51,'#111');addBox(V,.14,.16,.06,.24,.12,.51,'#111')});S.head.add(S.eyes);

 const tr=(m,o)=>{m.material.transparent=true;m.material.opacity=o;return m};
 // Everest (scène du ciel)
 S.ev=new THREE.Group();S.ev.add(mk(V=>{addBox(V,16,5,12,0,2.5,0,'#6E6A66');addBox(V,12,5,9,0,7.5,0,'#7F7B76');addBox(V,8,5,6,0,12.5,0,'#9A968F');addBox(V,5,4,4,0,17,0,'#EEF2F5');addBox(V,2.6,3,2.6,0,20.5,0,'#FFFFFF')}));
 sea.add(S.ev);S.ev.position.set(2.4,4,-12);S.ev.rotation.y=.4;S.ev.scale.setScalar(.45);
 S.ring=mk(V=>{addBox(V,5,.12,5,0,0,0,'#FFFFFF')});sea.add(S.ring);S.ring.position.set(2.4,.35,-12);S.ring.visible=false;
 // diorama (haut dans le ciel, y=300) : 1 km = 2 unités
 const D=S.dio=new THREE.Group();sea.add(D);D.position.set(0,300,-30);
 D.add(mk(V=>{addBox(V,9,1,10,0,-.5,0,'#2A211C');for(const s of [-1,1]){addBox(V,6,3.2,10,s*7.5,1.6,0,'#4A3B32');addBox(V,6,8,10,s*13.5,4,0,'#5A483C');addBox(V,6,14,10,s*19.5,7,0,'#6A5646');addBox(V,6,19,10,s*25.5,9.5,0,'#7A6450')}}));
 D.add(mk(V=>{addBox(V,60,.18,10.4,0,22.5,0,'#BFE8FF')}));
 D.add(mk(V=>{addBox(V,240,22.5,.3,0,11.25,-5.5,'#2B78B8');addBox(V,240,80,.3,0,62.5,-5.6,'#CFE3F0')}));
 S.bar=mk(V=>{addBox(V,.3,21.8,.3,0,10.9,0,'#FFC24B');addBox(V,1.6,.3,.3,0,0,0,'#FFC24B');addBox(V,1.6,.3,.3,0,21.8,0,'#FFC24B')});S.bar.position.set(-9,0,5.6);D.add(S.bar);
 S.br2=mk(V=>{addBox(V,.3,4.8,.3,0,2.4,0,'#FFC24B');addBox(V,1.6,.3,.3,0,0,0,'#FFC24B');addBox(V,1.6,.3,.3,0,4.8,0,'#FFC24B')});S.br2.position.set(5.6,17.7,5.6);D.add(S.br2);
 S.ev2=new THREE.Group();S.ev2.add(mk(V=>{addBox(V,7.4,4.4,6.2,0,2.2,0,'#6E6A66');addBox(V,5.6,4.4,4.8,0,6.6,0,'#7F7B76');addBox(V,3.8,4.4,3.4,0,11,0,'#9A968F');addBox(V,2.6,2.6,2.4,0,14.5,0,'#EEF2F5');addBox(V,1.4,2,1.4,0,16.8,0,'#FFFFFF')}));D.add(S.ev2);
 S.boat=mk(V=>{addBox(V,5,.9,2.2,0,.45,0,'#5A3A1E');addBox(V,.2,4,.2,0,2.9,0,'#2A1A0E');addBox(V,.1,3,2,.1,3,0,'#F0E8D0')});S.boat.position.set(-12,22.6,0);D.add(S.boat);
 // 5 petits navires (teaser)
 S.sh=[];for(let i=0;i<5;i++){const m=mk(V=>{addBox(V,3.2,.7,1.4,0,.35,0,'#5A3A1E');addBox(V,.14,3,.14,0,2.2,0,'#2A1A0E');addBox(V,.08,2.2,1.5,.1,2.2,0,'#F0E8D0');addBox(V,.08,.5,.5,.1,3.9,0,'#FFC24B')});m.position.set(1.8+i*1.6,.6,-9);m.visible=false;sea.add(m);S.sh.push(m)}
 sea.add(new THREE.AmbientLight(0xffffff,.25));
}
const S=window.__S;try{VMAT.transparent=false;VMAT.opacity=1;VMAT.depthWrite=true}catch(e){}
S.old.forEach(c=>c.visible=false);
const dio=T>=3.3&&T<12.3;
sea.background.copy(dio?S.bgB:S.bgA);sea.fog.color.copy(dio?S.bgB:S.bgA);sea.fog.near=dio?400:50;sea.fog.far=dio?900:260;
S.dio.visible=dio;S.ev.visible=T<3.4;S.ring.visible=false;
// Everest tombe dans la mer (0.9-3.2)
{const k1=E((T-.9)/1.3), k2=E((T-2.2)/.8);S.ev.position.y=T<2.2?L_(4,.5,k1):L_(.5,-14,k2);S.ev.rotation.z=k2*.05;
 const r=T-2.15;if(r>0&&r<1.2){S.ring.visible=true;const s=.6+r*3.5;S.ring.scale.set(s,1,s);S.ring.position.set(2.4,.35,-12)}}
// diorama : barre profondeur, Everest qui tombe au fond, accolade
S.bar.scale.y=E((T-5.9)/1.2)||.001;S.bar.visible=T>5.9;
{const k=E((T-7.4)/1.3);S.ev2.position.set(0,T<7.4?30:L_(30,0,k),0);S.ev2.visible=T>=7.4}
S.br2.visible=T>10.3;S.br2.scale.y=E((T-10.3)/.6)||.001;S.boat.position.y=22.6+Math.sin(T*1.5)*.15;
S.stg.position.set(dio?600:0,Math.sin(T*1.2)*.12,0);S.stg.rotation.z=Math.sin(T*.9)*.01;
// navires teaser
S.sh.forEach((m,i)=>{const a=15.7+i*.4;m.visible=T>a&&!dio;const k=Math.min(1,Math.max(0,(T-a)/.3));m.scale.setScalar(.01+.8*E(k));m.position.y=.6+Math.sin(T*1.6+i)*.12;m.rotation.z=Math.sin(T*1.3+i)*.05;m.rotation.y=Math.PI/2+Math.sin(T*.7+i)*.12});
const c=S.cap;c.rotation.y=Math.sin(T*1.1)*.05;S.head.rotation.x=-A*.06+Math.sin(T*2)*.01;S.head.rotation.z=Math.sin(T*1.7)*.03;
S.head.rotation.y=(T<3.3)?-.3*E((T-.7)/.5):0;
S.mouth.scale.set(1,.35+A*2.6,1);S.mouth.position.y=-.27-A*.07;S.eyes.scale.y=((T%2.6)>2.5)?.15:1;
let xR=0,zR=0,rL=0;
if(T<.9){zR=-.9-A*.5;rL=.15+A*.2}
else if(T<3.4){xR=-1.4-Math.sin(T*8)*.05;zR=-.15;rL=1.2+Math.sin(T*6)*.2}
else if(T<12.3){zR=-.3+A*.2;rL=.3+A*.3}
else if(T<14.6){xR=-1.4-Math.sin(T*8)*.08;zR=-.15;rL=.2+A*.2}
else if(T<18.5){zR=-1.2+Math.sin(T*3)*.1;rL=.3+A*.3}
else{zR=-.2;rL=1.9+Math.sin(T*9)*.35}
S.armR.rotation.set(xR,0,zR);S.armL.rotation.set(0,0,rL);
// caméra
const KC=[[0,-1.6,4.6,6.8,3,6.5,-24],[3.2,-1.2,4.6,6.4,3,3,-24]];
let cp,ct;
if(T<3.3){const k=E(T/3.3);cp=[L_(.7,.4,k),L_(4.8,4.9,k),L_(8,6.4,k)];ct=[L_(.9,.7,k),L_(6.8,6.6,k),-12]}
else if(T<12.3){const y0=300,Z=-30;let pk;
 if(T<5.2){const k=E((T-3.3)/1.9);cp=[L_(-4,0,k),y0+L_(24,18,k),Z+L_(38,34,k)];ct=[0,y0+L_(14,11,k),Z]}
 else if(T<7.4){const k=E((T-5.2)/2.2);cp=[L_(0,-3,k),y0+L_(18,6,k),Z+L_(34,26,k)];ct=[L_(0,-4,k),y0+L_(11,5,k),Z]}
 else if(T<9.6){const k=E((T-7.4)/2.2);cp=[L_(-3,0,k),y0+L_(6,14,k),Z+L_(30,44,k)];ct=[L_(-4,0,k),y0+L_(5,11,k),Z]}
 else{const k=E((T-9.6)/2.7);cp=[L_(0,3,k),y0+L_(14,20,k),Z+L_(44,46,k)];ct=[L_(0,3,k),y0+L_(11,17,k),Z]}}
else if(T<15.6){const k=E((T-12.3)/3.3);cp=[L_(.3,-.4,k),L_(4.6,4.7,k),L_(5.8,7.0,k)];ct=[0,5.8,0]}
else{const k=E((T-15.6)/4.1);cp=[L_(-.4,1.6,k),L_(4.7,5.4,k),L_(6.2,12.5,k)];ct=[L_(0,2.6,k),L_(5.8,5.0,k),L_(0,-8,k)]}
camera.position.set(cp[0],cp[1],cp[2]);controls.target.set(ct[0],ct[1],ct[2]);camera.lookAt(controls.target);
window.__i={t:T,A:A};
