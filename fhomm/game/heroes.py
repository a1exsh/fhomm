from collections import namedtuple

# List of heroes names (later: with starting stats), in the order of portrait resources: 0-35
Hero = namedtuple('Hero', ['kind', 'name'], module='fhomm.game')

Kind = namedtuple('Kind', ['name', 'default_stats'], module='fhomm.game.heroes')

Stats = namedtuple(
    'Stats',
    ['attack', 'defense', 'power', 'knowledge'],
    module='fhomm.game.heroes',
)

KNIGHT    = Kind('Knight',    Stats(1, 2, 1, 1))
BARBARIAN = Kind('Barbarian', Stats(2, 1, 1, 1))
SORCERESS = Kind('Sorceress', Stats(0, 0, 2, 3))
WARLOCK   = Kind('Warlock',   Stats(0, 0, 3, 2))

KINDS = [KNIGHT, BARBARIAN, SORCERESS, WARLOCK]

# TODO: support translations!
HEROES = [
    # KNIGHT
    Hero(KNIGHT, "Lord Kilburn"),
    Hero(KNIGHT, "Lord Haart"),
    Hero(KNIGHT, "Sir Gallant"),
    Hero(KNIGHT, "Arturius"),
    Hero(KNIGHT, "Tyro"),
    Hero(KNIGHT, "Maximus"),
    Hero(KNIGHT, "Ector"),
    Hero(KNIGHT, "Dimitri"),
    Hero(KNIGHT, "Ambrose"),
    # BARBARIAN
    Hero(BARBARIAN, "Thundax"),
    Hero(BARBARIAN, "Ergon"),
    Hero(BARBARIAN, "Kelzen"),
    Hero(BARBARIAN, "Tsabu"),
    Hero(BARBARIAN, "Crag Hack"),
    Hero(BARBARIAN, "Jojosh"),
    Hero(BARBARIAN, "Atlas"),
    Hero(BARBARIAN, "Yog"),
    Hero(BARBARIAN, "Antoine"),
    # SORCERESS
    Hero(SORCERESS, "Ariel"),
    Hero(SORCERESS, "Vatawna"),
    Hero(SORCERESS, "Carlawn"),
    Hero(SORCERESS, "Rebecca"),
    Hero(SORCERESS, "Luna"),
    Hero(SORCERESS, "Astra"),
    Hero(SORCERESS, "Natasha"),
    Hero(SORCERESS, "Gem"),
    Hero(SORCERESS, "Troyan"),
    # WARLOCK
    Hero(WARLOCK, "Agar"),
    Hero(WARLOCK, "Crodo"),
    Hero(WARLOCK, "Falagar"),
    Hero(WARLOCK, "Barok"),
    Hero(WARLOCK, "Airie"),
    Hero(WARLOCK, "Kastore"),
    Hero(WARLOCK, "Sandro"),
    Hero(WARLOCK, "Wrathmont"),
    Hero(WARLOCK, "Vesper"),
]
