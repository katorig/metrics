#!/bin/bash

yum install gcc gcc-c++ cyrus-sasl-devel

export conda_env=app-env
conda env create -f environment.yml -n ${conda_env} && conda clean -af

kinit -kt secrets/${HADOOP_USER_NAME}.keytab ${HADOOP_USER_NAME}@CORP.TELE2.RU

cd app
conda run --no-capture-output -n app-env python src/main/segmentation_main.py
