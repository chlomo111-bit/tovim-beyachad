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
 const ship=(big)=>mk(V=>{addBox(V,3.2,.7,1.4,0,.35,0,'#5A3A1E');addBox(V,3.4,.18,1.5,0,.75,0,'#8E6A3F');addBox(V,.14,3,.14,0,2.2,0,'#2A1A0E');addBox(V,.08,2.2,1.5,.1,2.2,0,'#F0E8D0');addBox(V,.08,.5,.5,.1,3.9,0,big?'#FFC24B':'#C8362B');
  if(big){addBox(V,.14,2.2,.14,1.0,1.9,0,'#2A1A0E');addBox(V,.08,1.6,1.1,1.1,1.9,0,'#F0E8D0')}});
 // 5 navires (scène 1)
 S.sh=[];for(let i=0;i<5;i++){const m=ship(i===4);m.rotation.y=Math.PI/2;sea.add(m);S.sh.push(m)}
 // globe voxel + anneau + navires
 const G=S.glob=new THREE.Group();sea.add(G);G.position.set(0,300,-30);
 G.add(mk(V=>{const R=8;for(let x=-R;x<=R;x++)for(let y=-R;y<=R;y++)for(let z=-R;z<=R;z++){const d=Math.sqrt(x*x+y*y+z*z);if(d>R||d<R-1.3)continue;
   const land=(Math.sin(x*.9+y*.4)+Math.cos(z*.8-y*.5)+Math.sin((x+z)*.5))>1.15;addBox(V,1,1,1,x,y,z,land?'#4C9A4F':'#2B78B8')}}));
 S.dots=[];for(let i=0;i<48;i++){const a=i/48*Math.PI*2;const d=mk(V=>addBox(V,.34,.34,.34,0,0,0,'#FFC24B'));d.position.set(Math.sin(a)*11.5,0,Math.cos(a)*11.5);G.add(d);S.dots.push(d)}
 S.spain=mk(V=>{addBox(V,.2,3,.2,0,1.5,0,'#2A1A0E');addBox(V,1.4,.9,.1,.7,2.6,0,'#C8362B');addBox(V,1.4,.3,.12,.7,2.6,0,'#FFC24B')});S.spain.position.set(0,0,13.6);G.add(S.spain);
 S.vic=ship(true);S.vic.scale.setScalar(1.15);G.add(S.vic);
 S.mag=ship(false);S.mag.scale.setScalar(1.0);G.add(S.mag);
 S.mx=mk(V=>{addBox(V,.3,3,.3,0,1.5,0,'#FFC24B');addBox(V,2,.3,.3,0,2.4,0,'#FFC24B')});G.add(S.mx);
 // amis (scène 3)
 S.fr=[];const cols=['#C8362B','#2E8FD6','#4C9A4F','#B05AC8'];
 for(let i=0;i<4;i++){const f=mk(V=>{addBox(V,.9,1.3,.55,0,.65,0,cols[i]);addBox(V,.7,.7,.7,0,1.65,0,'#F2C49B');addBox(V,.2,1,.2,-.58,.75,0,cols[i]);addBox(V,.2,1,.2,.58,.75,0,cols[i]);addBox(V,.8,.25,.8,0,2.15,0,'#222')});
  f.position.set([-4.6,-2.8,2.8,4.6][i],1.16,-3.6);f.userData.b=1.5;S.stg.add(f);S.fr.push(f)}
 S.poof=mk(V=>addBox(V,2.2,.1,2.2,0,0,0,'#FFFFFF'));S.stg.add(S.poof);S.poof.visible=false;
 // fonds marins (teaser)
 const SB=S.sb=new THREE.Group();sea.add(SB);SB.position.set(0,300,-150);
 SB.add(mk(V=>addBox(V,30,1,30,0,-.6,0,'#06101C')));
 S.tiles=[];for(let r=0;r<8;r++)for(let c=0;c<8;c++){const t=mk(V=>addBox(V,3.5,.5,3.5,0,0,0,'#2E8FD6'));t.position.set((c-3.5)*3.7,0,(r-3.5)*3.7);SB.add(t);S.tiles.push({m:t,r,c})}
 S.tdark=[];for(let r=0;r<8;r++)for(let c=0;c<8;c++){const t=mk(V=>addBox(V,3.5,.4,3.5,0,-.05,0,'#0D2238'));t.position.set((c-3.5)*3.7,0,(r-3.5)*3.7);SB.add(t)}
 S.lit=[];const pat=[[0,0],[0,1],[1,0],[1,1],[1,2],[2,1],[2,2],[2,3],[5,5],[5,6],[6,5],[6,6],[6,7],[7,6],[3,7],[4,0]];
 S.tiles.forEach(o=>{const k=pat.findIndex(p=>p[0]===o.r&&p[1]===o.c);o.k=k;o.m.visible=false});
 sea.add(new THREE.AmbientLight(0xffffff,.25));
 const ours=[S.stg,S.glob,S.sb,...S.sh];S.others=sea.children.filter(c=>!ours.includes(c)&&!S.old.includes(c)&&(c.isMesh||c.isGroup||c.isPoints||c.isLine));
}
const S=window.__S;try{VMAT.transparent=false;VMAT.opacity=1;VMAT.depthWrite=true}catch(e){}
S.old.forEach(c=>c.visible=false);
const sc=T<4.0?1:(T<11.88?2:(T<15.29?3:(T<17.81?4:5)));
const darkBg=(sc===2||sc===4);
sea.background.copy(darkBg?S.bgB:S.bgA);sea.fog.color.copy(darkBg?S.bgB:S.bgA);sea.fog.near=darkBg?400:50;sea.fog.far=darkBg?900:260;
if(darkBg){if(!S.hid){S.others.forEach(c=>{c.__v=c.visible});S.hid=true}S.others.forEach(c=>c.visible=false)}else if(S.hid){S.others.forEach(c=>c.visible=c.__v);S.hid=false}S.glob.visible=sc===2;S.sb.visible=sc===4;
// capitaine : cacher son plateau pendant globe/fonds marins (il est à x=600)
S.stg.position.set(darkBg?600:0,Math.sin(T*1.2)*.12,0);S.stg.rotation.z=Math.sin(T*.9)*.01;
// --- scène 1 : 5 navires partent, 4 disparaissent
S.sh.forEach((m,i)=>{m.visible=sc===1;const base=[-7,-3.6,3.6,7,0][i];const go=E((T-.62)/1.7);
 let z=-9-go*(i===4?30:38), x=base*(1-go*.35)+(i===4?0:0);
 let sc_=1;if(i<4){const v=2.5+i*.32;const k=E((T-v)/.45);sc_=1-k;m.position.set(x,.6+Math.sin(T*1.6+i)*.12-k*.8,z)}else{sc_=1.35;m.position.set(x*(1-E((T-2.4)/1.4)),.6+Math.sin(T*1.6+i)*.12,z+ (T>2.4?E((T-2.4)/1.5)*12:0))}
 m.scale.setScalar(Math.max(.001,sc_));m.rotation.z=Math.sin(T*1.3+i)*.05;m.rotation.y=Math.PI/2+Math.sin(T*.7+i)*.08});
