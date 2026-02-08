from collections import namedtuple

# import fhomm.game.heroes

Modifiers = namedtuple(
    'Modifiers',
    ['attack', 'defense', 'power', 'knowledge', 'morale', 'luck', 'gold'],
    defaults=[0, 0, 0, 0, 0, 0, 0],
    module='fhomm.game.artifacts',
)

# List of artifacts in the order of resources: 0-37
Artifact = namedtuple(
    'Artifact',
    ['id', 'name', 'modifiers'],
    defaults=[Modifiers()],
    module='fhomm.game',
)

# TODO: support translations!
ARTIFACTS = [
    Artifact(
        0,
        "Ultimate Book of Knowledge",
        Modifiers(knowledge=+12),
    ),
    Artifact(
        1,
        "Ultimate Sword of Dominion",
        Modifiers(attack=+12),
    ),
    Artifact(
        2,
        "Ultimate Cloack of Protection",
        Modifiers(defense=+12),
    ),
    Artifact(
        3,
        "Ultimate Wand of Power",
        Modifiers(power=+12),
    ),
    Artifact( 4, "Arcane Necklace"),
    Artifact( 5, "Caster's Bracelet"),
    Artifact( 6, "Mage's Ring"),
    Artifact( 7, "Witch's Broach"),
    Artifact( 8, "Medal of Valor"),
    Artifact( 9, "Medal of Courage"),
    Artifact(10, "Medal of Honor"),
    Artifact(11, "Medal of Distinction"),
    Artifact(12, "Fizbin of Misfortune"),
    Artifact(13, "Thunder Mace"),
    Artifact(14, "Armored Gauntlet"),
    Artifact(15, "Defender Helm"),
    Artifact(16, "Giant Flail"),
    Artifact(17, "Ballista of Quickness"),
    Artifact(18, "Stealth Shield"),
    Artifact(19, "Dragon Sword"),
    Artifact(20, "Power Axe"),
    Artifact(21, "Divine Breastplate"),
    Artifact(22, "Minor Scroll"),
    Artifact(23, "Major Scroll"),
    Artifact(24, "Superior Scroll"),
    Artifact(25, "Foremost Scroll"),
    Artifact(26, "Endless Sack"),
    Artifact(27, "Endless Bag"),
    Artifact(28, "Endless Purse"),
    Artifact(29, "Nomad's Boots"),
    Artifact(30, "Traveler's Boots"),
    Artifact(31, "Rabbit's Foot"),
    Artifact(32, "Golden Horseshoe"),
    Artifact(33, "Gambler's Coin"),
    Artifact(34, "Lucky Clover"),
    Artifact(35, "True Compass of Mobility"),
    Artifact(36, "Astrolabe"),
    Artifact(37, "Magic Book"),
]
