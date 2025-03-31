from typing import Dict, Any, Optional
from pydantic import BaseModel, model_validator, Field

class BggCollectableStats(BaseModel):
    max_players: int = Field(alias="maxplayers")
    min_players: int = Field(alias="minplayers")
    max_playtime: int = Field(alias="maxplaytime")
    min_playtime: int = Field(alias="minplaytime")
    num_owned: int = Field(alias="numowned")
    playing_time: int = Field(alias="playingtime")


class BggCollectableStatus(BaseModel):
    for_trade: int = Field(alias="fortrade")
    # REVIEW: can we turn this into a date type?
    last_modified: str = Field(alias="lastmodified")
    own: int
    pre_ordered: int = Field(alias="preordered")
    prev_owned: int = Field(alias="prevowned")
    want: int
    want_to_buy: int = Field(alias="wanttobuy")
    want_to_play: int = Field(alias="wanttoplay")
    wishlist: int


class BggCollectable(BaseModel):
    collection_id: int = Field(alias="collid")
    image: str
    name: str
    num_plays: int = Field(alias="numplays")
    object_id: int = Field(alias="objectid")
    object_type: str = Field(alias="objecttype")
    subtype: str
    thumbnail: str
    yearpublished: int
    stats: BggCollectableStats
    status: BggCollectableStatus
