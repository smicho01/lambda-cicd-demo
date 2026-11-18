pipeline {
    agent any

    stages {
        stage('Verify Git Checkout') {
            steps {
                echo 'Jenkins successfully loaded the pipeline from GitHub!'
                sh 'git log -1 --format="%h %s"'
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker version'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        --platform linux/amd64 \
                        -t "lambda-cicd-demo:${GIT_COMMIT}" .
                '''

                sh 'docker image inspect "lambda-cicd-demo:${GIT_COMMIT}" --format "{{.Id}}"'
            }
        }

        stage('Check AWS CLI') {
            steps {
                sh 'aws --version'
            }
        }
    }
}