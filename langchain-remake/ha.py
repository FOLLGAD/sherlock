import requests
import os

access_token = os.getenv("HASS_TOKEN")
url = os.getenv("HASS_SERVER")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

def ha_entities():
    response = requests.get(url + "/api/states", headers=headers)
    entities = response.json()

    ls = ["entity_id\tfriendly_name\tstate"] + [f"{e['entity_id']}\t\"{e['attributes']['friendly_name']}\"\t{e['state']}" for e in entities]

    return ls

def play_music(spotify_uri: str):
    # Construct the API endpoint URL
    play_media_url = f"{url}/api/services/media_player/play_media"

    payload = {
        "entity_id": "media_player.spotify_emil",
        "media_content_id": spotify_uri,
        "media_content_type": spotify_uri.split(":")[1],
    }

    response = requests.post(play_media_url, json=payload, headers=headers)
    print(response.json())

    return response.status_code

if __name__ == "__main__":
    e = ha_entities()
    lines = "\n".join(e)
    print(lines)
