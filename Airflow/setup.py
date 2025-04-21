import time, socket
import subprocess as sub

def db_init():
    print("Iniciando banco de dados\n")

    db = sub.run(args=["docker", "compose", "up", "-d", "db"], capture_output=True, text=True)

    if db.returncode == 0 and db_check("localhost", 9191):
        print("Banco de dados criado com sucesso\n")
        return True
    else:
        return False

def db_check(host: str, port: int, timeout: int = 60):
    t_ini = time.time()
    while time.time() - t_ini < timeout:
        try:
            with socket.create_connection((host, port), timeout = 2):
                return True
        except (socket.timeout, ConnectionRefusedError):
            time.sleep(2)

    print("Banco de dados com problemas de conexão")
    return False

def init():
    #Ta dando errado 
    print("Criando administrador\n")

    #Talvez colocar o path para ele saber onde tem que trabalhar???
    ini = sub.run(args=["docker", "compose", "run", "--rm", "airflow-init"], capture_output=True, text=True)

    if ini.returncode == 0:
        print(f"- {ini.stdout}")
    else:
        print(f"- Erro: {ini.stderr}")
    
    #Continua dando errado, mas agora tem uns passos a mais

    print(ini)

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
        
        if db_init():
            
            '''
        if init():

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