// --- scène 2 : globe
{const t0=4.0,tEnd=10.25;const p=Math.min(1,Math.max(0,(T-t0)/(tEnd-t0)));const a=p*Math.PI*2;
 S.vic.position.set(Math.sin(a)*11.5,.4+Math.sin(T*2)*.1,Math.cos(a)*11.5);S.vic.rotation.y=a+Math.PI/2*0;
 const pm=Math.min(1,Math.max(0,(T-t0)/(7.0-t0)));const am=pm*Math.PI*1.0*0.62;
 S.mag.position.set(Math.sin(am)*11.5,.4+Math.sin(T*2+1)*.1,Math.cos(am)*11.5);S.mag.rotation.y=am;S.mag.visible=T<7.0;
 S.mx.position.set(Math.sin(am)*11.5,0,Math.cos(am)*11.5);S.mx.visible=T>=7.0;S.mx.scale.y=E((T-7.0)/.4)||.001;
 S.dots.forEach((d,i)=>{const ai=i/48*Math.PI*2;d.visible=ai<=a+.05;d.scale.setScalar(T>10.25?1+.5*Math.max(0,Math.sin((T-10.25)*5)):1)});
 S.glob.rotation.y=0;S.vic.visible=true;
}
// --- scène 3 : amis, un disparaît
S.fr.forEach((f,i)=>{f.visible=sc===3;const k=i===2?E((T-13.9)/.35):0;f.scale.setScalar(Math.max(.001,(1-k)*1.5));f.visible=f.visible&&!(i===2&&T>14.3);f.position.y=1.16+(i===2?k*1.5:0)});
S.poof.visible=sc===3&&T>13.9&&T<14.7;{const k=(T-13.9)/.8;S.poof.scale.set(.5+k*3,1,.5+k*3);S.poof.position.set(2.8,1.3,-3.6)}
// --- scène 4 : fonds marins
{const k=Math.min(1,Math.max(0,(T-15.4)/1.8));S.tiles.forEach(o=>{o.m.visible=sc===4&&o.k>=0&&o.k<=k*pl(16)});function pl(n){return n}}
// capitaine
const c=S.cap;c.rotation.y=Math.sin(T*1.1)*.05;S.head.rotation.x=-A*.06+Math.sin(T*2)*.01+((T>6.94&&T<8.4)?.22*E((T-6.94)/.3):0);S.head.rotation.z=Math.sin(T*1.7)*.03;
S.head.rotation.y=(T<2.5)?-.3*E((T-.7)/.5):0;
S.mouth.scale.set(1,.35+A*2.6,1);S.mouth.position.y=-.27-A*.07;S.eyes.scale.y=((T%2.6)>2.5)?.15:1;
let xR=0,zR=0,rL=0;
if(T<.6){zR=-.9-A*.5;rL=.15+A*.2}
else if(T<4.0){xR=-1.4-Math.sin(T*8)*.05;zR=-.15;rL=1.2+Math.sin(T*6)*.2}
else if(T<11.88){zR=-.3+A*.2;rL=.3+A*.3}
else if(T<15.3){xR=-1.4-Math.sin(T*8)*.08;zR=-.15;rL=.2+A*.2}
else if(T<17.8){zR=-.3+A*.2;rL=.3+A*.3}
else{zR=-.2;rL=1.9+Math.sin(T*9)*.35}
S.armR.rotation.set(xR,0,zR);S.armL.rotation.set(0,0,rL);
// caméra
let cp,ct;
if(sc===1){const k=E((T-.5)/1.6);cp=[L_(.7,6.5,k),L_(4.8,6.2,k),L_(8,10,k)];ct=[L_(.9,-1.5,k),L_(6.8,3.2,k),L_(-12,-18,k)];
 if(T>2.3){const k2=E((T-2.3)/1.7);cp=[L_(6.5,3,k2),L_(6.2,5.2,k2),L_(10,6.5,k2)];ct=[L_(-1.5,.5,k2),L_(3.2,5.3,k2),L_(-18,-4,k2)]}}
