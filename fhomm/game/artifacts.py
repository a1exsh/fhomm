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
    ['name', 'modifiers'],
    defaults=[Modifiers()],
    module='fhomm.game',
)

# TODO: support translations!
ARTIFACTS = [
    Artifact(
        "Ultimate Book of Knowledge",
        Modifiers(knowledge=+12),
    ),
    Artifact(
        "Ultimate Sword of Dominion",
        Modifiers(attack=+12),
    ),
    Artifact(
        "Ultimate Cloack of Protection",
        Modifiers(defense=+12),
    ),
    Artifact(
        "Ultimate Wand of Power",
        Modifiers(power=+12),
    ),
    Artifact("Arcane Necklace"),
    Artifact("Caster's Bracelet"),
    Artifact("Mage's Ring"),
    Artifact("Witch's Broach"),
    Artifact("Medal of Valor"),
    Artifact("Medal of Courage"),
    Artifact("Medal of Honor"),
    Artifact("Medal of Distinction"),
    Artifact("Fizbin of Misfortune"),
    Artifact("Thunder Mace"),
    Artifact("Armored Gauntlet"),
    Artifact("Defender Helm"),
    Artifact("Giant Flail"),
    Artifact("Ballista of Quickness"),
    Artifact("Stealth Shield"),
    Artifact("Dragon Sword"),
    Artifact("Power Axe"),
    Artifact("Divine Breastplate"),
    Artifact("Minor Scroll"),
    Artifact("Major Scroll"),
    Artifact("Superior Scroll"),
    Artifact("Foremost Scroll"),
    Artifact("Endless Sack"),
    Artifact("Endless Bag"),
    Artifact("Endless Purse"),
    Artifact("Nomad's Boots"),
    Artifact("Traveler's Boots"),
    Artifact("Rabbit's Foot"),
    Artifact("Golden Horseshoe"),
    Artifact("Gambler's Coin"),
    Artifact("Lucky Clover"),
    Artifact("True Compass of Mobility"),
    Artifact("Astrolabe"),
    Artifact("Magic Book"),
]
