import subprocess
import sys


arg = sys.argv[1] if len(sys.argv) > 1 else None
apis = [
        ("main", 8000),
        ]


processes = []

for module, port in apis:
    cmd = ["python", "-m", "uvicorn", f"{module}:app", "--reload", "--port", str(port)]
    p = subprocess.Popen(cmd)
    processes.append(p)

for p in processes:
    p.wait()
