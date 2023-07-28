from typing import Dict, Optional

from BaseClasses import Item, ItemClassification

base_id = 0xD00_000

class CaveStoryItemData:
    name: str
    classification: ItemClassification
    item_id: Optional[int]
    _cnt: int
    def __init__(self, name: str, classification: ItemClassification,
                 item_id: Optional[int]):
        self.name = name
        self.classification = classification
        self.item_id = item_id

class CaveStoryItem(Item):
    game = "Cave Story"
    def __init__(self, name: str, classification: ItemClassification,
                 item_id: Optional[int], player: int):
        super().__init__(name, classification, item_id, player)

ALL_ITEMS: Dict[str, CaveStoryItemData] = {
    # C=Custom Container, N=NPC or TSC gift, E=Extra commands needed
    ## Start of inventory items
    # No item
    "Arthur's Key": CaveStoryItemData("Arthur's Key", ItemClassification.progression, base_id+1),
    "Map System": CaveStoryItemData("Map System", ItemClassification.progression, base_id+2),
    #C"Santa's Key": CaveStoryItemData("Santa's Key", ItemClassification.progression, base_id+3),
    "Silver Locket": CaveStoryItemData("Silver Locket", ItemClassification.progression, base_id+4),
    # Beast Fang
    # Life Capsule
    "ID Card": CaveStoryItemData("ID Card", ItemClassification.progression, base_id+7),
    #C"Jellyfish Juice": CaveStoryItemData("Jellyfish Juice", ItemClassification.progression, base_id+8),
    #N"Rusty Key": CaveStoryItemData("Rusty Key", ItemClassification.progression, base_id+9),
    #N"Gum Key": CaveStoryItemData("Gum Key", ItemClassification.progression, base_id+10),
    #E"Gum Base": CaveStoryItemData("Gum Base", ItemClassification.progression, base_id+11),
    #C"Charcoal": CaveStoryItemData("Charcoal", ItemClassification.progression, base_id+12),
    #E"Bomb": CaveStoryItemData("Bomb", ItemClassification.progression, base_id+13),
    # Puppy
    #N"Life Pot": CaveStoryItemData("Life Pot", ItemClassification.progression, base_id+15),
    #E"Cure-All": CaveStoryItemData("Cure-All", ItemClassification.progression, base_id+16),
    #N"Clinic Key": CaveStoryItemData("Clinic Key", ItemClassification.progression, base_id+17),
    #N"Booster 0.8": CaveStoryItemData("Booster 0.8", ItemClassification.progression, base_id+18),
    "Arms Barrier": CaveStoryItemData("Arms Barrier", ItemClassification.progression, base_id+19),
    #N"Turbocharge": CaveStoryItemData("Turbocharge", ItemClassification.progression, base_id+20),
    #N"Curly's Air Tank": CaveStoryItemData("Curly's Air Tank", ItemClassification.progression, base_id+21),
    #E"Nikumaru Counter": CaveStoryItemData("Nikumaru Counter", ItemClassification.progression, base_id+22),
    #N"Booster 2.0": CaveStoryItemData("Booster 2.0", ItemClassification.progression, base_id+23),
    #N"Mimiga Mask": CaveStoryItemData("Mimiga Mask", ItemClassification.progression, base_id+24),
    #C"Teleporter Key": CaveStoryItemData("Teleporter Key", ItemClassification.progression, base_id+25),
    #N"Sue's Letter": CaveStoryItemData("Sue's Letter", ItemClassification.progression, base_id+26),
    #N"Controller": CaveStoryItemData("Controller", ItemClassification.progression, base_id+27),
    #N"Broken Sprinkler": CaveStoryItemData("Broken Sprinkler", ItemClassification.progression, base_id+28),
    #N"Sprinkler": CaveStoryItemData("Sprinkler", ItemClassification.progression, base_id+29),
    "Tow Rope": CaveStoryItemData("Tow Rope", ItemClassification.progression, base_id+30),
    #N"Clay Figure Metal": CaveStoryItemData("Clay Figure Metal", ItemClassification.progression, base_id+31),
    #N"Little Man": CaveStoryItemData("Little Man", ItemClassification.progression, base_id+32),
    #N"Mushroom Badge": CaveStoryItemData("Mushroom Badge", ItemClassification.progression, base_id+33),
    #N"Ma Pignon": CaveStoryItemData("Ma Pignon", ItemClassification.progression, base_id+34),
    "Curly's Panties": CaveStoryItemData("Curly's Panties", ItemClassification.progression, base_id+35),
    #N"Alien Metal": CaveStoryItemData("Alien Metal", ItemClassification.progression, base_id+36),
    #N"Chaco's Lipstick": CaveStoryItemData("Chaco's Lipstick", ItemClassification.progression, base_id+37),
    #N"Whimsical Star": CaveStoryItemData("Whimsical Star", ItemClassification.progression, base_id+38),
    #N"Iron Bond": CaveStoryItemData("Iron Bond", ItemClassification.progression, base_id+39),
    ## Start of weapons
    # None
    #"Snake": CaveStoryItemData("Snake", ItemClassification.useful, base_id+101),
    "Polar Star": CaveStoryItemData("Polar Star", ItemClassification.progression, base_id+102),
    #"Fireball": CaveStoryItemData("Fireball", ItemClassification.progression, base_id+103),
    #"Machine Gun": CaveStoryItemData("Machine Gun", ItemClassification.useful, base_id+104),
    "Progressive Missile Launcher": CaveStoryItemData("Progressive Missile Launcher", ItemClassification.progression, base_id+105),
    # Unused
    #"Bubbler": CaveStoryItemData("Bubbler", ItemClassification.useful, base_id+107),
    # Unused
    #"Blade": CaveStoryItemData("Blade", ItemClassification.useful, base_id+109),
    #MERGED to 105 "Super Missile Launcher": CaveStoryItemData("Super Missile Launcher", ItemClassification.useful, base_id+110),
    # Unused
    #"Nemesis": CaveStoryItemData("Nemesis", ItemClassification.useful, base_id+112),
    #"Spur": CaveStoryItemData("Spur", ItemClassification.useful, base_id+113),
    ## Start of upgrades
    "+3 Life Capsule": CaveStoryItemData("+3 Life Capsule", ItemClassification.useful, base_id+201),
    "+4 Life Capsule": CaveStoryItemData("+4 Life Capsule", ItemClassification.useful, base_id+202),
    "+5 Life Capsule": CaveStoryItemData("+5 Life Capsule", ItemClassification.useful, base_id+203),
    "+5 Missile Ammo": CaveStoryItemData("+5 Missile Ammo", ItemClassification.useful, base_id+204),
    #"+24 Missile Ammo": CaveStoryItemData("+24 Missile Ammo", ItemClassification.useful, base_id+205),
    ## Start of filler
    #"Heart Bundle": CaveStoryItemData("Heart Bundle", ItemClassification.useful, base_id+301), #+6 HP
    #"Missile Bundle": CaveStoryItemData("Missile Bundle", ItemClassification.useful, base_id+301), #+3 Missiles
    #"Energy Bundle": CaveStoryItemData("Energy Bundle", ItemClassification.useful, base_id+301), #+20 Energy
}

DUPES = {
    #E"Progressive Missile Launcher": 1,
    #N"Progressive Booster": 1,
    "+3 Life Capsule": 2,
    "+4 Life Capsule": 1,
    "+5 Life Capsule": 6,
    "+5 Missile Ammo": 1, #3
}