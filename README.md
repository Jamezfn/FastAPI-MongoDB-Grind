# FastAPI-MongoDB Grind

A comprehensive collection of projects designed to master MongoDB database design and FastAPI integration through progressive, hands-on development.

## Overview

This repository contains 12 projects that systematically build your database design and API development skills. Each project introduces new MongoDB-specific concepts and increases in complexity, covering real-world patterns from basic CRUD operations to advanced features like geospatial queries, transactions, and change streams.

## Prerequisites

- Python 3.9+
- Basic understanding of REST APIs
- Familiarity with MongoDB fundamentals (documents, collections, basic queries)
- MongoDB installed locally or access to a MongoDB instance
- Understanding of async/await in Python (for Projects 7-12)

## Getting Started

Each project is self-contained in its own directory with dedicated setup instructions, database schemas, and API endpoints.

```bash
git clone https://github.com/Jamezfn/fastapi-mongodb-grind.git
cd fastapi-mongodb-grind
```

## Projects

### Project 1: Todo API
**Core Concepts**: Single collection, basic CRUD, document structure

A simple task management API to learn MongoDB fundamentals.

**Key Learning**:
- Connecting to MongoDB with PyMongo
- Basic CRUD operations (insert_one, find, update_one, delete_one)
- Document structure and _id field
- Basic queries and filters
- Timestamps and default values

**Challenge Extension**:
- Add task categories with color coding
- Implement task priority sorting
- Add due date reminders

---

### Project 2: Blog with Comments
**Core Concepts**: Embedded documents, array operations, schema validation

A blogging platform where comments are embedded within posts.

**Key Learning**:
- Embedding documents vs referencing
- Working with arrays in documents
- Updating nested documents
- Array operators ($push, $pull, $addToSet)
- MongoDB schema validation rules
- When to embed vs reference

**Challenge Extension**:
- Add comment threading (nested replies)
- Implement comment voting system
- Add markdown support for posts

---

### Project 3: Library Management System
**Core Concepts**: One-to-many relationships, references, $lookup

A library system with books, authors, and members using references.

**Key Learning**:
- Reference-based relationships
- $lookup for joining collections
- Populate pattern
- Managing relationships with ObjectId
- Cascade delete considerations
- Partial indexes for active records

**Challenge Extension**:
- Add book reservation queue
- Implement overdue fine calculations
- Add reading history and recommendations

---

### Project 4: URL Shortener
**Core Concepts**: Indexes, atomic operations, TTL

A high-performance URL shortening service with click tracking.

**Key Learning**:
- Creating and using indexes
- Unique indexes for constraints
- TTL indexes for auto-expiration
- Atomic increment operations ($inc)
- Compound indexes for query optimization

**Challenge Extension**:
- Add rate limiting per user/IP
- Implement custom short URL aliases
- Add QR code generation for URLs

---

### Project 5: Recipe Manager
**Core Concepts**: Complex arrays, text search, embedded objects

A recipe platform with ingredients, steps, and full-text search.

**Key Learning**:
- Text indexes for search
- Complex nested arrays
- Aggregation for filtering and sorting
- Projection and field selection
- Search scoring and relevance

**Challenge Extension**:
- Add nutrition calculation from ingredients
- Implement recipe scaling (servings adjustment)
- Add ingredient substitution suggestions

---

### Project 6: Location-based Service (Restaurant Finder)
**Core Concepts**: Geospatial indexes, location queries

Find restaurants near a location with distance-based queries.

**Key Learning**:
- 2dsphere indexes
- GeoJSON format
- $near and $geoWithin queries
- Distance calculations
- Location-based aggregations

**Challenge Extension**:
- Implement geofencing alerts
- Add delivery radius validation
- Create heat maps of popular areas

---

### Project 7: Async Todo API with Real-time Updates
**Core Concepts**: Motor basics, async CRUD, WebSocket notifications

A reimagined todo API using Motor with real-time updates. **Introduces Motor for async operations.**

**Key Learning**:
- Transitioning from PyMongo to Motor (async driver)
- Async/await patterns with FastAPI
- Basic change streams
- WebSocket integration
- Concurrent request handling

**Challenge Extension**:
- Add collaborative task lists
- Implement real-time presence indicators
- Add task assignment notifications

---

### Project 8: Social Media API
**Core Concepts**: Many-to-many relationships, denormalization, fan-out patterns

A social network with posts, followers, likes, and activity feeds.

**Key Learning**:
- Denormalization strategies
- Fan-out on write vs read
- Many-to-many without junction tables
- Optimizing for read-heavy workloads
- Activity feed patterns
- Handling concurrent operations

**Challenge Extension**:
- Add hashtag trending system
- Implement post bookmarking
- Add content recommendation algorithm

---

### Project 9: E-commerce Analytics
**Core Concepts**: Aggregation pipelines, data transformation, reporting

Process orders and generate sales reports with complex aggregations.

**Key Learning**:
- Aggregation pipeline stages ($match, $group, $project)
- $lookup in aggregations
- Date operations and grouping
- Statistical operations ($sum, $avg, $max)
- Pipeline optimization
- Materialized views pattern

**Challenge Extension**:
- Add customer lifetime value calculation
- Implement inventory forecasting
- Create dynamic dashboard data

---

### Project 10: Time-series Data (IoT Sensor System)
**Core Concepts**: Time-series collections, bucketing, capped collections

