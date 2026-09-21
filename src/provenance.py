"""Kodo tapatybė, planuojamas biudžetas ir proceso atminties matavimas."""
import ctypes
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from sklearn.model_selection import ParameterGrid
from src.models import grid_for


def provenance(project):
    project = Path(project).resolve()
    files = sorted([*project.glob('*.py'), *project.glob('src/*.py'),
                    *project.glob('configs/*.yaml'), project / 'requirements.txt'])
    hashes = {str(p.relative_to(project)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    identity = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    # Aiškus git-dir veikia ir kai projekto savininkas skiriasi nuo vykdytojo.
    repository = next((p / '.git' for p in [project, *project.parents] if (p / '.git').is_dir()), None)
    command = ['git', f'--git-dir={repository}', 'rev-parse', '--verify', 'HEAD'] if repository else ['git', 'rev-parse', '--verify', 'HEAD']
    try:
        result = subprocess.run(command, cwd=project, capture_output=True, text=True)
        revision = result.stdout.strip() if result.returncode == 0 else None
        git_error = result.stderr.strip() if result.returncode else None
    except OSError as exc:
        revision, git_error = None, str(exc)
    return {'created_utc': datetime.now(timezone.utc).isoformat(), 'code_sha256': identity,
            'file_sha256': hashes, 'git_revision': revision,
            'git_status_note': 'File hashes identify the actual executed files, including uncommitted changes.',
            'git_error': git_error}


def planned_fits(cfg):
    per_split = 2
    for name in ['svm', 'mlp', 'rbf', 'svm_linear', 'svm']:
        per_split += len(ParameterGrid(grid_for(name, cfg))) * cfg['inner_folds'] + 1
    final = len(ParameterGrid(grid_for('svm', cfg))) * cfg['inner_folds'] + 1
    return per_split * cfg['outer_folds'] * len(cfg['outer_seeds']) + final


def peak_rss_bytes():
    # Windows pateikia tikrą proceso didžiausią working set nuo jo paleidimo.
    if os.name == 'nt':
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [
                (name, ctypes.c_size_t) for name in ['PeakWorkingSetSize', 'WorkingSetSize',
                'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
                'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage']]
        counter = Counters()
        counter.cb = ctypes.sizeof(counter)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        api = ctypes.WinDLL('psapi', use_last_error=True).GetProcessMemoryInfo
        api.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
        if not api(kernel.GetCurrentProcess(), ctypes.byref(counter), counter.cb):
            raise ctypes.WinError(ctypes.get_last_error())
        return int(counter.PeakWorkingSetSize)
    import resource
    import sys
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == 'darwin' else value * 1024)
