FROM python:3.12
ARG PROJECT_NAME="csca-5028-final-project"
COPY ../../components/pyproject.toml /home/${PROJECT_NAME}/components/pyproject.toml
COPY ../../components/rmatzke /home/${PROJECT_NAME}/components/rmatzke
COPY ../../applications/data-collector/requirements.txt /home/${PROJECT_NAME}/applications/data-collector/requirements.txt
COPY ../../applications/data-collector/src /home/${PROJECT_NAME}/applications/data-collector/src
WORKDIR /home/${PROJECT_NAME}/applications/data-collector
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]
