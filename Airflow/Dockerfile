#Caso abram o dockerfile no VScode, o from vai ficar amarelo pq tem uma vulnerabilidade com o airflow, vou tentar dar um jeito mais tarde
FROM apache/airflow:2.8.1-python3.10

#Aqui mudamos o usuário para instalar td que não é do airflow
USER root

RUN apt-get update && \
    apt-get install -y libmysqlclient-dev default-libmysqlclient-dev gcc python3-dev build-essential && \
    apt-get clean

#Voltando para o airflow
USER airflow

RUN pip install "apache-airflow[mysql]==2.8.1"
