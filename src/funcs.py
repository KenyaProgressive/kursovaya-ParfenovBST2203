import os
import platform
import shutil
import socket
import subprocess
import tempfile
import time

import psutil
import wmi

from src.const import (
    ANTIVIRUS_LIST,
    EICAR_STRING,
    GOOGLE_SERVER_ADDRESS,
    PORT,
    RETURN_TIME,
    WINDOWS_FIREWALL_PROFILES_RUS_ENG,
    WMI_NAMESPACE,
    URL_FOR_CHECK_WORK_FIREWALL,
)

from requests import get as GET
from requests import RequestException


def check_internet_connection() -> None:
    conn_data = (GOOGLE_SERVER_ADDRESS, PORT)
    try:
        socket.create_connection(conn_data, timeout=3)
        print("Подлючение к интернету установлено")
    except OSError:  ## Ошибки, связанные с веб-взаимодействием
        print("Подключение к интернету отсутствует")
    finally:
        time.sleep(RETURN_TIME)

    return


def check_installed_antivirus() -> None:
    ## Случай 1. Антивирус -- активный процесс

    for process in psutil.process_iter(["name"]):
        name = process.info["name"].lower()
        if any(av_process_name_part in name for av_process_name_part in ANTIVIRUS_LIST):
            print(
                f"Антивирус {process.info["name"]} установлен и находится во включенном состоянии"
            )
            time.sleep(RETURN_TIME)
            return

    ## Случай 2. Антивирус не включён. Проверка на нахождение в системе

    if platform.system() == "Windows":

        av_list = []
        data = wmi.WMI(name=WMI_NAMESPACE)
        for av_name in data.AntiVirusProduct():
            av_list.append(av_name)

        if not av_list:
            print("Антивирус не установлен в системе")
            time.sleep(RETURN_TIME)
            return

        print("Установленные антивирусы:" * av_list)

    elif platform.system() == "Linux":
        av_list = []
        for av in ANTIVIRUS_LIST:
            res = subprocess.run(["dpkg", "-l", av], capture_output=True, text=True)
            if res.stdout:
                av_list.append(av)

        if not av_list:
            print("Антивирус не установлен в системе")
            time.sleep(RETURN_TIME)
            return

        print("Установленные антивирусы:" * av_list)


def check_installed_firewall() -> None:
    if platform.system() == "Windows":
        try:
            res = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"],
                capture_output=True,
                text=True,
            )

            output = res.stdout.lower()

            if any(profile in output for profile in WINDOWS_FIREWALL_PROFILES_RUS_ENG):
                print("Файервол установлен в системе")
                return

            print("Файервол не установлен в системе")

        except Exception as e:
            print(f"Ошибка при проверке наличия файервола -- {e}")
            return

    elif platform.system() == "Linux":
        try:
            if shutil.which("ufw") or shutil.which("iptables") or shutil.which("nft"):
                print("Файервол установлен в системе")
            else:
                print("Файервол не установен в системе")
            time.sleep(RETURN_TIME)
            return
        except Exception as e:
            print(f"Ошибка при проверке наличия файервола -- {e}")
            return


def check_work_antivirus(before_check: int = 3) -> None:
    test_file = os.path.join(tempfile.gettempdir(), "test_file.txt")

    with open(test_file, "w") as file:
        file.write(EICAR_STRING)

    time.sleep(before_check)

    if not os.path.exists(test_file):
        print("Антивирус работает корректно")
        time.sleep(RETURN_TIME)
        return

    os.remove(test_file)
    print("Антивирус не работает")
    time.sleep(RETURN_TIME)


def check_work_firewall() -> None:
    try:
        r = GET(URL_FOR_CHECK_WORK_FIREWALL)
        if 200 <= r.status_code < 300:
            print("Файервол не работает (ресурс доступен)")
    except RequestException:
        print("Файервол работает (доступ к ресурсу заблокирован)")

    time.sleep(RETURN_TIME)