Store and analyze sensor data from IoT devices.

**Key Learning**:
- Time-series collections (MongoDB 5.0+)
- Capped collections for fixed-size logs
- Bucketing patterns
- Time-based aggregations
- Retention policies
- Efficient time-range queries

**Challenge Extension**:
- Add anomaly detection alerts
- Implement data downsampling for old data
- Create predictive maintenance alerts

---

### Project 11: Banking Transaction System
**Core Concepts**: Multi-document transactions, ACID compliance

A banking system requiring atomic operations across accounts.

**Key Learning**:
- Multi-document transactions
- Session management
- Rollback and error handling
- Read and write concerns
- Transaction best practices
- Optimistic concurrency control

**Challenge Extension**:
- Add transaction approval workflow
- Implement recurring payments
- Add fraud detection patterns

---

### Project 12: Real-time Notification System
**Core Concepts**: Change streams, real-time updates, async event handling

A notification system that reacts to database changes in real-time using async patterns.

**Key Learning**:
- MongoDB Change Streams with Motor
- Async watch operations on collections
- WebSocket integration with async FastAPI
- Resume tokens for reliability
- Filtering change events
- Event-driven architecture patterns

**Challenge Extension**:
- Add notification preferences and filtering
- Implement notification batching
- Add push notification integration

---

### Bonus Project 13: File Storage Service
**Core Concepts**: GridFS, large binary data

Store and retrieve large files (images, videos, documents) efficiently.

**Key Learning**:
- GridFS architecture (chunks and files)
- Storing binary data
- Streaming large files
- Metadata management
- File versioning

**Challenge Extension**:
- Add image thumbnail generation
- Implement file deduplication
- Add file sharing with expiring links

---

## Technical Stack

- **FastAPI**: Modern Python web framework (supports both sync and async)
- **MongoDB**: NoSQL document database
- **PyMongo**: Synchronous MongoDB driver (Projects 1-6)
- **Motor**: Async MongoDB driver (Projects 7-13, for concurrent operations)
- **Pydantic**: Data validation and settings management
- **pytest**: Testing framework with pytest-asyncio for async tests

## Learning Path

Each project is designed to be completed sequentially, building on MongoDB concepts from previous projects.

**Progression**:
- **Projects 1-6**: Use PyMongo (synchronous) to master core MongoDB concepts
- **Project 7**: Gentle transition to Motor with familiar todo app + real-time features
- **Projects 8-13**: Advanced async patterns and complex MongoDB features

## Key Concepts Covered

- **Document Modeling**: Embedding vs referencing, schema design patterns, denormalization
- **CRUD Operations**: Insert, find, update, delete operations and their variations
- **Indexing**: Single field, compound, text, geospatial, TTL, and partial indexes
- **Aggregation Framework**: Pipelines, stages, operators, and optimization
- **Relationships**: One-to-one, one-to-many, many-to-many in MongoDB
- **Text Search**: Full-text search indexes and queries
- **Geospatial Queries**: Location-based searches and distance calculations
- **Time-series Data**: Time-series collections and temporal queries
- **Capped Collections**: Fixed-size collections for logs and real-time data
- **Transactions**: Multi-document ACID transactions
- **Change Streams**: Real-time change detection and event-driven architecture
- **GridFS**: Large file storage and retrieval
- **Schema Validation**: Enforcing document structure and data types
- **Performance**: Query optimization, explain plans, index strategies

## Testing Strategy

Each project includes:
- **Unit Tests**: Testing individual functions and MongoDB operations
- **Integration Tests**: End-to-end API testing with test database
- **MongoDB In-Memory Server**: For fast, isolated testing (mongomock for simple cases, mongodb-memory-server for advanced features)
- **Async Testing**: pytest-asyncio for Motor-based projects
- **Test Data Factories**: Using factory patterns for consistent test data

Example test structure:
```python
# tests/test_todos.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/todos", json={"title": "Test"})
        assert response.status_code == 201
```

## Deployment Considerations

While the projects focus on local development, later projects touch on production concerns:

- **MongoDB Atlas**: Cloud deployment setup (Project 8+)
- **Replica Sets**: High availability configuration (Project 11)
- **Connection Pooling**: Efficient connection management (All async projects)
- **Environment Configuration**: Using Pydantic Settings for different environments
- **Monitoring**: Basic logging and performance monitoring patterns
- **Docker**: Containerization for consistent environments (optional)

## Project Structure

Each project follows a consistent structure:
```
project-name/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # MongoDB connection
│   ├── models.py            # Pydantic models
│   ├── routes/              # API endpoints
│   └── services/            # Business logic
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── requirements.txt
├── .env.example
└── README.md                # Project-specific instructions
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests with improvements, additional projects, or documentation enhancements.

**Areas for contribution**:
- Additional challenge extensions
- Performance optimization examples
- More test coverage examples
- Docker compose setups
- CI/CD pipeline examples

## License

MIT License - feel free to use these projects for learning and development.

## Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [MongoDB University](https://university.mongodb.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [MongoDB Compass](https://www.mongodb.com/products/compass)
- [MongoDB Performance Best Practices](https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/)

## Acknowledgments

Built as a personal learning journey to master MongoDB and FastAPI integration. Inspired by real-world production patterns and MongoDB best practices.
