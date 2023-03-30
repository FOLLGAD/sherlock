import requests
import os

def ha_entities():
    access_token = os.getenv("HASS_TOKEN")
    url = os.getenv("HASS_SERVER")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url + "/api/states", headers=headers)
    entities = response.json()

    ls = ["entity_id\tfriendly_name\tstate"] + [f"{e['entity_id']}\t{e['attributes']['friendly_name']}\t{e['state']}" for e in entities]

    return ls

if __name__ == "__main__":
    e = ha_entities()
    lines = "\n".join(e)
    print(lines)