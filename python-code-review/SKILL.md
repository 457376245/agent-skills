---
name: python-code-review
description: Systematic code review for Python projects covering type safety, exception handling, Pythonic idioms, mutable defaults, security, concurrency, and performance. Use when user says "review code", "check this PR", "code review", or before merging changes in Python projects.
---

# Python Code Review Skill

Systematic code review checklist for Python projects (3.10+).

## Review Strategy

1. **Quick scan** - Understand intent, identify scope
2. **Checklist pass** - Go through each category below
3. **Summary** - List findings by severity (Critical -> Minor)

## Output Format

```markdown
## Code Review: [file/feature name]

### Critical
- [Issue description + line reference + suggestion]

### Improvements
- [Suggestion + rationale]

### Minor/Style
- [Nitpicks, optional improvements]

### Good Practices Observed
- [Positive feedback]
```

---

## Review Checklist

### 1. None Safety & Type Hints

**Check for:**
```python
# Bad: unguarded attribute access on possibly-None value
def greet(user: User | None) -> str:
    return user.name.upper()  # AttributeError if None

# Good: guard or narrow
def greet(user: User | None) -> str:
    if user is None:
        return "Anonymous"
    return user.name.upper()

# Bad: type: ignore without explanation
result = some_call()  # type: ignore

# Good: explain suppression
result = some_call()  # type: ignore[return-value]  # checked at runtime

# Bad: using Optional incorrectly in mutable containers
def process(items: list[str] | None = None) -> None: ...

# Good: use sentinel pattern or overloads for clarity
def process(items: list[str] | None = None) -> None:
    items = items if items is not None else []
```

**Flags:**
- Missing type hints on public function signatures
- Chained attribute access without None checks
- Blanket `# type: ignore` without error code or comment
- Using `Any` where a more specific type exists
- `isinstance` checks that could be replaced by structural typing / Protocol

**Suggest:**
- Enable `mypy --strict` or `pyright` in CI
- Use `X | None` (3.10+) over `Optional[X]`
- Use `TypeGuard` for custom narrowing functions

### 2. Exception Handling

**Check for:**
```python
# Bad: bare except
try:
    process()
except:
    pass

# Bad: broad except that swallows everything
try:
    process()
except Exception:
    pass

# Bad: losing traceback
try:
    process()
except ValueError as e:
    raise RuntimeError(str(e))

# Good: chain exceptions
try:
    process()
except ValueError as e:
    raise RuntimeError("Processing failed") from e

# Good: specific handling with logging
try:
    process()
except (ConnectionError, TimeoutError) as e:
    logger.exception("Network call failed")
    raise
```

**Flags:**
- Bare `except:` or `except Exception:` with `pass`
- `raise` new exception without `from e` (loses traceback)
- Using exceptions for control flow (`StopIteration` outside iterators)
- Catching and silently logging without re-raising when failure matters
- `except BaseException` (catches `KeyboardInterrupt`, `SystemExit`)

**Suggest:**
- Always chain with `from e` or `from None` (intentional suppression)
- Use `logger.exception()` to include traceback automatically
- Create domain-specific exception hierarchies for libraries
- Use `contextlib.suppress()` for intentional ignore of specific exceptions

### 3. Mutable Default Arguments

**Check for:**
```python
# Bad: mutable default - shared across calls
def append_to(item, target=[]):
    target.append(item)
    return target

# Good: use None sentinel
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target

# Bad: mutable class attribute shared across instances
class Config:
    options = {}  # shared between ALL instances

# Good: initialize in __init__
class Config:
    def __init__(self):
        self.options = {}

# Bad: mutable default in dataclass
@dataclass
class Job:
    tags: list[str] = []  # ValueError at definition time (3.x)

# Good: use field(default_factory=...)
@dataclass
class Job:
    tags: list[str] = field(default_factory=list)
```

