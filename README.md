# MLSD_Litvinov_AITH

## Demo
<video width="100%" controls>
  <source src="assets/demo.mp4" type="video/mp4">
</video>

Если видео не работает в README, перейдите на [Google Drive](https://drive.google.com/file/d/1RpuIViNcYc7VJHia77GYsXSAgNf8vTnw/view?usp=sharing)

## Описание проекта
Специализированный фреймворк для дообучения Vision-Language Model (VLM) с использованием LoRA (Low-Rank Adaptation) для улучшения описания русских культурных персонажей на изображениях. Проект включает полный пайплайн подготовки данных, обучения модели и оценки качества.

## Основные возможности
- 📚 Полный фреймворк для LoRA дообучения VLM
- 🖼️ Поддержка работы с изображениями русских персонажей (Алёша, Чебурашка, Гена, Колобок)
- 🎨 Streamlit WebUI для демонстрации и тестирования
- 📈 Документированные эксперименты и результаты

## Структура проекта
- `docs/` — ML System Design документация
- `data/` — датасет изображений русских персонажей
- `finetune_testing/` — тестирование и результаты дообучения
- `service/` — Streamlit сервис для демонстрации
- `train_qwen_with_lora.py` — основной скрипт для обучения

## Быстрый старт
1. Клонируйте репозиторий:
```bash
git clone https://github.com/maksimlitvinov39kg/MLSD_Litvinov_AITH.git
cd MLSD_Litvinov_AITH
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Запустите сервис (опционально):
```bash
cd service
streamlit run app.py
```

4. (Опционально) Установите инструменты разработки (линтер/форматтер и pre-commit):
```bash
pip install --upgrade pip
pip install ruff pre-commit
pre-commit install
pre-commit run --all-files
```

## Требования к окружению
- Python 3.10+
- GPU рекомендуется (CUDA 11.8+)
- Зависимости указаны в `requirements.txt`

## Конфигурация разработки
В репозитории используются:
- `pyproject.toml` — конфигурация для ruff (линтер/форматтер)
- `.pre-commit-config.yaml` — автоматические проверки перед коммитом

## Результаты
Результаты дообучения и тестирования доступны в `finetune_testing/` с детальными метриками и сравнением.



## ML README (SFT Data Team Testing)

В репозитории есть отдельный файл с деталями по ML-экспериментам, подготовке данных и быстрому старту: `README_ML.md`.
В нём описаны структура датасета, скрипты (`caption_data.py', 'test_pretrain.ipynb'), инструкции по подготовке окружения, запуску генерации подписей, а также ограничения и рекомендации по дальнейшей работе.

Рекомендуется ознакомиться с `README_ML.md` перед запуском экспериментов:

- Быстрый старт и установка зависимостей
- Инструкция по созданию `.env` с API-ключами для генерации подписи
- Команды для запуска генерации аннотаций и обучения

См. файл: `README_ML.md`

