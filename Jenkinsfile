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
    }
}