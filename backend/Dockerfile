FROM python:3.10.13-alpine

WORKDIR /src/backend

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./prestart.sh .
RUN sed -i 's/\r$//g' /src/backend/prestart.sh
RUN chmod +x /src/backend/prestart.sh


COPY . .

ENTRYPOINT ["/src/backend/prestart.sh"]