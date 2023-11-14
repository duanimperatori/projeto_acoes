FROM jupyter/all-spark-notebook:2021-10-07

RUN pip install yfinance

ENV GRANT_SUDO=yes
ENV JUPYTER_ENABLE_LAB=yes
ENV PYTHONPATH=/usr/local/spark/python/lib/py4j-0.10.9-src.zip:/usr/local/spark/python
ENV PYSPARK_PYTHON=python3

VOLUME /usr/local/spark/conf
VOLUME /spark/home
VOLUME /home/jovyan/work

EXPOSE 8888
