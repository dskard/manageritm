FROM ghcr.io/rstudio/checkrs-tew:0.7.0-prerelease-20220315-1

ARG MANAGERITM_VERSION=0.1.0

COPY manageritm-${MANAGERITM_VERSION}-py3-none-any.whl /tmp/.
RUN pip install /tmp/manageritm-${MANAGERITM_VERSION}-py3-none-any.whl
