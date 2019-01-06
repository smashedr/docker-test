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
        String GIT_ORG = "shane"
        String GIT_REPO = "docker-test"
        GString STACK_NAME = "${GIT_ORG}-${GIT_REPO}"
        String COMPOSE_FILE = "docker-compose-swarm.yml"
    }
    stages {
        stage('Init') {
            steps {
                // Checkout config files here...
                //getEnvFiles("${GIT_ORG}-${GIT_REPO}")
                echo "${env.GIT_BRANCH}"
            }
        }
        stage('Dev Deployment') {
            when {
                not { triggeredBy 'UserIdCause' }
            }
            environment {
                GString ENV_FILE = "${GIT_REPO}/dev.env"
                GString FULL_STACK_NAME = "dev_${STACK_NAME}"
            }
            steps {
                echo "this is a dev deployment"
                //withCredentials([[$class: 'UsernamePasswordMultiBinding',
                //                  credentialsId: '5c9a657c-23e1-43f6-a3b0-11e455d02902',
                //                  usernameVariable: 'USERNAME',
                //                  passwordVariable: 'PASSWORD']])
                //        {
                //            sh "docker-compose -f ${COMPOSE_FILE} build --force-rm"
                //            sh "docker login --username ${USERNAME} --password ${PASSWORD} harbor01.cssnr.com"
                //            sh "docker-compose -f ${COMPOSE_FILE} push"
                //            sh "docker stack deploy ${FULL_STACK_NAME} -c ${COMPOSE_FILE} --with-registry-auth"
                //        }
            }
        }
        stage('Production Deployment') {
            when {
                allOf {
                    equals expected: 'origin/master', actual: env.GIT_BRANCH
                    triggeredBy 'UserIdCause'
                }
            }
            environment {
                GString ENV_FILE = "${GIT_REPO}/prod.env"
                GString FULL_STACK_NAME = "prod_${STACK_NAME}"
            }
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                                  credentialsId: '5c9a657c-23e1-43f6-a3b0-11e455d02902',
                                  usernameVariable: 'USERNAME',
                                  passwordVariable: 'PASSWORD']])
                        {
                            // build should happen in different step, but combining now for simplicity
                            sh "docker-compose -f ${COMPOSE_FILE} build --force-rm"
                            sh "docker login --username ${USERNAME} --password ${PASSWORD} harbor01.cssnr.com"
                            sh "docker-compose -f ${COMPOSE_FILE} push"
                            // this should be the only thing done on a manager node and building should be on a slave
                            sh "docker stack deploy ${FULL_STACK_NAME} -c ${COMPOSE_FILE} --with-registry-auth"
                        }
            }
        }
    }
    //post {
    //    always {
    //        script {
    //            currentBuild.result = currentBuild.result ?: 'SUCCESS'
    //        }
    //    }
    //}
}
