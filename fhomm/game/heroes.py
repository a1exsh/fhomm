from collections import namedtuple

# List of heroes names (later: with starting stats), in the order of portrait resources: 0-35
Hero = namedtuple('Hero', ['name'], module='fhomm.game')

# TODO: support translations!
HEROES = [
    Hero("Lord Kilburn"),
    Hero("Lord Haart"),
    Hero("Sir Gallant"),
    Hero("Arturius"),
    Hero("Tyro"),
    Hero("Maximus"),
    Hero("Ector"),
    Hero("Dimitri"),
    Hero("Ambrose"),
    Hero("Thundax"),
    Hero("Ergon"),
    Hero("Kelzen"),
    Hero("Tsabu"),
    Hero("Crag Hack"),
    Hero("Jojosh"),
    Hero("Atlas"),
    Hero("Yog"),
    Hero("Antoine"),
    Hero("Ariel"),
    Hero("Vatawna"),
    Hero("Carlawn"),
    Hero("Rebecca"),
    Hero("Luna"),
    Hero("Astra"),
    Hero("Natasha"),
    Hero("Gem"),
    Hero("Troyan"),
    Hero("Agar"),
    Hero("Crodo"),
    Hero("Falagar"),
    Hero("Barok"),
    Hero("Airie"),
    Hero("Kastore"),
    Hero("Sandro"),
    Hero("Wrathmont"),
    Hero("Vesper"),
]
