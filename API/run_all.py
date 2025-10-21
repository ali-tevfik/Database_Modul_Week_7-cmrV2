import subprocess
import sys


arg = sys.argv[1] if len(sys.argv) > 1 else None

if arg == "2":
    print("2")
    apis = [
        ("main", 8000),
        ]

else:
    print("1")
    apis = [
        ("views.MentorApi", 8000),
        ("views.LoginApi", 8001),
        ("views.InterviewsApi", 8002)
    ]

processes = []

for module, port in apis:
    cmd = ["python", "-m", "uvicorn", f"{module}:app", "--reload", "--port", str(port)]
    p = subprocess.Popen(cmd)
    processes.append(p)

for p in processes:
    p.wait()
