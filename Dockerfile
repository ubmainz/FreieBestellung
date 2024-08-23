FROM python:3.12-slim
LABEL maintainer="m.genzmehr@ub.uni-mainz.de"
ENV TZ="Europe/Berlin"
RUN pip install --upgrade pip && \
    pip install Flask requests gunicorn && \
    mkdir /var/log/request-form
WORKDIR /opt/request-form
COPY folio/ folio
COPY theapp/ theapp
COPY user/ user
COPY wsgi.py .
COPY connection.ini .
COPY config.py theapp/config.py
EXPOSE 8080
CMD ["gunicorn", "-w", "8", "--bind", "0.0.0.0:8080", "wsgi:app"]
