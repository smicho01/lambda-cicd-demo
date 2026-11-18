
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

        stage('Push Image to ECR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-lambda-cicd',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        set +x
                        export DOCKER_CONFIG="$(mktemp -d)"
                        trap 'rm -rf "$DOCKER_CONFIG"' EXIT

                        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
                        REGISTRY="${ACCOUNT_ID}.dkr.ecr.eu-west-2.amazonaws.com"
                        IMAGE_URI="${REGISTRY}/lambda-cicd-demo:${GIT_COMMIT}"

                        aws ecr get-login-password --region eu-west-2 |
                            docker login --username AWS --password-stdin "$REGISTRY"

                        docker tag "lambda-cicd-demo:${GIT_COMMIT}" "$IMAGE_URI"

                        docker push "$IMAGE_URI"

                        echo "Pushed image: $IMAGE_URI"
                    '''
                }
            }
        }
    }
}
