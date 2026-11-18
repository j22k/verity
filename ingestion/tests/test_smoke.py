from typer.testing import CliRunner

from ingestion import __version__
from ingestion.cli import app
from ingestion.config import get_settings


def test_cli_version():
    result = CliRunner().invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_settings_defaults():
    assert get_settings().embedding_dim == 384
