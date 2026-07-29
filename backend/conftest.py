import pytest
from pathlib import Path
from db import FileDB

@pytest.fixture
def safe_path_test_settings(tmp_path, monkeypatch):
    class SafePathTestSettings:
        db_path: Path = ":memory:"
        upload_dir: Path = tmp_path / "uploads"
        tmp_dir: Path = tmp_path / "tmp"
        output_dir: Path = tmp_path / "outputs"

    settings = SafePathTestSettings()

    settings.upload_dir.mkdir()
    settings.tmp_dir.mkdir()
    settings.output_dir.mkdir()

    monkeypatch.setattr('core.helper_functions.get_settings', lambda: settings)

    return settings

@pytest.fixture
def tmp_db(safe_path_test_settings, monkeypatch):
    monkeypatch.setattr('core.helper_functions.get_settings', lambda: safe_path_test_settings)
    monkeypatch.setattr(FileDB, 'DB_PATH', ':memory:')
    db = FileDB()
    yield db
    db.close()