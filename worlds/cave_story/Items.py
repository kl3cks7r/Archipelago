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
    "Arthur's Key": CaveStoryItemData(ItemClassification.progression, base_id + 1),
    "Map System": CaveStoryItemData(ItemClassification.useful, base_id + 2),
    "Santa's Key": CaveStoryItemData(ItemClassification.progression, base_id + 3),
    "Silver Locket": CaveStoryItemData(ItemClassification.progression, base_id + 4),
    "ID Card": CaveStoryItemData(ItemClassification.progression, base_id + 7),
    "Jellyfish Juice": CaveStoryItemData(ItemClassification.progression, base_id + 8),
    "Rusty Key": CaveStoryItemData(ItemClassification.progression, base_id + 9),
    "Gum Key": CaveStoryItemData(ItemClassification.progression, base_id + 10),
    "Gum Base": CaveStoryItemData(ItemClassification.progression, base_id + 11),
    "Charcoal": CaveStoryItemData(ItemClassification.progression, base_id + 12),
    "Explosive": CaveStoryItemData(ItemClassification.progression, base_id + 13),
    "Puppy": CaveStoryItemData(ItemClassification.progression, base_id + 14, 5),
    "Life Pot": CaveStoryItemData(ItemClassification.useful, base_id + 15),
    "Cure-All": CaveStoryItemData(ItemClassification.progression, base_id + 16),
    "Clinic Key": CaveStoryItemData(ItemClassification.progression, base_id + 17),
    "Progressive Booster": CaveStoryItemData(ItemClassification.progression, base_id + 18, 2),
    "Arms Barrier": CaveStoryItemData(ItemClassification.useful, base_id + 19),
    "Turbocharge": CaveStoryItemData(ItemClassification.useful, base_id + 20),
    "Curly's Air Tank": CaveStoryItemData(ItemClassification.progression, base_id + 21),
    "Nikumaru Counter": CaveStoryItemData(ItemClassification.filler, base_id + 22),
    "Mimiga Mask": CaveStoryItemData(ItemClassification.progression, base_id + 24),
    "Teleporter Room Key": CaveStoryItemData(ItemClassification.progression, base_id + 25),
    "Sue's Letter": CaveStoryItemData(ItemClassification.progression, base_id + 26),
    "Controller": CaveStoryItemData(ItemClassification.progression, base_id + 27),
    "Broken Sprinkler": CaveStoryItemData(ItemClassification.progression, base_id + 28),
    "Sprinkler": CaveStoryItemData(ItemClassification.progression, base_id + 29),
    "Tow Rope": CaveStoryItemData(ItemClassification.progression, base_id + 30),
    "Clay Figure Medal": CaveStoryItemData(ItemClassification.filler, base_id + 31),
    "Little Man": CaveStoryItemData(ItemClassification.progression, base_id + 32),
    "Mushroom Badge": CaveStoryItemData(ItemClassification.progression, base_id + 33),
    "Ma Pignon": CaveStoryItemData(ItemClassification.progression, base_id + 34),
    "Curly's Panties": CaveStoryItemData(ItemClassification.filler, base_id + 35),
    "Alien Medal": CaveStoryItemData(ItemClassification.filler, base_id + 36),
    "Chaco's Lipstick": CaveStoryItemData(ItemClassification.filler, base_id + 37),
    "Whimsical Star": CaveStoryItemData(ItemClassification.useful, base_id + 38),
    "Iron Bond": CaveStoryItemData(ItemClassification.progression, base_id + 39),
    # Start of weapons
    "Snake": CaveStoryItemData(ItemClassification.useful, base_id + 101),
    "Progressive Polar Star": CaveStoryItemData(ItemClassification.progression, base_id + 102, 2),
    "Fireball": CaveStoryItemData(ItemClassification.progression, base_id + 103),
    "Machine Gun": CaveStoryItemData(ItemClassification.progression, base_id + 104),
    "Progressive Missile Launcher": CaveStoryItemData(ItemClassification.progression, base_id + 105, 2),
    "Bubbler": CaveStoryItemData(ItemClassification.useful, base_id + 107),
    "Blade": CaveStoryItemData(ItemClassification.progression, base_id + 109),
    "Nemesis": CaveStoryItemData(ItemClassification.useful, base_id + 112),
    # Start of life capsules:
    "+3 Life Capsule": CaveStoryItemData(ItemClassification.useful, base_id + 203, 3),
    "+4 Life Capsule": CaveStoryItemData(ItemClassification.useful, base_id + 204, 2),
    "+5 Life Capsule": CaveStoryItemData(ItemClassification.useful, base_id + 205, 7),
    # Start of missile ammo upgrades:
    "+5 Missile Expansion": CaveStoryItemData(ItemClassification.useful, base_id + 305, 4),
    "Hell Missile Expansion": CaveStoryItemData(ItemClassification.useful, base_id + 324),
    # Start of filler
    # "Heart Refill": CaveStoryItemData(ItemClassification.filler, base_id + 401),
    # "Missile Refill": CaveStoryItemData(ItemClassification.filler, base_id + 401),
    # "Energy Refill": CaveStoryItemData(ItemClassification.filler, base_id + 401),
}
