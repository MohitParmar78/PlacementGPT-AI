import json


def load_role_skills():

    with open(
        "data/roles/role_skills.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)