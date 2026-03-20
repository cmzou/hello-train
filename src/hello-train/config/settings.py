import yaml

class Settings:
    def __init__(self) -> None:
        self.config = yaml.safe_load(open("./config.yml"))

settings = Settings()
