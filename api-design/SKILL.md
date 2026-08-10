---
name: api-design
description: Spring Boot REST API design rules and implementation guidance
license: MIT
---

# API Design Skill

Use this skill when designing, implementing, or reviewing Spring Boot REST APIs.

## When to Use

- Creating new REST endpoints in Spring Boot
- Refactoring existing controller contracts
- Reviewing API consistency and maintainability
- Defining request and response DTOs
- Writing or updating OpenAPI documentation

## Scope

This skill is for Spring Boot REST APIs.

- Default stack: `spring-boot-starter-web`, `spring-boot-starter-validation`, `spring-boot-starter-security`, `springdoc-openapi`
- Default style: resource-oriented REST APIs
- Not covered: GraphQL, gRPC, event-driven APIs

## Core Rules

### 1. Design URLs Around Resources

Use plural nouns for resources and standard HTTP methods for CRUD.

```text
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
PATCH  /api/v1/users/{id}
DELETE /api/v1/users/{id}
```

Use nested resources only for clear ownership or relationships.

```text
GET  /api/v1/users/{id}/orders
POST /api/v1/users/{id}/orders
```

Use action endpoints only when CRUD does not fit.

```text
POST /api/v1/orders/{id}/cancel
POST /api/v1/users/{id}/activate
```

Avoid RPC-style paths:

- `/getUserById`
- `/createUser`
- `/queryUserList`
- `/updateUserStatus`

### 2. Keep Controllers Thin

Controllers should only handle HTTP concerns:

- request binding
- validation triggering
- calling services
- building response entities

Do not put these in controllers:

- business orchestration
- repository queries
- transaction management
- repeated try/catch response mapping

### 3. Always Use DTOs at the API Boundary

Do not expose JPA entities directly from controllers.

Use:

- request DTOs for incoming payloads
- response DTOs for outgoing payloads
- entities only inside service or repository layers

This prevents:

- leaking internal fields
- lazy-loading surprises
- tight coupling between DB structure and API contract

### 4. Validate All External Input

Validate `@RequestBody`, query params, and path params explicitly.

Rules:

- put `@Validated` on controller classes when needed
- use `@Valid` on request bodies
- use Bean Validation annotations on DTO fields
- reject invalid data before it reaches business logic

Example:

```java
public record CreateUserRequest(
        @NotBlank @Size(max = 100) String name,
        @NotBlank @Email String email,
        @NotBlank @Size(min = 8, max = 64) String password
) {}
```

```java
@RestController
@RequestMapping("/api/v1/users")
@Validated
public class UserController {

    @PostMapping
    public ResponseEntity<ApiResponse<UserResponse>> create(
            @Valid @RequestBody CreateUserRequest request) {
        UserResponse response = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success(response));
    }
}
```

### 5. Make HTTP Semantics Match the Behavior

Use methods and status codes consistently.

| Method | Meaning | Success |
|--------|---------|---------|
| GET | Read | 200 |
| POST | Create | 201 |
| PUT | Replace | 200 |
| PATCH | Partial update | 200 |
| DELETE | Remove | 204 |

Common errors:

- `400` or `422` for invalid input
- `401` for unauthenticated
- `403` for forbidden
- `404` for missing resource
- `409` for conflict

Pick one rule for validation failures and use it consistently across the project.

### 6. Standardize the Response Shape

Do not let each endpoint invent its own response format.

Recommended success shape:

```json
{
  "data": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
  },
  "meta": {
    "requestId": "req-123"
  }
}
```

Recommended error shape:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "must be a well-formed email address"
      }
    ]
  },
  "meta": {
    "requestId": "req-123"
  }
}
```

Suggested wrapper classes:

```java
public record ApiResponse<T>(
        T data,
        Meta meta
) {
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(data, new Meta(null));
    }
}

public record ApiErrorResponse(
        ErrorBody error,
        Meta meta
) {}

public record ErrorBody(
        String code,
        String message,
        List<ErrorDetail> details
) {}

public record ErrorDetail(
        String field,
        String message
) {}

public record Meta(
        String requestId
) {}
```

### 7. Centralize Exception Handling

Do not build error responses in every controller method.

Use `@RestControllerAdvice` for:

- validation failures
- request parsing failures
- not-found cases
- business exceptions
- fallback unexpected errors

Example:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        List<ErrorDetail> details = ex.getBindingResult()
                .getFieldErrors()
                .stream()
                .map(error -> new ErrorDetail(error.getField(), error.getDefaultMessage()))
                .toList();

        ApiErrorResponse response = new ApiErrorResponse(
                new ErrorBody("VALIDATION_ERROR", "Validation failed", details),
                new Meta(null)
        );
        return ResponseEntity.badRequest().body(response);
    }

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ApiErrorResponse> handleNotFound(NotFoundException ex) {
        ApiErrorResponse response = new ApiErrorResponse(
                new ErrorBody("NOT_FOUND", ex.getMessage(), List.of()),
                new Meta(null)
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
    }
}
```

