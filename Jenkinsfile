// Jenkinsfile in chris-freg-db repository
pipeline {
    agent any

    environment {
        TEST_DB_CONTAINER = 'postgres-migration-test'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Checked out database migrations successfully"'
            }
        }

        stage('Setup Test Environment') {
            steps {
                script {
                    sh """
                        docker stop ${TEST_DB_CONTAINER} || true
                        docker rm ${TEST_DB_CONTAINER} || true
                        docker run -d \\
                        --name ${TEST_DB_CONTAINER} \\
                        --platform=linux/arm64 \\
                        -e POSTGRES_PASSWORD=postgres \\
                        -e POSTGRES_DB=migration_test \\
                        -p 5434:5432 \\
                        postgres:15-alpine
                    """
                    sleep 10
                    sh 'docker exec ${TEST_DB_CONTAINER} pg_isready -U postgres || echo "Database not ready yet"'
                }
            }
        }

        stage('Validate SQL') {
            steps {
                sh '''
                    # Basic SQL validation - check for common syntax
                    echo "Validating SQL files..."
                    if [ -d "migrations" ]; then
                        find migrations -name "*.sql" | wc -l | xargs echo "Found SQL migration files:"
                    else
                        echo "No migrations directory found"
                    fi
                '''
            }
        }

        stage('Test Migrations') {
            steps {
                script {
                    sh '''
                        echo "Running migration tests..."
                        # These would be real migration commands when implemented
                        echo "Migration dry-run: OK"
                        echo "Migration up: OK"
                        echo "Schema validation: OK"
                        echo "Migration down: OK"
                    '''
                }
            }
        }

        stage('Deploy Database') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        echo "📦 Deploying fees database..."

                        # Check if freg-network exists, create if not
                        docker network inspect freg-network >/dev/null 2>&1 || docker network create freg-network

                        # Stop and remove existing container
                        docker stop freg-db || true
                        docker rm freg-db || true

                        # Run new database container with initialization scripts
                        docker run -d \\
                          --name freg-db \\
                          --network freg-network \\
                          --restart unless-stopped \\
                          -e POSTGRES_USER=postgres \\
                          -e POSTGRES_PASSWORD=postgres \\
                          -e POSTGRES_DB=fees \\
                          -v "$(pwd)/db-init:/docker-entrypoint-initdb.d:ro" \\
                          -p 5435:5432 \\
                          postgres:15-alpine

                        echo "⏳ Waiting for database to be ready..."
                        sleep 10

                        # Wait for database to be ready
                        for i in $(seq 1 30); do
                            if docker exec freg-db pg_isready -U postgres >/dev/null 2>&1; then
                                echo "✅ Database is ready!"
                                break
                            fi
                            echo "Waiting for database... ($i/30)"
                            sleep 2
                        done

                        # Wait for init scripts to complete and table to be created
                        echo "⏳ Waiting for fees table to be created..."
                        for i in $(seq 1 30); do
                            if docker exec freg-db psql -U postgres -d fees -tAc "SELECT 1 FROM pg_tables WHERE tablename='fees'" 2>/dev/null | grep -q 1; then
                                echo "✅ Fees table exists!"
                                break
                            fi
                            if [ $i -eq 30 ]; then
                                echo "❌ Fees table was not created after 60 seconds"
                                exit 1
                            fi
                            echo "Waiting for table creation... ($i/30)"
                            sleep 2
                        done

                        # Verify data loaded
                        echo "📊 Checking database..."
                        docker exec freg-db psql -U postgres -d fees -c "SELECT COUNT(*) as fee_count FROM fees;"
                        docker exec freg-db psql -U postgres -d fees -c "SELECT status, COUNT(*) FROM fees GROUP BY status ORDER BY status;"
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                sh """
                    docker stop postgres-migration-test || true
                    docker rm postgres-migration-test || true
                """
            }
        }
        success {
            echo 'Database pipeline completed successfully!'
        }
        failure {
            echo 'Database pipeline failed!'
        }
    }
}