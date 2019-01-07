#!/usr/bin/env groovy

@Library('jenkins-libraries')_

pipeline {
    agent {
        label 'manager'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr:'5'))
        timeout(time: 1, unit: 'HOURS')
        ansiColor('xterm')
    }
    environment {
        String GIT_ORG = "shane"
        String GIT_REPO = "docker-test"
        String DEV_PORT_0 = '10123'
        String PROD_PORT_0 = '10124'
        String COMPOSE_FILE = "docker-compose-swarm.yml"
        String VERSION = getVersion("${env.GIT_BRANCH}")
        GString STACK_NAME = "${GIT_ORG}-${GIT_REPO}"
    }
    stages {
        stage('Init') {
            steps {
                echo "Starting Init..."
                echo "STACK_NAME: ${STACK_NAME}"
                echo "VERSION: ${VERSION}"

                // comment this out if you do not need config files
                getConfigs()
            }
        }
        stage('Dev Deploy') {
            when {
                allOf {
                    not { branch 'master' }
                }
            }
            environment {
                GString ENV_FILE = "deploy-configs/services/${STACK_NAME}/dev.env"
                GString FULL_STACK_NAME = "dev_${STACK_NAME}"
                GString DOCKER_PORT = "${DEV_PORT_0}"
            }
            steps {
                echo "Starting Dev Deploy..."
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${FULL_STACK_NAME}", "${COMPOSE_FILE}")
            }
        }
        stage('Prod Deploy') {
            when {
                allOf {
                    branch 'master'
                    triggeredBy 'UserIdCause'
                }
            }
            environment {
                GString ENV_FILE = "deploy-configs/services/${STACK_NAME}/prod.env"
                GString FULL_STACK_NAME = "prod_${STACK_NAME}"
                GString DOCKER_PORT = "${PROD_PORT_0}"
            }
            steps {
                echo "Starting Prod Deploy..."
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${FULL_STACK_NAME}", "${COMPOSE_FILE}")
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
