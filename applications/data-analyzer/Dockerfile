FROM python:3.12
ARG PROJECT_NAME="csca-5028-final-project"
COPY ../../components/pyproject.toml /home/${PROJECT_NAME}/components/pyproject.toml
COPY ../../components/rmatzke /home/${PROJECT_NAME}/components/rmatzke
COPY ../../applications/data-analyzer/requirements.txt /home/${PROJECT_NAME}/applications/data-analyzer/requirements.txt
COPY ../../applications/data-analyzer/src /home/${PROJECT_NAME}/applications/data-analyzer/src
WORKDIR /home/${PROJECT_NAME}/applications/data-analyzer
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]
