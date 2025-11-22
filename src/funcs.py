import os
import platform
import shutil
import socket
import subprocess
import tempfile
import time

import psutil
from requests import RequestException
from requests import get as GET

from src.const import (
    ANTIVIRUS_LIST,
    EICAR_STRING,
    GOOGLE_SERVER_ADDRESS,
    PORT,
    RETURN_TIME,
    URL_FOR_CHECK_WORK_FIREWALL,
    WINDOWS_FIREWALL_PROFILES_RUS_ENG,
    WMI_NAMESPACE,
)


def check_internet_connection() -> str:

    res: str = ""
    conn_data = (GOOGLE_SERVER_ADDRESS, PORT)
    try:
        socket.create_connection(conn_data, timeout=3)
        res += "Подлючение к интернету установлено\n"
        print("Подлючение к интернету установлено\n")
    except OSError as e:  ## Ошибки, связанные с веб-взаимодействием
        res += f"Подключение к интернету отсутствует. Ошибка: {e}\n"
        print(f"Подключение к интернету отсутствует. Ошибка: {e}\n")
    finally:
        time.sleep(RETURN_TIME)

    return res


def check_installed_antivirus() -> str:
    res: str = ""

    if platform.system() == "Windows":
        import wmi

        av_list = []
        data = wmi.WMI(namespace=WMI_NAMESPACE)
        for av in data.AntiVirusProduct():
            av_list.append(av.displayName)

        if not av_list:
            res += "Антивирус не установлен в системе\n"
            print("Антивирус не установлен в системе\n")
            time.sleep(RETURN_TIME)
            return res

        res += f"Установленные антивирусы: {av_list}"
        print("Установленные антивирусы:", av_list)
        return res

    elif platform.system() == "Linux":
        av_list = []
        for av in ANTIVIRUS_LIST:
            result = subprocess.run(["dpkg", "-l", av], capture_output=True, text=True)
            if result.stdout:
                av_list.append(av)

        if not av_list:
            res += "Антивирус не установлен в системе\n"
            print("Антивирус не установлен в системе")
            time.sleep(RETURN_TIME)
            return res

        res += f"Установленные антивирусы: {av_list}\n"
        print("Установленные антивирусы:", av_list)
        return res


def check_installed_firewall() -> str:

    res: str = ""

    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"],
                capture_output=True,
                text=True,
                encoding="cp866"
            )

            output = result.stdout.lower()

            if any(profile in output for profile in WINDOWS_FIREWALL_PROFILES_RUS_ENG):
                res += "Файервол установлен в системе\n"
                print("Файервол установлен в системе")
                return res

            res += "Файервол не установлен в системе\n"
            print("Файервол не установлен в системе")
            return res

        except Exception as e:
            res += f"Ошибка при проверке наличия файервола -- {e}\n"
            print(f"Ошибка при проверке наличия файервола -- {e}")
            return res

    elif platform.system() == "Linux":
        try:
            if shutil.which("ufw") or shutil.which("iptables") or shutil.which("nft"):
                res += "Файервол установлен в системе\n"
                print("Файервол установлен в системе")
            else:
                res += "Файервол не установен в системе\n"
                print("Файервол не установен в системе")
            time.sleep(RETURN_TIME)
            return res
        except Exception as e:
            res += f"Ошибка при проверке наличия файервола -- {e}\n"
            print(f"Ошибка при проверке наличия файервола -- {e}")
            return res


def check_work_antivirus(before_check: int = 5) -> str:
    res: str = ""

    test_file: str = "virus.txt"

    with open(test_file, "w") as file:
        file.write(EICAR_STRING)

    time.sleep(before_check)

    if not os.path.exists(test_file):
        res += "Антивирус работает корректно\n"
        print("Антивирус работает корректно")
        time.sleep(RETURN_TIME)
        return res

    os.remove(test_file)
    res += "Антивирус не работает\n"
    print("Антивирус не работает")
    time.sleep(RETURN_TIME)
    return res


def check_work_firewall() -> str:
    res: str = ""
    try:
        r = GET(URL_FOR_CHECK_WORK_FIREWALL, timeout=3)
        res += "Файервол не работает (ресурс доступен)\n"
        print("Файервол не работает (ресурс доступен)")
    except RequestException:
        res += "Файервол работает (доступ к ресурсу заблокирован)\n"
        print("Файервол работает (доступ к ресурсу заблокирован)")

    time.sleep(RETURN_TIME)
    return res
