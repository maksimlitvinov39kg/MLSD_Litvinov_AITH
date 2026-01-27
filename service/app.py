import streamlit as st
import torch
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from peft import PeftModel
from PIL import Image
import logging
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_resource
def load_model_with_lora(
    base_model_name: str = "Qwen/Qwen2.5-VL-3B-Instruct",
    lora_path: str = "../results/qwen-vl-regional/exp_r=16_alpha=32_seq=256_ne=25/checkpoint-430"
):
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    logger.info(f"Загрузка базовой модели: {base_model_name}")

    processor = AutoProcessor.from_pretrained(base_model_name)

    base_model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        base_model_name,
        dtype="auto",
        device_map="auto" if device.type == "cuda" else None,
        trust_remote_code=True
    )

    if device.type != "cuda":
        base_model.to(device)

    logger.info(f"Загрузка LoRA адаптеров из: {lora_path}")

    try:
        model = PeftModel.from_pretrained(base_model, lora_path)
        logger.info("LoRA адаптеры успешно применены")
    except Exception as e:
        logger.error(f"Ошибка загрузки LoRA адаптеров: {e}")
        logger.info("Используется базовая модель без адаптеров")
        model = base_model

    return processor, model, device


def run_chat_with_lora(processor, model, device, image, user_text: str, max_new_tokens: int = 256):
    from qwen_vl_utils import process_vision_info

    messages = [
        {"role": "user", "content": [
            {"type": "image", "image": image},
            {"type": "text", "text": user_text}
        ]}
    ]

    prompt = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    image_inputs, video_inputs = process_vision_info(messages)

    inputs = processor(
        text=prompt,
        images=image_inputs,
        videos=video_inputs,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=processor.tokenizer.pad_token_id
        )

    generated_text = processor.batch_decode(output, skip_special_tokens=True)[0]

    if "<|im_start|>assistant" in generated_text:
        response = generated_text.split("<|im_start|>assistant")[-1].strip()
        if response.endswith("<|im_end|>"):
            response = response[:-10].strip()
    else:
        response = generated_text.split(prompt)[-1].strip()

    return response


def main():
    st.set_page_config(
        page_title="Image Caption Generator",
        page_icon="🖼️",
        layout="wide"
    )

    st.title("🖼️ Генератор описаний изображений")
    st.markdown("### Qwen2.5-VL-3B с LoRA fine-tuning")

    st.sidebar.header("Настройки")

    lora_path = st.sidebar.text_input(
        "Путь к LoRA весам",
        value="../results/qwen-vl-regional/exp_r=16_alpha=32_seq=256_ne=25/checkpoint-430",
        help="Путь к чекпоинту LoRA адаптеров"
    )

    max_new_tokens = st.sidebar.slider(
        "Максимальная длина ответа (токены)",
        min_value=64,
        max_value=512,
        value=256,
        step=32
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### О модели")
    st.sidebar.info(
        "Модель: Qwen2.5-VL-3B-Instruct\n\n"
        "Fine-tuning: LoRA (r=16, alpha=32)\n\n"
        "Специализация: Описание русских сказочных персонажей"
    )

    with st.spinner("Загрузка модели..."):
        try:
            processor, model, device = load_model_with_lora(lora_path=lora_path)
            st.success(f"✅ Модель загружена на устройство: {device}")
        except Exception as e:
            st.error(f"❌ Ошибка загрузки модели: {e}")
            return

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Загрузите изображение")

        uploaded_file = st.file_uploader(
            "Выберите изображение",
            type=["jpg", "jpeg", "png", "webp"],
            help="Поддерживаемые форматы: JPG, JPEG, PNG, WEBP"
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Загруженное изображение", use_container_width=True)

    with col2:
        st.header("Задайте вопрос")

        default_prompts = [
            "Опиши подробно, что изображено на картинке.",
            "Кто или что находится на этом изображении?",
            "Какие детали ты видишь на этой картинке?",
            "Расскажи о персонаже на изображении.",
            "Что происходит на этой картинке?"
        ]

        prompt_option = st.selectbox(
            "Выберите готовый промпт или введите свой",
            ["Свой вопрос"] + default_prompts
        )

        if prompt_option == "Свой вопрос":
            user_prompt = st.text_area(
                "Ваш вопрос к изображению",
                value="Опиши подробно, что изображено на картинке.",
                height=100
            )
        else:
            user_prompt = prompt_option
            st.text_area("Выбранный промпт", value=user_prompt, height=100, disabled=True)

        generate_button = st.button("🚀 Сгенерировать описание", type="primary", use_container_width=True)

    if generate_button:
        if uploaded_file is None:
            st.warning("⚠️ Пожалуйста, загрузите изображение")
            return

        if not user_prompt.strip():
            st.warning("⚠️ Пожалуйста, введите вопрос")
            return

        with st.spinner("Генерация описания..."):
            try:
                response = run_chat_with_lora(
                    processor,
                    model,
                    device,
                    image,
                    user_prompt,
                    max_new_tokens
                )

                st.markdown("---")
                st.header("📝 Результат")
                st.markdown(f"**Вопрос:** {user_prompt}")
                st.markdown(f"**Ответ модели:**")
                st.info(response)

            except Exception as e:
                st.error(f"❌ Ошибка при генерации: {e}")
                logger.exception("Ошибка инференса")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Powered by Qwen2.5-VL-3B-Instruct + LoRA"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
