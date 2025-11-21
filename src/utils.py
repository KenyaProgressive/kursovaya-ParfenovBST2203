from src.cli import app_cli
from src.const import VARIANTS


def variant_validate(variant) -> bool:
    return isinstance(variant, int) and variant in VARIANTS


def invalid_variant_handler():
    print("Выбранной опции не существует")
    try:
        is_exit = int(input("Хотите выйти? Введите 0 или 1 (0 - Нет, 1 - да)"))
        if is_exit:
            exit()
        else:
            app_cli()
    except TypeError:
        invalid_variant_handler()
