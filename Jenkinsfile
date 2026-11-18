
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

                    mkdir -p test-results
                    rm -f test-results/pytest.xml

                    docker build \
                        --platform linux/amd64 \
                        -f Dockerfile.test \
                        -t "lambda-cicd-demo-tests:${GIT_COMMIT}" .

                    container_id=$(docker create \
                        "lambda-cicd-demo-tests:${GIT_COMMIT}" \
                        python -m pytest -v --junitxml=/tmp/pytest.xml)

                    trap 'docker rm -f "$container_id" >/dev/null 2>&1 || true' EXIT

                    docker start -a "$container_id" || true

                    docker cp \
                        "$container_id:/tmp/pytest.xml" \
                        test-results/pytest.xml

                    exit_code=$(docker inspect \
                        --format '{{.State.ExitCode}}' "$container_id")

                    test "$exit_code" -eq 0
                '''
            }

            post {
                always {
                    junit testResults: 'test-results/pytest.xml',
                        allowEmptyResults: true
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


        stage('Trivy Security Scan') {
            steps {
                sh '''
                    set -eu

                    image_archive="lambda-image.tar"
                    scanner_container=""

                    cleanup() {
                        rm -f "$image_archive"

                        if [ -n "$scanner_container" ]; then
                            docker rm -f "$scanner_container" >/dev/null 2>&1 || true
                        fi
                    }

                    trap cleanup EXIT

                    docker save \
                        -o "$image_archive" \
                        "lambda-cicd-demo:${IMAGE_TAG}"

                    scanner_container=$(docker create \
                        -v trivy-cache:/root/.cache \
                        ghcr.io/aquasecurity/trivy:0.76.2 \
                        image \
                        --input /tmp/lambda-image.tar \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --exit-code 1)

                    docker cp \
                        "$image_archive" \
                        "$scanner_container:/tmp/lambda-image.tar"

                    docker start -a "$scanner_container" || true

                    scan_exit_code=$(docker inspect \
                        --format '{{.State.ExitCode}}' \
                        "$scanner_container")

                    test "$scan_exit_code" -eq 0
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
