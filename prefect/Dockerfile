FROM prefecthq/prefect:3.6.5-python3.12
COPY flows.py install.sh /opt/bdat/prefect/
ARG CI_JOB_TOKEN
RUN /opt/bdat/prefect/install.sh
WORKDIR /opt/bdat/
