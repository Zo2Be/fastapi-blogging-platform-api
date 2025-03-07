# FastAPI Blogging Platform API

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tools & Technologies](#tools--technologies)
- [Module Descriptions](#module-descriptions)
  - [Main Application & Error Handling](#main-application--error-handling)
  - [Actions](#actions)
  - [API Endpoints](#api-endpoints)
  - [Core Modules](#core-modules)
  - [CRUD Operations](#crud-operations)
  - [Tests](#tests)
  - [Utilities](#utilities)
- [API Endpoints Details](#api-endpoints-details)
  - [Posts](#posts)

## Overview

A pet project API built with FastAPI for a blogging platform. This project demonstrates a modular, asynchronous RESTful API design with authentication, caching, and database interactions.

## Features

- **User Authentication & Management:** Registration, login, password reset, and email verification using FastAPI-Users.
- **CRUD for Posts:** Create, read, update, and delete blog posts with support for filtering, pagination, and sorting.
- **Asynchronous Operations:** Asynchronous endpoints using FastAPI and asyncpg.
- **Caching:** Redis is used to cache frequently accessed data.
- **Error Handling:** Custom error handlers for 404, 401, and 403 HTTP errors.
- **Database Migrations:** Managed with Alembic.
- **Testing:** Tests using Pytest and AsyncClient.

## Tools & Technologies

- **Python 3.12**
- **FastAPI:** Web framework for building APIs.
- **Uvicorn:** ASGI server.
- **Pydantic & Pydantic Settings:** Data validation and configuration management.
- **SQLAlchemy & asyncpg:** ORM and async database driver.
- **Alembic:** Database migrations.
- **Redis:** In-memory data store for caching.
- **FastAPI-Users:** Simplifies authentication and user management.
- **Orjson:** Fast JSON serialization.
- **Poetry:** Dependency management.
- **Docker & Docker Compose:** Containerization and service orchestration.
- **Pytest:** Testing framework.


## Module Descriptions

### Main Application & Error Handling
- **`app/main.py`**  
  Initializes the FastAPI application, sets up the lifespan events (startup and shutdown), includes all routers, and configures ORJSON as the default response serializer.

- **`app/error_handlers.py`**  
  Implements custom exception handlers for common errors (NotFound, Unauthorized, Forbidden).

### Actions
- **`app/actions/create_superuser.py`**  
  Provides a script to create a default superuser using environment variables and the FastAPI-Users framework.

### API Endpoints
- **`app/api/api_v1/auth.py`**  
  Contains routes for user authentication including login, registration, token verification, and password reset endpoints.

- **`app/api/api_v1/fastapi_users.py`**  
  Configures the FastAPI-Users instance, integrating authentication backends and user management utilities.

- **`app/api/api_v1/messages.py`**  
  Defines endpoints for retrieving public messages as well as restricted secret messages for superusers.

- **`app/api/api_v1/posts.py`**  
  Manages blog posts with endpoints for listing, retrieving, creating, updating, and deleting posts. Supports query parameters for search, pagination, and ordering.

- **`app/api/api_v1/users.py`**  
  Provides user profile endpoints, allowing users to view and update their own data.

- **Dependencies:**  
  - **`app/api/dependencies/authentication/`**  
    Includes modules to handle token access, backend configuration, and custom user management strategies.
  - **`app/api/dependencies/posts.py`**  
    Provides dependency functions to validate post existence and ownership.

### Core Modules
- **`app/core/cache.py`**  
  Sets up Redis caching
- **`app/core/config.py`**  
  Uses Pydantic Settings to manage configuration for the API, database, Redis, and token settings.
- **`app/core/constants.py`**  
  Defines common HTTP response templates for error handling.
- **`app/core/exceptions.py`**  
  Contains custom exception classes for handling not found, unauthorized, and forbidden errors.
- **`app/core/logger.py`**  
  Configures application logging to track requests and errors.
- **`app/core/authentication/`**  
  Provides the bearer transport configuration and a custom user manager for handling authentication.
- **`app/core/models/`**  
  Defines the ORM models for Users, Posts, Categories, and AccessTokens along with helper mixins.
- **`app/core/schemas/`**  
  Contains Pydantic models for request validation and response serialization for posts, users, and categories.
- **`app/core/types/`**  
  Defines custom type aliases.

### CRUD Operations
- **`app/crud/posts.py`**  
  Implements the CRUD logic for posts, including functions for fetching all posts (with search, pagination, ordering), retrieving a post by ID, creating, updating, and deleting posts. Also handles category creation and association.

### Tests
- **`app/tests/conftest.py`**  
  Sets up testing fixtures for database sessions, test users, and an asynchronous HTTP client.
- **`app/tests/test_posts.py`**  
  Contains integration tests for the posts endpoints to ensure proper behavior for creating, retrieving, updating, and deleting posts.

### Utilities
- **`app/utils/case_converter.py`**  
  Provides a helper function to convert CamelCase strings to snake_case.

## API Endpoints Details

### Posts

- **List Posts**: `GET /api/v1/posts`  
  Retrieves a list of posts.  
  **Query Parameters:**
  - `search`: Filter posts by title or category (minimum 2 characters).
  - `limit`: Number of posts per page (default 10, range 1-100).
  - `offset`: Pagination offset.
  - `order`: Sorting field (`id`, `title`, or `created_at`).

- **Get Post by ID**: `GET /api/v1/posts/{post_id}`  
  Retrieves details for a specific post.

- **Update Post**: `PATCH /api/v1/posts/{post_id}`
  Allows partial updates (e.g., title, content, category, tags).
  **Example Update:**
  ```json
  {
  "title": "Updated Post Title"
  }
  ```
  
  **Delete Post**: DELETE /api/v1/posts/{post_id}
  Deletes the specified post. Requires proper authorization (author or superuser).
  
- **Create Post**: `POST /api/v1/posts`  
  **Request Body Example:**
  ```json
  {
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "category": "Tech",
    "tags": ["fastapi", "python"]
  }
  ```
  **Response Example:**
  ``` json
  {
  "id": 1,
  "title": "My First Post",
  "content": "This is the content of my first post.",
  "category": "Tech",
  "tags": ["fastapi", "python"],
  "user": "user@example.com",
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
  }
  ```
  
