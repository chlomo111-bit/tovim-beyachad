const L=ship.len,B=ship.beam,c=ship.view;[PIR,ENV,...BALLS,...FIRE].forEach(o=>{if(o.parent!==evRoot)evRoot.add(o)});
evRoot.visible=true;const E=k=>{k=Math.max(0,Math.min(1,k));return k*k*(3-2*k)};
if(!window.CRATER){window.CRATER=new THREE.Mesh(new THREE.CylinderGeometry(1,1,.05,20),new THREE.MeshBasicMaterial({color:0x1a1008}));sea.add(CRATER);
 window.SMOKE=[];for(let i=0;i<6;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(1,10,8),new THREE.MeshBasicMaterial({color:0x555555,transparent:true,opacity:.6}));sea.add(s);SMOKE.push(s)}}
const I=ship.group.localToWorld(new THREE.Vector3(1.2,ship.walk[0].y,.2));const sc=L/14;
function boom(t,ti){const k=t-ti;BALLS.forEach(b=>b.visible=false);FIRE.forEach(f=>f.visible=false);CRATER.visible=k>0;CRATER.position.copy(I);CRATER.position.y+=.05;CRATER.scale.set(sc*.9,1,sc*.9);
 SMOKE.forEach((s,i)=>{s.visible=k>0;const a=i*1.05;s.position.set(I.x+Math.cos(a)*sc*.5*(1+k),I.y+sc*(.3+Math.min(k,2)*.5+i*.12),I.z+Math.sin(a)*sc*.5*(1+k));s.scale.setScalar(sc*Math.min(.5,.2+k*.15));s.material.opacity=.5});
 if(k<0){const b=BALLS[0];b.visible=true;const u=E(1+k/1.2*0+0)&&1;const v=Math.min(1,.45+.55*(t/ti));b.position.set(lerp(I.x-L*.25,I.x,v),lerp(I.y+L*.3,I.y,v),lerp(I.z+B*1.3,I.z,v));b.scale.setScalar(sc*1.3);const f=FIRE[2];f.visible=true;f.position.copy(b.position);f.position.x-=sc*.3;f.position.y+=sc*.4;f.position.z+=sc*.6;f.scale.setScalar(sc*.7);f.material.opacity=.6}
 else if(k<.9){const f=FIRE[0];f.visible=true;f.position.copy(I);f.position.y+=sc*.6;f.scale.setScalar(sc*(.8+k*3.2));f.material.opacity=Math.max(0,.95-k*1.4);
  const f2=FIRE[1];f2.visible=k<.5;f2.position.copy(I);f2.position.y+=sc*1.2;f2.scale.setScalar(sc*(.5+k*2.5));f2.material.opacity=Math.max(0,.9-k*1.8)}
 return k}
CRATER.visible=false;SMOKE.forEach(s=>s.visible=false);
const k=Math.min(1,(t+1.6)/2.6),u=(t+.2)/1.4;PIR.visible=true;PIRPOS(.1+.45*k);SHOT(u);ROTZ=-.06;SNK2=.04;
{const p=PIR.position,T=t+2;R.cam(L*(.05-.15*T/8),L*(.62-.1*T/8),L*(1.15-.25*T/8),p.x*.3,L*.02,p.z*.38)}
