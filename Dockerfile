FROM python:3.6

RUN mkdir -p /var/www/app
WORKDIR /var/www/app
ADD . /var/www/app/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python3",  "/var/www/app/app.py"]