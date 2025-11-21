import time
from src.cli import app_cli
from src.funcs import (
    check_installed_antivirus,
    check_installed_firewall,
    check_internet_connection,
    check_work_antivirus,
    check_work_firewall
)
from src.utils import invalid_variant_handler, variant_validate
from src.const import RETURN_TIME


def decision_handler(variant: int) -> None:
    check_results = "" ## TODO: Сохранение сюда всех результатов и вывод их.
    if not variant_validate:
        invalid_variant_handler()
        return
    match variant:
        case 0:
            exit(0)
        case 1:
            check_internet_connection()
            app_cli()
        case 2:
            check_installed_antivirus()
            app_cli()
        case 3:
            check_installed_firewall()
            app_cli()
        case 4:
            check_work_antivirus()
            app_cli()
        case 5:
            check_work_firewall()
            app_cli()
        case 6:
            print(check_results)
            time.sleep(RETURN_TIME)
            app_cli()
        case _:
            invalid_variant_handler()
