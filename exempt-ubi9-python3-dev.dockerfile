## Jack S. - NON-Root Python Dev Container

# FROM registry.access.redhat.com/ubi9:latest as base - ubi9 is unable to downgrade libffi which breaks spire.doc
FROM registry.access.redhat.com/ubi8/python-311:latest as base

ENV USERNAME=devusr
ENV USER_GROUP=devgrp
ENV USER_UID=540
ENV USER_GID=352
ENV HOME="/home/${USERNAME}"
ENV WORKING_DIR_NAME="${HOME}/project"

USER root

RUN sed -i.ORIG -rn 's/(^UID_MIN)(.+)(1000)/\1 \2 500/p; /^UID_MIN/!p' /etc/login.defs && \
    groupadd -g ${USER_GID} -r ${USER_GROUP} && \
    useradd -s /bin/bash -u ${USER_UID} -g 0 -G ${USER_GROUP} -d ${HOME} -m ${USERNAME} 

COPY ../. ${WORKING_DIR_NAME}

RUN chmod -R 775 /usr/local/bin && \
    chown -R ${USERNAME}:0 /usr/local/bin && \
    chown -R ${USERNAME}:${USER_GID} ${HOME} && \
    chmod -R 777 ${HOME} && \
    mkdir -p ${WORKING_DIR_NAME} && \
    chown -R ${USERNAME}:${USER_GID} ${WORKING_DIR_NAME} && \
    chmod -R 777 ${WORKING_DIR_NAME} && \
    rm -f /var/logs/*

# Install any possibly needed compile time packages / test issues - system_packages.list file contains this list
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
RUN dnf install -y --setopt=tsflags=nodocs --exclude container-selinux < ${WORKING_DIR_NAME}/system_packages.list
RUN dnf clean all && \
    ln -s /usr/bin/python3 /usr/bin/python

FROM base as interum

# Install any pip required packageds from REQ
RUN pip install -r ${WORKING_DIR_NAME}/docker_only_requirements.txt

FROM interum as final

USER ${USER_UID}
WORKDIR ${WORKING_DIR_NAME} 

ENTRYPOINT ["/usr/bin/bash"]
