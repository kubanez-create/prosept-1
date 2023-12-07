FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install -U sentence-transformers
COPY ./src /code/src