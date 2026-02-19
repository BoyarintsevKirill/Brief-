#!/usr/bin/env python3
"""
AI Marketing Copy Generator MVP
Генерирует вариации рекламных текстов с использованием LLM
"""

import os
from anthropic import Anthropic

# Инициализируем клиент Anthropic
client = Anthropic()

def generate_marketing_copy(product_name: str, product_description: str, target_audience: str, channel: str) -> dict:
    """
    Генерирует вариации маркетингового копирайта для продукта

    Args:
        product_name: Название продукта
        product_description: Описание продукта и его возможностей
        target_audience: Целевая аудитория (например: "руководители SMB", "фрилансеры", "маркетологи")
        channel: Канал распространения ("поиск" / "инстаграм" / "email" / "тиктток")

    Returns:
        dict с вариантами копирайта для каждого канала
    """

    # Промпт с чётким форматом результата
    system_prompt = """Ты профессиональный маркетолог и копирайтер с опытом в создании рекламных текстов
для технологических продуктов. Твоя задача - генерировать убедительные, короткие и результативные
тексты объявлений для разных каналов.

Правила:
1. Каждый текст должен содержать: проблема → решение → call-to-action
2. Используй эмоциональные триггеры и социальные доказательства где уместно
3. Адаптируй стиль под канал (поиск = краткий, инстаграм = вовлекающий, email = личный)
4. Не придумывай функции, которых нет в описании
5. Текст должен быть на русском языке

Результат выводи в формате:
ВАРИАНТ 1: [заголовок текста]
[Сам текст объявления]

ВАРИАНТ 2: [заголовок текста]
[Сам текст объявления]

И так далее для всех вариантов."""

    user_message = f"""Создай 3 варианта рекламного текста для объявлений в канале "{channel}".

ИНФОРМАЦИЯ О ПРОДУКТЕ:
- Название: {product_name}
- Описание: {product_description}
- Целевая аудитория: {target_audience}
- Канал: {channel}

Адаптируй стиль под этот канал:
- Если "поиск": максимум 80 символов, включи ключевые слова, фокус на преимущества
- Если "инстаграм": 150-250 символов, эмоциональный, с хэштегами, вовлекающий
- Если "email": 100-200 символов, личный тон, фокус на выгоду для адресата
- Если "тиктток": 50-150 символов, молодежный тон, тренды, скорость

Создай 3 разных варианта, которые можно тестировать."""

    # Отправляем запрос к API
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    # Парсим результат
    response_text = message.content[0].text

    return {
        "status": "success",
        "product_name": product_name,
        "target_audience": target_audience,
        "channel": channel,
        "generated_copies": response_text,
        "model_used": "claude-opus-4-6",
        "tokens_used": {
            "input": message.usage.input_tokens,
            "output": message.usage.output_tokens
        }
    }


def interactive_mode():
    """Интерактивный режим для генерации копирайта"""

    print("\n" + "="*60)
    print("🚀 AI Marketing Copy Generator")
    print("="*60)
    print("\nДобро пожаловать! Я помогу вам создать варианты рекламных текстов.\n")

    conversation_history = []

    while True:
        print("\n" + "-"*60)
        print("Выберите действие:")
        print("1. Сгенерировать новый копирайт")
        print("2. Получить рекомендации по копирайту")
        print("3. Выход")
        print("-"*60)

        choice = input("\nВаш выбор (1-3): ").strip()

        if choice == "1":
            print("\n📝 Заполните информацию о продукте:\n")

            product_name = input("Название продукта: ").strip()
            if not product_name:
                print("❌ Название не может быть пустым")
                continue

            product_description = input("Описание продукта (50+ символов): ").strip()
            if len(product_description) < 50:
                print("❌ Описание должно быть не менее 50 символов")
                continue

            print("\nДоступные целевые аудитории:")
            print("- руководители SMB")
            print("- маркетологи")
            print("- фрилансеры")
            print("- владельцы интернет-магазинов")
            print("- разработчики")
            audience = input("\nЦелевая аудитория (или своя): ").strip()

            print("\nДоступные каналы:")
            print("- поиск")
            print("- инстаграм")
            print("- email")
            print("- тиктток")
            channel = input("\nКанал (выберите из списка): ").strip().lower()

            if channel not in ["поиск", "инстаграм", "email", "тиктток"]:
                print("❌ Неверный канал")
                continue

            print("\n⏳ Генерирую варианты... это может занять 10-30 секунд\n")

            result = generate_marketing_copy(product_name, product_description, audience, channel)

            if result["status"] == "success":
                print("\n✅ Результат готов!\n")
                print("="*60)
                print(f"Продукт: {result['product_name']}")
                print(f"Аудитория: {result['target_audience']}")
                print(f"Канал: {result['channel']}")
                print("="*60)
                print("\n" + result['generated_copies'])
                print("\n" + "="*60)
                print(f"📊 Токены: {result['tokens_used']['input']} вход, {result['tokens_used']['output']} выход")
                print("="*60)

                conversation_history.append({
                    "product": product_name,
                    "result": result
                })

        elif choice == "2":
            if not conversation_history:
                print("\n⚠️  Сначала сгенерируйте копирайт")
                continue

            print("\n💡 Рекомендации по оптимизации копирайта:\n")

            # Просим AI дать советы
            products_info = "\n".join([f"- {h['product']}" for h in conversation_history])

            advice_message = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=800,
                system="Ты эксперт по маркетингу и копирайту. Дай краткие, практичные советы.",
                messages=[
                    {"role": "user", "content": f"""На основе сгенерированных текстов дай 3-5 советов по улучшению копирайта для продуктов: {products_info}

Фокусируйся на:
1. Структуре текста
2. Эмоциональных триггерах
3. Call-to-action
4. A/B тестировании

Будь краток и практичен."""}
                ]
            )

            print(advice_message.content[0].text)

        elif choice == "3":
            print("\n👋 До свидания!")
            break

        else:
            print("❌ Неверный выбор")


def batch_mode(products: list):
    """Режим пакетной обработки для нескольких продуктов"""

    results = []
    for product in products:
        print(f"\n⏳ Обработка: {product['name']}...")
        result = generate_marketing_copy(
            product_name=product['name'],
            product_description=product['description'],
            target_audience=product['audience'],
            channel=product['channel']
        )
        results.append(result)

    return results


if __name__ == "__main__":
    import sys

    # Проверяем ключ API
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Ошибка: переменная ANTHROPIC_API_KEY не установлена")
        print("Установите её: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    # Запуск интерактивного режима
    interactive_mode()