else if(sc===2){const p=Math.min(1,Math.max(0,(T-4.0)/6.25));const a=p*Math.PI*2-.45;const R=L_(44,36,E((T-4)/6));cp=[Math.sin(a)*R,300+L_(14,16,E((T-4)/7)),-30+Math.cos(a)*R];ct=[0,300,-30];
 if(T>10.25){const k=E((T-10.25)/1.6);cp=[L_(Math.sin(-.45+Math.PI*2)*36,0,k),300+L_(16,24,k),-30+L_(Math.cos(-.45)*36,50,k)];ct=[0,300,-30]}}
else if(sc===3){const k=E((T-11.88)/3.4);cp=[L_(.3,-.3,k),L_(5.2,5.8,k),L_(14,15.5,k)];ct=[0,L_(7.6,7.0,k),0]}
else if(sc===4){const k=E((T-15.29)/2.5);cp=[L_(-14,10,k),300+L_(20,26,k),-150+L_(22,26,k)];ct=[0,300,-150]}
else{const k=E((T-17.81)/1.4);cp=[L_(.3,.7,k),L_(4.6,4.8,k),L_(6,8,k)];ct=[L_(0,.9,k),L_(5.8,6.8,k),L_(0,-12,k)]}
camera.position.set(cp[0],cp[1],cp[2]);controls.target.set(ct[0],ct[1],ct[2]);camera.lookAt(controls.target);
window.__i={t:T,A:A,sc:sc};
