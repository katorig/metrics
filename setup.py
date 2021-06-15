from os.path import dirname, join
from setuptools import setup, find_packages
from dynaconf import settings
import argparse

PROJECT_NAME = "dvv_monitoring"
SOURCES_DIR = "app/src"


def read(*names, **kwargs):
    this_directory = dirname(__file__)
    with open(join(this_directory, *names), encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('model_id', metavar='model_id', type=int, help='Please type model_id')
    parser.add_argument('report_date', metavar='report_date', type=str,
                        help="Please type report_date in 'YYYY-MM-DD' format")
    args = parser.parse_args()
    settings.MODEL_ID = args.model_id
    settings.REPORT_DATE = args.report_date
    return args.model_id, args.report_date


def read_version(path):
    for line in read(path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


if __name__ == "__main__":
    setup(
        name=PROJECT_NAME,
        version=read_version("app/src/__init__.py"),
        package_dir={"": SOURCES_DIR},
        packages=find_packages(
            where="src",
            exclude=["contrib", "docs", "tests*", "tasks"],
        ),
        python_requires=" >= 3.7.3",  # TODO: change Python version?
        install_requires=read("requirements.txt"),
        test_suite="tests",

        description="This library is for monitoring models health and data validation.",
        long_description=read("README.md"),
        long_description_content_type="text/markdown",
        maintainer="Tele2 BDO MLE Team",
        maintainer_email="bde@tele2.ru",
        url="https://gitlab.tdp.corp.tele2.ru/mle/monitoring/tele2_dvv_monitoring",
        keywords=["bigdata", "monitoring", "metrics", "alerts", "dvv"],
        classifiers=[
            "Programming Language :: Python :: 3.7.3"
        ]
    )
