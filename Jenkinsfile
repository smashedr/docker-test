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
        //String GIT_ORG = getGitGroup("${GIT_URL}")
        //String GIT_REPO = getGitRepo("${GIT_URL}")
        String GIT_ORG = "shane"
        String GIT_REPO = "docker-test"
        String DEV_PORT = '10123'
        String PROD_PORT = '10124'
        String COMPOSE_FILE = "docker-compose-swarm.yml"
        String VERSION = getVersion("${GIT_BRANCH}")
        GString STACK_NAME = "${GIT_ORG}-${GIT_REPO}"
        GString SERVICE_NAME = "${STACK_NAME}"
    }
    stages {
        stage('Init') {
            steps {
                echo "\n--- Build Details ---\n" +
                        "SERVICE_NAME:  ${SERVICE_NAME}\n" +
                        "STACK_NAME:    ${STACK_NAME}\n" +
                        "GIT_BRANCH:    ${GIT_BRANCH}\n" +
                        "VERSION:       ${VERSION}\n"
                verifyBuild()
                getConfigs("${SERVICE_NAME}")   // remove this if you do not need config files

                script {
                    def group = getGitGroup("${GIT_URL}")
                    echo group
                    currentBuild.rawBuild.result = Result.ABORTED
                    throw (new hudson.AbortException("Test Abort."))
                }
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
                sendDiscord("smashed-alerts", "Dev Deploy Started")
                setupNfs("${STACK_NAME}")       // remove this if you do not need nfs volumes
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
                sendDiscord("smashed-alerts", "Prod Deploy Started")
                setupNfs("${STACK_NAME}")       // remove this if you do not need nfs volumes
                stackPush("${COMPOSE_FILE}")
                stackDeploy("${COMPOSE_FILE}", "${STACK_NAME}")
            }
        }
    }
    post {
        always {
            script { if (!env.INVALID_BUILD) {
                sendDiscord("smashed-alerts", "Deploy Finished: ${currentBuild.currentResult}")
            } }
            cleanWs()
        }
    }
}
