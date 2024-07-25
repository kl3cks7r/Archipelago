from typing import Dict, Optional

from BaseClasses import Item, ItemClassification

base_id = 0xD00_000


class CaveStoryItemData:
    classification: ItemClassification
    item_id: Optional[int]
    cnt: int
    def __init__(self, classification: ItemClassification,
                 item_id: Optional[int], cnt: int = 1):
        self.classification = classification
        self.item_id = item_id
        self.cnt = cnt


class CaveStoryItem(Item):
    game = "Cave Story"

    def __init__(self, name: str, classification: ItemClassification,
                 item_id: Optional[int], player: int):
        super().__init__(name, classification, item_id, player)


ALL_ITEMS: Dict[str, CaveStoryItemData] = {
    # Start of inventory items
    "Progressive Polar Star": CaveStoryItemData(ItemClassification.progression, base_id + 2, 2),
    "Fireball": CaveStoryItemData(ItemClassification.progression, base_id + 4),
    "Snake": CaveStoryItemData(ItemClassification.useful, base_id + 5),
    "Bubbler": CaveStoryItemData(ItemClassification.useful, base_id + 7),
    "Machine Gun": CaveStoryItemData(ItemClassification.progression, base_id + 8),
    "Blade": CaveStoryItemData(ItemClassification.progression, base_id + 9),
    "Nemesis": CaveStoryItemData(ItemClassification.useful, base_id + 10),
    "+3 Life Capsule": CaveStoryItemData(ItemClassification.useful, base_id + 12, 3),
    "+4 Life Capsule": CaveStoryItemData(ItemClassification.useful, base_id + 13, 2),
    "+5 Life Capsule": CaveStoryItemData(ItemClassification.useful, base_id + 14, 7),
    "Puppy": CaveStoryItemData(ItemClassification.progression, base_id + 20, 5),
    "Missile Expansion": CaveStoryItemData(ItemClassification.useful, base_id + 30, 5),
    "Super Missile Launcher": CaveStoryItemData(ItemClassification.useful, base_id + 34),
    "Hell Missile Expansion": CaveStoryItemData(ItemClassification.useful, base_id + 35),
    "Arthur's Key": CaveStoryItemData(ItemClassification.progression, base_id + 51),
    "Map System": CaveStoryItemData(ItemClassification.useful, base_id + 52),
    "Santa's Key": CaveStoryItemData(ItemClassification.progression, base_id + 53),
    "Silver Locket": CaveStoryItemData(ItemClassification.progression, base_id + 54),
    "ID Card": CaveStoryItemData(ItemClassification.progression, base_id + 57),
    "Jellyfish Juice": CaveStoryItemData(ItemClassification.progression, base_id + 58),
    "Rusty Key": CaveStoryItemData(ItemClassification.progression, base_id + 59),
    "Gum Key": CaveStoryItemData(ItemClassification.progression, base_id + 60),
    "Gum Base": CaveStoryItemData(ItemClassification.progression, base_id + 61),
    "Charcoal": CaveStoryItemData(ItemClassification.progression, base_id + 62),
    "Explosive": CaveStoryItemData(ItemClassification.progression, base_id + 63),
    "Life Pot": CaveStoryItemData(ItemClassification.useful, base_id + 65),
    "Cure-All": CaveStoryItemData(ItemClassification.progression, base_id + 66),
    "Clinic Key": CaveStoryItemData(ItemClassification.progression, base_id + 67),
    "Progressive Booster": CaveStoryItemData(ItemClassification.progression, base_id + 68, 2),
    "Arms Barrier": CaveStoryItemData(ItemClassification.useful, base_id + 69),
    "Turbocharge": CaveStoryItemData(ItemClassification.useful, base_id + 70),
    "Curly's Air Tank": CaveStoryItemData(ItemClassification.progression, base_id + 71),
    "Nikumaru Counter": CaveStoryItemData(ItemClassification.filler, base_id + 72),
    "Mimiga Mask": CaveStoryItemData(ItemClassification.progression, base_id + 74),
    "Teleporter Room Key": CaveStoryItemData(ItemClassification.progression, base_id + 75),
    "Sue's Letter": CaveStoryItemData(ItemClassification.progression, base_id + 76),
    "Controller": CaveStoryItemData(ItemClassification.progression, base_id + 77),
    "Broken Sprinkler": CaveStoryItemData(ItemClassification.progression, base_id + 78),
    "Sprinkler": CaveStoryItemData(ItemClassification.progression, base_id + 79),
    "Tow Rope": CaveStoryItemData(ItemClassification.progression, base_id + 80),
    "Clay Figure Medal": CaveStoryItemData(ItemClassification.filler, base_id + 81),
    "Little Man": CaveStoryItemData(ItemClassification.progression, base_id + 82),
    "Mushroom Badge": CaveStoryItemData(ItemClassification.progression, base_id + 83),
    "Ma Pignon": CaveStoryItemData(ItemClassification.progression, base_id + 84),
    "Curly's Panties": CaveStoryItemData(ItemClassification.filler, base_id + 85),
    "Alien Medal": CaveStoryItemData(ItemClassification.filler, base_id + 86),
    "Chaco's Lipstick": CaveStoryItemData(ItemClassification.filler, base_id + 87),
    "Whimsical Star": CaveStoryItemData(ItemClassification.useful, base_id + 88),
    "Iron Bond": CaveStoryItemData(ItemClassification.progression, base_id + 89),
}

FILLER_ITEMS: Dict[str, CaveStoryItemData] = {
    "Refill Station": CaveStoryItemData(ItemClassification.filler, base_id + 17),
}

TRAP_ITEMS: Dict[str, CaveStoryItemData] = {
    "Black Wind": CaveStoryItemData(ItemClassification.filler, base_id + 110),
}
