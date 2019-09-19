from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="genome-to-sqlite",
    description="Import your genome into a SQLite database",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/dogsheep/genome-to-sqlite",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["genome_to_sqlite"],
    entry_points="""
        [console_scripts]
        genome-to-sqlite=genome_to_sqlite.cli:cli
    """,
    install_requires=["sqlite-utils"],
    extras_require={"test": ["pytest"]},
    tests_require=["genome-to-sqlite[test]"],
)
