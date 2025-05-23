import time, socket, urllib.request
import subprocess as sub

def comando(cmd_docker, **arg_opcional):
    return sub.run(args=cmd_docker, capture_output=True, text=True, **arg_opcional )

def db_init():
    print("Iniciando banco de dados")

    db = comando(["docker", "compose", "up", "-d", "db"])

    if db.returncode == 0 and db_check():
        print("\t- Banco de dados criado com sucesso\n")
        return True
    
    else:
        return erro(db.stderr)

def db_check(host = "localhost", port = 9191, timeout = 90):
        
    t_inicio = time.time()
    while time.time() - t_inicio < timeout:
        try:
            with socket.create_connection((host, port), timeout = 2):
                break

        except (socket.timeout, ConnectionRefusedError):
            time.sleep(2)

    else:
        print("Banco de dados com problemas de conexão")
        return False

    t_inicio = time.time()
    while time.time() - t_inicio < timeout:
        db_funf = comando(["docker", "inspect", "-f", "{{.State.Health.Status}}", "airflow-db"])

        if db_funf.returncode == 0 and "healthy" in db_funf.stdout.strip():
            return True
        
        time.sleep(2)

    print("O banco de dados não iniciou a tempo, reinicie o setup")
    return False

def init():
    print("Criando administrador")

    ini = comando(["docker", "compose", "run", "--rm", "airflow-init"])

    if ini.returncode == 0:
        print(f"\t- Registro de Admin criado com sucesso\n")
        return True
    
    else:
        return erro(ini.stderr)
    
def comp():
    print("Criando ambiente do Airflow")
    
    airflow = comando(["docker", "compose", "up", "-d"])

    if airflow.returncode == 0:
        print("\t- Ambiente criado com sucesso\n")
        return True
    
    else:
        return erro(airflow.stderr)
    
def web_up(host = "localhost", port = 9090, timeout = 60):
    print("Aguardando o webserver iniciar...")

    url = f"http://{host}:{port}"
    t_inicio = time.time()

    while time.time() - t_inicio < timeout:
        try:
            with urllib.request.urlopen(url, timeout = 5) as resposta:
                if resposta.status == 200:
                    return True
        except Exception:
            time.sleep(2)

    print("Não foi possivel iniciar o Airflow webserver")
    return False

def ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip

def erro(erro: str):
    print("\nErro durante a configuração do airflow")
    
    erro_formatado = erro.strip().replace(chr(10), '\n\t')
    print(f"\t- {erro_formatado}")

    input("\nAperte enter para continuar...")

    return False


def main():
    doc = sub.run(args=["docker", "info"], capture_output=True)

    if doc.returncode == 0:
        
        if db_init() and init() and comp():
            
            if web_up():

               print(f"\nAirflow iniciado \
                    \nAcesse colocando os seguintes endereços no navegador:\n \
                    \nMesma máquina: http://localhost:9090 \
                    \nOutra máquina: http://{ip()}:9090\n")
               
               input("Aperte enter para continuar...")

    else:
        print("\nDocker não esta funcionando, verifique se esta ligado ou instalado")

        input("\nAperte enter para continuar...")


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(f"Erro inesperado: {e}")