**Flags:**
- `def f(x=[])`, `def f(x={})`, `def f(x=set())` in signatures
- Mutable class-level attributes intended as instance state
- Dataclass fields with mutable defaults without `field(default_factory=...)`

### 4. Resource Management

**Check for:**
```python
# Bad: manual open/close
f = open("data.txt")
data = f.read()
f.close()  # skipped if read() raises

# Good: context manager
with open("data.txt") as f:
    data = f.read()

# Bad: manual resource cleanup
conn = get_connection()
try:
    cursor = conn.cursor()
    cursor.execute(query)
finally:
    conn.close()

# Good: context manager or contextlib
with get_connection() as conn:
    conn.execute(query)

# Bad: suppressing close errors
try:
    resource.close()
except Exception:
    pass

# Good: implement __enter__/__exit__ or use contextlib.closing
from contextlib import closing
with closing(legacy_resource()) as r:
    r.do_work()
```

**Flags:**
- `open()` without `with` statement
- Manual `try/finally` for cleanup that could use a context manager
- Missing `__enter__`/`__exit__` on classes that manage resources
- Database connections, sockets, temp files not using context managers

**Suggest:**
- Use `contextlib.contextmanager` for simple resource wrappers
- Use `contextlib.ExitStack` for dynamic/multiple resource management
- Use `tempfile.NamedTemporaryFile` / `TemporaryDirectory` as context managers

### 5. Pythonic Idioms

**Check for:**
```python
# Bad: C-style loop
for i in range(len(items)):
    print(items[i])

# Good: direct iteration
for item in items:
    print(item)

# Good: when index is needed
for i, item in enumerate(items):
    print(i, item)

# Bad: manual dict construction from two lists
d = {}
for i in range(len(keys)):
    d[keys[i]] = values[i]

# Good
d = dict(zip(keys, values))

# Bad: checking key existence then accessing
if key in d:
    val = d[key]
else:
    val = default

# Good
val = d.get(key, default)

# Bad: unnecessary list() in iteration context
for x in list(some_generator()):
    process(x)

# Good: iterate generator directly
for x in some_generator():
    process(x)

# Bad: string formatting with + or %
msg = "Hello " + name + ", you are " + str(age)

# Good: f-string
msg = f"Hello {name}, you are {age}"

# Bad: manual swap
temp = a
a = b
b = temp

# Good: tuple unpacking
a, b = b, a

# Bad: checking boolean value explicitly
if flag == True:
if len(items) > 0:

# Good: truthy/falsy
if flag:
if items:
```

**Flags:**
- `range(len(...))` without needing index for mutations
- Manual dict building that could use comprehension or `dict(zip(...))`
- `list()` wrapping generators when only iterating
- `%` formatting or `+` concatenation over f-strings
- `if x == True`, `if x == None` instead of `if x:`, `if x is None`
- `if len(x) > 0` instead of `if x:`
- Not using unpacking, `*args` spread, or walrus operator where beneficial

### 6. Data Modeling & API Design

**Check for:**
```python
# Bad: passing dicts everywhere
def create_user(data: dict) -> dict:
    return {"id": 1, "name": data["name"]}

# Good: use dataclasses or Pydantic models
@dataclass
class User:
    id: int
    name: str

# Bad: too many positional parameters
def send_email(to, subject, body, cc, bcc, reply_to, headers):
    ...

# Good: use keyword-only args or a config object
def send_email(
    to: str,
    subject: str,
    body: str,
    *,
    cc: str | None = None,
    bcc: str | None = None,
    reply_to: str | None = None,
) -> None: ...

# Bad: boolean flags that change behavior
def process(data, fast=False, validate=True, strict=False):
    ...

# Good: use Enum or Literal
class Mode(StrEnum):
    FAST = "fast"
    STRICT = "strict"

def process(data, mode: Mode = Mode.STRICT) -> None: ...

# Bad: returning different types based on flags
def fetch(id: int, as_dict: bool = False):
    ...

# Good: separate functions or overloads
def fetch(id: int) -> User: ...
def fetch_as_dict(id: int) -> dict: ...
```

