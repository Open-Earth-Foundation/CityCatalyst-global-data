FROM mageai/mageai:latest

ARG PROJECT_NAME=cc-mage
ARG MAGE_CODE_PATH=/home/src
ARG USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

WORKDIR ${MAGE_CODE_PATH}

COPY ${PROJECT_NAME} ${PROJECT_NAME}

ENV USER_CODE_PATH=${USER_CODE_PATH}

RUN pip3 install -r ${USER_CODE_PATH}/requirements.txt

# Keep production pipeline runs independent of runtime extension downloads.
RUN python3 -c "import duckdb; connection = duckdb.connect(); [connection.install_extension(name) for name in ('aws', 'httpfs', 'postgres')]"

ENV PYTHONPATH="${PYTHONPATH}:${MAGE_CODE_PATH}"

CMD ["/bin/sh", "-c", "/app/run_app.sh"]
