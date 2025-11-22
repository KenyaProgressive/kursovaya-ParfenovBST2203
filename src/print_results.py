from datetime import datetime

from src.const import RESULTS_FILE_NAME


def print_results(results: str) -> None:

    if results == "":
        print("Не было произведено ни одной проверки")
        return

    try:
        in_file = int(input("Сохранить в файл? Введите цифру (0 - Нет, 1 - Да)"))
    except TypeError:
        in_file = 0

    if in_file == 1:
        write_results_to_file(results, RESULTS_FILE_NAME)
    else:
        write_results_to_cli(results)


def write_results_to_file(results: str, filename: str = RESULTS_FILE_NAME) -> None:
    with open(filename, "w") as f:
        f.write("=== РЕЗУЛЬТАТЫ РАБОТЫ ===\n")
        f.write(results)
        f.write(f"\nПроверка проведена: {pretty_time(datetime.now())}")


def write_results_to_cli(results: str) -> None:
    print("=== РЕЗУЛЬТАТЫ РАБОТЫ ===\n")
    print(results)
    print(f"Проверка проведена: {pretty_time(datetime.now())}\n")


def pretty_time(t: datetime) -> str:
    time_format: str = "%d:%m:%y %H:%M"
    return datetime.strftime(t, time_format)
