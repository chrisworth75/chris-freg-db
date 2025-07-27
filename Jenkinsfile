pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Running build...'
                // Insert your actual build logic here
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // Insert test commands here (e.g., pytest, npm test, etc.)
            }
        }
    }
}
