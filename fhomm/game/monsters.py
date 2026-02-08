from collections import namedtuple

# List of monsters in the order of resources: 0-27
Monster = namedtuple('Monster', ['id', 'name'], module='fhomm.game')

# TODO: support translations!
MONSTERS = [
    Monster( 0, "Peasant"),
    Monster( 1, "Archer"),
    Monster( 2, "Pikeman"),
    Monster( 3, "Swordsman"),
    Monster( 4, "Cavalry"),
    Monster( 5, "Paladdin"),
    Monster( 6, "Goblin"),
    Monster( 7, "Orc"),
    Monster( 8, "Wolf"),
    Monster( 9, "Ogre"),
    Monster(10, "Troll"),
    Monster(11, "Cyclops"),
    Monster(12, "Sprite"),
    Monster(13, "Dwarf"),
    Monster(14, "Elf"),
    Monster(15, "Druid"),
    Monster(16, "Unicorn"),
    Monster(17, "Phoenix"),
    Monster(18, "Centaur"),
    Monster(19, "Gargoyle"),
    Monster(20, "Griffin"),
    Monster(21, "Minotaur"),
    Monster(22, "Hydra"),
    Monster(23, "Dragon"),
    Monster(24, "Rogue"),
    Monster(25, "Nomad"),
    Monster(26, "Ghost"),
    Monster(27, "Genie"),
]
