from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """Ты опытный маркетолог и редактор. Твоя задача — превратить сырые заметки
с интервью в структурированный бриф для команды (копирайтер, дизайнер, SMM).

Правила:
1. Используй только то, что есть в тексте. Не придумывай.
2. Если какого-то раздела нет в тексте — напиши [нужно уточнить].
3. Пиши кратко и конкретно, без воды.
4. Результат всегда на русском языке.
5. Используй Markdown-форматирование.

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

**Что нужно уточнить:**
- [список открытых вопросов]
---"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    notes = data.get("notes", "").strip()
    material_type = data.get("material_type", "").strip()

    if not notes:
        return jsonify({"error": "Введите заметки"}), 400

    type_hint = f"\nТип материала (подсказка): {material_type}" if material_type else ""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Вот сырые заметки с интервью. Составь бриф.{type_hint}\n\n---\n{notes}\n---"}
            ],
            max_tokens=1500,
            temperature=0.3,
        )

        brief = response.choices[0].message.content
        return jsonify({"brief": brief})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
