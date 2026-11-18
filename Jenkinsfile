
pipeline {
    agent any

    stages {
        stage('Verify Git Checkout') {
            steps {
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

        stage('Verify AWS Identity') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-lambda-cicd',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh 'aws sts get-caller-identity --query Arn --output text'
                }
            }
        }
    }
}
