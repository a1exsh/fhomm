from collections import namedtuple

Stats = namedtuple(
    'Stats',
    ['attack', 'defense', 'power', 'knowledge'],
    module='fhomm.game.heroes',
)


class Hero(
    namedtuple(
        'Hero',
        ['id', 'kind', 'name', 'artifacts'],
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
    Hero( 0, KNIGHT, "Lord Kilburn"),
    Hero( 1, KNIGHT, "Lord Haart"),
    Hero( 2, KNIGHT, "Sir Gallant"),
    Hero( 3, KNIGHT, "Arturius"),
    Hero( 4, KNIGHT, "Tyro"),
    Hero( 5, KNIGHT, "Maximus"),
    Hero( 6, KNIGHT, "Ector"),
    Hero( 7, KNIGHT, "Dimitri"),
    Hero( 8, KNIGHT, "Ambrose"),
    # BARBARIAN
    Hero( 9, BARBARIAN, "Thundax"),
    Hero(10, BARBARIAN, "Ergon"),
    Hero(11, BARBARIAN, "Kelzen"),
    Hero(12, BARBARIAN, "Tsabu"),
    Hero(13, BARBARIAN, "Crag Hack"),
    Hero(14, BARBARIAN, "Jojosh"),
    Hero(15, BARBARIAN, "Atlas"),
    Hero(16, BARBARIAN, "Yog"),
    Hero(17, BARBARIAN, "Antoine"),
    # SORCERESS
    Hero(18, SORCERESS, "Ariel"),
    Hero(19, SORCERESS, "Vatawna"),
    Hero(20, SORCERESS, "Carlawn"),
    Hero(21, SORCERESS, "Rebecca"),
    Hero(22, SORCERESS, "Luna"),
    Hero(23, SORCERESS, "Astra"),
    Hero(24, SORCERESS, "Natasha"),
    Hero(25, SORCERESS, "Gem"),
    Hero(26, SORCERESS, "Troyan"),
    # WARLOCK
    Hero(27, WARLOCK, "Agar"),
    Hero(28, WARLOCK, "Crodo"),
    Hero(29, WARLOCK, "Falagar"),
    Hero(30, WARLOCK, "Barok"),
    Hero(31, WARLOCK, "Airie"),
    Hero(32, WARLOCK, "Kastore"),
    Hero(33, WARLOCK, "Sandro"),
    Hero(34, WARLOCK, "Wrathmont"),
    Hero(35, WARLOCK, "Vesper"),
]
