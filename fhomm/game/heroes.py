from collections import namedtuple

Stats = namedtuple(
    'Stats',
    ['attack', 'defense', 'power', 'knowledge'],
    module='fhomm.game.heroes',
)


class Hero(
    namedtuple(
        'Hero',
        ['kind', 'name', 'artifacts'],
        defaults=[(None,) * 14],
        module='fhomm.game',
    )
):
    __slots__ = ()

    @property
    def stats(self):
        artifact_stats = self.artifact_stats
        return Stats(
            attack=self.kind.stats.attack + artifact_stats.attack,
            defense=self.kind.stats.defense + artifact_stats.defense,
            power=self.kind.stats.power + artifact_stats.power,
            knowledge=self.kind.stats.knowledge + artifact_stats.knowledge,
        )

    @property
    def artifact_stats(self):
        return Stats(
            attack=sum(a.modifiers.attack for a in self.artifacts if a),
            defense=sum(a.modifiers.defense for a in self.artifacts if a),
            power=sum(a.modifiers.power for a in self.artifacts if a),
            knowledge=sum(a.modifiers.knowledge for a in self.artifacts if a),
        )

    @staticmethod
    def set_artifact(idx, artifact):
        def set_art(h):
            art_list = list(h.artifacts)
            art_list[idx] = artifact
            return h._replace(artifacts=tuple(art_list))

        return set_art


Kind = namedtuple(
    'Kind',
    ['name', 'stats'],
    module='fhomm.game.heroes',
)

KNIGHT    = Kind('Knight',    Stats(1, 2, 1, 1))
BARBARIAN = Kind('Barbarian', Stats(2, 1, 1, 1))
SORCERESS = Kind('Sorceress', Stats(0, 0, 2, 3))
WARLOCK   = Kind('Warlock',   Stats(0, 0, 3, 2))

KINDS = [KNIGHT, BARBARIAN, SORCERESS, WARLOCK]

# List of heroes in the order of portrait resources: 0-35
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
