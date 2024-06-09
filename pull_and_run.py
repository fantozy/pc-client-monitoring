import subprocess

"""
NOTE: For windows if it does not work
#!/bin/bash
docker pull fantozy/monitoring_client:latest
docker run -e USER=$(whoami) --entrypoint /app/run.sh fantozy/monitoring_client:latest
"""

def pull_and_run():
    user = subprocess.run(["whoami"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    subprocess.run(["docker", "pull", "fantozy/monitoring_client:latest"])
    subprocess.run(["docker", "run", "-e", f"USER={user}", "--entrypoint", "/app/run.sh", "fantozy/monitoring_client:latest"])


if "__main__" == __name__:
    pull_and_run()
