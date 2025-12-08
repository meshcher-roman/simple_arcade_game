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


def load_settings_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки настроек: {e}. Используются значения по умолчанию.")
        return {
            "window": {
                "screen_width": 400,
                "screen_height": 600,
                "app_min_width": 1000,
                "app_min_height": 700,
            },
            "audio": {
                "music_volume": 0.5,
                "sfx_volume": 1.0,
                "music_muted": False,
                "sfx_muted": False,
            },
            "gameplay": {"fps": 60, "spawn_interval": 1500},
            "bird": {
                "start_x": 50,
                "start_y": 200,
                "size": 30,
                "gravity": 0.5,
                "jump_velocity": -7,
                "rotation_multiplier": 3,
            },
            "pipe": {"width": 60, "speed": 3, "gap_size": 150},
        }


def save_settings_to_json(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("Настройки сохранены.")
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
