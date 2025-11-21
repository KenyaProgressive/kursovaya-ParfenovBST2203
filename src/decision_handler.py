from src.utils import variant_validate
from src.utils import invalid_variant_handler
from src.cli import app_cli
from src.funcs import (
    check_internet_connection,
    check_installed_antivirus
)

def decision_handler(variant: int) -> None:
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
            ...
        case 4:
            ...
        case 5:
            ...
        case _:
            invalid_variant_handler()
