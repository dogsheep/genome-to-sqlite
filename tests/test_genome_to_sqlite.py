from click.testing import CliRunner
from genome_to_sqlite import cli, utils
import pytest
import sqlite_utils
import pathlib
import zipfile


@pytest.fixture
def text_path():
    return str(pathlib.Path(__file__).parent / "example.txt")


@pytest.fixture
def db(text_path):
    db = sqlite_utils.Database(":memory:")
    utils.convert_genome_text_to_sqlite(open(text_path, "rb"), db)
    return db


def test_conversion(db):
    assert ["genome"] == db.table_names()
    rows = list(db["genome"].rows)
    assert [
        {"rsid": "rs12564807", "chromosome": "1", "position": 326472, "genotype": "AA"},
        {"rsid": "rs3131972", "chromosome": "1", "position": 583459, "genotype": "GG"},
        {"rsid": "rs1488288", "chromosome": "1", "position": 876634, "genotype": "CC"},
        {"rsid": "rs12124819", "chromosome": "1", "position": 947369, "genotype": "GG"},
    ] == rows


def test_help():
    result = CliRunner().invoke(cli.cli, ["--help"])
    assert result.output.startswith("Usage: cli")


def test_cli_parses_zip(text_path, tmpdir):
    db_path = str(tmpdir / "output.db")
    # Put the example in a zip file
    zip_path = str(tmpdir / "genome.zip")
    with zipfile.ZipFile(str(zip_path), "w") as z:
        z.write(text_path, "genome.txt")
    # Now use CLI tool to import that zip file
    result = CliRunner().invoke(cli.cli, [zip_path, db_path])
    assert 0 == result.exit_code
    db = sqlite_utils.Database(db_path)
    assert ["genome"] == db.table_names()


def test_cli_parses_text(text_path, tmpdir):
    db_path = str(tmpdir / "output.db")
    result = CliRunner().invoke(cli.cli, [text_path, db_path])
    assert 0 == result.exit_code
    db = sqlite_utils.Database(db_path)
    assert ["genome"] == db.table_names()
