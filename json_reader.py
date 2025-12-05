import json

from theme import Theme


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


def load_themes_from_json(file_path):
    themes_list = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            # Создаем объект Theme, используя данные из словаря
            new_theme = Theme(
                name=item["name"],
                bg_path=item["bg_path"],
                bird_path=item["bird_path"],
                pipe_path=item["pipe_path"],
                text_color_hex=item["text_color_hex"],
            )
            themes_list.append(new_theme)

    except Exception as e:
        print(f"Ошибка загрузки тем: {e}")

        default_theme = Theme(
            "Backup",
            "assets/images/background.png",
            "assets/images/bird.png",
            "assets/images/pipe.png",
            "#FFFFFF",
        )
        themes_list.append(default_theme)

    return themes_list
