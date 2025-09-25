# Step 6: Repositories

## tl;dr

_If you want to get the application up and running as quickly as possible you can copy/paste the code into the stubbed classes without reading the rest of the material._

Repositories represent all objects of a certain type as a conceptual set (usually emulated). They act like collections, except with more elaborate querying capability. Objects of the appropriate type are added and removed, and the machinery behind the repository inserts them or deletes them from the database.

```java
package dddhexagonalworkshop.conference.attendees.persistence;

import dddhexagonalworkshop.conference.attendees.domain.aggregates.Attendee;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

import java.util.Optional;

/**
* Repository for managing Attendee aggregate persistence.
*
* This class bridges between the domain model (Attendee) and the persistence
* model (AttendeeEntity), handling all conversion and database operations.
* The repository implements the domain's persistence interface while using
* Quarkus Panache for the actual database operations.
  */
  @ApplicationScoped
  public class AttendeeRepository implements PanacheRepository<AttendeeEntity> {

  /**
    * Persists an Attendee aggregate to the database.
    * Converts the domain aggregate to a persistence entity and saves it.
    *
    * @param aggregate The Attendee domain aggregate to persist
      */
      public void persist(Attendee aggregate) {
      // Convert domain aggregate to persistence entity
      AttendeeEntity attendeeEntity = fromAggregate(aggregate);
    
          // Use inherited Panache method to persist
          persist(attendeeEntity);
      }

  /**
    * Converts a domain Attendee aggregate to an AttendeeEntity for persistence.
    * This is where domain concepts are mapped to database structures.
    *
    * @param attendee The domain aggregate
    * @return The persistence entity
      */
      private AttendeeEntity fromAggregate(Attendee attendee) {
          return new AttendeeEntity(attendee.getEmail());
      }
}

```

[Step 7: Outbound Adapters](07-Outbound-Adapters.md)

### Learning Objectives

- Understand the Repository pattern as the bridge between domain and persistence
- Implement AttendeeRepository that converts between aggregates and entities
- Apply domain-driven persistence patterns while maintaining clean architecture
- Connect domain aggregates to database storage through proper abstraction layers

## What You'll Build

An AttendeeRepository that handles all persistence operations for attendees, converting between domain Attendee aggregates and persistence AttendeeEntity objects while maintaining clean separation of concerns.

## Why Repositories Are Essential in DDD

Repositories solve the fundamental problem of how domain objects interact with persistence without being contaminated by database concerns:
The Persistence Pollution Problem: Without repositories, domain logic gets mixed with database code:

❌ Domain service polluted with persistence concerns

```java

@ApplicationScoped
public class AttendeeService {
@Inject EntityManager entityManager;

    public AttendeeDTO registerAttendee(RegisterAttendeeCommand command) {
        // Domain logic mixed with JPA code
        AttendeeEntity entity = new AttendeeEntity(command.email());
        entityManager.persist(entity);  // Database concerns in domain service
        entityManager.flush();

        // More JPA code mixed with business logic
        return new AttendeeDTO(entity.getEmail());
    }
}
```

The Repository Solution: Repositories encapsulate all persistence logic:

✅ Clean separation through repository pattern

```java
@ApplicationScoped
public class AttendeeService {
@Inject AttendeeRepository attendeeRepository;  // Domain interface

    public AttendeeDTO registerAttendee(RegisterAttendeeCommand command) {
        // Pure domain logic
        AttendeeRegistrationResult result = Attendee.registerAttendee(command.email());

        // Repository handles all persistence concerns
        attendeeRepository.persist(result.attendee());

        return new AttendeeDTO(result.attendee().getEmail());
    }
}
```

## Repository Pattern: Core Concepts

**Collection Abstraction:** Repositories make persistence feel like working with an in-memory collection of domain objects. You add, remove, and find aggregates without thinking about SQL or database details.

**Domain Interface:** The repository interface is defined in the domain layer, expressing operations in business terms, not database terms.

**Implementation Separation:** The actual persistence implementation can use JPA, MongoDB, files, or any other technology without affecting domain code.

**Aggregate Boundary:** Each aggregate root gets its own repository. You don't have repositories for every entity - only for aggregates you need to retrieve independently.

### Deep Dive: Repository Responsibilities vs Other Patterns

#### Repository vs Data Access Object (DAO)

| Aspect | Repository (DDD) | DAO (Data Access) |
|--------|------------------|-------------------|
| Focus | Domain aggregates | Database tables/entities |
| Interface | Business operations | CRUD operations |
| Conversion | Aggregate ⟷ Entity | Entity ⟷ Database |
| Query Language | Domain concepts | SQL/Database terms |
| Scope | Per aggregate root | Per table/entity |

### Repository Example (Domain-focused):

```java
public interface AttendeeRepository {
    void persist(Attendee attendee);                    // Business operation
    Optional<Attendee> findByEmail(String email);       // Business query
    List<Attendee> findRegisteredAttendees();           // Business concept
    void remove(Attendee attendee);                     // Business operation
}
```

### DAO Example (Database-focused):

