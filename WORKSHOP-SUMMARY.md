# Domain-Driven Design & Hexagonal Architecture Workshop

## Workshop Overview

A hands-on, practical workshop where you'll learn Domain-Driven Design (DDD) and Hexagonal Architecture by building a real microservice from the ground up. This workshop emphasizes **learning by doing** – you'll spend your time writing code that demonstrates architectural concepts, not just listening to theory.

By the end of this workshop, you'll have built a complete conference attendee registration system that demonstrates clean architecture, business-focused design, and proper separation of concerns.

## What You'll Build

A production-ready microservice featuring:
- **REST API** for attendee registration
- **Business logic** encapsulated in rich domain models
- **Event-driven architecture** using Kafka
- **Clean hexagonal architecture** with clear boundaries
- **PostgreSQL persistence** with proper domain/database separation

## Who Should Attend

This workshop is designed for:
- **Software developers** who want to move beyond CRUD applications
- **Architects** looking to implement DDD in practice, not just theory
- **Technical leads** responsible for system design decisions
- **Anyone** who believes architecture is best learned through hands-on implementation

### Prerequisites
- Working knowledge of Java
- Basic understanding of REST APIs and databases
- Enthusiasm for getting hands on a keyboard
- No prior DDD experience required

## Workshop Agenda

### Module 1: End-to-End Domain-Driven Design (Core Module)
**Duration:** 2-3 hours
**Format:** 10 progressive steps, each building on the last

Build a complete DDD workflow from REST endpoint to database and message queue:

1. **Domain Events** - Capture business facts that have occurred
2. **Commands** - Represent business intentions and requests
3. **Result Objects** - Combine multiple outputs cleanly
4. **Aggregates** - Encapsulate core business logic
5. **Persistence Entities** - Separate database concerns from domain
6. **Repositories** - Abstract data access with collection-like interface
7. **Outbound Adapters** - Integrate with external systems (Kafka)
8. **Application Services** - Orchestrate business workflows
9. **Data Transfer Objects** - Define API contracts
10. **Inbound Adapters** - Complete the HTTP interface

**Key Takeaway:** A working microservice demonstrating the complete hexagonal architecture pattern.

---

### Module 2: Value Objects
**Duration:** 1-1.5 hours
**Format:** 7 focused steps

Enhance your domain model with immutable value objects:

1. **Create Value Objects** - Build an immutable Address value object
2. **Update Commands** - Incorporate value objects into business requests
3. **Update Aggregates** - Enrich domain model with value objects
4. **Update Events** - Include value objects in domain events
5. **Persistence Mapping** - Use @Embedded for value object storage
6. **Update DTOs** - Expose value objects through API
7. **Update Services** - Complete the integration

**Key Takeaway:** Richer domain models that express business concepts clearly and eliminate primitive obsession.

---

### Module 3: Anti-Corruption Layer
**Duration:** 1-1.5 hours
**Format:** 5 implementation steps

Protect your domain from external system complexity:

1. **External System Integration** - Understand the integration challenge
2. **Implement Translator** - Build the anti-corruption layer
3. **Inbound Adapter** - Accept external formats
4. **Value Objects** - Create domain-specific value objects
5. **Update Commands** - Complete the translation pipeline

**Key Takeaway:** Keep your domain model clean while integrating with messy external systems.

---

### Module 4: Refactoring to DDD (Optional)
**Duration:** 1-2 hours
**Format:** Self-guided refactoring exercise

Transform a traditional MVC application into a DDD architecture:

- Start with an **anemic domain model** (traditional JavaEE/WildFly app)
- Identify **transaction script** patterns
- Refactor to **rich domain models**
- Implement **hexagonal architecture**
- Apply lessons from Modules 1-3

**Key Takeaway:** Practical experience refactoring legacy code to DDD patterns.

---

## Total Workshop Duration

- **Core Path (Modules 1-3):** 4.5 - 6 hours
- **Complete Workshop (All 4 Modules):** 5.5 - 8 hours
- **Flexible pacing:** Each module is self-contained and can be completed at your own speed

## Learning Outcomes

