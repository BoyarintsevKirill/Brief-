#!/usr/bin/env python3
"""
MVP: Генератор брифа из сырых заметок интервью
Принимает текст → возвращает структурированный бриф через LLM
"""

import os
import sys
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """Ты опытный маркетолог и редактор. Твоя задача — превратить сырые заметки
с интервью в структурированный бриф для команды (копирайтер, дизайнер, SMM).

Правила:
1. Используй только то, что есть в тексте. Не придумывай.
2. Если какого-то раздела нет в тексте — напиши [нужно уточнить].
3. Пиши кратко и конкретно, без воды.
4. Результат всегда на русском языке.
5. Формат — строго по шаблону ниже.

Шаблон брифа:
---
## Бриф

**Тип материала:** [пост / баннер / лендинг / статья / другое]

**Цель:** [чего хотим достичь — продажи, охват, регистрации, узнаваемость]

**Целевая аудитория:** [кто читатель/зритель, их боли и контекст]

**Ключевое сообщение:** [одно главное, что человек должен запомнить]

**Что важно показать:** [конкретные преимущества, факты, цифры]

**Тон и стиль:** [формальный / дружелюбный / экспертный / молодёжный и т.д.]

**Ограничения:** [чего нельзя использовать, что обязательно включить]

**Примеры или референсы:** [если упоминались]

**Дедлайн:** [если назван]

**Что нужно уточнить:** [список открытых вопросов, которые остались]
---"""


def generate_brief(raw_notes: str, material_type: str = "") -> dict:
    """
    Генерирует структурированный бриф из сырых заметок.

    Args:
        raw_notes: сырой текст заметок с интервью
        material_type: опциональная подсказка о типе материала

    Returns:
        dict с брифом и метаданными
    """
    type_hint = f"\nТип материала (подсказка от пользователя): {material_type}" if material_type else ""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Вот сырые заметки с интервью. Составь бриф.{type_hint}\n\n---\n{raw_notes}\n---"
            }
        ]
    )

    return {
        "brief": message.content[0].text,
        "tokens_in": message.usage.input_tokens,
        "tokens_out": message.usage.output_tokens,
    }


def run():
    """Интерактивный запуск в терминале."""

    print("\n" + "=" * 60)
    print("  Генератор брифа из заметок интервью")
    print("=" * 60)

    history = []  # multi-turn: сохраняем предыдущие брифы в сессии

    while True:
        print("\nВставьте заметки с интервью (завершите ввод строкой '---'):")
        lines = []
        while True:
            line = input()
            if line.strip() == "---":
                break
            lines.append(line)

        raw_notes = "\n".join(lines).strip()
        if not raw_notes:
            print("Пустой ввод, попробуйте ещё раз.")
            continue

        material_type = input("\nТип материала (необязательно, Enter — пропустить): ").strip()

        print("\nГенерирую бриф...\n")

        result = generate_brief(raw_notes, material_type)
        history.append(result)

        print(result["brief"])
        print(f"\n[токены: {result['tokens_in']} вход / {result['tokens_out']} выход]")

        again = input("\nСгенерировать ещё один бриф? (y/n): ").strip().lower()
        if again != "y":
            print("\nГотово. Всего обработано брифов в этой сессии:", len(history))
            break


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Ошибка: переменная ANTHROPIC_API_KEY не задана.")
        print("Задайте её: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    run()
