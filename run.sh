#!/bin/bash

export conda_env=app-env
conda env create -f environment.yml -n ${conda_env} && conda clean -af

kinit -kt ${HADOOP_USER_NAME}.keytab ${HADOOP_USER_NAME}@CORP.TELE2.RU

cd app
conda run --no-capture-output -n app-env python src/tests/test_metrics.py
