
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
                    echo "Starting PostgreSQL container with mounted SQL files"
                    sh """
                        docker rm -f ${POSTGRES_CONTAINER} || true

                        docker run -d \
                          --name ${POSTGRES_CONTAINER} \
                          -e POSTGRES_USER=${POSTGRES_USER} \
                          -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
                          -e POSTGRES_DB=${POSTGRES_DB} \
                          -v \${PWD}/db-init:/docker-entrypoint-initdb.d \
                          -p ${POSTGRES_PORT}:5432 \
                          postgres:15
                    """
                }
            }
        }

        stage('Verify Schema Loaded') {
            steps {
                script {
                    sh '''
                        echo "Waiting for Postgres to become ready..."
                        for i in {1..30}; do
                          if docker exec ${POSTGRES_CONTAINER} pg_isready -U postgres; then
                            echo "Postgres is ready!"
                            break
                          fi
                          sleep 2
                        done

                        echo "Checking if tables exist..."
                        docker exec ${POSTGRES_CONTAINER} psql -U postgres -d ${POSTGRES_DB} -c '\\dt'
                    '''
                }
            }
        }

        stage('Trigger API Build') {
            steps {
                build job: 'chris-freg-api-multibranch', wait: false
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Postgres container ${POSTGRES_CONTAINER} should still be running."
        }
    }
}