By completing this workshop, you will be able to:

### Domain-Driven Design
✅ Distinguish between Commands and Events
✅ Identify proper Aggregate boundaries
✅ Create immutable Value Objects
✅ Implement Domain Services for complex workflows
✅ Apply the Repository pattern correctly
✅ Build an Anti-Corruption Layer for external integrations

### Hexagonal Architecture
✅ Separate business logic from technical concerns
✅ Create Inbound Adapters (REST, messaging, etc.)
✅ Create Outbound Adapters (database, events, external APIs)
✅ Design clean interfaces between layers
✅ Build testable, technology-independent domain logic

### Practical Skills
✅ Build event-driven microservices
✅ Work with modern Java frameworks (Quarkus)
✅ Implement proper persistence abstraction
✅ Integrate with Kafka for event streaming
✅ Refactor legacy code to clean architecture

## Workshop Format

### Hands-On Coding Approach
- **No Death by PowerPoint** - Minimal slides, maximum coding
- **Stubbed Classes** - Start with skeleton code and clear instructions
- **Progressive Building** - Each step compiles and runs
- **TL;DR Sections** - Quick reference for fast implementation
- **Complete Solutions** - Reference implementations for each module

### Technology Stack
- **Quarkus** - Supersonic, subatomic Java framework
- **Java 21** - Modern Java with records and pattern matching
- **PostgreSQL** - Relational database
- **Kafka** - Event streaming platform
- **Maven** - Build automation

### Development Environment Options
1. **GitHub Codespaces** - Zero setup, runs in browser
2. **Local Quarkus Dev Mode** - Single command: `./mvnw quarkus:dev`
3. **DevSpaces** - Cloud development environment

**Why Quarkus?**
One command (`./mvnw quarkus:dev`) automatically starts:
- Your application with live reload
- PostgreSQL database
- Kafka broker
- Integrated testing capabilities

Focus on DDD concepts, not infrastructure configuration.

## What Makes This Workshop Different

### Theory Meets Practice
Most DDD workshops drown you in theory. This workshop teaches concepts **through implementation**. You'll learn what aggregates are by building one, understand events by publishing them to Kafka, and grasp hexagonal architecture by creating actual ports and adapters.

### Real Code, Real Architecture
You won't build toy examples. By the end, you'll have a working microservice with:
- REST endpoints handling HTTP requests
- Domain logic enforcing business rules
- Database persistence with clean separation
- Event publishing to Kafka
- Proper error handling and validation

### Production Patterns
Learn patterns you'll actually use:
- How to structure domain models
- Where business logic belongs
- How to keep your domain clean
- When to use value objects vs entities
- How to integrate with external systems safely

### Instructor Support
- Stuck on a step? Solutions are provided for every module
- Can't compile? Each step includes working code
- Want to experiment? Complete the basics first, then customize
- Questions welcome throughout

## Workshop Materials Included

- ✅ Complete source code for all 4 modules
- ✅ Step-by-step documentation with code examples
- ✅ Reference solutions for self-checking
- ✅ Pre-configured development environment
- ✅ Sample API requests and test data

## After the Workshop

All materials remain available on GitHub:
- Continue learning at your own pace
- Reference the patterns in your own projects
- Explore additional refactoring challenges
- Connect with instructors for questions

## Ready to Get Started?

This workshop will change how you think about software architecture. You'll leave with practical skills, working code, and the confidence to implement DDD in your own projects.

**Architecture is best learned through practice. Let's build something.**

---

## Quick Start Checklist

Before the workshop:
- [ ] Clone the repository
- [ ] Ensure Java 21+ is installed (or use Codespaces)
- [ ] Test Quarkus dev mode: `./mvnw quarkus:dev`
- [ ] Verify PostgreSQL and Kafka auto-start
- [ ] Be ready to code!

Alternative (zero local setup):
- [ ] Open repository in GitHub Codespaces
- [ ] Run `./mvnw quarkus:dev`
- [ ] Start coding!

---

*This workshop is brought to you by developers who believe that architecture without implementation is just philosophy, and implementation without architecture is just hacking. We prefer neither extreme.*
