import os
import time
import uuid
import psutil
import socketio
from datetime import datetime
from socketio.exceptions import BadNamespaceError, ConnectionError


def retry(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except (BadNamespaceError, ConnectionError) as e:
                print("Retrying connection to server")
                time.sleep(5)

    return wrapper


def get_mac_address():
    mac_num = hex(uuid.getnode()).replace("0x", "").upper()
    mac = ":".join(mac_num[i : i + 2] for i in range(0, 12, 2))
    return mac


def monitor_cpu():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage


def monitor_memory():
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    return memory_usage


@retry
def send_monitoring_data(server_url):
    sio = socketio.Client()

    @sio.event
    def connect():
        print("Connected to server")

    sio.connect(server_url, wait_timeout=10)
    try:
        while True:
            cpu_usage = monitor_cpu()
            memory_usage = monitor_memory()
            time = datetime.now()
            user = os.getenv("USER", None)
            data = {
                "time": f"{time.hour}:{time.minute}:{time.second}",
                "mac_address": get_mac_address(),
                "pc_name": user if user else psutil.users()[0].name,
                "cpu": cpu_usage,
                "memory": memory_usage,
            }
            sio.emit("stream", data)
    except KeyboardInterrupt:
        sio.disconnect()


server_url = "http://54.93.118.164:5000/"
send_monitoring_data(server_url)
