class Movie:
    def __init__(self, id: int = None, year: int = None, title: str = None,
                 studios: str = None, producers: str = None, winner: bool = None):
        self.id = id
        self.year = year
        self.title = title
        self.studios = studios
        self.producers = producers
        self.winner = winner
