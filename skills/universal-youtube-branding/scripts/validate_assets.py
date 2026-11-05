#!/usr/bin/env python3
"""Strict six-asset technical QA; visual/brand review remains a separate gate.

Example:
 python validate_assets.py ./out/project --profile reference6 --report ./out/project/reports/qa.json --manifest-out ./out/project/manifest.json --safe-preview ./out/project/reports/SafeArea.jpg

Exit 0 if six technically valid files + upload JPG. Exits 2 otherwise.
The PASS result is *technical only*, not proof of accurate text, different scenes,
YouTube handle availability, image provenance or creative quality.
"""
import argparse,hashlib,json,pathlib,sys
from PIL import Image,ImageChops,ImageOps,ImageStat,ImageDraw
ROOT=pathlib.Path(__file__).resolve().parents[1]

def asset_spec(profile):
 return json.loads((ROOT/'templates'/('asset_spec_reference6.json' if profile=='reference6' else 'asset_spec.json')).read_text(encoding='utf-8'))

def sha256(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1<<20),b''):h.update(block)
 return h.hexdigest()

def compare_same_scene(path1,path2):
 """High-confidence pixel near-duplicate warning, not a semantic similarity test."""
 try:
  with Image.open(path1) as a,Image.open(path2) as b:
   aa=ImageOps.fit(a.convert('RGB'),(80,45),method=Image.Resampling.BICUBIC)
   bb=ImageOps.fit(b.convert('RGB'),(80,45),method=Image.Resampling.BICUBIC)
   diff=ImageChops.difference(aa,bb)
   return sum(ImageStat.Stat(diff).mean)/3
 except Exception:return None

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('project_root',help='Project directory containing 01_SIX_MAIN_ASSETS & 02_YOUTUBE_READY')
 ap.add_argument('--profile',choices=['reference6','legacy5'],default='reference6')
 ap.add_argument('--report')
 ap.add_argument('--manifest-out')
 ap.add_argument('--safe-preview')
 ap.add_argument('--human-review',help='Completed manual review JSON; never generated as approved automatically')
 args=ap.parse_args()
 root=pathlib.Path(args.project_root).resolve()
 spec=asset_spec(args.profile)
 rows=[];errors=[];warnings=[];manifest=[];valid_paths={}
 expected=spec['required_assets']+spec.get('upload_assets',[])
 if len(spec['required_assets'])!=6 and args.profile=='reference6':errors.append('SPEC_COUNT_NOT_SIX')
 for item in expected:
  rel=item['filename'];f=root/rel
  rec={'file':rel,'status':'PASS','issues':[]}
  if not f.is_file():
   rec['issues'].append('MISSING');errors.append(rel+':MISSING')
  else:
   try:
    with Image.open(f) as im:
     im.load()
     rec.update({'dimensions':[im.width,im.height],'format':im.format,'mode':im.mode,'bytes':f.stat().st_size})
     if (im.width,im.height)!=(item['width'],item['height']):rec['issues'].append('WRONG_DIMENSIONS')
     if im.format!=item['format']:rec['issues'].append('WRONG_FORMAT')
     if im.format=='JPEG' and im.mode not in ('RGB','L'):rec['issues'].append('UNUSUAL_JPEG_COLOR_MODE')
     if item.get('alpha_required'):
      if 'A' not in im.getbands():rec['issues'].append('NO_ALPHA_CHANNEL')
      else:
       hist=im.getchannel('A').histogram();n=im.width*im.height
       tr=hist[0]/n;nontr=(n-hist[0])/n
       rec.update({'fully_transparent_fraction':round(tr,5),'visible_content_fraction':round(nontr,5)})
       if tr<item.get('minimum_fully_transparent_fraction',0.02):rec['issues'].append('INSUFFICIENT_REAL_TRANSPARENCY')
       if nontr<item.get('minimum_content_fraction',0.03):rec['issues'].append('NEARLY_EMPTY_LOGO')
     if item.get('max_bytes') is not None and f.stat().st_size>item['max_bytes']:rec['issues'].append('EXCEEDS_UPLOAD_LIMIT')
     rec['sha256']=sha256(f)
     valid_paths[item.get('id',rel)]=f
   except Exception as e:rec['issues'].append('CANNOT_DECODE:'+str(e))
  if rec['issues']:
   rec['status']='FAIL'
   errors.extend([rel+':'+e for e in rec['issues']])
  rows.append(rec)
  manifest.append({'id':item.get('id','bonus'),'file':rel,'role':item.get('role','youtube_ready'), 'expected_dimensions':[item['width'],item['height']],'actual_dimensions':rec.get('dimensions'), 'sha256':rec.get('sha256'), 'status':rec['status'],'source_provenance':'NOT_MACHINE_VERIFIED'})
 # Exactly six files of final image type in primary directory for strict six-profile.
 if args.profile=='reference6':
  maindir=root/'01_SIX_MAIN_ASSETS'
  if maindir.is_dir():
   expected_names={pathlib.PurePosixPath(it['filename']).name for it in spec['required_assets']}
   found={p.name for p in maindir.iterdir() if p.is_file() and p.suffix.lower() in ('.jpg','.jpeg','.png','.webp')}
   extras=found-expected_names
   if extras:
    errors.append('UNEXPECTED_MAIN_ASSETS:'+','.join(sorted(extras)))
  if '02' in valid_paths and '06' in valid_paths:
   mse=compare_same_scene(valid_paths['02'],valid_paths['06'])
   if mse is not None:
    if mse < 3.0:errors.append('SCENES_A_B_NEAR_DUPLICATE_HIGH_CONFIDENCE')
    elif mse < 11.0:warnings.append('SCENES_A_B_VISUALLY_SIMILAR_CHECK_DISTINCT_LAYOUT_MANUALLY')
    else:warnings.append('SCENES_A_B_NOT_CONFIRMED_DISTINCT_BY_HUMAN')
 if args.profile=='legacy5':warnings.append('LEGACY_5 is only for user-affirmed five-asset jobs; not six reference images.')
 review_state='NOT_REVIEWED'
 visual_checks={}
 if args.human_review:
  try:
   rv=json.loads(pathlib.Path(args.human_review).read_text(encoding='utf-8'))
   visual_checks=rv.get('checks',{})
   if rv.get('approved') is True and str(rv.get('reviewer','')).strip() and visual_checks and all(x is True for x in visual_checks.values()):
    review_state='APPROVED_BY_REVIEWER'
   else:review_state='INCOMPLETE_OR_NOT_APPROVED'
  except Exception as e:review_state='INVALID_REVIEW_FILE';warnings.append('Human review read error: '+str(e))
 status='FAIL_TECHNICAL' if errors else ('PASS_RELEASE_REVIEWED' if review_state=='APPROVED_BY_REVIEWER' else 'PASS_TECHNICAL_VISUAL_PENDING')
 out={
  'profile':args.profile,'status':status,'technical_pass':not bool(errors),
  'release_ready':not bool(errors) and review_state=='APPROVED_BY_REVIEWER',
  'main_assets_expected':len(spec['required_assets']),'main_assets_found':sum(1 for r in rows[:len(spec['required_assets'])] if 'MISSING' not in r['issues']),
  'human_visual_review':review_state,'limitations':'Machine QA cannot verify typography spelling, brand continuity, original creativity, true alpha appearance, claim of independently generated assets, actual YouTube safe-area text layout or unique handle.',
  'errors':errors,'warnings':warnings,'items':rows,
  'handle_status':'UNVERIFIED, CHECK IN STUDIO','trademark_status':'NOT_CHECKED'
 }
 if args.report:
  rf=pathlib.Path(args.report);rf.parent.mkdir(parents=True,exist_ok=True)
  rf.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 if args.manifest_out:
  mf=pathlib.Path(args.manifest_out);mf.parent.mkdir(parents=True,exist_ok=True)
  mf.write_text(json.dumps({'version':spec['version'],'profile':args.profile,'required_main_count':len(spec['required_assets']), 'assets':manifest,'technical_status':status,'human_visual_review':review_state},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 if args.safe_preview and spec['upload_assets']:
  img_path=root/spec['upload_assets'][0]['filename']
  if img_path.exists():
   with Image.open(img_path) as src:
    im=src.convert('RGB').copy()
    x1,y1,x2,y2=spec['safe_area_youtube_px']['bbox_center']
    shade=Image.new('RGB',im.size,'#111111')
    shade.paste(im.crop((x1,y1,x2,y2)),(x1,y1))
    # Blend only outside safe region; mark the safe boundary.
    outim=Image.blend(im,shade,0.40)
    dr=ImageDraw.Draw(outim)
    dr.rectangle((x1,y1,x2,y2),outline='#00F5A4',width=8)
    dr.text((x1+12,y1+12),'YOUTUBE SAFE AREA: VISUALLY INSPECT NAME AND LOGO',fill='white')
    sf=pathlib.Path(args.safe_preview);sf.parent.mkdir(parents=True,exist_ok=True)
    outim.save(sf,quality=88)
 print(json.dumps({'status':status,'main':out['main_assets_found'],'expected':out['main_assets_expected'],'errors':errors,'warnings':warnings},ensure_ascii=False))
 return 2 if errors else 0

if __name__=='__main__':sys.exit(main())