**Flags:**
- Passing raw dicts where a dataclass/Pydantic model would add safety
- Functions with > 3 positional params (use keyword-only `*`)
- Boolean flags that change return type or behavior significantly
- Missing `__repr__`/`__str__` on domain objects
- Using plain tuples for structured data instead of `NamedTuple` / `dataclass`
- Not using `Enum` / `StrEnum` for fixed choice sets

### 7. Import & Module Hygiene

**Check for:**
```python
# Bad: star import
from os.path import *

# Bad: import side effects at module level
import heavy_module  # triggers expensive initialization

# Bad: circular import at module level
# a.py
from b import helper  # b.py also imports from a

# Good: defer import to function body when circular
def process():
    from b import helper
    return helper()
```

**Flags:**
- `from x import *` (pollutes namespace, hides origin)
- Unused imports (should be caught by linter / `ruff`)
- Circular imports causing `ImportError`
- Heavy imports at top of frequently-imported modules (lazy-import where needed)
- Relative imports that escape the package (`from ... import ...`)

**Suggest:**
- Use `ruff` or `isort` for consistent import ordering
- Group: stdlib -> third-party -> local, separated by blank lines
- Use `TYPE_CHECKING` block for import-only-for-type-hints to break cycles

### 8. Concurrency & Async

**Check for:**
```python
# Bad: shared mutable state across threads without lock
cache = {}

def update_cache(key, value):
    cache[key] = value  # race condition with readers

# Good: use threading.Lock
_lock = threading.Lock()
cache = {}

def update_cache(key, value):
    with _lock:
        cache[key] = value

# Bad: blocking I/O in async context
async def fetch_data():
    data = requests.get(url)  # blocks the event loop!

# Good: use async HTTP client
async def fetch_data():
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

# Bad: creating threads for CPU-bound work
threads = [Thread(target=cpu_heavy, args=(chunk,)) for chunk in chunks]

# Good: use ProcessPoolExecutor for CPU-bound
with ProcessPoolExecutor() as pool:
    results = pool.map(cpu_heavy, chunks)

# Bad: fire-and-forget tasks
asyncio.create_task(some_work())  # exception silently lost

# Good: store reference and handle errors
task = asyncio.create_task(some_work())
task.add_done_callback(handle_task_result)
```

**Flags:**
- Shared mutable state across threads without locks
- Blocking I/O calls (`requests`, `open`, `time.sleep`) inside `async def`
- Using `threading` for CPU-bound work (GIL limits parallelism)
- Fire-and-forget `asyncio.create_task()` without error handling
- Mixing sync and async code without `asyncio.to_thread()` or `run_in_executor()`
- Missing `async with` / `async for` for async context managers / iterators

### 9. Security

**Check for:**
```python
# Bad: eval/exec on user input
result = eval(user_input)

# Bad: shell injection
import subprocess
subprocess.run(f"echo {user_input}", shell=True)

# Good: use list form
subprocess.run(["echo", user_input])

# Bad: pickle untrusted data
data = pickle.loads(untrusted_bytes)

# Bad: SQL string formatting
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Good: parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Bad: hardcoded secrets
API_KEY = "sk-abc123..."

# Good: environment or secrets manager
API_KEY = os.environ["API_KEY"]

# Bad: path traversal
filepath = os.path.join(upload_dir, user_filename)

# Good: validate resolved path
filepath = os.path.join(upload_dir, user_filename)
if not os.path.realpath(filepath).startswith(os.path.realpath(upload_dir)):
    raise ValueError("Invalid path")
```

**Flags:**
- `eval()`, `exec()`, `compile()` on external input
- `subprocess` with `shell=True` and string interpolation
- `pickle.loads()` / `yaml.load()` (without `Loader=SafeLoader`) on untrusted data
- SQL queries built with f-strings or `%` formatting
- Hardcoded credentials, API keys, tokens
- Path traversal: user input in file paths without validation
- `os.system()` usage (prefer `subprocess.run`)
- Disabled SSL verification (`verify=False`)

