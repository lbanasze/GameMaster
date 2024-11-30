from enum import Enum
import random

name_bank = ["Aimee", "Alvin", "Alyse", "Anders", "Bhea", "Billi", "Braden", "Buford", "Cesspyr", "Cinder", "Cloak", "Constance", "Dawna", "Dewly", "Doneel", "Dugan", "Ellaine", "Emmie", "Ewan", "Eward", "Flannera", "Fog", "Foster", "Frink", "Gemma", "Golden", "Greta", "Gustav", "Harper", "Henny", "Hinnic", "Howerd", "Igrin", "Ilso", "Inda", "Irwen", "Jacly", "Jasper", "Jinx", "Johann", "Keilee", "Keera", "Kagan", "Konnor", "Laina", "Lindyn", "Lockler", "Longtooth", "Masgood", "Mint", "Monca", "Murty", "Nail", "Nan", "Nigel", "Nomi", "Olaga", "Omin", "Orry", "Oxley", "Pattee", "Phona", "Pintin", "Prewitt", "Quay", "Quentin", "Quill", "Quinella", "Reece", "Rhodia", "Roric", "Rose", "Sarra", "Selwin", "Sorin", "Stasee", "Tammora", "Thickfur", "Timber", "Tondric", "Ulveny", "Ulvid", "Ummery", "Urma", "Vance", "Vennic",  "Vittora", "Vost", "Wanda", "Wettlecress", "Whickam", "Woodleaf", "Xander", "Xara", "Xeelie", "Xim", "Yasmin", "Yates", "Yolenda", "Yotterie", "Zachrie", "Zain", "Zoic", "Zola"]
name_enums = Enum('Name', [(name_bank[i], i) for i in range(len(name_bank))])

species_bank = ["badger", "beaver", "bluejay", "cat", "fox", "hawk", "lizard", "mouse", "opossum", "otter", "owl", "rabbit", "raccoon", "squirrel", "wolf"]
species_enums = Enum('Species', [(species_bank[i], i) for i in range(len(species_bank))])

drive_bank = ["to get revenge", "to get rich", "to make family safe", "to make home safe", "to gain power", "to explore", "to build something magnificent", "to resist invaders", "to defend the weak", "to destroy an enemy", "to wage war", "to prove worth", "to undermine a figure of power", "to find comfort", "to serve a higher cause", "to escape", "to negotiate peaceful resolutions", "to survive at all costs", "to earn social status and position", "to take control", "to exert power and authority on others", "to lay waste"]
drive_enums = Enum('Drive', [(drive_bank[i], i) for i in range(len(drive_bank))])

class HarmTrack:
    def __init__(self, injury: int, exhaustion: int, wear: int, morale: int):
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

HARM_TRACKS = {
    "standard": HarmTrack(1, 1, 1, 1), 
    "brute": HarmTrack(3, 2, 3, 2),
    "leader": HarmTrack(1, 2, 1, 3),
    "lieutenant": HarmTrack(2, 2, 3, 3),
    "bear": HarmTrack(5, 5, 2, 4)
}

class Attack:
    def __init__(self, name: str, injury=0, exhaustion=0, wear=0):
        self.name = name,
        self.injury = injury, 
        self.exhaustion = exhaustion,
        self.wear = wear

class NPC:
    def __init__(self, name=None, species=None, drive=None, attack=None, harm_track=None):
        self.name = name if name else random.choice(list(name_enums))
        self.species = species if species else random.choice(list(species_enums))
        self.drive = drive if drive else random.choice(list(drive_enums))
        self.harm_track = HARM_TRACKS[harm_track] if harm_track else HARM_TRACKS["standard"]
        self.attack = attack

    def __str__(self):
        return f"Name: {self.name.name.title()}\nSpecies: {self.species.name.title()}\nDrive: {self.drive.name.capitalize()}\nHarm track:\t{str(self.harm_track)}"

print(NPC(harm_track="brute"))