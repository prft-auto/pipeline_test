pipeline {
    agent any

    parameters {
        string(name: 'selenium', defaultValue: 'http://selenium-grid:4444/wd/hub')
        string(name: 'elastic', defaultValue: 'http://elastic:9200')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '15', artifactNumToKeepStr: '15'))
    }

    stages {
        stage('Stage checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check python') {
            steps {
                sh 'python -version'
            }
        }

        stage('Generate Command') {
            steps {
                script {
                    command = 'python selenium_test.py --selenium-grid '\
                     + params.selenium + ' --elastic ' + params.elastic
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    sh "${command}"
                }
            }
        }
    }
}
