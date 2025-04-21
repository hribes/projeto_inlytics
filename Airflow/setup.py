import os, socket

def init():
    #Ta dando errado 
    print("Iniciando banco de dados e criando administrador\n")
    os.system("docker compose run --rm airflow-init")

def comp():
    #Ta dando errado 2
    print("Criando ambiente do Airflow\n")
    os.system("docker compose up -d")

def ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def main():
    #Inicialização de banco de dados e criação de adm
    init()
    #Inicia a interface do Airflow
    comp()
    
    #Aqui é só pra flr que deu td certo e mostrar os endereços para acessar
    print(f"\nAirflow iniciado \
           \nAcesse colocando os seguintes endereços no navegador: \
           \nMesma máquina: http://localhost:9090 \
           \nOutra máquina: http://{ip()}:9090\n")


if __name__ == "__main__":
    main()
