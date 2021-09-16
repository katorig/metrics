pip install twine --timeout 10 --index-url http://nexus.t2ru-bda-wds-008.corp.tele2.ru/repository/pypi-all/simple \
--trusted-host nexus.t2ru-bda-wds-008.corp.tele2.ru
python3 setup.py clean --all
python3 setup.py bdist_wheel
twine upload dist/* --verbose --repository-url=http://nexus.t2ru-bda-wds-008.corp.tele2.ru/repository/pypi-hosted/ \
-u ${NEXUS_USER} -p ${NEXUS_PASSWORD}

twine upload dist/* --verbose --repository-url=https://artifactory.tdp.corp.tele2.ru/artifactory/api/pypi/bdo-pypi \
-u ${FROG_USER} -p ${FROG_PASSWORD}
