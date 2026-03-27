import yaml

class Secrets:
    def __init__(self) -> None:
        self.config = yaml.safe_load(open("./secrets.yml"))

secrets = Secrets()
