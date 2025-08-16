pipeline {
    agent any

    environment {
        POSTGRES_CONTAINER = 'freg-db'
        POSTGRES_USER = 'postgres'
        POSTGRES_PASSWORD = 'postgres'
        POSTGRES_DB = 'fees'
        POSTGRES_PORT = '5432'
    }

    stages {
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
                    docker-compose up -d
                '''
            }
        }

        stage('Trigger API Build') {
            steps {
                echo "Triggering API build is disabled for local development."
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Postgres container ${POSTGRES_CONTAINER} should still be running."
        }
    }
}
