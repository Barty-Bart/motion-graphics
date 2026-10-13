"""Writes report.html after a sound pass: a review page grouped into scenes.

Press play on any sound and the page plays that whole scene of the video with every sound in it,
the one you are trying swapped in, mixed live over the music with the same timing and levels as
sound_pass.py. Sounds that are used at several moments say where, so a swap can be applied to all
of them and the video keeps one consistent set of sounds. "Copy my picks" puts the swaps on the
clipboard; paste them back to Claude, which re-runs sound_pass.py with --swaps.

Everything the page needs (sounds and music bed) is embedded, so it works opened straight from
disk, in a preview pane, or published as a page. Only after.mp4 has to sit next to it.
"""
import os, re, json, base64, subprocess

def _label(e):
    if e.get('title') and e.get('creator'): return f"{e['title']} — {e['creator']}"
    if e.get('runtime_url'): return 'Mixkit #' + str(e.get('mixkit_id') or re.search(r'/(\d+)/', e['runtime_url']).group(1))
    b = os.path.basename(e.get('file', '')).rsplit('.', 1)[0]
    kenney = b.startswith('kenney-')
    b = re.sub(r'^fs-?\d+-?', '', b); b = re.sub(r'^kenney-', '', b)
    b = b.replace('-', ' ').replace('_', ' ').strip()
    who = 'Kenney' if kenney else (e.get('attribution') or '').split(' via ')[0].strip()
    name = b.capitalize() if b else 'Freesound ' + (re.search(r'\d+', e.get('file', '')) or [''])[0]
    return f'{name} — {who}' if who else name

def _data_uri(path):
    """mp3 data URI so every browser can decode it (Safari has gaps with Ogg Vorbis)."""
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '2', '-ar', '44100', '-b:a', '128k', '-f', 'mp3', '-'], capture_output=True)
    if r.returncode or not r.stdout: return None
    return 'data:audio/mpeg;base64,' + base64.b64encode(r.stdout).decode()

def _dur(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True)
    try: return round(float(r.stdout), 2)
    except ValueError: return None

def write(out, placed, dur, fps, lufs, peak, gain_db=0.0, limit=False, music=None):
    sounds, enc = {}, {}
    def add(e, local, kit=False):
        i = e['id']
        if i in sounds:
            sounds[i]['kit'] = sounds[i]['kit'] or kit; return
        play = None
        if local:
            if local not in enc: enc[local] = _data_uri(local)
            play = enc[local]
        sounds[i] = {'label': _label(e), 'cat': e.get('category'), 'kit': kit or bool(e.get('title') and e.get('creator')),
                     'license': e.get('license') or '', 'credit': e.get('credit') or e.get('attribution') or '',
                     'src': e.get('source_url') or e.get('source_page'), 'dur': e.get('duration_s') or (_dur(local) if local else None),
                     'play': play}
    cues = []
    for c in placed:
        for o in c['options']: add(o, o.get('local'))
        if c['sfx'] not in sounds:
            add({'id': c['sfx'], 'category': c['category'], 'source_url': c['source_url'], 'license': c['license'], 'credit': c['credit'],
                 'file': c['sfx'] if not str(c['sfx']).startswith('http') else None, 'runtime_url': c['sfx'] if str(c['sfx']).startswith('http') else None}, c['sfx_path'])
        elif not sounds[c['sfx']]['play'] and c.get('sfx_path'):
            sounds[c['sfx']]['play'] = _data_uri(c['sfx_path'])
        cues.append({'i': c['idx'], 't': c['t'], 'type': c['type'], 'desc': c.get('desc', ''), 'seg': c.get('segment', 'Scene'),
                     'dur': c.get('dur'), 'pre': c.get('pre', 0), 'gain_db': c['gain_db'], 'used': c['sfx'],
                     'options': [o['id'] for o in c['options']]})
    data = {'duration': dur, 'fps': fps, 'lufs': lufs, 'peak': peak, 'gain_db': gain_db, 'limit': limit or None,
            'video': 'after.mp4', 'music': _data_uri(music) if music and os.path.exists(music) else None,
            'cues': cues, 'sounds': sounds}
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report_template.html'), encoding='utf-8').read()
    html = tpl.replace('/*DATA*/null', json.dumps(data, separators=(',', ':')).replace('</', '<\\/'))
    open(os.path.join(out, 'report.html'), 'w', encoding='utf-8').write(html)
    return os.path.join(out, 'report.html')
