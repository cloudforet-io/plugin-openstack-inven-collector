FROM cloudforet/python-core:1

ENV PYTHONUNBUFFERED 1
ENV CLOUDONE_PORT 50051
ENV SERVER_TYPE grpc
ENV PKG_DIR /tmp/pkg
ENV SRC_DIR /tmp/src
ENV OPENSTACK_PKG_DIR /usr/local/lib/python3.8/site-packages/openstack

RUN apt update && apt upgrade -y
RUN apt install gcc -y

COPY pkg/*.txt ${PKG_DIR}/

RUN pip install --upgrade pip && \
    pip install --upgrade -r ${PKG_DIR}/pip_requirements.txt && \
    pip install --upgrade --pre spaceone-core spaceone-api

COPY src ${SRC_DIR}

WORKDIR ${SRC_DIR}

RUN python3 setup.py install
COPY pkg/external_sdk/openstack ${OPENSTACK_PKG_DIR}/
RUN rm -rf /tmp/*

EXPOSE ${CLOUDONE_PORT}

ENTRYPOINT ["spaceone"]
CMD ["grpc", "spaceone.inventory"]
