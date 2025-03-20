import requests
import xml.etree.ElementTree as ET 

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
            if text:
                item_properties[tag] = text
            elif attrib:
                item_properties[tag] = attrib

        
        items.append(item_properties)

    return items


def get_bgg_user_collection(username):
    resp = requests.get(f"https://boardgamegeek.com/xmlapi2/collection?username={username}")
    if resp.status_code != 200:
        return None

    root = ET.fromstring(resp.text)
    collection = parse_xml_items(root)
    """ 
    Example item from collection:

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

    boardgames = []
    for item in collection:
        if item.get("subtype") == "boardgame":
            new_boardgame = get_bgg_game(item.get("objectid"))
            if new_boardgame:
                boardgames.append(new_boardgame)
    
    return boardgames

def get_bgg_game(game_id):
    resp = requests.get(f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}")
    if resp.status_code != 200:
        return None

    root = ET.fromstring(resp.text)
    game = parse_xml_items(root)
    return game

def main():
    # parse_bgg_user_collection()
    boardgames = get_bgg_user_collection("thebigbuggyboo")
    print(boardgames)


main()