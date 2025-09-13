# chris-freg Projects

This is part of a 3-project system designed for local development and deployment on an M1 Mac using Jenkins and Docker Desktop:

- **chris-freg** - Frontend application
- **chris-freg-api** - REST API backend
- **chris-freg-db** - Database initialization and schema

All projects are configured to be built and deployed automatically by a local Jenkins installation that polls GitHub repositories, builds Docker images, and deploys containers with full CI/CD pipeline integration.

## chris-freg-db

Database initialization and schema management for the fees management system.

### Features
- PostgreSQL schema definitions
- Database initialization scripts
- Test data generation utilities
- Jenkins CI/CD pipeline integration

### Structure
```
db-init/
├── 01-schema.sql    # Database schema creation
└── 02-data.sql      # Initial data and test records
```

### Database Schema
- `fees` table with comprehensive fee management fields
- Support for fee codes, values, descriptions, and metadata
- Date range management (start_date, end_date)
- Categorization (type, service, jurisdiction)

### Development
The database initialization scripts are automatically executed during deployment:
1. Schema creation (`01-schema.sql`)
2. Data population (`02-data.sql`)

### Deployment
Jenkins pipeline automatically:
1. Starts PostgreSQL container
2. Executes initialization scripts
3. Validates database connectivity
4. Provides database service to API backend