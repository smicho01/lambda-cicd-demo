
pipeline {
    agent any

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

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                        --platform linux/amd64 \
                        -t "lambda-cicd-demo:${IMAGE_TAG}" .
                '''
            }
        }
    }
}
