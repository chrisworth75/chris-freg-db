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
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Validate SQL') {
            steps {
                sh '''
                    # Install sqlfluff if not already installed
                    pip3 install sqlfluff || true
                    sqlfluff lint migrations/ --dialect postgres || true
                '''
            }
        }

        stage('Test Migrations') {
            steps {
                script {
                    sh '''
                        export DATABASE_URL="postgresql://postgres:postgres@localhost:5434/migration_test"

                        # Test dry run
                        npm run migrate:dry-run

                        # Test up migrations
                        npm run migrate:up

                        # Validate schema
                        npm run schema:validate

                        # Test down migrations
                        npm run migrate:down

                        # Test up again to ensure repeatability
                        npm run migrate:up
                    '''
                }
            }
        }

        stage('Deploy Migrations') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Backup production database first
                    sh '''
                        docker exec postgres-prod pg_dump -U postgres freg_prod > backup-$(date +%Y%m%d_%H%M%S).sql
                    '''

                    // Run migrations on production
                    sh '''
                        export DATABASE_URL="postgresql://postgres:prodpassword@localhost:5432/freg_prod"
                        npm run migrate:production
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'backup-*.sql', fingerprint: true
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
    }
}
