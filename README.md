# MLSD_Litvinov_AITH

Репозиторий проекта по ML System Design (курс/проект). Этот репозиторий содержит материалы, исследования и вспомогательные скрипты для выполнения заданий и разработки ML-систем.

## Содержание
- `docs/` — дизайн системы и документация
- `requirements.txt` — зависимости проекта

## Быстрый старт
1. Клонируйте репозиторий:

	git clone <repo-url>

2. Создайте виртуальное окружение и установите зависимости:

	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

3. (Опционально) Установите инструменты разработки (линтер/форматтер и pre-commit):

	pip install --upgrade pip
	pip install ruff pre-commit

4. Активируйте хуки pre-commit:

	pre-commit install
	pre-commit run --all-files

## Конфигурация разработки
В репозитории добавлены файлы конфигурации для автоматического форматирования и линтинга:

- `pyproject.toml` — конфигурация для ruff (линтер/форматтер).
- `.pre-commit-config.yaml` — хуки pre-commit (ruf, базовые проверки YAML, удаление пробелов и т.д.).

Используйте `ruff` для проверки/исправления кода и `pre-commit` для автозапуска этих проверок перед коммитом.

## Контакты
Автор: Maksim Litvinov

