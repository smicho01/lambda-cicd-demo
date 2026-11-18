
pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    stages {
        stage('Validate Branch') {
            steps {
                script {
                    def branchName = env.BRANCH_NAME

                    if (!(branchName == 'master' || branchName ==~ /^JEN-[0-9]+$/)) {
                        error("Invalid branch name: ${branchName}")
                    }

                    env.IMAGE_TAG = branchName

                    echo "Branch: ${branchName}"
                    echo "Docker image tag: ${env.IMAGE_TAG}"
                }
            }
        }

        
        stage('Unit Tests') {
            steps {
                sh '''
                    set -eu

                    docker build \
                        --platform linux/amd64 \
                        -f Dockerfile.test \
                        -t "lambda-cicd-demo-tests:${GIT_COMMIT}" .

                    docker run --rm \
                        "lambda-cicd-demo-tests:${GIT_COMMIT}"
                '''
            }
        }


        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        --platform linux/amd64 \
                        -t "lambda-cicd-demo:${IMAGE_TAG}" .
                '''
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
                        set -eu
                        set +x

                        export DOCKER_CONFIG="$(mktemp -d)"
                        trap 'rm -rf "$DOCKER_CONFIG"' EXIT

                        AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
                        ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.eu-west-2.amazonaws.com"
                        IMAGE_URI="${ECR_REGISTRY}/lambda-cicd-demo:${IMAGE_TAG}"

                        aws ecr get-login-password --region eu-west-2 |
                            docker login --username AWS --password-stdin "$ECR_REGISTRY"

                        docker tag "lambda-cicd-demo:${IMAGE_TAG}" "$IMAGE_URI"
                        docker push "$IMAGE_URI"

                        echo "Published: $IMAGE_URI"
                    '''
                }
            }
        }
    }
}
