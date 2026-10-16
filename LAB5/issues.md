# Static Analysis Issues and Fixes

## 1. Initial Findings

The original `school_transport.py` was analyzed using Pylint, Bandit, and Flake8.

| Tool | Initial findings |
|---|---|
| Pylint | 4.00/10; naming violations, missing docstrings, long lines, and resource-handling issues |
| Bandit | SQL injection risk, shell execution risk, bare exception, and assertion usage |
| Flake8 | Long lines, missing whitespace, insufficient blank lines, and bare exception |

## 2. Fixes Implemented

- Replaced string-built SQL queries with parameterized queries.
- Removed shell-based subprocess execution.
- Replaced bare exception handling with explicit fee calculation.
- Replaced the runtime assertion with explicit error handling.
- Converted function names to snake_case.
- Added module and function docstrings.
- Used context managers for database connections and file handling.
- Corrected whitespace, line lengths, and formatting.
- Preserved rider registration, roster export, dispatch, and fee calculation functionality.

## 3. Final Results

| Tool | Final result |
|---|---|
| Pylint | 10.00/10 |
| Bandit | No issues identified |
| Flake8 | No violations reported |

## 4. Conclusion

Static analysis helped identify security, maintainability, and formatting issues in the original program. The revised implementation addresses the identified issues while preserving the intended functionality.