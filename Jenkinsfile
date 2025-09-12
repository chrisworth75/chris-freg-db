
pipeline {
    agent any

    environment {
        POSTGRES_CONTAINER = 'freg-db'
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = 'postgres'
        POSTGRES_DB = 'fees'
        POSTGRES_PORT = '5432'
        NETWORK_NAME = 'freg-net'
    }

    stages {
        stage('Ensure Network') {
            steps {
                sh '''
                    if ! docker network ls --format '{{.Name}}' | grep -w ${NETWORK_NAME}; then
                        docker network create ${NETWORK_NAME}
                    fi
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "This step is now handled by docker-compose."
                }
            }
        }

        stage('Start Container') {
            steps {
                sh '''
                    if [ -f docker-compose.yml.bak ] && [ ! -f docker-compose.yml ]; then
                        mv docker-compose.yml.bak docker-compose.yml
                    fi
                    docker stop freg-db || true
                    docker rm freg-db || true
                    docker-compose up -d
                    docker network connect ${NETWORK_NAME} freg-db || true
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Postgres container ${POSTGRES_CONTAINER} should still be running."
        }
        success {
            script {
                echo "Triggering chris-freg-api build."
                build job: 'chris-freg-api/main', wait: true, propagate: false

                echo "Triggering chris-freg frontend build."
                build job: 'chris-freg/main', wait: true, propagate: false
            }
        }
    }
}
