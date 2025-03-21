import requests
import time
import xml.etree.ElementTree as ET 

small_collection_user = "thebigbuggyboo" # < 20 games
mid_collection_user = ""
huge_collection_user = "Tazzmann" # > 850 games

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
    item_elements = root.findall('./item')
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
    resp = requests.get(f"https://boardgamegeek.com/xmlapi2/collection?username={username}&own=1&subtype={subtype}&stats=1")
    if resp.status_code != 200:
        return None
    end_time = time.time()
    print(f"Request for collection by username took {end_time - start_time} seconds")

    root = ET.fromstring(resp.text)
    collection = parse_xml_items(root)

    return collection

def get_bgg_game_details(game_id):
    resp = requests.get(f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}")
    if resp.status_code != 200:
        return None

    root = ET.fromstring(resp.text)
    game = parse_xml_items(root)
    return game

def main():
    # parse_bgg_user_collection()
    start_time = time.time()
    boardgames = get_bgg_user_collection(huge_collection_user)
    end_time = time.time()
    print(f"Querying {len(boardgames)} took {end_time - start_time} seconds.")
    
    i = 1
    time_total = 0
    for game in boardgames:
        start_time = time.time()
        get_bgg_game_details(game["objectid"])
        end_time = time.time()
        delta = end_time - start_time
        time_total += delta
        print(f"Requesting details for game {i}/{len(boardgames)} took {delta} seconds.")
        i += 1

    print(f"Requesting details for {len(boardgames)} took {time_total} seconds.")

# main()