### 10. Performance Considerations

**Check for:**
```python
# Bad: repeated list search
if item in large_list:  # O(n) each time

# Good: use set for membership testing
item_set = set(large_list)
if item in item_set:  # O(1)

# Bad: building list just to get length
count = len([x for x in items if x.is_active()])

# Good: use sum with generator
count = sum(1 for x in items if x.is_active())

# Bad: loading entire large file into memory
data = open("huge.csv").read()

# Good: stream line by line
with open("huge.csv") as f:
    for line in f:
        process(line)

# Bad: repeated attribute lookup in hot loop
for item in large_collection:
    result.append(item.lower().strip())

# Good: local reference
lower = str.lower
strip = str.strip
for item in large_collection:
    result.append(strip(lower(item)))

# Bad: creating intermediate lists unnecessarily
result = list(filter(lambda x: x > 0, map(lambda x: x * 2, items)))

# Good: generator expression
result = [x * 2 for x in items if x * 2 > 0]

# Bad: N+1 queries in ORM loops (Django/SQLAlchemy)
for order in Order.objects.all():
    print(order.customer.name)  # extra query per order

# Good: prefetch/joinedload
for order in Order.objects.select_related("customer").all():
    print(order.customer.name)
```

**Flags:**
- `in` membership test on `list` in loops (use `set` or `dict`)
- List comprehension where generator expression suffices (especially with `sum`, `any`, `all`, `min`, `max`)
- Loading entire file into memory when streaming is possible
- N+1 query patterns with Django `select_related`/`prefetch_related` or SQLAlchemy `joinedload`
- Repeated expensive computation without `functools.lru_cache` / `functools.cache`
- Concatenating strings in loops instead of `"".join()`
- Using `+` to build large lists instead of `.extend()`

### 11. Testing Practices

**Suggest tests for:**
- None / empty inputs
- Boundary values and edge cases
- Exception paths (use `pytest.raises`)
- Parametrized cases (`@pytest.mark.parametrize`)
- Side effects are isolated (use `unittest.mock.patch` or `monkeypatch`)

**Flags:**
- Tests that depend on external services without mocking
- Missing `conftest.py` fixtures for shared setup
- `assert True` or no assertions in test body
- Overly broad assertions (`assert result is not None` without checking value)
- Test function names that don't describe the scenario
- Using `unittest.TestCase` style in a pytest-only project (mixing styles)

---

## Severity Guidelines

| Severity | Criteria |
|----------|----------|
| **Critical** | Security vulnerability, data loss risk, production crash |
| **High** | Bug likely, significant performance issue, breaks API contract |
| **Medium** | Code smell, maintainability issue, missing best practice |
| **Low** | Style, minor optimization, suggestion |

## Token Optimization

- Focus on changed lines (use `git diff`)
- Group similar findings instead of repeating
- Reference line numbers, not full code quotes
- Skip auto-generated files, migrations, and test fixtures

## Quick Reference Card

| Category | Key Checks |
|----------|------------|
| None Safety | Unguarded access, missing type hints, blanket type: ignore |
| Exceptions | Bare except, lost traceback, missing `from e` |
| Mutable Defaults | `def f(x=[])`, mutable class attrs, dataclass defaults |
| Resources | `open()` without `with`, manual cleanup |
| Idioms | range(len), f-strings, truthiness, unpacking |
| API Design | Raw dicts vs dataclass, boolean flags, keyword-only args |
| Imports | Star imports, circular deps, unused imports |
| Concurrency | Blocking in async, GIL-bound threads, unguarded state |
| Security | eval, shell=True, pickle, SQL injection, hardcoded secrets |
| Performance | list vs set lookup, generators, N+1 queries, join vs + |
