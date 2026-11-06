import tempfile,subprocess,sys,json
from pathlib import Path
from PIL import Image
SCRIPT=Path(__file__).resolve().parent.parent/'scripts'/'studio.py'
SPEC=Path(__file__).resolve().parent.parent/'configs'/'sample_custom_assets.json'

def run(*parts):return subprocess.run([sys.executable,str(SCRIPT),*map(str,parts)],capture_output=True,text=True)

def test_gates():
    with tempfile.TemporaryDirectory() as tmp:
        job=Path(tmp)/'job'
        a=run('init','--dir',job,'--niche','generic science','--name','EXAMPLE BRAND','--count','10')
        assert a.returncode==0,a.stderr
        assert json.loads((job/'job.json').read_text())['preview_count']==10
        # Cannot force six or make production before approval
        assert run('select','--dir',job,'--ids','01').returncode!=0
        assert run('lock-spec','--dir',job,'--spec',SPEC).returncode!=0
        assert run('check-previews','--dir',job).returncode!=0
        for i in range(1,11):
            im=Image.new('RGB',(800,500),(10*i,100,30));im.save(job/'previews'/f'{i:02d}.png')
        assert run('check-previews','--dir',job).returncode==0
        assert run('select','--dir',job,'--ids','02,09').returncode==0
        assert run('lock-spec','--dir',job,'--spec',SPEC).returncode==0
        assert json.loads((job/'output_spec.lock.json').read_text())['profile']=='CUSTOM'
        assert len(json.loads((job/'output_spec.lock.json').read_text())['assets'])==3
        assert run('check-final','--dir',job).returncode!=0
        specs=json.loads(SPEC.read_text())['assets']
        for entry in specs:
            if entry['transparent']:
                im=Image.new('RGBA',(entry['width'],entry['height']),(0,0,0,0))
                # Transparent edges + nontrivial core.
                from PIL import ImageDraw
                d=ImageDraw.Draw(im); w,h=im.size;d.rectangle((w//4,h//3,w*3//4,h*2//3),fill=(80,100,110,255))
            else:im=Image.new('RGB',(entry['width'],entry['height']),(60,120,80))
            im.save(job/'final'/entry['filename'])
        assert run('check-final','--dir',job).returncode==0
        assert json.loads((job/'reports'/'final_qa.json').read_text())['complete'] is False
        assert run('bundle','--dir',job).returncode!=0
        assert run('approve-final','--dir',job,'--confirmed').returncode==0
        assert run('bundle','--dir',job).returncode==0
        assert (job/'deliverables.zip').exists()

def test_invalid_count():
    with tempfile.TemporaryDirectory() as tmp:
        a=run('init','--dir',Path(tmp)/'j','--niche','n','--count','21','--name','TEST')
        assert a.returncode!=0

if __name__=='__main__':
    test_gates();test_invalid_count();print('PASS 2/2 tests: stage gates, 10 previews, custom 3 files, refusal to claim complete')
