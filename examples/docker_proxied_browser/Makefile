DCYML=docker/compose.yaml
DCARGS=
HOURMINSEC=`date +'%H%M%S'`
MANAGERITM_VERSION=$(shell cd ../../; poetry version | grep manageritm | cut -d' ' -f2)
PROJECT=manageritm
NETWORK=${PROJECT}_default
SCALE_CHROME=1
SCALE_CLIENT=1
SCALE_SERVER=1
SCALE_FIREFOX=1
SELENIUM_VERSION=4.1.2-20220217
TRE_IMAGE?=manageritm:tre
USER_UID_GID=`id -u`:`id -g`
WORKDIR=/home/docker

DOCKER_RUN_COMMAND=docker run --rm --init -it \
	    --name=tre-${HOURMINSEC} \
	    --network=$(NETWORK) \
	    --user=${USER_UID_GID} \
	    --volume=${CURDIR}:${WORKDIR} \
	    --workdir=${WORKDIR} \
	    ${TRE_IMAGE}

COMMAND=bash

.PHONY: all
all: build

.PHONY: build
build: build-services build-tre

.PHONY: build-services
build-services:
	cp ../../dist/manageritm-*-py3-none-any.whl docker/manageritm/.
	MANAGERITM_VERSION=${MANAGERITM_VERSION} \
	SELENIUM_VERSION=${SELENIUM_VERSION} \
	USER_UID_GID=${USER_UID_GID} \
	docker-compose -f ${DCYML} -p ${PROJECT} build

.PHONY: build-tre
build-tre:
	cp ../../dist/manageritm-*-py3-none-any.whl docker/tre/.
	docker build -t ${TRE_IMAGE} docker/tre

.PHONY: run
run:
	${DOCKER_RUN_COMMAND} ${COMMAND}

.PHONY: test-env-up
test-env-up:
	MANAGERITM_VERSION=${MANAGERITM_VERSION} \
	SELENIUM_VERSION=${SELENIUM_VERSION} \
	USER_UID_GID=${USER_UID_GID} \
	docker-compose \
		-f ${DCYML} \
		-p ${PROJECT} \
		up \
		-d \
		--scale manageritm-server=${SCALE_SERVER} \
		--scale manageritm-client=${SCALE_CLIENT} \
		--scale chrome=${SCALE_CHROME} \
		--scale firefox=${SCALE_FIREFOX}

.PHONY: test-env-down
test-env-down:
	MANAGERITM_VERSION=${MANAGERITM_VERSION} \
	SELENIUM_VERSION=${SELENIUM_VERSION} \
	USER_UID_GID=${USER_UID_GID} \
	docker-compose \
		-f ${DCYML} \
		-p ${PROJECT} \
		down

.PHONY: test-env-logs
test-env-logs:
	MANAGERITM_VERSION=${MANAGERITM_VERSION} \
	SELENIUM_VERSION=${SELENIUM_VERSION} \
	USER_UID_GID=${USER_UID_GID} \
	docker-compose \
		-f ${DCYML} \
		-p ${PROJECT} \
		logs \
			--timestamps \
			--follow \
			${DCARGS}

.PHONY: test-env-compose
test-env-compose:
	MANAGERITM_VERSION=${MANAGERITM_VERSION} \
	SELENIUM_VERSION=${SELENIUM_VERSION} \
	USER_UID_GID=${USER_UID_GID} \
	docker-compose \
		-f ${DCYML} \
		-p ${PROJECT} \
		${DCARGS}

.PHONY: clean
clean:
	rm -rf \
		hars \
		docker/manageritm/manageritm-*-py3-none-any.whl \
		docker/tre/manageritm-*-py3-none-any.whl \
