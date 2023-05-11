FROM python:3.11

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


WORKDIR /drf_ecommerce/apps
COPY . .

COPY requirements/requirements.txt /drf_ecommerce/requirements/requirements.txt
COPY start.sh /drf_ecommerce/start.sh
RUN pip install -r /drf_ecommerce/requirements/requirements.txt
RUN chmod +x /drf_ecommerce/start.sh

EXPOSE 8000

CMD ["/drf_ecommerce/start.sh"]
