FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# install pip dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r /app/requirements.txt

# copy project
COPY . /app

# collect static files (if any). do not fail the build if collectstatic needs settings from env
RUN python manage.py collectstatic --noinput || true

EXPOSE 14000

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:14000" ]
