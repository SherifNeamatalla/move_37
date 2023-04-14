import os

from src.config.env_loader import load_env
from src.runners.python_app_runner import PythonAppRunner


def main():
    load_env()
    runner = PythonAppRunner()
    runner.run()


if __name__ == "__main__":
    main()
