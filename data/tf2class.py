import enum
from util import jsonreader

classes = {
    "scout",
    "soldier",
    "pyro",
    "demoman",
    "heavy",
    "engineer",
    "medic",
    "sniper",
    "spy"
}

class TF2Character:
    def __init__(self, asName):
        lowername = asName.lower()
        if lowername not in classes:
            raise ValueError(f"'{asName}' is not a valid TF2 class.")

        data = jsonreader.read("./data/tf2.json")
        self.name = lowername
        self.thumbnail = data[lowername]["_thumb"]
        self.description = data[lowername]["_desc"]

    def __str__(self):
        return f"{self.name} ({self.role}) - Weapon: {self.weapon}"