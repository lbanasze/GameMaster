from enum import Enum
import json
import random
import os


class Attack:
    def __init__(self, name: str, injury=0, exhaustion=0, wear=0):
        self.name = (name,)
        self.injury = (injury,)
        self.exhaustion = (exhaustion,)
        self.wear = wear


class HarmTrack:
    def __init__(self, injury=0, exhaustion=0, wear=0, morale=0):
        self.injury = injury
        self.exhaustion = exhaustion
        self.wear = wear
        self.morale = morale

    def __str__(self):
        return f"""
            Injury: {self.injury}
            Exhaustion: {self.exhaustion}
            Wear: {self.wear}
            Morale: {self.morale}
        """


class NPC:
    def __init__(
        self, name=None, species=None, drive=None, attack=None, harm_track=None
    ):
        self.name = name if name else random.choice(list(name_enums))
        self.species = species if species else random.choice(list(species_enums))
        self.drive = drive if drive else random.choice(list(drive_enums))
        self.harm_track = (
            HARM_TRACKS[harm_track] if harm_track else HARM_TRACKS["standard"]
        )
        self.attack = attack

    def __str__(self):
        return f"Name: {self.name.name.title()}\nSpecies: {self.species.name.title()}\nDrive: {self.drive.name.capitalize()}\nHarm track:\t{str(self.harm_track)}"


def initialize_data():
    with open("/Users/bug/github/GameMaster/GameMaster/root/root.json") as infile:
        root_data = json.load(infile)
        name_enums = Enum(
            "Name", [(root_data["names"][i], i) for i in range(len(root_data["names"]))]
        )
        species_enums = Enum(
            "Species",
            [(root_data["species"][i], i) for i in range(len(root_data["species"]))],
        )
        drive_enums = Enum(
            "Drive",
            [(root_data["drives"][i], i) for i in range(len(root_data["drives"]))],
        )
        harm_tracks = {
            key: HarmTrack(**value) for (key, value) in root_data["harm_tracks"].items()
        }

        return name_enums, species_enums, drive_enums, harm_tracks
