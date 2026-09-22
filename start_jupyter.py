"""Paleidžia projekto Jupyter fone ir naršyklę atidaro tik serveriui atsakius."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser


ROOT = Path(__file__).resolve().parent
STATE = ROOT / '.jupyter-run'


# Ieško veikiančio šio projekto vietinio Jupyter serverio ir patikrina jo atsaką.
# Grąžina serverio informaciją arba None; žetono nespausdina.
def active_server():
    # Tik šio projekto serveris; žetonai lieka vietiniuose Jupyter failuose.
    from jupyter_core.paths import jupyter_runtime_dir
    for directory in [STATE / 'runtime', Path(jupyter_runtime_dir())]:
        try:
            files = list(directory.glob('jpserver-*.json'))
        except OSError:
            continue
        for path in files:
            try:
                info = json.loads(path.read_text(encoding='utf-8'))
                if Path(info.get('root_dir', '')).resolve() != ROOT:
                    continue
                base = info['url']
                if urllib.parse.urlsplit(base).hostname not in ('localhost', '127.0.0.1', '::1'):
                    continue
                request = urllib.request.Request(base.rstrip('/') + '/api/status')
                if info.get('token'):
                    request.add_header('Authorization', 'token ' + info['token'])
                with urllib.request.urlopen(request, timeout=1) as response:
                    if response.status == 200:
                        return info
            except (OSError, ValueError, KeyError, urllib.error.URLError):
                continue
    return None


# Panaudoja esamą serverį arba paleidžia naują; sulaukusi atsako gali atidaryti naršyklę.
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--status', action='store_true')
    args = parser.parse_args()
    server = active_server()
    if args.status:
        print('Jupyter serveris veikia.' if server else 'Jupyter serveris neveikia.')
        return 0 if server else 1
    if server is None:
        STATE.mkdir(exist_ok=True)
        (STATE / 'runtime').mkdir(exist_ok=True)
        env = os.environ.copy()
        env['JUPYTER_RUNTIME_DIR'] = str(STATE / 'runtime')
        flags = (subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == 'nt' else 0
        # Atsietas procesas nenutraukiamas uždarius START.cmd langą.
        with (STATE / 'server.log').open('ab') as log:
            process = subprocess.Popen(
                [sys.executable, '-m', 'jupyterlab', '--no-browser',
                 '--ServerApp.ip=127.0.0.1', '--ServerApp.port=8888',
                 '--ServerApp.port_retries=20', f'--ServerApp.root_dir={ROOT}'],
                cwd=ROOT, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                creationflags=flags, start_new_session=(os.name != 'nt'))
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            server = active_server()
            if server:
                break
            if process.poll() is not None:
                raise RuntimeError(f'Jupyter sustojo. Klaidos žurnalas: {STATE / "server.log"}')
            time.sleep(.5)
        if server is None:
            raise RuntimeError(f'Serveris neatsakė. Klaidos žurnalas: {STATE / "server.log"}')
    if not args.no_browser:
        url = server['url'].rstrip('/') + '/lab'
        if server.get('token'):
            url += '?' + urllib.parse.urlencode({'token': server['token']})
        webbrowser.open(url)
    print('Jupyter veikia fone. Si langa galite uzdaryti.')
    print('Serveri sustabdysite Jupyter meniu File > Shut Down.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
