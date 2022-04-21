FROM python:3.9.2-slim-buster

ARG MANAGERITM_VERSION=0.1.0

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        curl \
        jq \
        libnss-wrapper \
        procps; \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*;

# Create user named "docker" with no password
RUN useradd --create-home --shell /bin/bash manageritm \
    && passwd manageritm -d

# set an entrypoint script that allows us to
# dynamically change the uid/gid of the container's user
COPY entry_point.sh /opt/bin/
ENTRYPOINT ["/opt/bin/entry_point.sh"]

RUN pip install gunicorn
COPY manageritm-${MANAGERITM_VERSION}-py3-none-any.whl /tmp/.
RUN pip install /tmp/manageritm-${MANAGERITM_VERSION}-py3-none-any.whl
