FROM python:3
ENV PYTHONUNBUFFERD 1
LABEL maintainer = "i@yorling.com"
LABEL author = "Yorling"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && \
    python manage.py collectstatic --noinput && \
    python manage.py makemigrations luck auths --noinput && \
    python manage.py migrate --noinput

#CMD ["uwsgi", '--chdir /app', "--module luckycore.wsgi:application", "--processes 4", "--master", \
#"--pidfile /app/luckycore.pid", "--vacuum", "--max-requests 5000", \
#"--chmod-socket=666", "--socket=/app/luckycore.sock"]
CMD uwsgi --chdir /app --module luckycore.wsgi:application --processes 4 \
    --master --pidfile /app/tmp/luckycore.pid \
    --vacuum --max-requests 5000 --chmod-socket=666 --socket /app/tmp/luckycore.sock
