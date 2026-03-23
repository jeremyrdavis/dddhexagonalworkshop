# Attendee Registration - Traditional MVC Application

This is a traditional JavaEE MVC application for conference attendee registration. It serves as the starting point for refactoring to Domain-Driven Design (DDD) patterns.

## Architecture Overview

This application follows the traditional **Model-View-Controller (MVC)** pattern with:

- **Model**: JPA entities with anemic domain model (`AttendeeEntity`, `Address`)
- **View**: REST API endpoints (no traditional UI views)
- **Controller**: REST controllers handling HTTP requests (`AttendeeController`)

### Key Characteristics (Traditional Approach)

1. **Anemic Domain Model**: Entities are just data holders with getters/setters
2. **Transaction Script Pattern**: Business logic concentrated in service layer
3. **Database-Centric Design**: Domain model mirrors database structure
4. **Tight Coupling**: Direct dependencies between layers
5. **CRUD Operations**: Simple Create-Read-Update-Delete operations

## Project Structure

```
src/main/java/com/conference/attendees/
├── config/
│   └── RestConfiguration.java          # JAX-RS configuration
├── controller/
│   ├── AttendeeController.java         # REST endpoints
│   ├── ErrorResponse.java              # Error response DTO
│   └── PaginatedResponse.java          # Pagination wrapper
├── dto/
│   ├── AttendeeRegistrationRequest.java # Input DTO
│   └── AttendeeResponse.java           # Output DTO
├── model/
│   ├── Address.java                    # Address POJO (will become Value Object)
│   └── AttendeeEntity.java             # JPA Entity (will become Aggregate)
├── repository/
│   └── AttendeeRepository.java         # Data Access Object (DAO)
└── service/
    ├── AttendeeService.java            # Business logic service
    ├── EventPublisher.java             # CDI event publisher
    ├── AttendeeRegistrationEvent.java  # CDI event
    ├── AttendeeAlreadyExistsException.java
    └── AttendeeNotFoundException.java
```

## Technology Stack

- **Jakarta EE 10** - Enterprise Java platform
- **JAX-RS** - REST API framework
- **JPA/Hibernate** - Object-relational mapping
- **CDI** - Contexts and Dependency Injection
- **PostgreSQL** - Database
- **WildFly 31 / JBoss EAP** - Application server
- **Maven** - Build tool

## Building and Running

### Prerequisites

- Java 11+
- Maven 3.6+
- Docker (for database)
- WildFly 31 or JBoss EAP (or use Docker)

### Build the Application

```bash
mvn clean package
```

### Setup Database with Docker

```bash
docker-compose up postgres -d
```

### Deploy to WildFly

1. **Download PostgreSQL JDBC Driver**:
   ```bash
   wget -O postgresql-42.7.3.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
   ```

2. **Setup WildFly** (copy the JDBC jar to your WildFly installation first):
   ```bash
   $WILDFLY_HOME/bin/jboss-cli.sh --connect --file=wildfly-setup.cli
   ```

3. **Deploy the WAR**:
   ```bash
   cp target/attendee-registration.war $WILDFLY_HOME/standalone/deployments/
   ```

### Run with Docker Compose

```bash
docker-compose up --build
```

## API Endpoints

### Register Attendee
```bash
POST /api/attendees
Content-Type: application/json

{
    "email": "john.doe@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "streetAddress": "123 Main Street",
    "bus": "Apt 4B",
    "postalCode": "12345",
    "townOrMunicipality": "Springfield"
}
```

### Get All Attendees
```bash
GET /api/attendees?page=0&size=20
```

### Get Attendee by ID
```bash
GET /api/attendees/{id}
```

### Get Attendee by Email
```bash
GET /api/attendees/email/{email}
```

### Update Attendee
```bash
PUT /api/attendees/{id}
Content-Type: application/json

{
    "email": "john.doe@example.com",
    "firstName": "John",
    "lastName": "Doe Updated",
    "streetAddress": "456 New Street",
    "bus": null,
    "postalCode": "54321",
    "townOrMunicipality": "New City"
}
```

### Delete Attendee
```bash
DELETE /api/attendees/{id}
```

### Health Check
```bash
GET /api/attendees/health
```

## What Will Be Refactored to DDD

This application will be refactored to implement Domain-Driven Design patterns:

1. **Value Objects**: `Address` will become an immutable value object with validation
2. **Aggregates**: `AttendeeEntity` will become an `Attendee` aggregate with business logic
3. **Domain Services**: Extract complex business logic from application services
4. **Repository Pattern**: Abstract persistence concerns from domain logic
5. **Domain Events**: Replace CDI events with proper domain events
6. **Application Services**: Coordinate between domain and infrastructure
7. **Hexagonal Architecture**: Implement ports and adapters pattern

## Testing the Application

### Sample Requests

1. **Register a new attendee**:
   ```bash
   curl -X POST http://localhost:8080/attendee-registration/api/attendees \
   -H "Content-Type: application/json" \
   -d '{
     "email": "test@example.com",
     "firstName": "Test",
     "lastName": "User",
     "streetAddress": "123 Test Street",
     "postalCode": "12345",
     "townOrMunicipality": "Test City"
   }'
   ```

2. **Get all attendees**:
   ```bash
   curl http://localhost:8080/attendee-registration/api/attendees
   ```

## Current Limitations (To Be Addressed with DDD)

1. **No Business Rules Enforcement**: Domain logic scattered across services
2. **Anemic Domain Model**: Entities are just data containers
3. **Tight Coupling**: Direct dependencies between all layers
4. **No Domain Language**: Technical implementation doesn't reflect business concepts
5. **Limited Testability**: Hard to unit test business logic in isolation
6. **Scalability Issues**: Difficult to evolve complex business rules

These limitations will be addressed through the DDD refactoring process.