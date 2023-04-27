import sys


def init_health_check(name: str) -> None:
    with open(f"{name}.txt", "w") as file:
        file.write("healthy")


def set_unhealthy(name: str) -> None:
    with open(f"{name}.txt", "w") as file:
        file.write("unhealthy")


def check_health(name: str) -> None:
    print(name)
    with open(f"{name}.txt", "r") as file:
        if file.read() == "unhealthy":
            sys.exit(1)


if __name__ == "__main__":
    check_health(sys.argv[1])
