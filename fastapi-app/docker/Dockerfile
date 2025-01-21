FROM python:3.9.13-slim-buster
COPY ./ /app/

RUN pip install -r /app/docker/requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
RUN pip install pytest==7.1.2 \
    && pip install pytest-cov==3.0.0 \
    #&& rm -rf /app/tests/ /app/docker/ /app/README.md /app/*.sh /app/unittest.sh /app/main.py /app/.gitignore /app/.gitlab-ci.yml /app/release.ini \
    #&& rm -rf /app/docker-compose.yaml /app/init /app/deployments /app/config /app/.git /app/__pycache__ /app/*/__pycache__


WORKDIR /app/
EXPOSE 8000
CMD ["python", "/app/index.py"]
