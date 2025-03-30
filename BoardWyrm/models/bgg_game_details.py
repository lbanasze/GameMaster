from typing import Dict, Any, Optional
from pydantic import BaseModel, model_validator, Field


class BggGameDetailsLink(BaseModel):
    """Represents a link associated with a board game"""
    id: int
    kind: str = Field(alias="type")
    value: str


class BggGameDetailsName(BaseModel):
    """Represents the alternative name information of a board game"""
    value: str
    kind: str = Field(alias="type")
    sort_index: int = Field(alias="sortindex")


class BggGameDetailsPoll(BaseModel):
    """Represents poll information related to a board game"""
    name: str
    title: str
    total_votes: int = Field(alias="totalvotes")


class BggGameDetailsPollSummary(BaseModel):
    """Represents a summary of poll information for a board game"""
    name: str
    title: str


class BggGameDetails(BaseModel):
    """Describes game details fetched from Board Game Geek"""
    id: int
    description: str
    image: str
    maxplayers: int
    maxplaytime: int
    minage: int
    minplayers: int
    playingtime: int
    thumbnail: str
    game_type: Optional[str] = None
    year_published: str = Field(alias="yearpublished")
    link: BggGameDetailsLink
    name: BggGameDetailsName
    poll: BggGameDetailsPoll
    poll_summary: BggGameDetailsPollSummary = Field(alias="poll-summary")

    @model_validator(mode="before")
    @classmethod
    def unwrap_values(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unwraps values from the data dictionary.

        If a field value is a dictionary with a single 'value' key,
        its value is extracted and used directly.
        """
        unwrapped_data = {}

        for field_name, field_value in data.items():
            if (
                isinstance(field_value, dict)
                and len(field_value) == 1
                and "value" in field_value
            ):
                unwrapped_data[field_name] = field_value["value"]
            else:
                unwrapped_data[field_name] = field_value

        return unwrapped_data
