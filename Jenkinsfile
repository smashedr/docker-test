#!/usr/bin/env groovy

@Library('jenkins-libraries')_

pipeline {
    agent {
        label 'manager'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr:'5'))
        timeout(time: 1, unit: 'HOURS')
    }
    environment {
        String GIT_ORG = "shane"
        String GIT_REPO = "docker-test"
        String DEV_PORT = '10123'
        String PROD_PORT = '10124'
        String COMPOSE_FILE = "docker-compose-swarm.yml"
        String VERSION = getVersion("${GIT_BRANCH}")
        GString STACK_NAME = "${GIT_ORG}-${GIT_REPO}"
        GString SERVICE_NAME = "${GIT_ORG}-${GIT_REPO}"
    }
    stages {
        stage('Init') {
            steps {
                echo "\nBuild Details:\n" +
                        "SERVICE_NAME:  ${SERVICE_NAME}\n" +
                        "STACK_NAME:  ${STACK_NAME}\n" +
                        "GIT_BRANCH:  ${GIT_BRANCH}\n" +
                        "VERSION:     ${VERSION}\n"
                verifyBuild()
            }
        }
        stage('Dev Deploy') {
            when {
                allOf {
                    not { branch 'master' }
                }
            }
            environment {
                GString ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/dev.env"
                GString STACK_NAME = "dev_${STACK_NAME}"
                GString DOCKER_PORT = "${DEV_PORT}"
            }
            steps {
                echo "Starting Dev Deploy..."
                sendDiscord("smashed-coding", "Dev Deploy Started")
                setupNfs("${STACK_NAME}")       // remove this if you do not need nfs volumes
                getConfigs("${SERVICE_NAME}")   // remove this if you do not need config files
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
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
                GString ENV_FILE = "deploy-configs/services/${SERVICE_NAME}/prod.env"
                GString STACK_NAME = "prod_${STACK_NAME}"
                GString DOCKER_PORT = "${PROD_PORT}"
            }
            steps {
                echo "Starting Prod Deploy..."
                sendDiscord("smashed-coding", "Prod Deploy Started")
                setupNfs("${STACK_NAME}")       // remove this if you do not need nfs volumes
                getConfigs("${SERVICE_NAME}")   // remove this if you do not need config files
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
            }
        }
    }
    post {
        always {
            echo "currentBuild.currentResult: ${currentBuild.result}"
            sendDiscord("smashed-coding", "Deploy Finished: ${currentBuild.currentResult}")
            cleanWs()
        }
    }
}
