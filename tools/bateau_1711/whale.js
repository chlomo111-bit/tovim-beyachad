const L=ship.len,B=ship.beam,c=ship.view;[PIR,ENV,...BALLS,...FIRE].forEach(o=>{if(o.parent!==evRoot)evRoot.add(o)});
evRoot.visible=true;PIR.visible=false;BALLS.forEach(b=>b.visible=false);FIRE.forEach(f=>f.visible=false);
const E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)};const wy=ship.walk[0].y;
if(!window.WHL){const V=[];const C1='#2D5B8F',C2='#244A75',W='#E8F0F7';
 for(let k=0;k<9;k++){const s=1-Math.pow(Math.abs(k-2.5)/7,1.4);addBox(V,1.25,2.4*s+.5,2.6*s+.5,k*1.2,0,0,k%2?C1:C2);addBox(V,1.25,.5,1.8*s+.3,k*1.2,-(1.2*s+.25),0,W)}
 addBox(V,1.4,.6,4.4,10.8,.2,0,C1);addBox(V,.9,.5,1.6,10.0,.1,0,C2);
 addBox(V,2.6,.35,1.2,2.2,-.9,1.9,C2);addBox(V,2.6,.35,1.2,2.2,-.9,-1.9,C2);
 for(const s of [1,-1]){addBox(V,.95,.95,.2,-.1,.45,s*1.42,'#FFFFFF');addBox(V,.5,.55,.24,-.25,.4,s*1.46,'#101010');addBox(V,.18,.18,.26,-.35,.55,s*1.48,'#FFFFFF')}
 addBox(V,.2,.18,2.4,-.62,-.35,0,'#101010');addBox(V,.6,.25,.6,1.0,1.42,0,'#1B3A5E');for(const s of [1,-1])addBox(V,1.2,.22,.24,-.15,1.05,s*1.47,'#0d1a2b');
 const m=vmesh(V);m.position.x=-4.6;window.WHI=new THREE.Group();WHI.add(m);window.WHL=new THREE.Group();WHL.add(WHI);sea.add(WHL);
 window.SPL=[];for(let i=0;i<26;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(1,8,6),new THREE.MeshBasicMaterial({color:i%3?0xDDF3FF:0xFFFFFF,transparent:true,opacity:.92}));sea.add(s);SPL.push(s)}}
const ws=L/15;WHL.scale.setScalar(ws);WHL.rotation.set(0,Math.PI/2,0);
// trajectoire : saute depuis -z vers la coque, impact à TI
const ti=TI,k=t-ti;const zh=-B/2;const hx=L*.05;
let u=Math.min(1,(t+ (typeof T0!=='undefined'?T0:0))/ (ti+(typeof T0!=='undefined'?T0:0)));
if(k<0){const z=lerp(zh-ws*11,zh-ws*5.3,E(u)),y=lerp(-ws*1.5,ws*1.6,Math.sin(u*Math.PI*.6));WHL.position.set(hx,y,z);WHI.rotation.z=lerp(-.55,-.05,u)}
else{const kk=Math.min(1,k/1.2);WHL.position.set(hx,lerp(ws*1.6,-ws*3.5,E(kk)),zh-ws*5.3+ws*.6*kk);WHI.rotation.z=lerp(-.05,.6,E(kk))}
const H=new THREE.Vector3(hx,wy*.6,zh);
SPL.forEach((s,i)=>{const kk=k-i*.02;s.visible=kk>0&&kk<1.6;if(s.visible){const a=i*2.39,uu=kk/1.6;s.position.set(H.x+Math.cos(a)*ws*(1+uu*4),H.y+ws*(uu*7-uu*uu*7.5)+Math.sin(a)*ws*.5,H.z-ws*(.5+uu*2.5)+Math.sin(a*1.3)*ws);s.scale.setScalar(ws*(.35+.2*(i%3)));s.material.opacity=Math.max(0,.95-uu*.8)}});
const tk=k>0?E(k/1.5):0;ROTX=.16*tk*Math.cos(Math.max(0,k)*3)*(1/(1+Math.max(0,k)));ROTZ=.02*tk;SNK2=.05+.06*tk;
const sh=k>0&&k<.8?(.8-k)*.9:0;window.__i={whl:WHL.position.toArray().map(v=>+v.toFixed(2)),ws};
const W=WHL.position;
const HD=new THREE.Vector3(W.x,W.y+ws*.3,W.z+ws*4.6);if(MODE==='eye'){R.cam(HD.x+ws*6.5+Math.sin(t*61)*sh,HD.y+ws*1.4+Math.cos(t*47)*sh,HD.z-ws*3.2,HD.x,HD.y,HD.z+ws*.5)}
else if(MODE==='hit'){R.cam(H.x+L*1.1+Math.sin(t*61)*sh,H.y+L*.32+Math.cos(t*47)*sh,zh-ws*.2,H.x-L*.05,H.y+L*.06,zh-ws*1.6)}
else{WHL.position.set(-L*.05,-ws*2.2+ws*.5*Math.sin(t*1.6),B/2+ws*5.5);WHI.rotation.z=.9+.35*Math.sin(t*2.2);ROTX=.07+.04*Math.sin(t*1.8);ROTZ=.03;SNK2=.12+.03*E(t/3);
SPL.forEach(s=>s.visible=false);const a=-1.25+t*.05;R.cam(Math.cos(a)*c.d*.62,c.h*1.3+5,Math.sin(a)*c.d*.62,0,.2,-ws*1.5)}
