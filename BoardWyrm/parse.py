import json
import requests
import time
import xml.etree.ElementTree as ET

small_collection_user = "thebigbuggyboo"  # < 20 games
mid_collection_user = ""
huge_collection_user = "Tazzmann"  # > 850 games

""" 
    Example item from User collection:

    {
        "objecttype": "thing",
        "objectid": "359871",
        "subtype": "boardgame",
        "collid": "130489491",
        "name": "Arcs",
        "yearpublished": "2024",
        "image": "https://cf.geekdo-images.com/XWImAu_3RK61wbzcKboVdA__original/img/43ianMZOks7UHlZILx0VBRntOmM=/0x0/filters:format(png)/pic8145530.png",
        "thumbnail": "https://cf.geekdo-images.com/XWImAu_3RK61wbzcKboVdA__thumb/img/Ry-6KHwNgERWadyxs1X1_P3dMvY=/fit-in/200x150/filters:strip_icc()/pic8145530.png",
        "status": {
            "own": "1",
            "prevowned": "0",
            "fortrade": "0",
            "want": "0",
            "wanttoplay": "0",
            "wanttobuy": "0",
            "wishlist": "0",
            "preordered": "0",
            "lastmodified": "2025-03-18 19:37:10"
        },
        "numplays": "0"
    }  
"""


def parse_xml_items(root):
    """Parse a tree, look for "items", convert to json with all properties

    Args:
        tree (_type_): _description_

    Returns:
        _type_: _description_
    """
    item_elements = root.findall("./item")
    items = []
    for item in item_elements:
        item_properties = {}
        item_attrib = item.attrib
        for key, value in item_attrib.items():
            item_properties[key] = value
        for prop in item:
            tag = prop.tag
            text = prop.text
            attrib = prop.attrib
            if text and text.strip():
                item_properties[tag] = text
            elif attrib:
                item_properties[tag] = attrib

        items.append(item_properties)

    return items


def get_bgg_user_collection(username, subtype="boardgame"):
    start_time = time.time()
    resp = requests.get(
        f"https://boardgamegeek.com/xmlapi2/collection?username={username}&own=1&subtype={subtype}&stats=1"
    )
    if resp.status_code != 200:
        return None
    end_time = time.time()
    print(f"Request for collection by username took {end_time - start_time} seconds")

    root = ET.fromstring(resp.text)
    collection = parse_xml_items(root)

    return collection


def get_cached_bgg_game_details(game_ids):
    with open("all_cached_games.json", "r") as infile:
        all_cached_games = json.load(infile)

    cached_games = []
    uncached_game_ids = []
    for game_id in game_ids:
        if game_id in all_cached_games.keys():
            cached_games.append(all_cached_games[game_id])
        else:
            uncached_game_ids.append(game_id)

    return cached_games, uncached_game_ids


def get_bgg_game_details(game_id):
    resp = requests.get(f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}")
    if resp.status_code == 202:
        time.sleep(1)
        resp = requests.get(f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}")

    if resp.status_code == 429:  # Rate limit
        print("Hit rate limit, sleeping for 5 seconds")
        time.sleep(5)
        resp = requests.get(f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}")

    if resp.status_code != 200:
        print(f"Response code {resp.status_code}, {resp.text}")
        return []

    root = ET.fromstring(resp.text)
    game = parse_xml_items(root)
    return game


def batch_bgg_details(game_ids):
    # The API allows up to 20 ids per request, so chunk the game ids to improve the request efficiency
    chunked_game_ids = [game_ids[i : i + 20] for i in range(0, len(game_ids), 20)]
    game_details = {}
    i = 1
    time_total = 0
    for chunk in chunked_game_ids:
        start_time = time.time()
        new_game_details = get_bgg_game_details(",".join(chunk))
        for game in new_game_details:
            game_details[game["id"]] = game

        end_time = time.time()
        delta = end_time - start_time
        time_total += delta
        print(
            f"Requesting details for chunk {i}/{len(chunked_game_ids)} took {delta} seconds."
        )
        i += 1

    print(
        f"Requesting chunked details for {len(chunked_game_ids)} took {time_total} seconds."
    )

    return game_details


def main():
    # parse_bgg_user_collection()
    start_time = time.time()
    boardgames = get_bgg_user_collection(small_collection_user)
    end_time = time.time()
    print(f"Querying {len(boardgames)} took {end_time - start_time} seconds.")

    game_ids = [game["objectid"] for game in boardgames]
    cached_games, uncached_game_ids = get_cached_bgg_game_details(game_ids)
    game_details = batch_bgg_details(uncached_game_ids)

    print(game_details)


# main()
