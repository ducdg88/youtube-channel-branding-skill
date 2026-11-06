#!/usr/bin/env python3
"""Channel Brand Studio workflow state and QA. No image model is called here.

Python 3.9+. Pillow is needed for image QA; init, set-name, status, select and lock-spec use the stdlib.

States written to job.json:
  AWAITING_NAME_SELECTION -> PREVIEWS_PENDING -> (PREVIEWS_INCOMPLETE) -> AWAITING_USER_SELECTION
  -> AWAITING_OUTPUT_SPEC -> PRODUCTION -> (PRODUCTION_INCOMPLETE) -> REVIEW_REQUIRED -> COMPLETE
Any upstream change (check-previews, select, lock-spec, check-final) clears the human approval,
so a job only reaches COMPLETE through approve-final on the exact files that passed QA.
"""
import argparse, hashlib, json, os, re, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

VERSION = '3.0.1'
NAME_STATES = {'AWAITING_NAME_SELECTION', 'PREVIEWS_PENDING'}
SELECT_STATES = {'AWAITING_USER_SELECTION', 'AWAITING_OUTPUT_SPEC', 'PRODUCTION',
                 'PRODUCTION_INCOMPLETE', 'REVIEW_REQUIRED', 'COMPLETE'}
SPEC_STATES = SELECT_STATES - {'AWAITING_USER_SELECTION'}
FINAL_STATES = {'PRODUCTION', 'PRODUCTION_INCOMPLETE', 'REVIEW_REQUIRED', 'COMPLETE'}
FORMATS = ('PNG', 'JPEG', 'WEBP')


def err(msg):
    print('ERROR:', msg, file=sys.stderr)
    return 2


