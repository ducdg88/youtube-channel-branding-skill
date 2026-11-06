import json, subprocess, sys, tempfile, zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / 'scripts' / 'studio.py'
SPEC = ROOT / 'configs' / 'sample_custom_assets.json'


def run(*parts):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, parts)], capture_output=True, text=True)


def state(job):
    return json.loads((job / 'job.json').read_text(encoding='utf-8'))


def make_previews(job, count=10, seed=0):
    for i in range(1, count + 1):
        Image.new('RGB', (800, 500), (10 * i + seed, 100, 30)).save(job / 'previews' / f'{i:02d}.png')


def make_finals(job):
    for entry in json.loads(SPEC.read_text(encoding='utf-8'))['assets']:
        if entry['transparent']:
            im = Image.new('RGBA', (entry['width'], entry['height']), (0, 0, 0, 0))
            w, h = im.size
            ImageDraw.Draw(im).rectangle((w // 4, h // 3, w * 3 // 4, h * 2 // 3), fill=(80, 100, 110, 255))
        else:
            im = Image.new('RGB', (entry['width'], entry['height']), (60, 120, 80))
        im.save(job / 'final' / entry['filename'])


def complete_job(job, ids='02'):
    assert run('init', '--dir', job, '--niche', 'generic science', '--name', 'EXAMPLE BRAND', '--count', '10').returncode == 0
    make_previews(job)
    assert run('check-previews', '--dir', job).returncode == 0
    assert run('select', '--dir', job, '--ids', ids).returncode == 0
    assert run('lock-spec', '--dir', job, '--spec', SPEC).returncode == 0
    make_finals(job)
    assert run('check-final', '--dir', job).returncode == 0
    assert run('approve-final', '--dir', job, '--confirmed').returncode == 0
    assert state(job)['state'] == 'COMPLETE'


def test_gates():
    with tempfile.TemporaryDirectory() as tmp:
        job = Path(tmp) / 'job'
        a = run('init', '--dir', job, '--niche', 'generic science', '--name', 'EXAMPLE BRAND', '--count', '10')
        assert a.returncode == 0, a.stderr
        assert state(job)['preview_count'] == 10
        # Cannot force six or start production before approval
        assert run('select', '--dir', job, '--ids', '01').returncode != 0
        assert run('lock-spec', '--dir', job, '--spec', SPEC).returncode != 0
        assert run('check-previews', '--dir', job).returncode != 0
        make_previews(job)
        assert run('check-previews', '--dir', job).returncode == 0
        assert run('select', '--dir', job, '--ids', '02,09').returncode == 0
        assert run('lock-spec', '--dir', job, '--spec', SPEC).returncode == 0
        locked = json.loads((job / 'output_spec.lock.json').read_text(encoding='utf-8'))
        assert locked['profile'] == 'CUSTOM' and len(locked['assets']) == 3
        assert run('check-final', '--dir', job).returncode != 0
        make_finals(job)
        assert run('check-final', '--dir', job).returncode == 0
        assert json.loads((job / 'reports' / 'final_qa.json').read_text(encoding='utf-8'))['complete'] is False
        assert state(job)['state'] == 'REVIEW_REQUIRED'
        assert run('bundle', '--dir', job).returncode != 0
        assert run('approve-final', '--dir', job, '--confirmed').returncode == 0
        assert run('bundle', '--dir', job).returncode == 0
        with zipfile.ZipFile(job / 'deliverables.zip') as z:
            names = set(z.namelist())
            manifest = json.loads(z.read('manifest.json'))
        assert {'assets/avatar.png', 'assets/channel_banner.png', 'assets/brand_wordmark.png',
                'brand.lock.json', 'output_spec.lock.json', 'reports/final_qa.json', 'manifest.json'} <= names
        assert len(manifest['assets']) == 3 and all(len(x['sha256']) == 64 for x in manifest['assets'])


def test_invalid_count():
    with tempfile.TemporaryDirectory() as tmp:
        assert run('init', '--dir', Path(tmp) / 'j', '--niche', 'n', '--count', '21', '--name', 'TEST').returncode != 0


def test_name_gate():
    """KD-2: without an approved name, previews and selection are blocked until set-name."""
    with tempfile.TemporaryDirectory() as tmp:
        job = Path(tmp) / 'job'
        assert run('init', '--dir', job, '--niche', 'x', '--count', '10').returncode == 0
        assert state(job)['state'] == 'AWAITING_NAME_SELECTION'
        make_previews(job)
        assert run('check-previews', '--dir', job).returncode != 0
        assert run('select', '--dir', job, '--ids', '01').returncode != 0
        assert state(job)['state'] == 'AWAITING_NAME_SELECTION'
        assert not (job / 'brand.lock.json').exists()
        assert run('set-name', '--dir', job, '--name', '   ').returncode != 0
        assert run('set-name', '--dir', job, '--name', 'Kênh Thử').returncode == 0
        assert state(job)['state'] == 'PREVIEWS_PENDING'
        assert run('check-previews', '--dir', job).returncode == 0
        assert run('set-name', '--dir', job, '--name', 'Other').returncode != 0
        assert run('select', '--dir', job, '--ids', '01').returncode == 0
        lock = json.loads((job / 'brand.lock.json').read_text(encoding='utf-8'))
        assert lock['channel_name'] == 'Kênh Thử'


def test_reselect_after_complete_needs_new_approval():
    """KD-1: a new selection, spec or preview check after COMPLETE clears the approval."""
    with tempfile.TemporaryDirectory() as tmp:
        job = Path(tmp) / 'job'
        complete_job(job)
        assert run('select', '--dir', job, '--ids', '07').returncode == 0
        s = state(job)
        assert s['state'] == 'AWAITING_OUTPUT_SPEC' and s['user_approved_final'] is False
        assert run('lock-spec', '--dir', job, '--spec', SPEC).returncode == 0
        assert run('check-final', '--dir', job).returncode == 0
        assert state(job)['state'] == 'REVIEW_REQUIRED'
        assert run('bundle', '--dir', job).returncode != 0
        assert not (job / 'deliverables.zip').exists()
        # re-running check-previews after approval also reopens the choice
        assert run('approve-final', '--dir', job, '--confirmed').returncode == 0
        assert run('check-previews', '--dir', job).returncode == 0
        s = state(job)
        assert s['state'] == 'AWAITING_USER_SELECTION' and s['user_approved_final'] is False and s['selected_ids'] == []
        assert run('bundle', '--dir', job).returncode != 0


def test_bundle_rejects_files_changed_after_qa():
    """KD-3: bundle re-checks size and sha256 of every file against final_qa.json."""
    with tempfile.TemporaryDirectory() as tmp:
        job = Path(tmp) / 'job'
        complete_job(job)
        Image.new('RGB', (10, 10)).save(job / 'final' / 'avatar.png')
        r = run('bundle', '--dir', job)
        assert r.returncode != 0 and 'changed after QA' in r.stderr
        assert not (job / 'deliverables.zip').exists()
        assert state(job)['state'] != 'COMPLETE'
        # approve-final cannot be reused on swapped files either
        assert run('approve-final', '--dir', job, '--confirmed').returncode != 0


def test_lock_spec_rejects_bad_json_cleanly():
    """KD-7: malformed specs give one ERROR line, never a traceback."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        job = tmp / 'job'
        assert run('init', '--dir', job, '--niche', 'x', '--name', 'N', '--count', '2').returncode == 0
        make_previews(job, count=2)
        assert run('check-previews', '--dir', job).returncode == 0
        assert run('select', '--dir', job, '--ids', '01').returncode == 0
        bad = {'list.json': '[1,2]', 'broken.json': '{"assets": [', 'noassets.json': '{"profile": "CUSTOM"}',
               'item.json': '{"assets": [1]}',
               'size.json': '{"assets": [{"filename": "a.png", "width": "10", "height": 10}]}',
               'path.json': '{"assets": [{"filename": "../a.png", "width": 10, "height": 10}]}'}
        for name, text in bad.items():
            (tmp / name).write_text(text, encoding='utf-8')
            r = run('lock-spec', '--dir', job, '--spec', tmp / name)
            assert r.returncode == 2, (name, r.stderr)
            assert 'Traceback' not in r.stderr and r.stderr.startswith('ERROR:'), (name, r.stderr)
        r = run('lock-spec', '--dir', job, '--spec', tmp / 'missing.json')
        assert r.returncode == 2 and 'Traceback' not in r.stderr
        assert state(job)['state'] == 'AWAITING_OUTPUT_SPEC'


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for t in tests:
        t()
    print(f'PASS {len(tests)}/{len(tests)} tests: stage gates, name gate, re-approval, sha256 bundle check, clean spec errors')
