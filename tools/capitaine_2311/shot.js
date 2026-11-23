// Plateau « הקפטן מספר » : הקפטן parle (bouche sur l'amplitude de la voix), caméra qui bouge, Endurance qui remonte, banquise, navire de guerre qui coule (teaser).
const T=t, E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)}, L_=(a,b,k)=>a+(b-a)*k;
const A=(window.AMP&&window.AMP.length)?(window.AMP[Math.max(0,Math.min(window.AMP.length-1,Math.floor((window.TS!==undefined?window.TS:T)*30)))]||0):0;
if(!window.__S){
 const S=window.__S={};
 const mk=f=>{const V=[];f(V);return vmesh(V)};
 sea.background=new THREE.Color('#CFE3F0');sea.fog=new THREE.Fog(new THREE.Color('#CFE3F0'),50,260);
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
 // Endurance
 S.end=new THREE.Group();const en=new THREE.Group();S.end.add(en);S.endI=en;
 en.add(mk(V=>{addBox(V,13,1.8,3.6,0,0,0,'#4A2F1B');addBox(V,3,1.6,2.6,7.6,.1,0,'#4A2F1B');addBox(V,1.6,1.4,1.4,9.5,.3,0,'#4A2F1B');addBox(V,13.2,.25,3.7,0,1.0,0,'#8A6A43');addBox(V,3,.25,2.7,7.6,1.0,0,'#8A6A43');addBox(V,5,1.2,2.6,-4,1.7,0,'#6B4A2B');addBox(V,2.2,1,2.4,-.4,1.6,0,'#6B4A2B');
  for(const x of [-3.5,.5,4.2]){addBox(V,.3,10,.3,x,6,0,'#2A1A0E');addBox(V,.2,.2,4.6,x,9.3,0,'#2A1A0E');addBox(V,.2,.2,3.6,x,6.8,0,'#2A1A0E');addBox(V,.1,2.2,3.4,x+.15,8.0,0,'#E8E2D0');addBox(V,.1,2.0,2.8,x+.15,5.6,0,'#DAD2BC')}
  addBox(V,4,.2,.2,11,1.6,0,'#2A1A0E');addBox(V,.14,.14,9,2,3,1.4,'#2A1A0E')}));
 sea.add(S.end);S.end.position.set(7,-14,-22);S.end.rotation.y=.35;
 // navire de guerre (teaser)
 S.vasa=new THREE.Group();const vi=new THREE.Group();S.vasa.add(vi);S.vasaI=vi;
 vi.add(mk(V=>{addBox(V,12,2.2,3.8,0,0,0,'#5A3A1E');addBox(V,3,2.6,3.4,-5,1.6,0,'#7A5028');addBox(V,12.4,.2,4,0,1.2,0,'#C9A24B');addBox(V,3,1.8,2.6,7,.2,0,'#5A3A1E');
  for(const x of [-3,0,3])for(const z of [1.95,-1.95])addBox(V,.5,.4,.14,x,.3,z,'#111');
  for(const x of [-2.5,2.5]){addBox(V,.3,9,.3,x,6,0,'#2A1A0E');addBox(V,.1,2.6,3.4,x+.15,7.6,0,'#F0E8D0');addBox(V,.1,2.2,3.0,x+.15,5.0,0,'#E6DCC0')}
  addBox(V,.1,1.2,1.0,-2.5,11,0,'#FFC24B')}));
 sea.add(S.vasa);S.vasa.position.set(-4.5,.3,-11);S.vasa.rotation.y=-.4;S.vasa.scale.setScalar(1.15);S.vasa.visible=false;
 // banquise
 S.ice=[];const R=(()=>{let s=77;return()=>{s=(s*16807)%2147483647;return s/2147483647}})();
 for(let i=0;i<14;i++){const m=mk(V=>{const w=2+R()*4,h=.6+R()*1.2,d=2+R()*3;addBox(V,w,h,d,0,h/2-.3,0,'#F4FAFF');addBox(V,w*.7,h*.8,d*.7,.2,h-.1,0,'#DDEFFA')});m.position.set((R()-.5)*50,0,-8-R()*40);m.userData.p=R()*6;sea.add(m);S.ice.push(m)}
 S.berg=mk(V=>{addBox(V,12,9,9,0,3.5,0,'#EAF6FF');addBox(V,8,6,6,-1,9,0,'#F5FBFF');addBox(V,5,4,5,2,12,0,'#FFFFFF');addBox(V,12.2,1,9.2,0,-.5,0,'#9CCBE6')});S.berg.position.set(-22,0,-42);sea.add(S.berg);
 sea.add(new THREE.AmbientLight(0xffffff,.25));
}
const S=window.__S;
// visibilité selon le temps
S.vasa.visible=T>11.6;
S.end.visible=T<12.4;
// Endurance remonte de 4.6 à 8.4 (sous l'eau puis droite et visible)
const kE=E((T-4.4)/3.2);S.end.position.y=L_(-13,0.2,kE)+Math.sin(T*1.3)*.15;S.end.rotation.z=(1-kE)*.12+Math.sin(T*1.1)*.01;
// navire de guerre qui coule (12.3→15.8)
if(T>11.6){const k=E((T-12.3)/3.5);S.vasa.position.y=.3-k*6.5;S.vasa.rotation.z=k*.55;S.vasa.rotation.x=k*.08}
S.ice.forEach(m=>{m.position.y=Math.sin(T*.8+m.userData.p)*.12;m.position.x+=0});
// plateforme et capitaine
S.stg.position.y=Math.sin(T*1.2)*.12;S.stg.rotation.z=Math.sin(T*.9)*.01;
const c=S.cap;c.rotation.y=Math.sin(T*1.1)*.05;S.head.rotation.x=-A*.06+Math.sin(T*2)*.01;S.head.rotation.z=Math.sin(T*1.7)*.03;S.head.rotation.y=(T>5.4&&T<9.5)?-.35*E((T-5.4)/.6)*(1-E((T-9.2)/.3)):0;
S.mouth.scale.set(1,.35+A*2.6,1);S.mouth.position.y=-.27-A*.07;
const bl=(T%2.6)>2.5;S.eyes.scale.y=bl?.15:1;
const pulse=Math.sin(T*8)*.05;
// bras : gestes selon la phrase
let rR=0,rL=0,xR=0,zR=0;
if(T<2.2){zR=-.9-A*.5;rL=.15+A*.2}
else if(T<4.2){zR=-.35+Math.sin(T*3)*.2;rL=.25+A*.3}
else if(T<5.5){zR=-.2;rL=.3+A*.3}
else if(T<9.5){zR=-1.45+Math.sin(T*4)*.06;rL=.25+A*.35}       // montre la mer
else if(T<11.95){xR=-1.4-pulse;zR=-.15;rL=.2}                  // pointe vers le spectateur
else if(T<14.9){zR=-.4+A*.25;rL=.4-A*.2}
else {zR=-.2;rL=1.9+Math.sin(T*9)*.35}                          // salut : « עקבו »
S.armR.rotation.set(xR,0,zR);S.armL.rotation.set(0,0,rL);
// caméra : trajectoire continue
const K=[[0,.4,4.55,5.4,0,4.3,0],[2.1,.1,4.55,4.4,0,4.3,0],[2.6,3.8,4.3,8.6,0,3.5,0],[4.2,5.2,3.8,10.2,-1.5,3.6,-4],
  [5.4,-5.2,3.9,6,5,3.1,-22],[7.4,-5.3,3.6,-4,6,2.8,-22],[9.3,-5.4,3.4,-9,7,2.8,-22],[10.0,.5,4.3,6.2,.2,4.1,0],[11.9,-.2,4.2,5.4,.2,4.0,0],
  [12.6,1.8,4.5,8.2,-2.0,3.6,-4],[14.3,1.2,4.4,7.0,-1.6,3.8,-4],[15.3,0,4.4,4.8,0,4.2,0],[16.2,0,4.4,4.4,0,4.2,0]];
let i=0;while(i<K.length-2&&T>=K[i+1][0])i++;
const a=K[i],b=K[i+1];const kk=E((T-a[0])/Math.max(.01,b[0]-a[0]));const cut=(b[0]-a[0])<.2; // sauts courts = coupes
const g=cut?(T>=b[0]?1:0):kk;
const P=j=>L_(a[j],b[j],g);
camera.position.set(P(1),P(2),P(3));controls.target.set(P(4),P(5),P(6));camera.lookAt(controls.target);
window.__i={t:T,A:A};
