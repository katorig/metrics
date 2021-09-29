pip install twine --timeout 10 --index-url xxx \
--trusted-host xxx
python3 setup.py clean --all
python3 setup.py bdist_wheel
twine upload dist/* --verbose --repository-url=xxx \
-u ${NEXUS_USER} -p ${NEXUS_PASSWORD}

twine upload dist/* --verbose --repository-url=xxx \
-u ${FROG_USER} -p ${FROG_PASSWORD}
