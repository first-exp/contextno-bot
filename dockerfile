# Используем официальный образ Python в качестве базового
FROM python:3.12.2-slim AS builder

# Переходим в рабочую директорию
WORKDIR /app

# Установка зависимостей проекта
# Копируем только файлы pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction 


FROM python:3.12.2-slim


COPY --from=builder /app /app

# Копируем все остальные файлы проекта
COPY . ./

ENV VENV_PATH="/app/.venv"

# Указание команды для запуска приложения
# CMD ["/app/.venv/bin/python", "main.py"]