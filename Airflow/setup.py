import os, socket
import subprocess as sub

def init():
    #Ta dando errado 
    print("Iniciando banco de dados e criando administrador\n")
    db = sub.run(args=["docker", "compose", "run", "--rm", "db"], capture_output=True, text=True)

    print(db)
    #Talvez colocar o path para ele saber onde tem que trabalhar???
    ini = sub.run(args=["docker", "compose", "run", "--rm", "airflow-init"], capture_output=True, text=True)

    if ini.returncode == 0:
        print(f"- {ini.stdout}")
    else:
        print(f"- Erro: {ini.stderr}")
    
    #Continua dando errado, mas agora tem uns passos a mais

    print(ini)
    #os.system("docker compose run --rm airflow-init")

def comp():
    #Ta dando errado 2
    print("Criando ambiente do Airflow\n")
    #Path aqui também?
    #os.system("docker compose up -d")

def ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def main():
    doc = sub.run(args=["docker", "info"], capture_output=True)

    if doc.returncode == 0:
        if init():

            '''
            #Ver se o init deu certo tbm antes de vir pra cá
            #Inicia a interface do Airflow
            comp()

            #E só se der td certo ele mostra isso
            #Aqui é só pra flr que deu td certo e mostrar os endereços para acessar
            print(f"\nAirflow iniciado \
                   \nAcesse colocando os seguintes endereços no navegador: \
                   \nMesma máquina: http://localhost:9090 \
                   \nOutra máquina: http://{ip()}:9090\n")
            '''

    else:
        print("Docker não esta funcionando")


if __name__ == "__main__":
    main()
