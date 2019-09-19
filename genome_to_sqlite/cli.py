import click
import os
import zipfile
import sqlite_utils
from .utils import convert_genome_text_to_sqlite


@click.command()
@click.argument(
    "export_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option("-s", "--silent", is_flag=True, help="Don't show progress bar")
def cli(export_file, db_path, silent):
    """Import your genome into a SQLite database. EXPORT_FILE can be .zip or .txt

    More information: https://github.com/dogsheep/genome-to-sqlite
    """
    try:
        zf = zipfile.ZipFile(export_file)
    except zipfile.BadZipFile:
        # Assume it is text
        fp = open(export_file, "rb")
        file_length = os.path.getsize(export_file)
    else:
        # Ensure export.xml is in there
        filenames = [zi.filename for zi in zf.filelist]
        if len(filenames) != 1:
            raise click.ClickException("Zip file does not contain a single text file")
        filename = filenames[0]
        fp = zf.open(filename)
        file_length = zf.getinfo(filename).file_size
    db = sqlite_utils.Database(db_path)
    if silent:
        convert_genome_text_to_sqlite(fp, db)
    else:
        with click.progressbar(length=file_length, label="Importing genome") as bar:
            convert_genome_text_to_sqlite(fp, db, progress_callback=bar.update)
