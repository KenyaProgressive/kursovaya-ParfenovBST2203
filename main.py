from src.cli import app_cli
from src.decision_handler import decision_handler


def main():
    variant: int = -1

    while variant != 0:
        app_cli()
        variant = int(input("Введите опцию из списка: "))
        print()
        decision_handler(variant)


if __name__ == "__main__":
    main()
