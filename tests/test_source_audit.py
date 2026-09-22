import hashlib
import pytest
from src.source_audit import verify_training_source


def setup_sources(tmp_path, current, archived=b'x = 1\n'):
    original = b'x = 1\n'
    (tmp_path / 'audit/training_sources').mkdir(parents=True)
    (tmp_path / 'audit/training_sources/demo.py').write_bytes(archived)
    (tmp_path / 'demo.py').write_bytes(current)
    return hashlib.sha256(original).hexdigest()


def test_comments_allowed(tmp_path):
    digest = setup_sources(tmp_path, b'# paaiskinimas\nx = 1  # reiksme\n')
    verify_training_source(tmp_path, 'demo.py', digest)


def test_logic_change_rejected(tmp_path):
    digest = setup_sources(tmp_path, b'x = 2\n')
    with pytest.raises(ValueError, match='vykdomas'):
        verify_training_source(tmp_path, 'demo.py', digest)


def test_modified_archive_rejected(tmp_path):
    digest = setup_sources(tmp_path, b'# note\nx = 1\n', b'x = 2\n')
    with pytest.raises(ValueError, match='manifesto'):
        verify_training_source(tmp_path, 'demo.py', digest)
