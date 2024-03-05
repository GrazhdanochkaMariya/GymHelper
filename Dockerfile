FROM python:3.9

WORKDIR /gym-helper

COPY ./requirements.txt /gym-helper/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /gym-helper/requirements.txt

COPY . .

CMD alembic upgrade head && uvicorn main:app --host=0.0.0.0 --port 80 --reload