from src.cli import app_cli
from src.decision_handler import decision_handler


def main():
    app_cli()
    variant = input("Введите опцию из списка: ")
    decision_handler(variant)

if __name__ == "__main__":
    main()