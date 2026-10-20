"""BC thin technical glass family, derived from the user-supplied mesh generator.
True meshes, shared optical materials, no raster planes or metal surfaces.
"""
from pathlib import Path
import sys,math,json,hashlib,gzip,struct,shutil,re
import numpy as np
import trimesh as tm
from trimesh.visual.material import PBRMaterial
from pygltflib import GLTF2
import geometry as G
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/glass/models';OUT.mkdir(exist_ok=True)
PBR={
 'clear':PBRMaterial(name='BC thin clear technical glass',baseColorFactor=[.88,.95,1,1],metallicFactor=0,roughnessFactor=.09),
 'ruby':PBRMaterial(name='BC subtle ruby technical glass',baseColorFactor=[1,.83,.87,1],metallicFactor=0,roughnessFactor=.09),
 'edge':PBRMaterial(name='BC cool glass edge',baseColorFactor=[.48,.66,.79,1],metallicFactor=0,roughnessFactor=.26,emissiveFactor=[.04,.09,.14]),
 'signal':PBRMaterial(name='BC ruby signal edge',baseColorFactor=[.72,.002,.024,1],metallicFactor=0,roughnessFactor=.24,emissiveFactor=[.7,.002,.016]),
 'etch':PBRMaterial(name='BC etched pale glass',baseColorFactor=[.35,.47,.57,1],metallicFactor=0,roughnessFactor=.5,emissiveFactor=[.035,.065,.09])}
for key,kind in {'silver':'clear','bright':'edge','steel':'clear','graphite':'clear','black':'clear','red':'ruby','signal':'signal','edge':'edge','etch':'etch'}.items():G.MATERIALS[key]=PBR[kind]
original_add=G.Icon.add
def etched_add(self,mesh,mat='silver',name='part',pos=(0,0,0),rot=None,scale=None):
 if mat=='silver' and name in ['text rule','donut chart sector','pie chart sector','person head','person torso']:mat='etch'
 return original_add(self,mesh,mat,name,pos,rot,scale)
G.Icon.add=etched_add
orig_box,orig_tube,orig_ext=G.box,G.tube,G.extrusion

def tube(ic,pts,r=.025,mat='silver',name='pipe',sides=10,closed=False):
 return orig_tube(ic,pts,min(r*.48,.025), 'signal' if mat in ('signal','red') else 'edge' if r<.05 else mat,name,max(6,min(sides,8)),closed)
G.tube=tube

def box(ic,x,y,z,w,h,d,mat='silver',r=.055,name='glass element'):
 depth=.018 if d<.18 and min(w,h)>.07 else min(d,.012) if d<.09 else d*.66
 node=orig_box(ic,x,y,z,w,h,depth,mat,min(r,.025),name)
 if w>.2 and h>.15:
  pts=G.rounded(w-.003,h-.003,min(r,.025),4)
  orig_tube(ic,[(x+a,y+b,z+depth/2+.002) for a,b in pts],.0035,'signal' if mat=='red' else 'edge','etched pane contour',6,True)
 return node
G.box=box
G.extrusion=lambda points,depth:orig_ext(points,min(depth,.035) if depth<.2 else depth*.5)

def panel(ic,x=0,y=0,z=0,w=2,h=1.45,stand=False):
 box(ic,x,y,z,w,h,.018,'silver',.025,'thin glass panel')
 box(ic,x-.045,y+.035,z-.07,w,h,.018,'silver',.025,'laminated back panel')
 # Corner signals replace heavy frames and screws.
 for sx in [-1,1]:G.sphere(ic,(x+sx*(w/2-.065),y+h/2-.065,z+.012),.009,'edge','etched panel point')
 if stand:
  box(ic,x,y-h/2-.19,z-.015,.08,.32,.018,'silver',.009,'clear monitor stem')
  box(ic,x,y-h/2-.37,z+.03,.58,.018,.32,'silver',.012,'clear monitor foot')
G.panel=panel

def database(ic,x=0,y=0,z=0,r=.56,tiers=3,step=.37):
 for i in range(tiers):
  cy=y+(i-(tiers-1)/2)*step
  shell=G.lathe([(r,-step*.43),(r,step*.43),(r-.018,step*.43),(r-.018,-step*.43),(r,-step*.43)],48)
  ic.add(shell,'silver','hollow glass database shell',(x,cy,z))
  for yy in [cy-step*.43,cy+step*.43]:
   G.arc(ic,(x,yy,z),r,thick=.009,mat='bright',plane='xz',name='fine glass rim',steps=48)
  G.cyl(ic,(x,cy+step*.43-.004,z),r-.018,.008,'silver',name='thin glass end plate')
  if i in [0,tiers-1]:G.arc(ic,(x,cy-step*.43-.003,z),r+.004,.08,math.pi*.54,.009,'signal','ruby partial database arc','xz',48)
  G.sphere(ic,(x-r*.5,cy,z+r*.87),.012,'edge','data status')
