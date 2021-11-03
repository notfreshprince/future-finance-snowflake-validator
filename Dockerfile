FROM python:3.9.2-buster

ADD validator /task/
ADD sql /task/sql/
ADD requirements.txt /task/
WORKDIR /task

RUN pip3 install -r requirements.txt --target /task

#ENTRYPOINT ["python", "main.py"]
#CMD ["python", "main.py", "--query", "poc", "--metric-name", "VALIDATOR_METRIC_TEST"]
CMD ["python", "task_monitor.py"]