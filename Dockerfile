FROM python:3.10.9-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

RUN python -m venv /opt/venv

RUN adduser --disabled-password --gecos '' my_user

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /usr/src/app
COPY .env /usr/src/app/.env

RUN mkdir -p /usr/src/app/staticfiles && \
    chown -R my_user:my_user /usr/src/app && \
    chown -R my_user:my_user /usr/src/app/staticfiles

RUN chmod +x /usr/src/app/scripts/run.sh && \
    chown -R my_user:my_user /usr/src/app

USER my_user

CMD ["/usr/src/app/scripts/run.sh"]