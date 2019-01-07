#!/usr/bin/env groovy

@Library('jenkins-libraries')

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
        GString STACK_NAME = "${GIT_ORG}-${GIT_REPO}"
        //VERSION = ("${env.GIT_BRANCH}" =~ /master/) ? "latest" : "${env.GIT_BRANCH}"
        VERSION = getVersion("${env.GIT_BRANCH}")
    }
    stages {
        stage('Init') {
            steps {
                // Checkout config files here...
                //getEnvFiles("${GIT_ORG}-${GIT_REPO}")
                echo "VERSION: ${VERSION}"


                withCredentials(bindings: [sshUserPrivateKey(
                        credentialsId: '4aac7d8c-0463-449d-8fa7-b0550b5a5e77',
                        keyFileVariable: 'SSH_KEY')]) {
                    echo "SSH_KEY: ${SSH_KEY}"
                    sh "stat ${SSH_KEY}"
                    sh "cat ${SSH_KEY}"
                }



            }
        }
        stage('Dev Deployment') {
            when {
                triggeredBy 'UserIdCause-DISABLED'
            }
            environment {
                GString ENV_FILE = "${GIT_REPO}/dev.env"
                GString FULL_STACK_NAME = "dev_${STACK_NAME}"
                GString DOCKER_PORT = "${DEV_PORT_0}"
            }
            steps {
                echo "this is a dev deployment"
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                                  credentialsId: '5c9a657c-23e1-43f6-a3b0-11e455d02902',
                                  usernameVariable: 'USERNAME',
                                  passwordVariable: 'PASSWORD']]) {

                    // build should happen in different step, but combining now for simplicity
                    sh "docker-compose -f ${COMPOSE_FILE} build --force-rm"
                    sh "docker login --username ${USERNAME} --password ${PASSWORD} harbor01.cssnr.com"
                    sh "docker-compose -f ${COMPOSE_FILE} push"
                    // this should be the only thing done on a manager node and building should be on a slave
                    sh "docker stack deploy ${FULL_STACK_NAME} -c ${COMPOSE_FILE} --with-registry-auth"

                }
            }
        }
        stage('Production Deployment') {
            when {
                allOf {
                    //equals expected: 'origin/master', actual: env.GIT_BRANCH
                    branch 'master'
                    triggeredBy 'UserIdCause'
                }
            }
            environment {
                GString ENV_FILE = "${GIT_REPO}/prod.env"
                GString FULL_STACK_NAME = "prod_${STACK_NAME}"
                GString DOCKER_PORT = "${PROD_PORT_0}"
            }
            steps {
                echo "this is a prod deployment"
                withCredentials([[$class: 'UsernamePasswordMultiBinding',
                                  credentialsId: '5c9a657c-23e1-43f6-a3b0-11e455d02902',
                                  usernameVariable: 'USERNAME',
                                  passwordVariable: 'PASSWORD']]) {

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
