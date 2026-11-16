const L=ship.len,B=ship.beam,c=ship.view;[PIR,ENV,...BALLS,...FIRE].forEach(o=>{if(o.parent!==evRoot)evRoot.add(o)});
evRoot.visible=true;PIR.visible=false;const E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)};
const wy=ship.walk[0].y;const sc=L/14;
if(!window.HOLE){window.HOLE=new THREE.Mesh(new THREE.CircleGeometry(1,20),new THREE.MeshBasicMaterial({color:0x0a0604,side:THREE.DoubleSide}));ship.group.add(HOLE);
 window.SPR=[];for(let i=0;i<14;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(1,8,6),new THREE.MeshBasicMaterial({color:i%3?0xCFEFFF:0xFFFFFF,transparent:true,opacity:.9}));sea.add(s);SPR.push(s)}
 window.SMK=[];for(let i=0;i<5;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(1,10,8),new THREE.MeshBasicMaterial({color:0x4a4a4a,transparent:true,opacity:.55}));sea.add(s);SMK.push(s)}}
const hl=new THREE.Vector3(HX,wy*.95,-B/2-.06);HOLE.position.copy(hl);HOLE.rotation.set(0,Math.PI,0);
const H=ship.group.localToWorld(hl.clone());
const ti=TI,k=t-ti;
HOLE.visible=k>0;HOLE.scale.setScalar(sc*.55*Math.min(1,.4+k*3));
BALLS.forEach(b=>b.visible=false);FIRE.forEach(f=>f.visible=false);
if(k<0){const b=BALLS[0];b.visible=true;const v=Math.max(0,Math.min(1,.62+.38*(1+k/ti)));b.position.set(lerp(H.x+L*.22,H.x,v),lerp(H.y+L*.12,H.y,v),lerp(H.z-L*.32,H.z,v));b.scale.setScalar(sc*1.05);const f=FIRE[2];f.visible=true;f.position.set(b.position.x+sc*.5,b.position.y+sc*.3,b.position.z-sc*.6);f.scale.setScalar(sc*.6);f.material.opacity=.7}
else if(k<.8){const f=FIRE[0];f.visible=true;f.position.copy(H);f.position.z-=sc*.4;f.scale.setScalar(sc*(.9+k*3.5));f.material.opacity=Math.max(0,.95-k*1.3);
 const f2=FIRE[1];f2.visible=k<.45;f2.position.copy(H);f2.position.z-=sc*.6;f2.position.y+=sc*.4;f2.scale.setScalar(sc*(.5+k*2.6));f2.material.opacity=Math.max(0,.9-k*2)}
SPR.forEach((s,i)=>{const kk=k-.05-i*.035;s.visible=kk>0;if(kk>0){const a=i*2.39,u=(kk%1.1);s.position.set(H.x+Math.cos(a)*sc*.35*(1+u*2),H.y+sc*(Math.sin(a)*.3+u*1.6-u*u*1.9),H.z-sc*(.15+u*1.4));s.scale.setScalar(sc*(.14+.06*(i%3)));s.material.opacity=Math.max(0,.95-u*.7)}});
SMK.forEach((s,i)=>{const kk=k-.15;s.visible=kk>0;if(kk>0){s.position.set(H.x+(i-2)*sc*.25,H.y+sc*(.4+kk*.5+i*.1),H.z-sc*(.3+kk*.3));s.scale.setScalar(sc*Math.min(.32,.15+kk*.12));}});
const tk=E(k/2.2);ROTZ=0;ROTX=-.10*tk;SNK2=.04+.10*tk;
const sh=k>0&&k<.7?(.7-k)*.5:0;const d=1-t*.03;
R.cam(H.x-L*.18*d+Math.sin(t*61)*sh,H.y+L*.22*d+Math.cos(t*47)*sh,H.z-L*.55*d,H.x,H.y-L*.02,H.z+B*.3);
