const L=ship.len,B=ship.beam,c=ship.view;[PIR,ENV,...BALLS,...FIRE].forEach(o=>{if(o.parent!==evRoot)evRoot.add(o)});
evRoot.visible=true;PIR.visible=true;BALLS.forEach(b=>b.visible=false);FIRE.forEach(f=>f.visible=false);
const E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)};
if(!window.WHL){const V=[];const C1='#2D5B8F',C2='#244A75',W='#E8F0F7';
 for(let k=0;k<9;k++){const s=1-Math.pow(Math.abs(k-2.5)/7,1.4);addBox(V,1.25,2.4*s+.5,2.6*s+.5,k*1.2,0,0,k%2?C1:C2);addBox(V,1.25,.5,1.8*s+.3,k*1.2,-(1.2*s+.25),0,W)}
 addBox(V,1.4,.6,4.4,10.8,.2,0,C1);addBox(V,.9,.5,1.6,10.0,.1,0,C2);
 addBox(V,2.6,.35,1.2,2.2,-.9,1.9,C2);addBox(V,2.6,.35,1.2,2.2,-.9,-1.9,C2);
 for(const s of [1,-1]){addBox(V,.95,.95,.2,-.1,.45,s*1.42,'#FFFFFF');addBox(V,.5,.55,.24,-.25,.4,s*1.46,'#101010');addBox(V,.18,.18,.26,-.35,.55,s*1.48,'#FFFFFF')}
 addBox(V,.2,.18,2.4,-.62,-.35,0,'#101010');addBox(V,.6,.25,.6,1.0,1.42,0,'#1B3A5E');for(const s of [1,-1])addBox(V,1.2,.22,.24,-.15,1.05,s*1.47,'#0d1a2b');
 const m=vmesh(V);m.position.x=-4.6;window.WHI=new THREE.Group();WHI.add(m);window.WHL=new THREE.Group();WHL.add(WHI);sea.add(WHL);
 window.SPL=[];for(let i=0;i<26;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(1,8,6),new THREE.MeshBasicMaterial({color:i%3?0xDDF3FF:0xFFFFFF,transparent:true,opacity:.92}));sea.add(s);SPL.push(s)}}
const ws=L/15;WHL.scale.setScalar(ws);WHL.rotation.set(0,Math.PI/2,0);
// 18.11 : le lavyatan saute et retombe sur le bateau PIRATE (impact à TI), qui chavire
const zP=-(B/2+L*.75),xP=L*.3,T0v=(typeof T0!=='undefined'?T0:0);
const k=t-TI,u=Math.min(1,(t+T0v)/(TI+T0v));
let py=-.2,prx=0,prz=0;
if(k<0){const y=-ws*2+ws*22*u-ws*18.5*u*u;WHL.position.set(xP,y,lerp(zP-ws*11,zP-ws*4.4,u));WHI.rotation.z=lerp(-.65,.4,u)}
else{const kk=Math.min(1,k/1.4);WHL.position.set(xP,lerp(ws*1.5,-ws*4,E(kk)),zP-ws*4.4+ws*1.2*kk);WHI.rotation.z=lerp(.4,.9,E(kk));
 py=-.2-ws*2.6*E(k/1.8);prx=-.5*E(k/1.0);prz=.12*Math.sin(k*5)/(1+k*2)}
PIR.position.set(xP,py+Math.sin(t*2.4)*.08,zP);PIR.rotation.set(prx,0,prz+Math.sin(t*2)*.03);
const H=new THREE.Vector3(xP,1.5,zP);
SPL.forEach((s,i)=>{const kk=k-i*.02;s.visible=kk>0&&kk<1.8;if(s.visible){const a=i*2.39,uu=kk/1.8;s.position.set(H.x+Math.cos(a)*ws*(1.5+uu*6),H.y+ws*(uu*9-uu*uu*9.5)+Math.sin(a)*ws*.5,H.z+Math.sin(a*1.3)*ws*(1.5+uu*4));s.scale.setScalar(ws*(.45+.25*(i%3)));s.material.opacity=Math.max(0,.95-uu*.8)}});
// la ספינה tangue sous la vague
const tk=k>0?E(k/1.5):0;ROTX=-.05*tk*Math.cos(Math.max(0,k)*3);ROTZ=.01;SNK2=.04;
const sh=k>0&&k<.7?(.7-k)*1.0:0;window.__i={whl:WHL.position.toArray().map(v=>+v.toFixed(2)),ws,L};
if(MODE==='pir'){R.cam(xP+L*2.0+Math.sin(t*61)*sh,L*.42+Math.cos(t*47)*sh,zP-ws*3.2-t*ws*.3,xP,ws*3.4,zP-ws*4.2)}
else if(MODE==='close'){R.cam(xP+L*.55+Math.sin(t*61)*sh,ws*3.2+Math.cos(t*47)*sh,zP+L*.45,xP,ws*1.4,zP-ws*2.5)}
