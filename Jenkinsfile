
pipeline {
    agent {
        docker {
            image 'docker:24.0.6' // Or any version with Docker CLI
            args '-v /var/run/docker.sock:/var/run/docker.sock' // Needed to control Docker from inside the container
        }
    }

    environment {
        POSTGRES_CONTAINER = 'test-postgres'
        POSTGRES_PASSWORD = 'mysecretpassword'
        POSTGRES_DB = 'testdb'
    }

    stages {
        stage('Start Postgres Docker Container') {
            steps {
                script {
                    sh """
                        docker pull postgres:15
                        docker rm -f \$POSTGRES_CONTAINER || true
                        docker run -d \
                          --name \$POSTGRES_CONTAINER \
                          -e POSTGRES_PASSWORD=\$POSTGRES_PASSWORD \
                          -e POSTGRES_DB=\$POSTGRES_DB \
                          -p 5432:5432 \
                          -v \$PWD/db-init:/docker-entrypoint-initdb.d \
                          postgres:15
                    """
                }
            }
        }

        stage('Wait for DB to be Ready') {
            steps {
                script {
                    sh '''
                    echo "Waiting for Postgres to be ready..."
                    for i in {1..10}; do
                      if docker exec $POSTGRES_CONTAINER pg_isready -U postgres; then
                        echo "Postgres is ready."
                        break
                      fi
                      sleep 2
                    done
                    '''
                }
            }
        }

        stage('Verify Data') {
            steps {
                script {
                    sh """
                        docker exec -i \$POSTGRES_CONTAINER psql -U postgres -d \$POSTGRES_DB -c '\\dt'
                        docker exec -i \$POSTGRES_CONTAINER psql -U postgres -d \$POSTGRES_DB -c 'SELECT COUNT(*) FROM your_table;' || true
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Stopping Postgres container...'
            sh 'docker rm -f $POSTGRES_CONTAINER || true'
        }
    }
}
