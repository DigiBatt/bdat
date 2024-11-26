echo $CI_JOB_TOKEN
pip install --index-url https://gitlab-ci-token:${CI_JOB_TOKEN}@git.isea.rwth-aachen.de/api/v4/projects/2034/packages/pypi/simple mvl
pip install --index-url https://gitlab-ci-token:${CI_JOB_TOKEN}@git.isea.rwth-aachen.de/api/v4/projects/2493/packages/pypi/simple cadi_templates
pip install --index-url https://gitlab-ci-token:${CI_JOB_TOKEN}@git.isea.rwth-aachen.de/api/v4/projects/2305/packages/pypi/simple bdat
