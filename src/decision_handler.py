import time

from src.cli import app_cli
from src.const import RETURN_TIME
from src.funcs import (
    check_installed_antivirus,
    check_installed_firewall,
    check_internet_connection,
    check_work_antivirus,
    check_work_firewall,
)
from src.print_results import print_results
from src.utils import invalid_variant_handler, variant_validate

check_results: str = ""  ## TODO: Сохранение сюда всех результатов и вывод их.


def decision_handler(variant: int) -> None:

    global check_results

    if not variant_validate:
        invalid_variant_handler()
        return
    match variant:
        case 0:
            exit("Программа завершена")
        case 1:
            check_results += check_internet_connection()
        case 2:
            check_results += check_installed_firewall()
        case 3:
            check_results += check_work_firewall()
        case 4:
            check_results += check_installed_antivirus()
        case 5:
            check_results += check_work_antivirus()
        case 6:
            print_results(check_results)
            time.sleep(RETURN_TIME)
        case _:
            invalid_variant_handler()
