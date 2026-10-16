# Lab 5: Static Code Analysis

**Program:** `school_transport.py`  
**Tools:** Pylint, Bandit, Flake8

> Line numbers refer to the original version shown in the initial reports. The supplied PDF refers to reflection questions but does not list specific questions; reflections below are general responses.

## 1. Issues Identified

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| SQL query built with f-string | Security | Original line 9; Bandit B608 | Input values were interpolated directly into SQL text, potentially allowing SQL injection. | Use placeholders (?, ?, ?, ?) and pass (student, route, stop, fee) separately. Verify this is truly fixed; the shared diff still showed f-string interpolation. |
| Subprocess called with shell=True | Security | Original line 24; Bandit B602 | A command was assembled with route input and executed through a shell, creating command-injection risk. | Prefer print() if only a status message is needed. Otherwise pass an argument list and use shell=False. |
| Use of assert for runtime validation | Reliability | Original line 38; Bandit B101 | Assertions can be disabled with optimized Python execution and should not enforce essential runtime checks. | Replace with an explicit conditional and an appropriate exception or test failure. |
| Subprocess import flagged | Security review | Original line 1; Bandit B404 | Bandit flags subprocess use as worth reviewing; the import alone is not necessarily a vulnerability. | Remove the import if unnecessary; otherwise avoid shell=True and validate external input. |
| Long lines | Style | Original lines 5 and 9; Pylint C0301 / Flake8 E501 | SQL statements exceeded configured line-length limits. | Split SQL strings across adjacent literals and format multi-line calls. |
| Missing module/function docstrings | Maintainability | Original lines 1, 8, 13, 17, 23, 27, 34; Pylint C0114/C0116 | The module and functions did not document their purpose. | Add a module docstring and concise function docstrings. |
| Function names not snake_case | Style | Original lines 8, 13, 17, 23, 27; Pylint C0103 | Names such as enrollRider and routeRoster did not follow Python naming convention. | Rename to enroll_rider, route_roster, export_roster, dispatch_alert, fee_collected, and update call sites. |
| Unused driver argument | Maintainability | Original line 13; Pylint W0613 | The driver argument was not used by routeRoster. | Remove the unused parameter and update calls. |
| File opened without explicit encoding | Reliability | Original line 18; Pylint W1514 | Text-file behaviour could vary across environments when encoding is omitted. | Specify encoding='utf-8'. |
| File not managed by context manager | Reliability | Original line 18; Pylint R1732 | Manual close() may not run if an error occurs before the close statement. | Use with open(path, 'w', encoding='utf-8') as output_file. |
| Bare except clause | Reliability | Original line 30; Pylint W0702 / Flake8 E722 | Catching every exception can hide programming errors. | Catch the specific expected exception, such as sqlite3.Error, or remove unnecessary exception handling. |
| Missing whitespace after commas | Style | Original line 8; Flake8 E231 | Function parameters lacked spaces after commas. | Add spaces after commas in signatures and expressions. |
| Insufficient blank lines | Style | Original line 23; Flake8 E302 | A top-level function did not have the required blank-line separation. | Use two blank lines between top-level definitions. |

## 2. Reflection

### What did static analysis help identify?

The tools identified style and maintainability problems such as long lines, missing docstrings, naming conventions, an unused argument, and file handling. Bandit highlighted risky SQL construction, subprocess execution, and assert usage. The reports gave specific locations to review.

### How did the tools differ?

Pylint focused on code quality and maintainability, Flake8 focused on formatting and PEP 8 rules, and Bandit focused on potentially unsafe coding patterns.

### Why rerun the tools after changes?

Rerunning checks whether the reported findings disappeared and whether edits introduced new problems. The observed Pylint score was 10.00/10 and Bandit reported no issues. The saved Flake8 after-report is empty, so it should be rerun to confirm the result.

### What are the limitations of static analysis?

A clean report does not prove the program is fully secure or correct. Static analysis can miss risky code patterns and does not replace tests or careful review. SQL values should still use parameterized queries even if a scanner reports no finding.

## 3. Verification Notes

- Pylint after-fix output showed 10.00/10.
- Bandit after-fix output reported no issues identified.
- `flake8_after.txt` was 0 bytes. Rerun Flake8 and verify the result before submission.
- The SQL INSERT must use parameterized placeholders and a separate parameter tuple. A multiline f-string query remains unsafe.
- The handout requires three commits for changes related to the three tools. Verify the LAB5 files are committed and pushed in the SE-Labs repository.
