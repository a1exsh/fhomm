from collections import namedtuple

# List of monsters in the order of resources: 0-27
Monster = namedtuple('Monster', ['name'], module='fhomm.game')

# TODO: support translations!
MONSTERS = [
    Monster("Peasant"),
    Monster("Archer"),
    Monster("Pikeman"),
    Monster("Swordsman"),
    Monster("Cavalry"),
    Monster("Paladdin"),
    Monster("Goblin"),
    Monster("Orc"),
    Monster("Wolf"),
    Monster("Ogre"),
    Monster("Troll"),
    Monster("Cyclops"),
    Monster("Sprite"),
    Monster("Dwarf"),
    Monster("Elf"),
    Monster("Druid"),
    Monster("Unicorn"),
    Monster("Phoenix"),
    Monster("Centaur"),
    Monster("Gargoyle"),
    Monster("Griffin"),
    Monster("Minotaur"),
    Monster("Hydra"),
    Monster("Dragon"),
    Monster("Rogue"),
    Monster("Nomad"),
    Monster("Ghost"),
    Monster("Genie"),
]
