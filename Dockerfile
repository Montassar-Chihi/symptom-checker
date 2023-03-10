FROM python:3.10.8
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
 CMD ["python", "app.py","flask","--host","0.0.0.0"] 
