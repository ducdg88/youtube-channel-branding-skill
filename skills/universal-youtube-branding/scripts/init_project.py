#!/usr/bin/env python3
"""Create a six-reference production scaffold. Does NOT claim to generate images.
Usage: python scripts/init_project.py --brief templates/brief.json --out output/my-channel
"""
import argparse, json, pathlib
HERE=pathlib.Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--brief',required=True)
 p.add_argument('--out',required=True)
 p.add_argument('--profile',choices=['reference6','legacy5'],default=None)
 a=p.parse_args()
 brief=json.loads(pathlib.Path(a.brief).read_text(encoding='utf-8'))
 profile=a.profile or ('legacy5' if str(brief.get('asset_profile','REFERENCE_6')).upper()=='LEGACY_5' else 'reference6')
 spec=json.loads((HERE/'templates'/('asset_spec_reference6.json' if profile=='reference6' else 'asset_spec.json')).read_text(encoding='utf-8'))
 output=pathlib.Path(a.out).expanduser().resolve()
 output.mkdir(parents=True,exist_ok=True)
 for item in spec['required_assets']+spec['upload_assets']:
  (output/item['filename']).parent.mkdir(parents=True,exist_ok=True)
 (output/'prompts').mkdir(exist_ok=True)
 (output/'reports').mkdir(exist_ok=True)
 brief['asset_profile']={'reference6':'REFERENCE_6','legacy5':'LEGACY_5'}.get(profile,profile.upper())
 brief['required_assets']=len(spec['required_assets'])
 (output/'brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 lock={
  'brand_name':brief.get('brand_name') or '',
  'niche':brief.get('niche',''),
  'market':brief.get('market','Global'),
  'style':brief.get('style','AUTO'),
  'asset_profile':{'reference6':'REFERENCE_6','legacy5':'LEGACY_5'}.get(profile,profile.upper()),
  'asset_spec_version':spec['version'],
  'lock_status':'NOT_LOCKED',
  'palette':{},'logo_motif':'', 'descriptor':'', 'tagline':'',
  'handle_status':'UNVERIFIED, CHECK IN YOUTUBE STUDIO',
  'notes':'Complete brand_name/niche/style/palette/logo_motif. Then set lock_status to LOCKED before generating prompts or images.'
 }
 (output/'brand.lock.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name in ['name_research.md','brand_guide.md','content_ideas.md','README_upload.md']:
  f=output/name
  if not f.exists():f.write_text('# '+name+'\nPENDING: do not claim completed.\n',encoding='utf-8')
 (output/'reports'/'VISUAL_REVIEW_CHECKLIST.json').write_text(json.dumps({
   'approved':False,'reviewer':'','checks':{
    'brand_name_spelling_exact':False,
    'six_unique_asset_compositions':False,
    'style_and_subject_fit_niche':False,
    'logo_identical_across_assets':False,
    'banner_text_inside_youtube_safe_area':False,
    'avatar_readable_at_98px':False,
    'logos_transparent_on_light_and_dark':False,
    'no_misleading_trademark_or_unwanted_text':False,
   },'comment':'Visual review must be performed by a human or visual-capable AI after rendering; no default approval.'
  },ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'project':str(output),'profile':profile,'required_main_files':len(spec['required_assets']),'status':'SCAFFOLD_ONLY_NO_IMAGES'},ensure_ascii=False))

if __name__=='__main__':main()
