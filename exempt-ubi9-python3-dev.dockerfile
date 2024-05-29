## Jack S. - NON-Root Python Dev Container

FROM registry.access.redhat.com/ubi9:latest as base

ENV USERNAME=devusr
ENV USER_UID=540
ENV USER_GID=352
ENV WORKING_DIR_NAME="/home/${USERNAME}/project"

ENV HOME="/home/devusr"

USER root

# Install any possibly needed compile time packages
RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
    dnf install -y --setopt=tsflags=nodocs \
                    cmake \
                    openssh-server \
                    openssl-devel \
                    gcc \
                    g++ \
                    rust \
                    cargo \
                    python-devel \
                    platform-python-devel \
                    less \
                    lsof \
                    iperf \ 
                    nmap \
                    nmap-ncat \
                    supervisor \
                    unzip \
                    zip \
                    python3-pip \
                  --exclude container-selinux && \
    dnf clean all && \
    ln -s /usr/bin/python3 /usr/bin/python


RUN sed -i.ORIG -rn 's/(^UID_MIN)(.+)(1000)/\1 \2 500/p; /^UID_MIN/!p' /etc/login.defs && \
    groupadd -g 352 -r devgrp && \
    useradd -s /bin/bash -u 540 -g 0 -G devgrp -d /home/devusr -m devusr 

RUN chmod -R 775 /usr/local/bin && \
    chown -R ${USERNAME}:0 /usr/local/bin && \
    chown -R ${USERNAME}:0 ${HOME} && \
    chmod -R 775 ${HOME} && \
    mkdir -p ${WORKING_DIR_NAME} && \
    chown -R ${USERNAME}:0 ${WORKING_DIR_NAME} && \
    chmod -R 775 ${WORKING_DIR_NAME} && \
    rm -f /var/logs/*

COPY --chown="$USER_UID":"$USER_GID" --chmod=644 ../. ${WORKING_DIR_NAME}

# Install any pip required packageds from REQ
RUN pip install -r ${WORKING_DIR_NAME}/requirements.txt

USER 540
WORKDIR /home/devusr/project 

ENTRYPOINT ["/usr/bin/bash"]