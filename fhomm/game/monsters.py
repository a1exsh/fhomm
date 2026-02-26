from collections import namedtuple

# List of monsters in the order of resources: 0-27
Monster = namedtuple(
    'Monster',
    ['id', 'name', 'icn_name'],
    module='fhomm.game',
)

# TODO: support translations!
MONSTERS = [
    Monster( 0, "Peasant",      'peasant'),
    Monster( 1, "Archer",       'archer'),
    Monster( 2, "Pikeman",      'pikeman'),
    Monster( 3, "Swordsman",    'swrdsman'),
    Monster( 4, "Cavalry",      'cavalry'),
    Monster( 5, "Paladin",      'paladin'),
    Monster( 6, "Goblin",       'goblin'),
    Monster( 7, "Orc",          'orc'),
    Monster( 8, "Wolf",         'wolf'),
    Monster( 9, "Ogre",         'ogre'),
    Monster(10, "Troll",        'troll'),
    Monster(11, "Cyclops",      'cyclops'),
    Monster(12, "Sprite",       'sprite'),
    Monster(13, "Dwarf",        'dwarf'),
    Monster(14, "Elf",          'elf'),
    Monster(15, "Druid",        'druid'),
    Monster(16, "Unicorn",      'unicorn'),
    Monster(17, "Phoenix",      'phoenix'),
    Monster(18, "Centaur",      'centaur'),
    Monster(19, "Gargoyle",     'gargoyle'),
    Monster(20, "Griffin",      'griffin'),
    Monster(21, "Minotaur",     'minotaur'),
    Monster(22, "Hydra",        'hydra'),
    Monster(23, "Dragon",       'dragon'),
    Monster(24, "Rogue",        'rogue'),
    Monster(25, "Nomad",        'nomad'),
    Monster(26, "Ghost",        'ghost'),
    Monster(27, "Genie",        'genie'),
]

# list of monster icn_name's that have a .wip icon set
WIP_ICN_MONSTERS = set([
    'archer',
    'cavalry',
    'centaur',
    'cyclops',
    'druid',
    'dwarf',
    'elf',
    'goblin',
    'hydra',
    'minotaur',
    'nomad',
    'ogre',
    'orc',
    'paladin',
    'peasant',
    'pikeman',
    'rogue',
    'swrdsman',
    'troll',
    'unicorn',
    'wolf',
])
