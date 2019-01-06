#!/usr/bin/env groovy

pipeline {
    agent {
        label 'manager'
    }
    options {
        buildDiscarder(logRotator(numToKeepStr:'3'))
        timeout(time: 1, unit: 'HOURS')
        ansiColor('xterm')
    }
    environment {
        GIT_ORG = "shane"
        GIT_REPO = "docker-test"
        STACK_NAME = "${GIT_ORG}-${docker-test}"
        COMPOSE_FILE = "docker-compose-swarm.yml"
    }
    stages {
        stage('Init') {
            steps {
                //getEnvFiles("${GIT_ORG}-${GIT_REPO}")
            }
        }
        stage('Dev Deployment') {
            when {
                changeRequest()
            }
            steps {
                environment {
                    ENV_FILE = "${GIT_REPO}/dev.env"
                    FULL_STACK_NAME = "dev_${STACK_NAME}"
                }
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                                  credentialsId: '5c9a657c-23e1-43f6-a3b0-11e455d02902',
                                  usernameVariable: 'USERNAME',
                                  passwordVariable: 'PASSWORD']])
                    {
                        sh "docker-compose -f ${COMPOSE_FILE} build --force-rm"
                        sh "docker login --username ${USERNAME} --password ${PASSWORD} harbor01.cssnr.com"
                        sh "docker-compose -f ${COMPOSE_FILE} push"
                        sh "docker stack deploy ${FULL_STACK_NAME} -c ${COMPOSE_FILE} --with-registry-auth"
                    }
            }
        }
        stage('Production Deployment') {
            when {
                branch 'master'
            }
            steps {
                environment {
                    ENV_FILE = "${GIT_REPO}/dev.env"
                    FULL_STACK_NAME = "prod_${STACK_NAME}"
                }
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                                  credentialsId: '5c9a657c-23e1-43f6-a3b0-11e455d02902',
                                  usernameVariable: 'USERNAME',
                                  passwordVariable: 'PASSWORD']])
                        {
                            sh "docker-compose -f ${COMPOSE_FILE} build --force-rm"
                            sh "docker login --username ${USERNAME} --password ${PASSWORD} harbor01.cssnr.com"
                            sh "docker-compose -f ${COMPOSE_FILE} push"
                            sh "docker stack deploy ${FULL_STACK_NAME} -c ${COMPOSE_FILE} --with-registry-auth"
                        }
            }
        }
    }
    post {
        always {
            currentBuild.result = currentBuild.result ?: 'SUCCESS'
        }
    }
}
