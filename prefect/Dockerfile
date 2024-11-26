FROM prefecthq/prefect:2.18.0-python3.10
COPY flows.py install.sh /opt/bdat/prefect/
ARG CI_JOB_TOKEN
RUN /opt/bdat/prefect/install.sh
WORKDIR /opt/bdat/
