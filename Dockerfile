FROM python:3-windowsservercore
WORKDIR /app

COPY requirements.txt aw64.dll /app/
RUN pip install -r requirements.txt
COPY world_attributer/ /app/world_attributer

ENTRYPOINT [ "python /app/world_attributer" ]