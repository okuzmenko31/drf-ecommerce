FROM python:3.11

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/ecommerce

COPY requirements/requirements.txt /app/ecommerce/requirements/requirements.txt
COPY start.sh /app/ecommerce/start.sh
RUN pip install -r /app/ecommerce/requirements/requirements.txt
COPY . .
RUN chmod +x /app/ecommerce/start.sh

CMD ["/app/ecommerce/start.sh"]
