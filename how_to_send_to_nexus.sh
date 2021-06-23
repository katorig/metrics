pip install twine --timeout 10 --index-url http://nexus.t2ru-bda-wds-008.corp.tele2.ru/repository/pypi-all/simple \
--trusted-host nexus.t2ru-bda-wds-008.corp.tele2.ru
python3 setup.py clean --all
python3 setup.py bdist_wheel
twine upload dist/* --verbose --repository-url=http://nexus.t2ru-bda-wds-008.corp.tele2.ru/repository/pypi-hosted/ \
-u katorig -p The45key
