import json


def load_style_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Превращаем JSON словарь в строку CSS
        stylesheet = ""
        for selector, properties in data.items():
            stylesheet += f"{selector} {{\n"
            for key, value in properties.items():
                stylesheet += f"    {key}: {value};\n"
            stylesheet += "}\n"

        return stylesheet
    except Exception as e:
        print(f"Ошибка загрузки стилей: {e}")
        return ""
