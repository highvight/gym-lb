# Containerized Server to be pulled from Docker Hub
SERVICE_IP = "127.0.11.0"
SERVICE_PORT = 8080
SERVICE_SCHED = "wrr"
SERVICE_PROTOCOL = "tcp"

SERVER_IMAGE = "tutum/hello-world"
SERVER_SUBNET = "127.0.10."
SERVER_PORT = 8080
SERVER_N = 3

LOAD_ARGS = {
    "method": "GET",
    "duration": 5,
    "concurrency": 2,
    "headers": {},
    "quiet": False,
    "verbose": False,
    "auth": None,
    "content_type": "text/plain",
    "data": None,
    "pre_hook": None,
    "post_hook": None
}