def dump(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def check_image(path, size=None, fmt=None, transparent=False):
    from PIL import Image
    with Image.open(path) as im:
        im.load()
        if size and im.size != size:
            return f'size {im.size} != {size}'
        if fmt and (im.format or '').upper() != fmt.upper():
            return f'format {im.format} != {fmt}'
        if transparent:
            if im.mode != 'RGBA' or 'A' not in im.getbands():
                return 'missing RGBA alpha channel'
            a = im.getchannel('A')
            lo, hi = a.getextrema()
            if lo > 15 or hi < 245:
                return f'alpha not both transparent and opaque {(lo, hi)}'
            hist = a.histogram()
            pixels = im.width * im.height
            clear = sum(hist[:16]) / pixels
            opaque = sum(hist[245:]) / pixels
            if clear < .03 or opaque < .005:
                return f'fake/unusable transparency ({clear:.3%} clear, {opaque:.3%} opaque)'
            corners = [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]
            if sum(a.getpixel(p) < 40 for p in corners) < 3:
                return 'nontransparent corners for a transparent logo'
    return None


def validate_spec(spec):
    """Return (assets, None) when the output spec is usable, else (None, message)."""
    if not isinstance(spec, dict):
        return None, 'spec must be a JSON object with an "assets" list'
    assets = spec.get('assets')
    if not isinstance(assets, list) or not assets:
        return None, 'assets[] is required and must be a non-empty list (there is no default six)'
    names = []
    for i, x in enumerate(assets, 1):
        if not isinstance(x, dict):
            return None, f'assets[{i}] must be an object'
        fn = x.get('filename')
        if not isinstance(fn, str) or '..' in fn or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', fn):
            return None, f'unsafe or missing filename in assets[{i}]: {fn!r}'
        if fn in names:
            return None, 'duplicate asset filename: ' + fn
        names.append(fn)
        w, h = x.get('width'), x.get('height')
        if type(w) is not int or type(h) is not int or not (1 <= w <= 16384 and 1 <= h <= 16384):
            return None, 'invalid px size: ' + fn
        fmt = x.get('format', 'PNG')
        if not isinstance(fmt, str) or fmt.upper() not in FORMATS:
            return None, 'unsupported format (use PNG, JPEG or WEBP): ' + fn
        tr = x.get('transparent', False)
        if not isinstance(tr, bool):
            return None, 'transparent must be true or false: ' + fn
        if tr and fmt.upper() != 'PNG':
            return None, 'transparent exports require PNG: ' + fn
    return assets, None


def clear_approval(job, j):
    """Upstream change: the earlier human approval and final QA no longer apply."""
    job['user_approved_final'] = False
    qa = j / 'reports' / 'final_qa.json'
    if qa.exists():
        data = read(qa)
        data.update(user_visual_approved=False, complete=False, superseded=True)
        dump(qa, data)


def verify_against_qa(j, job):
    """Return None when every final file is byte-identical to what final QA recorded."""
    qa_path = j / 'reports' / 'final_qa.json'
    if not job.get('output_spec') or not qa_path.exists():
        return 'final QA report missing; run check-final'
    qa = read(qa_path)
    if not qa.get('technical_pass') or qa.get('superseded'):
        return 'final QA has not passed for the current spec; run check-final'
    spec_path = j / job['output_spec']
    if not spec_path.is_file() or sha256(spec_path) != qa.get('spec_sha256'):
        return 'output spec changed after QA; run check-final again'
    checks = {c['filename']: c for c in qa.get('file_checks', [])}
    for x in read(spec_path)['assets']:
        fn = x['filename']
        c, p = checks.get(fn), j / 'final' / fn
        if c is None:
            return f'{fn}: not covered by final QA; run check-final again'
        if not p.is_file():
            return f'{fn}: missing'
        if p.stat().st_size != c['bytes'] or sha256(p) != c['sha256']:
            return f'{fn}: changed after QA (size or sha256 differs); run check-final and approve-final again'
    return None


def main():
    # Channel names keep their exact Unicode spelling; never crash on a legacy console code page.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(description='Approval-first 10 concept studio CLI')
    sub = p.add_subparsers(dest='cmd', required=True)
    for name in ['init', 'set-name', 'status', 'check-previews', 'select', 'lock-spec',
                 'check-final', 'approve-final', 'bundle']:
        s = sub.add_parser(name)
        s.add_argument('--dir', type=Path, required=True)
        if name == 'init':
            s.add_argument('--niche', required=True)
            s.add_argument('--name', default='')
            s.add_argument('--count', type=int, default=10)
            s.add_argument('--locale', default='en')
        if name == 'set-name':
            s.add_argument('--name', required=True, help='Channel name the user approved, exact spelling')
        if name == 'select':
            s.add_argument('--ids', required=True, help='e.g. 03 or 03,07')
            s.add_argument('--notes', default='', help='Human-approved visual direction details')
        if name == 'lock-spec':
            s.add_argument('--spec', type=Path, required=True)
        if name == 'approve-final':
            s.add_argument('--confirmed', action='store_true', help='Explicit human review approved')
    a = p.parse_args()
    j = a.dir
    f = j / 'job.json'

    if a.cmd == 'init':
        if not 1 <= a.count <= 20:
            return err('count must be 1-20')
        if f.exists():
            return err('job already exists; choose new directory')
        for d in ['previews', 'final', 'reports']:
            (j / d).mkdir(parents=True, exist_ok=True)
        name = a.name.strip()
        job = {'version': VERSION, 'niche': a.niche, 'channel_name': name, 'locale': a.locale,
               'preview_count': a.count, 'state': 'PREVIEWS_PENDING' if name else 'AWAITING_NAME_SELECTION',
               'previews_passed': False, 'selected_ids': [], 'output_spec': None, 'user_approved_final': False,
               'created_at': timestamp(), 'preview_files': [], 'audit': []}
        dump(f, job)
        dump(j / 'concept_prompts.json', [{'id': f'{i:02d}', 'brief': (
            f'Distinct visual identity direction #{i:02d} for niche: {a.niche}; exact user name: '
            f'{name or "[TO BE APPROVED]"}; include recognizable logo symbol + name treatment + palette + '
            f'typography; different from the other {a.count - 1} concepts; NO final asset export yet.')}
            for i in range(1, a.count + 1)])
        print('CREATED', f, 'state=', job['state'], 'preview_count=', a.count)
        return 0

    if not f.exists():
        return err('job.json not found; run init')
    job = read(f)

    def audit(action):
        job['audit'].append({'at': timestamp(), 'action': action})

    def no_name():
        return not str(job.get('channel_name', '')).strip()

    if a.cmd == 'status':
        print(json.dumps({k: job.get(k) for k in ['state', 'channel_name', 'preview_count', 'selected_ids',
                                                 'output_spec', 'user_approved_final']}, ensure_ascii=False, indent=2))
        return 0

    if a.cmd == 'set-name':
        name = a.name.strip()
        if not name:
            return err('name must not be empty')
        if job['state'] not in NAME_STATES:
            return err('the name is fixed once previews are checked; start a new job to rename')
        job['channel_name'] = name
        job['state'] = 'PREVIEWS_PENDING'
        audit('USER_APPROVED_NAME:' + name)
        dump(f, job)
        print('NAME SET', name, 'state= PREVIEWS_PENDING')
        return 0

    if a.cmd == 'check-previews':
        if no_name():
            return err('channel name not approved yet: run set-name --name "..." first')
        errors, seen, good = [], set(), []
        for i in range(1, job['preview_count'] + 1):
            pid = f'{i:02d}'
            found = [c for c in (j / 'previews' / f'{pid}.{ext}' for ext in ('png', 'jpg', 'jpeg', 'webp')) if c.exists()]
            if len(found) != 1:
                errors.append(f'{pid}: expected exactly one real image file, found {len(found)}')
                continue
            path = found[0]
            try:
                fail = check_image(path)
                if fail:
                    errors.append(f'{pid}: {fail}')
                    continue
                from PIL import Image
                with Image.open(path) as im:
                    if im.width < 512 or im.height < 256:
                        errors.append(f'{pid}: low resolution {im.size}')
                        continue
                    h = hashlib.sha256(im.convert('RGB').resize((32, 32)).tobytes()).hexdigest()
                if h in seen:
                    errors.append(f'{pid}: duplicate image content')
                    continue
                seen.add(h)
                good.append(path.name)
            except Exception as e:
                errors.append(f'{pid}: invalid image: {e}')
        report = {'technical_pass': not errors, 'preview_count_expected': job['preview_count'],
                  'preview_count_valid': len(good), 'files': good, 'errors': errors,
                  'visual_review_required': True, 'user_selected': False}
        dump(j / 'reports' / 'preview_qa.json', report)
        # New previews reopen the choice: earlier selection, spec and approval no longer apply.
        if job.get('selected_ids') or job.get('output_spec'):
            lock = j / 'brand.lock.json'
            if lock.exists():
                data = read(lock)
                data['lock_status'] = 'SUPERSEDED'
                dump(lock, data)
        job.update(preview_files=good, previews_passed=not errors, selected_ids=[], output_spec=None)
        clear_approval(job, j)
        job['state'] = 'AWAITING_USER_SELECTION' if not errors else 'PREVIEWS_INCOMPLETE'
        audit('preview QA')
        dump(f, job)
        print(json.dumps(report, indent=2))
        return 0 if not errors else 1

    if a.cmd == 'select':
        if no_name():
            return err('channel name not approved yet: run set-name --name "..." first')
        passed = job.get('previews_passed', job['state'] in SELECT_STATES)
        if job['state'] not in SELECT_STATES or not passed:
            return err('cannot select: previews have not passed check-previews')
        ids = [x.strip().zfill(2) for x in a.ids.split(',') if x.strip()]
        valid = {f'{i:02d}' for i in range(1, job['preview_count'] + 1)}
        if not ids or len(set(ids)) != len(ids) or any(x not in valid for x in ids):
            return err('invalid selection IDs')
        job.update(selected_ids=ids, output_spec=None, state='AWAITING_OUTPUT_SPEC')
        clear_approval(job, j)
        audit('USER_APPROVED_CONCEPTS:' + ','.join(ids))
        dump(j / 'brand.lock.json', {'channel_name': job['channel_name'], 'locale': job['locale'],
                                     'niche': job['niche'], 'selected_concept_ids': ids,
                                     'approved_visual_direction_notes': a.notes,
                                     'needs_final_design_review': True, 'lock_status': 'LOCKED'})
        dump(f, job)
        print('SELECTED', ids, 'now choose exact output asset types/dimensions')
        return 0

    if a.cmd == 'lock-spec':
        if job['state'] not in SPEC_STATES or not job.get('selected_ids'):
            return err('must select concept(s) first')
        try:
            spec = read(a.spec)
        except (OSError, UnicodeDecodeError, ValueError) as e:
            return err(f'cannot read spec {a.spec}: {e.__class__.__name__}: {e}')
        assets, problem = validate_spec(spec)
        if problem:
            return err(problem)
        dump(j / 'output_spec.lock.json', spec)
        job.update(output_spec='output_spec.lock.json', state='PRODUCTION')
        clear_approval(job, j)
        audit('USER_APPROVED_OUTPUT_SPEC')
        dump(f, job)
        print('LOCKED', len(assets), 'custom asset type(s), not forced to six')
        return 0

    if a.cmd == 'check-final':
        if job['state'] not in FINAL_STATES or not job.get('output_spec'):
            return err('cannot inspect final assets before concept selection and spec lock')
        spec_path = j / job['output_spec']
        spec = read(spec_path)
        errors, results, checks = [], [], []
        for x in spec['assets']:
            path = j / 'final' / x['filename']
            if not path.is_file():
                errors.append(f'{path.name}: missing')
                continue
            try:
                fault = check_image(path, (x['width'], x['height']), x.get('format', 'PNG'), x.get('transparent', False))
            except Exception as e:
                fault = f'invalid image: {e}'
            if fault:
                errors.append(f'{path.name}: {fault}')
                continue
            results.append(path.name)
            checks.append({'filename': path.name, 'bytes': path.stat().st_size, 'sha256': sha256(path),
                           'width': x['width'], 'height': x['height']})
        # Fresh QA always needs a fresh human approval; check-final never marks a job COMPLETE.
        job['user_approved_final'] = False
        qa = {'technical_pass': not errors, 'valid': len(results), 'expected': len(spec['assets']),
              'files': results, 'file_checks': checks, 'spec_sha256': sha256(spec_path), 'errors': errors,
              'visual_review_required': True, 'user_visual_approved': False, 'complete': False}
        dump(j / 'reports' / 'final_qa.json', qa)
        job['state'] = 'REVIEW_REQUIRED' if not errors else 'PRODUCTION_INCOMPLETE'
        audit('final QA')
        dump(f, job)
        print(json.dumps(qa, indent=2))
        return 0 if not errors else 1

    if a.cmd == 'approve-final':
        if not a.confirmed:
            return err('explicit --confirmed required')
        if job['state'] != 'REVIEW_REQUIRED':
            return err('final QA must pass (state REVIEW_REQUIRED) before human approval; run check-final')
        problem = verify_against_qa(j, job)
        if problem:
            return err(problem)
        job.update(user_approved_final=True, state='COMPLETE')
        audit('USER_APPROVED_FINAL_ARTWORK')
        dump(f, job)
        qa_path = j / 'reports' / 'final_qa.json'
        qa = read(qa_path)
        qa.update(user_visual_approved=True, complete=True)
        dump(qa_path, qa)
        print('COMPLETE: human approval recorded')
        return 0

    if a.cmd == 'bundle':
        if job['state'] != 'COMPLETE' or not job.get('user_approved_final'):
            return err('cannot bundle before technical QA and visual approval')
        problem = verify_against_qa(j, job)
        if problem:
            job['state'] = 'PRODUCTION'
            clear_approval(job, j)
            audit('BUNDLE_REFUSED: ' + problem)
            dump(f, job)
            return err(problem)
        qa = read(j / 'reports' / 'final_qa.json')
        manifest = {'version': VERSION, 'channel_name': job['channel_name'],
                    'selected_concept_ids': job['selected_ids'], 'generated_at': timestamp(),
                    'assets': [{**c, 'path': 'assets/' + c['filename']} for c in qa['file_checks']]}
        out, tmp = j / 'deliverables.zip', j / 'deliverables.zip.part'
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
            for c in qa['file_checks']:
                z.write(j / 'final' / c['filename'], arcname='assets/' + c['filename'])
            for relative in ['brand.lock.json', 'output_spec.lock.json', 'reports/final_qa.json']:
                z.write(j / relative, arcname=relative)
            z.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        os.replace(tmp, out)
        print('DELIVERED', out)
        return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
