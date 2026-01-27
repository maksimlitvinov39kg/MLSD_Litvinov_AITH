# SFT Data Team Testing

Репозиторий для тестирования поведения предобученных Vision-Language моделей (VLM) и подготовки данных для последующей SFT / LoRA-адаптации, с фокусом на распознавание региональных культурных сущностей.

## 🔗 Навигация по проекту

### 📁 Структура репозитория
- [assets/](./assets/) - Вспомогательные ресурсы проекта
- [data/](./data/) - Основная папка с данными для обучения
  - [data/images/](./data/images/) - Изображения персонажей (по папкам)
  - [data/json/](./data/json/) - JSON конфигурации
  - [annotation.json](./data/annotation.json) - Основной файл разметки
- [finetune_testing/](./finetune_testing/) - Ноутбуки тестирования результатов

### 📓 Основные файлы
- [caption_data.py](./caption_data.py) - Генерация описаний изображений
- [test_pretrain.ipynb](./test_pretrain.ipynb) - Тестирование исходной модели
- [requirements.txt](./requirements.txt) - Зависимости Python

# Примечание
В этом файле сейчас сосредоточены инструкции по подготовке данных и проверке предобученной модели (pretrain). Описание и команды обучения временно опущены — их можно вернуть в отдельном разделе при необходимости.


## 🎯 Цель проекта

Большая часть современных open source VLM обучена на англоязычных датасетах и плохо знает культурные образы других регионов.

**Основные задачи:**
1. Выбрать VLM исходя из имеющихся ресурсов
2. Определить несколько региональных сущностей (например, Чебурашка) и собрать датасет
3. Убедиться, что модель не распознает эти сущности
4. Провести серию экспериментов по дообучению модели
5. Продемонстрировать и визуализировать результаты
6. Оформить код с инструкциями для тестирования на новых данных

---

## 🚀 Быстрый старт

### 1. Установка
```bash
git clone https://github.com/your-username/SFT-Data-team-testing.git
cd SFT-Data-team-testing

python -m venv .venv
source .venv/bin/activate 

pip install -r requirements.txt
```

### 2. Настройка API
Создайте файл `.env` в корневой папке:
```env
# API ключ для GigaChat (для caption генерации)
GIGACHAT_CREDENTIALS=your_gigachat_api_key_here
GIGACHAT_SCOPE=your_gigachat_scope_here
```

### 3. Подготовка данных
```bash
python caption_data.py
```

### 4. Тестирование предобученной модели (pretrain)

Для быстрой проверки поведения базовой VLM (до дообучения) используйте `test_pretrain.ipynb`. В ноутбуке реализована простая pipeline-инференса:

- загрузка `AutoProcessor` + VLM (в ноутбуке — пример с `Qwen/Qwen3-VL-2B-Instruct`),
- применение промптов из `data/json/base_prompts.json`,
- генерация ответов через `processor.apply_chat_template` и `model.generate`,
- вычисление CLIP Score (semantic similarity) для оценки соответствия сгенерированного текста и изображения.

CLIP Score: рекомендуется использовать CLIP (или ruCLIP для русского фокуса) как основную автоматическую метрику качества сопоставления image↔caption — ноутбук включает пример вычисления CLIP-score с `siglip2`.

---

## 📊 Результаты экспериментов

### Тестирование после дообучения
В папке [finetune_testing/](./finetune_testing/) представлены ноутбуки с результатами различных экспериментов:

- [test_after_finetune_lora_init.ipynb](./finetune_testing/test_after_finetune_lora_init.ipynb)
- [test_after_finetune_lora_v1.ipynb](./finetune_testing/test_after_finetune_lora_v1.ipynb)
- [test_after_finetune_lora_v2.ipynb](./finetune_testing/test_after_finetune_lora_v2.ipynb)
- [test_after_finetune_lora_v3.ipynb](./finetune_testing/test_after_finetune_lora_v3.ipynb)
- [Описание результатов](./finetune_testing/results.md)
---

### Оценка качества (CLIP Score)

В рамках быстрых sanity-check'ов и валидации baseline используется CLIP Score — семантическая мера соответствия между изображением и текстом. В `test_pretrain.ipynb` показано, как вычислять CLIP Score по сгенерированным ответам и как его использовать для сравнения до/после любых дальнейших дообучений.


## 📚 Датасет

### Персонажи в датасете
- **Алёша Попович** - ~20 изображений
- **Чебурашка** - ~30 изображений
- **Крокодил Гена** - ~ 20 изображений
- **Колобок** - ~20 изображений

*В репозитории загружено только по одному изображению для наглядности. Полный датасет доступен на [Google Drive](https://drive.google.com/drive/folders/1T_3XJvJv0nvGhF5j2txKP7Nj6hjOk1lE?usp=sharing)*

### Структура данных
```
data/
├── images/
│   ├── alyosha/      # Изображения Алёши Поповича
│   ├── cheburashka/  # Изображения Чебурашки
│   ├── gena/         # Изображения крокодила Гены
│   └── kolobok/      # Изображения Колобка
├── json/
│   ├── base_prompts.json      # Базовые промпты для генерации
│   └── character_names.json   # Соответствие папок и названий
└── annotation.json            # Основной файл разметки
```

---

## 🔄 Добавление новых персонажей

1. **Добавьте изображения**
   ```bash
   mkdir data/images/new_character
   ```

2. **Обновите конфигурацию**
   В файле [`data/json/character_names.json`](./data/json/character_names.json):
   ```json
   {
     "gena": "Крокодил Гена",
     "new_character": "Новый Персонаж"
   }
   ```

3. **Сгенерируйте описания**
   ```bash
   python caption_data.py
   ```
   Скрипт автоматически создаст описания только для новых изображений.

---

## ⚠️ Текущие ограничения

### Технические проблемы
- **Ресурсы**: 7B модели Qwen и LLaVA не помещаются в 24 ГБ памяти MacBook M4 Pro
- **Компромисс**: Используется Qwen-VL 3B модель

### Проблемы обучения
- Loss зависает на уровне ~4 (max_length=128) и ~2 (max_length=256)
- Качество генерации требует улучшения
- **Необходимо**: Расширение датасета для лучших результатов

### Качество разметки
- GigaChat показывает посредственные результаты как кепшенер
- Возможны проблемы с качеством описаний

### Нехватка данных
- Долго вручную скачивать нужные картинки в большом количестве, в будущем можно сделать скрипт который сам качает картинки с гугла