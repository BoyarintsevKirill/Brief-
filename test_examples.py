#!/usr/bin/env python3
"""
Примеры использования AI Marketing Copy Generator
Можно запустить для быстрого тестирования функционала
"""

from marketing_copy_generator import generate_marketing_copy
import os
import json

def test_cases():
    """Примеры запросов для тестирования"""

    test_products = [
        {
            "name": "Яндекс Метрика",
            "description": "Аналитическая платформа для отслеживания поведения пользователей на веб-сайтах. Показывает, откуда приходят посетители, как они взаимодействуют с сайтом, где они уходят. Поддерживает отслеживание целей, воронок конверсии и событий. Интеграция за 5 минут.",
            "audience": "маркетологи и руководители SMB",
            "channel": "поиск"
        },
        {
            "name": "Яндекс Директ",
            "description": "Сервис контекстной рекламы для привлечения целевых клиентов. Объявления показываются в поиске и партнёрских сайтах. Простая настройка, автоматизация ставок, аналитика по клюям слова.",
            "audience": "маркетологи",
            "channel": "инстаграм"
        },
        {
            "name": "Яндекс Бизнес",
            "description": "Бесплатная карточка компании в Яндекс.Картах и Яндекс.Справке. Управление часами работы, фото, отзывами, меню. Видна потенциальным клиентам при поиске на карте.",
            "audience": "владельцы кофеен, ресторанов, салонов красоты",
            "channel": "email"
        },
        {
            "name": "Яндекс Коллекции",
            "description": "Сервис для создания красивых коллекций товаров. Возможность добавлять фото, описания, ссылки. Автоматически генерируются красивые макеты. Шаринг в соцсетях.",
            "audience": "блогеры, инфлюэнсеры, владельцы интернет-магазинов",
            "channel": "тиктток"
        }
    ]

    return test_products


def print_result(result):
    """Красиво выводит результат"""
    print("\n" + "="*70)
    print(f"✅ Продукт: {result['product_name']}")
    print(f"👥 Аудитория: {result['target_audience']}")
    print(f"📱 Канал: {result['channel']}")
    print("="*70)
    print("\n" + result['generated_copies'])
    print("\n" + "="*70)
    print(f"📊 Использовано токенов:")
    print(f"   - Вход: {result['tokens_used']['input']}")
    print(f"   - Выход: {result['tokens_used']['output']}")
    print("="*70 + "\n")


def run_single_test():
    """Запустить один тест"""
    print("\n🔬 ТЕСТ: Генерация копирайта для Яндекс Метрики\n")

    result = generate_marketing_copy(
        product_name="Яндекс Метрика",
        product_description="Аналитическая платформа для отслеживания поведения пользователей на веб-сайтах. Показывает откуда приходят посетители, как они взаимодействуют с сайтом, где они уходят. Интеграция за 5 минут.",
        target_audience="маркетологи",
        channel="поиск"
    )

    print_result(result)


def run_all_tests():
    """Запустить все тесты"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Ошибка: ANTHROPIC_API_KEY не установлена")
        return

    test_products = test_cases()
    results = []

    print("\n" + "="*70)
    print("🚀 ЗАПУСК ПОЛНОГО ТЕСТИРОВАНИЯ")
    print(f"Будет протестировано {len(test_products)} продуктов")
    print("="*70)

    for i, product in enumerate(test_products, 1):
        print(f"\n⏳ [{i}/{len(test_products)}] Обработка: {product['name']} ({product['channel']})...")

        try:
            result = generate_marketing_copy(
                product_name=product['name'],
                product_description=product['description'],
                target_audience=product['audience'],
                channel=product['channel']
            )
            results.append(result)
            print_result(result)

        except Exception as e:
            print(f"❌ Ошибка при обработке {product['name']}: {str(e)}")

    # Общая статистика
    print("\n" + "="*70)
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print("="*70)
    total_input_tokens = sum(r['tokens_used']['input'] for r in results)
    total_output_tokens = sum(r['tokens_used']['output'] for r in results)

    print(f"✅ Успешно обработано: {len(results)} из {len(test_products)}")
    print(f"📊 Всего токенов: {total_input_tokens + total_output_tokens}")
    print(f"   - Вход: {total_input_tokens}")
    print(f"   - Выход: {total_output_tokens}")
    print("="*70 + "\n")


def test_with_bad_input():
    """Тест на обработку плохого инпута"""
    print("\n🔬 ТЕСТ: Обработка некорректного инпута\n")

    bad_inputs = [
        {
            "name": "X",  # Очень короткое название
            "description": "Короткое",  # Меньше 50 символов
            "audience": "все",
            "channel": "поиск"
        }
    ]

    for product in bad_inputs:
        print(f"Тест с названием: '{product['name']}', описанием: '{product['description']}'")

        # Проверка на 50+ символов
        if len(product['description']) < 50:
            print(f"❌ Ошибка валидации: описание должно быть не менее 50 символов (текущее: {len(product['description'])})")
            continue

        result = generate_marketing_copy(
            product_name=product['name'],
            product_description=product['description'],
            target_audience=product['audience'],
            channel=product['channel']
        )
        print_result(result)


def compare_channels():
    """Тест: сравнение генерации одного продукта для разных каналов"""
    print("\n🔬 ТЕСТ: Одно-продукт-разные-каналы\n")

    product_info = {
        "name": "Яндекс Директ",
        "description": "Сервис контекстной рекламы для привлечения целевых клиентов. Объявления показываются в Яндекс.Поиске и партнёрских сайтах. Автоматизация ставок, умные ставки, защита от некачественного трафика. Начните привлекать клиентов уже сегодня.",
        "audience": "маркетологи малого и среднего бизнеса"
    }

    channels = ["поиск", "инстаграм", "email", "тиктток"]

    for channel in channels:
        print(f"⏳ Генерирую для канала: {channel}...")
        result = generate_marketing_copy(
            product_name=product_info['name'],
            product_description=product_info['description'],
            target_audience=product_info['audience'],
            channel=channel
        )
        print_result(result)


if __name__ == "__main__":
    import sys

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Ошибка: переменная ANTHROPIC_API_KEY не установлена")
        print("\nУстановите её перед запуском:")
        print("  export ANTHROPIC_API_KEY='sk-ant-v1-xxxx'")
        sys.exit(1)

    print("\n" + "="*70)
    print("📋 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ AI Marketing Copy Generator")
    print("="*70)
    print("\nВыберите тест для запуска:")
    print("1. Один быстрый тест (Яндекс Метрика)")
    print("2. Полное тестирование (все 4 продукта)")
    print("3. Тест обработки плохого инпута")
    print("4. Сравнение одного продукта для разных каналов")
    print("="*70)

    choice = input("\nВаш выбор (1-4): ").strip()

    if choice == "1":
        run_single_test()
    elif choice == "2":
        run_all_tests()
    elif choice == "3":
        test_with_bad_input()
    elif choice == "4":
        compare_channels()
    else:
        print("❌ Неверный выбор")
