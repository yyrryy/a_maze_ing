class InvalideValue(Exception):
    pass


def parsing_line(line: str) -> tuple:
    line = line.strip()
    if "=" not in line:
        raise ValueError(f"Invalid line: {line}")

    key, value = line.split("=", 1)
    key = key.upper().strip()
    value = value.strip()

    if key in ("WIDTH", "HEIGHT"):
        if not value.isdigit():
            raise ValueError(f"{key} must be a positive integer. Got: {value}")
        if not value:
            raise ValueError(f"{key} must be a positive integer. Got: empty")    
        value = int(value)
    elif key in ("ENTRY", "EXIT"):
        parts = value.split(",")
        if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
            raise ValueError(f"{key} must be in format x,y. Got: {value}")
        value = tuple(int(p.strip()) for p in parts)
    elif key == "PERFECT":
        value = value.lower()
        if value not in ("true", "false"):
            raise ValueError(f"PERFECT must be True or False. Got: {value}")
        value = value == "true"
    elif key == "SEED":
        if value == "":
            raise ValueError("invalid input seed can just be "
                  "(int, float, str, bytes, None)")
    elif key == "OUTPUT_FILE":
        try:
            open(value, "w")
        except Exception:
            raise InvalideValue("OUTPUT_FILE cannot be directory")
        if not value:
            raise InvalideValue("OUTPUT_FILE cannot be '/' or empty")

    if key not in {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"}:
        raise InvalideValue(f"Unknown key: {key}")

    return key, value


def validate_config(config: dict):
    required_keys = {
        "WIDTH", "HEIGHT", "ENTRY",
        "EXIT", "OUTPUT_FILE",
        "PERFECT",
    }

    missing = required_keys - config.keys()
    if missing:
        raise ValueError(f"Missing configuration keys: {missing}")

    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        raise ValueError("WIDTH and HEIGHT must be greater than 0")

    x_entry, y_entry = config["ENTRY"]
    x_exit, y_exit = config["EXIT"]

    if not (0 <= x_entry < config["WIDTH"] and 0 <= y_entry < config["HEIGHT"]):
        raise ValueError("ENTRY is outside maze bounds")

    if not (0 <= x_exit < config["WIDTH"] and 0 <= y_exit < config["HEIGHT"]):
        raise ValueError("EXIT is outside maze bounds")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("Entry point and Exit point cannot be the same")


def read_file(path="config.txt"):
    config = {}

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = parsing_line(line)
            if key not in config:
                config[key] = value

    validate_config(config)
    return config
