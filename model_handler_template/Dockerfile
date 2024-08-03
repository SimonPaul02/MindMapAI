# Dockerfile
FROM python:3.9

WORKDIR /usr/project


RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install --upgrade pip
# Copy the requirements over to build the virtual environment
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. model_handler.proto

RUN useradd appuser
USER appuser

EXPOSE 8061

CMD ["python3", "-u", "model_handler_server.py"]