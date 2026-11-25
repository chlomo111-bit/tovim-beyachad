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
 // amis (scène 3)
 S.fr=[];const cols=['#C8362B','#2E8FD6','#4C9A4F','#B05AC8'];
 for(let i=0;i<4;i++){const f=mk(V=>{addBox(V,.9,1.3,.55,0,.65,0,cols[i]);addBox(V,.7,.7,.7,0,1.65,0,'#F2C49B');addBox(V,.2,1,.2,-.58,.75,0,cols[i]);addBox(V,.2,1,.2,.58,.75,0,cols[i]);addBox(V,.8,.25,.8,0,2.15,0,'#222')});
  f.position.set([-4.6,-2.8,2.8,4.6][i],1.16,-3.6);f.userData.b=1.5;S.stg.add(f);S.fr.push(f)}
 S.poof=mk(V=>addBox(V,2.2,.1,2.2,0,0,0,'#FFFFFF'));S.stg.add(S.poof);S.poof.visible=false;
 // fonds marins = carte posée à côté du capitaine
 const SB=S.sb=new THREE.Group();S.stg.add(SB);SB.position.set(3.5,5.3,-0.9);SB.scale.setScalar(.12);SB.rotation.x=.35;
 SB.add(mk(V=>addBox(V,31,1,31,0,-.6,0,'#0B2A47')));
 S.tiles=[];S.coarse=[];
 const pat=[[0,0],[0,1],[1,0],[1,1],[1,2],[2,1],[2,2],[2,3],[5,5],[5,6],[6,5],[6,6],[6,7],[7,6],[3,7],[4,0]];
 for(let r=0;r<8;r++)for(let c=0;c<8;c++){const k=pat.findIndex(p=>p[0]===r&&p[1]===c);
  const d=mk(V=>addBox(V,3.5,.4,3.5,0,-.05,0,'#0D2238'));d.position.set((c-3.5)*3.7,0,(r-3.5)*3.7);SB.add(d);
  if(k>=0){const t=mk(V=>addBox(V,3.5,.6,3.5,0,.1,0,'#3FD0FF'));t.position.set((c-3.5)*3.7,0,(r-3.5)*3.7);t.visible=false;SB.add(t);S.tiles.push({m:t,k})}
  else{const q=mk(V=>addBox(V,3.5,.5,3.5,0,.0,0,((r>>1)+(c>>1))%2?'#2A5A80':'#376C94'));q.position.set((c-3.5)*3.7,0,(r-3.5)*3.7);q.visible=false;SB.add(q);S.coarse.push({m:q,o:(r+c)})}}
 S.sat=mk(V=>{addBox(V,1.6,1.2,1.6,0,0,0,'#D8D8E0');addBox(V,4,.15,1.4,-3,0,0,'#2E8FD6');addBox(V,4,.15,1.4,3,0,0,'#2E8FD6')});S.sat.scale.setScalar(.35);S.stg.add(S.sat);
 // navire fantôme (sans personne)
 S.gh=ship(true);S.gh.rotation.y=Math.PI/2;sea.add(S.gh);
 S.hid0=null;
}
const S=window.__S;try{VMAT.transparent=false;VMAT.opacity=1;VMAT.depthWrite=true}catch(e){}
S.old.forEach(c=>c.visible=false);
const sc=T<.87?1:(T<6.8?2:(T<10.2?3:(T<13.4?4:5)));
const ghost=sc===4;
S.stg.position.set(ghost?600:0,Math.sin(T*1.2)*.12,0);S.stg.rotation.z=Math.sin(T*.9)*.01;
S.gh.visible=ghost;
{const g=T-10.2;S.gh.position.set(L_(8,-6,Math.min(1,g/3.2)),.5+Math.sin(T*1.5)*.18,-14+g*.4);S.gh.rotation.z=Math.sin(T*1.1)*.05;S.gh.rotation.y=Math.PI/2+.3*Math.sin(T*.6);S.gh.scale.setScalar(1.6)}
S.fr.forEach((f,i)=>{f.visible=false});
S.sb.visible=T>=.6&&!ghost&&T<10.2;
// quart qui s'allume 0.87 -> 3.67
{const k=Math.min(1,Math.max(0,(T-.95)/2.6));S.tiles.forEach(o=>{o.m.visible=o.k<=k*16-1+.999&&T>.95;o.m.scale.y=T>.95?1+Math.max(0,.5-(T-.95-o.k*.16))*0:1});
 const kc=Math.min(1,Math.max(0,(T-4.13)/1.6));S.coarse.forEach(o=>{o.m.visible=T>4.13&&o.o/14<=kc+.05});}
// satellite
S.sat.visible=T>4.13&&T<7;{const a=(T-4.13)*1.9;S.sat.position.set(3.5+Math.cos(a)*2.2,7.6+Math.sin(a*.7)*.3,Math.sin(a)*1.4);S.sat.rotation.y=a}
// capitaine
const c=S.cap;c.rotation.y=Math.sin(T*1.1)*.05;S.head.rotation.x=-A*.06+Math.sin(T*2)*.01;S.head.rotation.z=Math.sin(T*1.7)*.03;
S.head.rotation.y=(T>.9&&T<6.8)?.38*E((T-.9)/.5):(T>6.8?.38*(1-E((T-6.8)/.4)):0);
S.mouth.scale.set(1,.35+A*2.6,1);S.mouth.position.y=-.27-A*.07;S.eyes.scale.y=((T%2.6)>2.5)?.15:1;
let xR=0,zR=0,rL=0;
if(T<.9){zR=-.9-A*.5;rL=.15+A*.2}
else if(T<6.8){xR=-.3;zR=-.2+A*.2;rL=1.2+Math.sin(T*3)*.1}  // bras gauche vers la carte
else if(T<10.2){xR=-1.4-Math.sin(T*8)*.08;zR=-.15;rL=.3+A*.3}
else if(T<13.4){zR=-.3+A*.2;rL=.3+A*.3}
else{zR=-.2;rL=1.9+Math.sin(T*9)*.35}
S.armR.rotation.set(xR,0,zR);S.armL.rotation.set(0,0,rL);
// caméra
let cp,ct;
if(sc===1){const k=E(T/.9);cp=[L_(.7,1.2,k),L_(5.2,5.6,k),L_(10,14,k)];ct=[L_(.5,1.5,k),L_(5.8,5.6,k),0]}
else if(sc===2){const k=E((T-.87)/5.9);cp=[L_(1.3,2.0,k),L_(5.6,6.2,k),L_(14,12.5,k)];ct=[L_(1.5,1.8,k),L_(5.6,5.4,k),0]}
else if(sc===3){const k=E((T-6.8)/3.4);cp=[L_(2.0,-.3,k),L_(6.2,5.4,k),L_(12.5,14,k)];ct=[L_(1.8,0,k),L_(5.4,5.2,k),0]}
else if(sc===4){const g=(T-10.2)/3.2;cp=[L_(-3,4,g),L_(3.2,4.2,g),L_(4,10,g)];ct=[L_(5,-3,g),3.4,-13]}
else{const k=E((T-13.4)/1.6);cp=[L_(0,.5,k),L_(5.4,4.8,k),L_(14,8,k)];ct=[L_(0,.5,k),L_(5.4,5.6,k),0]}
camera.position.set(cp[0],cp[1],cp[2]);controls.target.set(ct[0],ct[1],ct[2]);camera.lookAt(controls.target);
window.__i={t:T,A:A,sc:sc};
