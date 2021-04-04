FROM python:3.9.2

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install make

EXPOSE 5000

CMD [ "python3.9", "-m" , "flask", "run", "--host=0.0.0.0"]