### 8. Keep Pagination, Filtering, and Sorting Predictable

Use one parameter convention across the project.

Recommended query parameters:

- `page`
- `size`
- `sort`
- direct filter fields like `status`, `type`, `createdFrom`

Example:

```text
GET /api/v1/users?page=0&size=20&sort=createdAt,desc&status=ACTIVE
```

Recommended paged response:

```json
{
  "data": [],
  "meta": {
    "pagination": {
      "page": 0,
      "size": 20,
      "totalElements": 135,
      "totalPages": 7
    }
  }
}
```

Do not expose framework-specific pagination objects directly if they make the contract unstable.

### 9. Version the API Explicitly

Prefer URL versioning:

```text
/api/v1/users
/api/v2/users
```

For Spring Boot, make the version visible in `@RequestMapping`.

Do not hide breaking changes inside the same versioned endpoint.

### 10. Separate Authentication from Authorization

Design APIs with both concerns in mind.

- authentication answers "who are you"
- authorization answers "what can you do"

Rules:

- return `401` when the caller is not authenticated
- return `403` when the caller is authenticated but lacks permission
- keep authorization checks explicit in service or security configuration

### 11. Treat OpenAPI as Part of the Contract

Document each public endpoint with:

- purpose
- parameters
- request body
- response body
- error cases
- authentication requirements

Preferred tool:

- `springdoc-openapi`

### 12. Use Stable Naming

Rules:

- URL paths use lowercase
- JSON fields use `camelCase`
- time fields use names like `createdAt`, `updatedAt`
- identifiers use `id`, `userId`, `orderId`
- boolean fields use clear names like `enabled`, `deleted`

Avoid switching naming styles between endpoints.

### 13. Do Not Leak Infrastructure Details

Avoid:

- returning entities directly
- exposing DB column naming or internal codes
- returning stack traces to clients
- exposing raw JPA `Page` structures as public contracts

The API contract should represent business semantics, not persistence internals.

### 14. Preserve Backward Compatibility

Treat these as breaking changes:

- removing fields
- changing field types
- changing field meaning
- changing error code semantics
- changing pagination behavior

If a breaking change is necessary:

- prefer a new version
- avoid silent behavior changes

## Recommended Package Structure

Use a simple, predictable structure:

- `controller`
- `service`
- `repository`
- `dto.request`
- `dto.response`
- `exception`
- `config`

## Example Controller

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<UserResponse>> getById(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.success(userService.getById(id)));
    }

    @PostMapping
    public ResponseEntity<ApiResponse<UserResponse>> create(
            @Valid @RequestBody CreateUserRequest request) {
        UserResponse response = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success(response));
    }

    @PatchMapping("/{id}")
    public ResponseEntity<ApiResponse<UserResponse>> update(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        return ResponseEntity.ok(ApiResponse.success(userService.update(id, request)));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

## Review Checklist

### Resource Design

- [ ] URLs use plural resource names
- [ ] Paths are resource-oriented, not RPC-style
- [ ] Nested resources are used only when the relationship is clear

### Controller Design

- [ ] Controllers only handle HTTP concerns
- [ ] Entities are not exposed directly
- [ ] Request and response DTOs are explicit

### Validation and Errors

- [ ] All external input is validated
- [ ] Validation errors are returned consistently
- [ ] Exception handling is centralized
- [ ] Business errors use stable error codes

### HTTP Contract

- [ ] HTTP methods match behavior
- [ ] Status codes are consistent
- [ ] Response envelopes are consistent
- [ ] Pagination parameters and response metadata are standardized

### Security and Versioning

- [ ] Authentication is enforced where required
- [ ] Authorization is explicit
- [ ] API version is visible in the URL
- [ ] Breaking changes are not introduced silently

### Documentation

- [ ] OpenAPI documentation matches the implementation
- [ ] Request and response examples are clear
- [ ] Error responses are documented
- [ ] Authentication requirements are documented

## Default Recommendation

When the codebase has no prior convention, prefer this baseline:

1. resource-oriented URLs under `/api/v1`
2. DTOs at the API boundary
3. Bean Validation for all external input
4. `@RestControllerAdvice` for unified error handling
5. a single response envelope for success and failure
6. Spring Security for authentication and authorization
7. `springdoc-openapi` for documentation

Keep the implementation simple. Standardize the contract first, then optimize only where the project actually needs it.
