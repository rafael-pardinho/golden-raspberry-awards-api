from app.domain.entities.movie import Movie

class MovieRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_winner_movies(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM movies WHERE winner = 1")
        rows = cursor.fetchall()
        return [Movie(**dict(row)) for row in rows]