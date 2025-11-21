import socket
import psutil
import time
from src.const import GOOGLE_SERVER_ADDRESS, PORT, RETURN_TIME
from src.cli import app_cli

def check_internet_connection() -> None:
    conn_data = (GOOGLE_SERVER_ADDRESS, PORT)
    try:
        socket.create_connection(conn_data, timeout=3)
        print("Подлючение к интернету установлено")
    except OSError: ## Ошибки, связанные с веб-взаимодействием
        print("Подключение к интернету отсутствует")
    finally:
        time.sleep(RETURN_TIME)
        app_cli()

def check_installed_antivirus():
    ...


