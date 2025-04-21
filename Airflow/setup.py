import os


def init():
    print("Iniciando banco de dados e criando administrador")
    os.system("docker compose run --rm airflow-init")

def comp():
    print("Criando ambiente do Airflow")
    os.system("docker compose up -d")

def main():
    init()
    comp()
    print("")


if __name__ == "__main__":
    main()
