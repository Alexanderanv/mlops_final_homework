# MLOPS Итоговое домашнее задание
## Этап 1. Развертывание MLflow
### Артефакты
Каталог `./1_mlflow`  
### Скриншоты
*Логи сервисов*
![Логи сервисов](images/1_mlflow_logs.png)

*Эксперимент создан*
![Эксперимент создан](images/1_mlflow_exp_screen.png)

## Этап 2. Развертывание Airflow
### Артефакты
Каталог `./2_airflow`  
Даг `./2_airflow/data/airflow/dags/firstproj`
### Скриншоты
*Логи сервисов*
![Лог db](images/2_airflow_logs_1.png)
![Лог scheduler](images/2_airflow_logs_2.png)

*Демо даг выполнен*
![Даг выполнен](images/2_airflow_dag_complete.png)

## Этап 3. Развертывание LakeFS
### Артефакты
Каталог `./3_lakefs`
### Скриншоты
*Логи сервисов*
![Логи](images/3_dvc_logs.png)

*Lakefs diff*
![lakefs diff](images/3_lakefs_merge.png)

## Этап 4. Развертывание JupyterHub
### Артефакты
Каталог `./4_jupyterhub`
### Скриншоты
*Логи сервисов*
![Логи](images/4_jph_logs.png)

*Скрин запущенного сервиса*
![Скрин JPH](images/4_jph_screen.png)

## Этап 5. Развертывание ML-сервиса
### Артефакты
Каталог `./5_mlservice`
### Скриншоты
*Логи сервисов*
![Логи](images/5_mlservice_logs.png)

*Тесты запросов*
![Скрин JPH](images/5_mlservice_predicts.png)

*Логи работы модели в БД*
![Скрин JPH](images/5_mlservice_dblogs.png)

## Этап 6. Метрики развернутого сервиса
### Артефакты
Cервис с endpoint /metrics `./6_metrics/mlservice`
Prometheus + Grafana `./6_metrics/metrics`
### Скриншоты
*Логи сервисов*
![Логи](images/6_metrics_logs.png)

*Дашборд Grafana*
![Дашборд](images/6_metrics_dashboard.png)