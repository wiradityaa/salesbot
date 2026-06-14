"""Script to run tests and display results."""

import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "pytest", "test_log/test_analytics.py", "-v", "--tb=line"],
    cwd="e:\\salesbot",
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("STDERR:")
    print(result.stderr)

print(f"\nReturn code: {result.returncode}")
