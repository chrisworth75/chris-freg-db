
pipeline {
    agent any

    environment {
        POSTGRES_CONTAINER = 'fregdb-postgres'
        POSTGRES_PASSWORD = 'mypassword'
        POSTGRES_DB = 'fregdb'
        POSTGRES_PORT = '5432'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Starting PostgreSQL container with mounted SQL files"
                    sh """
                        docker rm -f \$POSTGRES_CONTAINER || true

                        docker run -d \
                          --name \$POSTGRES_CONTAINER \
                          -e POSTGRES_PASSWORD=\$POSTGRES_PASSWORD \
                          -e POSTGRES_DB=\$POSTGRES_DB \
                          -v \$PWD/db-init:/docker-entrypoint-initdb.d \
                          -p \$POSTGRES_PORT:5432 \
                          postgres:15
                    """
                }
            }
        }

        stage('Verify Schema Loaded') {
            steps {
                script {
                    sh """
                        echo "Waiting for Postgres to become ready..."
                        for i in {1..10}; do
                          if docker exec \$POSTGRES_CONTAINER pg_isready -U postgres; then
                            echo "Postgres is ready!"
                            break
                          fi
                          sleep 2
                        done

                        echo "Checking if tables exist..."
                        docker exec \$POSTGRES_CONTAINER psql -U postgres -d \$POSTGRES_DB -c '\\dt'
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up container...'
            sh 'docker rm -f $POSTGRES_CONTAINER || true'
        }
    }
}
