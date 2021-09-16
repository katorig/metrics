#!/bin/bash

yum groupinstall -y "Development Tools" && yum install -y gcc gcc-c++ python3-devel.x86_64 cyrus-sasl-devel

export conda_env=app-env
conda env create -f environment.yml -n ${conda_env} && conda clean -af

kinit -kt secrets/${HADOOP_USER_NAME}.keytab ${HADOOP_USER_NAME}@CORP.TELE2.RU

#conda run --no-capture-output -n app-env python src/tele2_metrics/<file>.py
