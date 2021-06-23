from setuptools import setup, find_packages
import os
import codecs

REQUIREMENTS = [
    'numpy',
    'pandas',
    'toml',
    'krb5',
    'pyhive',
    'pure-sasl',
    'dynaconf',
    'kerberos',
    'thrift',
    'thrift_sasl',
    'pure-transport',
    'teradatasql'
]


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description: str = fh.read()


setup(
    name='tele2_metrics',
    version=get_version("src/__init__.py"),
    description='Framework for models metrics and monitoring',
    author='Ekaterina Gruzdova',
    author_email='bde@tele2.ru',
    url="https://gitlab.tdp.corp.tele2.ru/mle/tele2_dvv_monitoring",
    license='LICENSE.txt',
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["contrib", "docs", "tests*", "tasks"],
    ),
    install_requires=REQUIREMENTS,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.7.3",
        "License :: OSI Approved :: MIT License",
        "Operation System :: OS Independent"
    ],
    zip_safe=False,
    python_requires='>=3.7',
)
