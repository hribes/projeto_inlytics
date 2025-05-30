#Caso abram o dockerfile no VScode, o from vai ficar amarelo pq tem uma vulnerabilidade com o airflow, vou tentar dar um jeito mais tarde
FROM apache/airflow:2.8.1-python3.10

#Voltando para o airflow
USER airflow

RUN pip install "apache-airflow[mysql]==2.8.1" \
    && pip install pymysql \
    && pip install mysql-connector-python