G.database=database

def analysis(ic):
 # Three layered analytical panes, data routes and one shared data source.
 for x,w in [(-.91,.7),(0,1.02),(.94,.68)]:panel(ic,x,.18,-.15,w,1.3)
 G.donut(ic,-.91,.39,-.1,.22,.12);G.text_lines(ic,-.91,-.16,-.1,.42,3,.1)
 G.bars(ic,-.35,-.37,-.08,[.19,.29,.41,.55],.13,.07)
 G.polyline(ic,[(-.4,.18,.01),(-.17,.33,.01),(.08,.25,.01),(.4,.64,.01)],.02,'signal','ruby analytical trend')
 G.text_lines(ic,.94,.54,-.1,.44,3,.16);G.donut(ic,.94,-.24,-.1,.19,.10)
 database(ic,0,-.76,.19,.24,2,.16)
 for x in [-.91,.94]:G.polyline(ic,[(0,-.76,.19),(x,-.76,.19),(x,-.48,-.06)],.018,'signal' if x>0 else 'silver','analytical flow')

def optical_export(ic,path):
 ic.scene.apply_translation(-ic.scene.bounds.mean(axis=0))
 # Consolidate by material to keep browser draw calls bounded.
 grouped={}
 for mesh in ic.scene.geometry.values():grouped.setdefault(mesh.visual.material.name,[]).append(mesh)
 scene=tm.Scene()
 for name,meshes in grouped.items():
  mesh=tm.util.concatenate(meshes);mesh.visual=tm.visual.TextureVisuals(material=meshes[0].visual.material)
  scene.add_geometry(mesh,node_name=name,geom_name=name)
 scene.apply_translation(-scene.bounds.mean(axis=0))
 tmp=path.with_suffix('.building.glb');tmp.write_bytes(scene.export(file_type='glb',include_normals=True));G.add_animations(tmp)
 gltf=GLTF2().load(str(tmp))
 for m in gltf.materials:
  m.doubleSided=True;m.pbrMetallicRoughness.metallicFactor=0
  if m.name in ['BC thin clear technical glass','BC subtle ruby technical glass']:
   red='ruby' in m.name
   m.extensions={'KHR_materials_transmission':{'transmissionFactor':.92 if red else .97},'KHR_materials_volume':{'thicknessFactor':.02,'attenuationDistance':.75 if red else 3,'attenuationColor':[.93,.53,.57] if red else [.84,.94,1]},'KHR_materials_ior':{'ior':1.45},'KHR_materials_clearcoat':{'clearcoatFactor':.3,'clearcoatRoughnessFactor':.05}}
 gltf.extensionsUsed=['KHR_materials_transmission','KHR_materials_volume','KHR_materials_ior','KHR_materials_clearcoat']
 gltf.asset.extras={'style':'BC Thin Technical Glass','reference':'BC_Reference_Thin_Glass_Test(3).zip','geometry':'real volumetric meshes, no raster planes','metallic':False,'up':'+Y','front':'+Z'}
 gltf.save_binary(str(tmp));tmp.replace(path)
 return int(sum(len(m.faces) for m in scene.geometry.values())),len(grouped)

records=[]
for n,name in list(enumerate(G.NAMES,1))+[(50,'Data Analysis')]:
 ic=G.Icon(name)
 if n==50:analysis(ic)
 else:G.build(n,ic)
 slug=re.sub('[^a-z0-9]+','-',name.lower());path=OUT/f'{n:02d}-{slug}.glb'
 triangles,draws=optical_export(ic,path)
 records.append({'id':n,'name':name,'file':path.name,'triangles':triangles,'parts':ic.count,'drawCalls':draws,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'animations':['Turntable_360','Float_Idle']})
 print(n,name,triangles,path.stat().st_size,flush=True)
ref=ROOT/'source/reference.glb'
if not ref.exists():ref.write_bytes(gzip.decompress((ROOT/'source/reference.glb.gz').read_bytes()))
shutil.copy2(ref,OUT/'49-data-architecture-reference.glb')
g=GLTF2().load(str(ref));records.append({'id':49,'name':'Data Architecture Reference','file':'49-data-architecture-reference.glb','bytes':ref.stat().st_size,'sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'animations':[a.name for a in g.animations],'referenceOriginal':True})
records.sort(key=lambda r:r['id']);(ROOT/'assets/glass/catalog.generated.json').write_text(json.dumps(records,indent=2))
