FROM python:3.12
ARG PROJECT_NAME="csca-5028-final-project"
COPY ../../components/pyproject.toml /home/${PROJECT_NAME}/components/pyproject.toml
COPY ../../components/rmatzke /home/${PROJECT_NAME}/components/rmatzke
COPY ../../applications/rest-api/requirements.txt /home/${PROJECT_NAME}/applications/rest-api/requirements.txt
COPY ../../applications/rest-api/src /home/${PROJECT_NAME}/applications/rest-api/src
WORKDIR /home/${PROJECT_NAME}/applications/rest-api
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]