```java
public interface AttendeeDAO {
    void insert(AttendeeEntity entity);                 // Database operation
    AttendeeEntity selectById(Long id);                 // Database query
    List<AttendeeEntity> selectAll();                   // Database operation
    void update(AttendeeEntity entity);                 // Database operation
    void delete(Long id);                               // Database operation
}
```

### Repository vs Service Layer

| Aspect | Repository | Service |
|--------|------------|---------|
| Purpose | Persistence abstraction | Business workflow orchestration |
| Scope | Single aggregate type | Cross-aggregate operations |
| Dependencies | Database/ORM only | Repositories, external services |
| Transaction | Usually single operations | Often manages transactions |
| Domain Events | Not responsible for events | Publishes domain events |


## What Belongs in Repository:

✅ Persistence operations for Attendee aggregate

```java
@ApplicationScoped
public class AttendeeRepository {
    public void persist(Attendee attendee) { ... }
    public Optional<Attendee> findByEmail(String email) { ... }
    public void remove(Attendee attendee) { ... }
}
```

### What Belongs in Service:

✅ Business workflow orchestration

```java
    @ApplicationScoped
public class AttendeeService {

    public AttendeeDTO registerAttendee(RegisterAttendeeCommand command) {
        AttendeeRegistrationResult result = Attendee.registerAttendee(command.email());
        attendeeRepository.persist(result.attendee());              // Use repository
        attendeeEventPublisher.publish(result.attendeeRegisteredEvent()); // Publish events
        return new AttendeeDTO(result.attendee().getEmail());
    }
}
```
### Repository vs Active Record

| Aspect | Repository Pattern | Active Record Pattern |
| ------ | ----------------- | -------------------- |
| Object Responsibility | Aggregate = business logic only | Object = business logic + persistence |
| Testability | Easy to mock/stub | Harder to test (database coupled) |
| Separation of Concerns | Clean separation | Mixed concerns |
| Framework Dependency | Isolated in repository | Throughout domain objects |

**Repository Pattern (Separation):**

```java
// Domain aggregate - pure business logic
public class Attendee {
public static AttendeeRegistrationResult registerAttendee(String email) {
// Only business logic, no persistence
}
}

// Repository - handles persistence separately
public class AttendeeRepository {
public void persist(Attendee attendee) { ... }
}
```

**Active Record Pattern (Mixed):**

```java
// Active Record - business logic + persistence mixed
public class Attendee extends ActiveRecord {
    public static AttendeeRegistrationResult registerAttendee(String email) {
        Attendee attendee = new Attendee(email);
        attendee.save();  // Persistence mixed with business logic
        return result;
    }
}
```

## Implementation

Repositories represent all objects of a certain type as a conceptual set (usually emulated). They act like collections, except with more elaborate querying capability. Objects of the appropriate type are added and removed, and the machinery behind the repository inserts them or deletes them from the database.

```java
package dddhexagonalworkshop.conference.attendees.persistence;

import dddhexagonalworkshop.conference.attendees.domain.aggregates.Attendee;
import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

import java.util.Optional;

/**
* Repository for managing Attendee aggregate persistence.
*
* This class bridges between the domain model (Attendee) and the persistence
* model (AttendeeEntity), handling all conversion and database operations.
* The repository implements the domain's persistence interface while using
* Quarkus Panache for the actual database operations.
  */
  @ApplicationScoped
  public class AttendeeRepository implements PanacheRepository<AttendeeEntity> {

  /**
    * Persists an Attendee aggregate to the database.
    * Converts the domain aggregate to a persistence entity and saves it.
    *
    * @param aggregate The Attendee domain aggregate to persist
      */
      public void persist(Attendee aggregate) {
      // Convert domain aggregate to persistence entity
      AttendeeEntity attendeeEntity = fromAggregate(aggregate);
    
          // Use inherited Panache method to persist
          persist(attendeeEntity);
      }

  /**
    * Converts a domain Attendee aggregate to an AttendeeEntity for persistence.
    * This is where domain concepts are mapped to database structures.
    *
    * @param attendee The domain aggregate
    * @return The persistence entity
      */
      private AttendeeEntity fromAggregate(Attendee attendee) {
          return new AttendeeEntity(attendee.getEmail());
      }
}

```

### Key Design Decisions

**Aggregate-to-Entity Conversion:** The fromAggregate() and toAggregate() methods handle all conversion logic, keeping domain and persistence models separate.

**Domain Interface:** Methods are named using business terminology (findByEmail, persist) rather than database terminology (selectByEmail, insert).

**Error Handling:** Repository methods throw domain exceptions, not database exceptions, maintaining the abstraction.

**Panache Integration:** We extend PanacheRepository<AttendeeEntity> to get basic CRUD operations while adding our domain-specific methods.

**Conversion Responsibility:** The repository is responsible for all conversion between domain and persistence models.

### Next Steps

In the next section we will create a second Outbound Adaper, `AttendeeEventPublisher` to send messages to the rest of the system: [Step 7: Outbound Adapters](07-Outbound-Adapters.md)

