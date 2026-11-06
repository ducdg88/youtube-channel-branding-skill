#!/usr/bin/env python3
"""Channel Brand Studio workflow/state+QA. No image model is called here.
Python 3.9+, Pillow needed for image QA; init/status/select/lock-spec use stdlib.
"""
import argparse, json, hashlib, re, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

def err(msg):
    print('ERROR:',msg,file=sys.stderr); return 2

def dump(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def timestamp():return datetime.now(timezone.utc).isoformat()

def check_image(path, size=None, fmt=None, transparent=False):
    from PIL import Image,ImageStat
    with Image.open(path) as im:
        im.load(); actual_format=im.format; actual_size=im.size
        if size and actual_size!=size:return f'size {actual_size} != {size}'
        if fmt and actual_format.upper()!=fmt.upper():return f'format {actual_format} != {fmt}'
        if transparent:
            if im.mode!='RGBA' or 'A' not in im.getbands():return 'missing RGBA alpha channel'
            a=im.getchannel('A'); from PIL import ImageChops
            extrema=a.getextrema()
            if extrema[0]>15 or extrema[1]<245:return f'alpha not both transparent and opaque {extrema}'
            import math
            hist=a.histogram(); pixels=im.width*im.height
            zero=sum(hist[:16])/pixels; opaque=sum(hist[245:])/pixels
            if zero<.03 or opaque<.005:return f'fake/unusable transparency ({zero:.3%} clear, {opaque:.3%} opaque)'
            # Transparent border is a useful signal for logo exports.
            points=[(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]
            if sum(a.getpixel(p)<40 for p in points)<3:return 'nontransparent corners for a transparent logo'
    return None

def main():
    p=argparse.ArgumentParser(description='Approval-first 10 concept studio CLI')
    sub=p.add_subparsers(dest='cmd',required=True)
    for name in ['init','status','check-previews','select','lock-spec','check-final','approve-final','bundle']:
        s=sub.add_parser(name);s.add_argument('--dir',type=Path,required=True)
        if name=='init':
            s.add_argument('--niche',required=True);s.add_argument('--name',default='');s.add_argument('--count',type=int,default=10)
            s.add_argument('--locale',default='en')
        if name=='select':s.add_argument('--ids',required=True,help='e.g. 03 or 03,07')
        if name=='lock-spec':s.add_argument('--spec',type=Path,required=True)
        if name=='select':s.add_argument('--notes',default='',help='Human-approved visual direction details')
        if name=='approve-final':s.add_argument('--confirmed',action='store_true',help='Explicit human review approved')
    a=p.parse_args();j=a.dir;f=j/'job.json'
    if a.cmd=='init':
        if not 1<=a.count<=20:return err('count must be 1-20')
        if f.exists():return err('job already exists; choose new directory')
        for d in ['previews','final','reports']: (j/d).mkdir(parents=True,exist_ok=True)
        job={'version':'3.0.0','niche':a.niche,'channel_name':a.name,'locale':a.locale,
            'preview_count':a.count,'state':'PREVIEWS_PENDING' if a.name else 'AWAITING_NAME_SELECTION',
            'selected_ids':[],'output_spec':None,'user_approved_final':False,
            'created_at':timestamp(),'preview_files':[], 'audit':[]}
        dump(f,job)
        concept_ideas=[{'id':f'{i:02d}','brief':f'Distinct visual identity direction #{i:02d} for niche: {a.niche}; exact user name: {a.name or "[TO BE APPROVED]"}; include recognizable logo symbol + name treatment + palette + typography; different from the other {a.count-1} concepts; NO final asset export yet.'} for i in range(1,a.count+1)]
        dump(j/'concept_prompts.json',concept_ideas)
        print('CREATED',f,'state=',job['state'],'preview_count=',a.count);return 0
    if not f.exists():return err('job.json not found; run init')
    job=read(f)
    def audit(action):job['audit'].append({'at':timestamp(),'action':action})
    if a.cmd=='status':
        print(json.dumps({k:job[k] for k in ['state','preview_count','selected_ids','output_spec','user_approved_final']},indent=2));return 0
    if a.cmd=='check-previews':
        errors=[];seen=set();good=[]
        for i in range(1,job['preview_count']+1):
            id=f'{i:02d}'
            candidates=[j/'previews'/f'{id}.{ext}' for ext in ('png','jpg','jpeg','webp')]
            found=[c for c in candidates if c.exists()]
            if len(found)!=1:errors.append(f'{id}: expected exactly one real image file, found {len(found)}');continue
            path=found[0]
            try:
                fail=check_image(path)
                if fail:errors.append(f'{id}: {fail}');continue
                from PIL import Image
                with Image.open(path) as im:
                    if im.width<512 or im.height<256:errors.append(f'{id}: low resolution {im.size}');continue
                    h=hashlib.sha256(im.convert('RGB').resize((32,32)).tobytes()).hexdigest()
                    if h in seen:errors.append(f'{id}: duplicate image content');continue
                    seen.add(h)
                good.append(path.name)
            except Exception as e:errors.append(f'{id}: invalid image: {e}')
        report={'technical_pass':not errors,'preview_count_expected':job['preview_count'],'preview_count_valid':len(good),
                'files':good,'errors':errors,'visual_review_required':True,'user_selected':False}
        dump(j/'reports'/'preview_qa.json',report)
        job['preview_files']=good
        job['state']='AWAITING_USER_SELECTION' if not errors else 'PREVIEWS_INCOMPLETE'
        audit('preview QA');dump(f,job)
        print(json.dumps(report,indent=2));return 0 if not errors else 1
    if a.cmd=='select':
        if job['state']!='AWAITING_USER_SELECTION':return err('cannot select: previews not passed and displayed')
        ids=[x.strip().zfill(2) for x in a.ids.split(',') if x.strip()]
        valid={f'{i:02d}' for i in range(1,job['preview_count']+1)}
        if not ids or len(set(ids))!=len(ids) or any(x not in valid for x in ids):return err('invalid selection IDs')
        job['selected_ids']=ids;job['state']='AWAITING_OUTPUT_SPEC';audit('USER_APPROVED_CONCEPTS:'+','.join(ids));dump(j/'brand.lock.json',{'channel_name':job['channel_name'],'locale':job['locale'],'niche':job['niche'],'selected_concept_ids':ids,'approved_visual_direction_notes':a.notes,'needs_final_design_review':True});dump(f,job)
        print('SELECTED',ids,'now choose exact output asset types/dimensions');return 0
    if a.cmd=='lock-spec':
        if job['state']!='AWAITING_OUTPUT_SPEC':return err('must select concept(s) first')
        try:spec=read(a.spec)
        except Exception as e:return err(str(e))
        assets=spec.get('assets',[])
        if not assets:return err('assets[] is required, no default 6')
        names=[]
        for x in assets:
            fn=x.get('filename','')
            if not fn or '/' in fn or '\\' in fn or '..' in fn or not re.fullmatch(r'[A-Za-z0-9_.-]+',fn):return err('unsafe filename: '+fn)
            if fn in names:return err('duplicate asset filename: '+fn)
            names.append(fn)
            if not isinstance(x.get('width'),int) or not isinstance(x.get('height'),int) or not 1<=x['width']<=16384 or not 1<=x['height']<=16384:return err('invalid px size: '+fn)
            if x.get('format','PNG').upper() not in ('PNG','JPEG','WEBP'):return err('unsupported format: '+fn)
            if x.get('transparent') and x.get('format','PNG').upper()!='PNG':return err('transparent exports require PNG: '+fn)
        dump(j/'output_spec.lock.json',spec)
        job['output_spec']='output_spec.lock.json';job['state']='PRODUCTION';audit('USER_APPROVED_OUTPUT_SPEC');dump(f,job)
        print('LOCKED',len(assets),'custom asset type(s), not forced to six');return 0
    if a.cmd=='check-final':
        if job['state'] not in ('PRODUCTION','REVIEW_REQUIRED','PRODUCTION_INCOMPLETE'):return err('cannot inspect final assets before concept selection and spec lock')
        spec=read(j/job['output_spec']); errors=[]; results=[]
        for x in spec['assets']:
            path=j/'final'/x['filename']
            if not path.is_file():errors.append(f'{path.name}: missing');continue
            try:
                fault=check_image(path, (x['width'],x['height']), x.get('format','PNG'),x.get('transparent',False))
                if fault:errors.append(f'{path.name}: {fault}')
                else:results.append(path.name)
            except Exception as e:errors.append(f'{path.name}: invalid image: {e}')
        qa={'technical_pass':not errors,'valid':len(results),'expected':len(spec['assets']),'files':results,
            'errors':errors,'visual_review_required':True,'user_visual_approved':job['user_approved_final'],
            'complete':not errors and job['user_approved_final']}
        dump(j/'reports'/'final_qa.json',qa)
        job['state']='COMPLETE' if not errors and job['user_approved_final'] else ('REVIEW_REQUIRED' if not errors else 'PRODUCTION_INCOMPLETE')
        audit('final QA');dump(f,job)
        print(json.dumps(qa,indent=2))
        return 0 if not errors else 1
    if a.cmd=='approve-final':
        if not a.confirmed:return err('explicit --confirmed required')
        qa_path=j/'reports'/'final_qa.json'
        if not qa_path.exists() or not read(qa_path).get('technical_pass'):return err('final QA must pass before human approval')
        job['user_approved_final']=True;job['state']='COMPLETE';audit('USER_APPROVED_FINAL_ARTWORK');dump(f,job)
        qa=read(qa_path);qa['user_visual_approved']=True;qa['complete']=True;dump(qa_path,qa)
        print('COMPLETE: human approval recorded');return 0
    if a.cmd=='bundle':
        if job['state']!='COMPLETE':return err('cannot bundle before technical QA and visual approval')
        spec=read(j/job['output_spec']);out=j/'deliverables.zip'
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
            for x in spec['assets']:
                source=j/'final'/x['filename']
                if not source.exists():return err('missing file before packaging: '+x['filename'])
                z.write(source,arcname='assets/'+x['filename'])
            for relative in ['brand.lock.json','output_spec.lock.json','reports/final_qa.json']:
                z.write(j/relative,arcname=relative)
        print('DELIVERED',out);return 0
    return 0
if __name__=='__main__':sys.exit(main())
