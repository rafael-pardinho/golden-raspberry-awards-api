from app.use_cases.producer_intervals import ProducerIntervalCalculator

''' obtém filmes vencedores do repositório e calcula os intervalos de prêmios para produtores, 
    retornando os resultados ou um erro caso não haja filmes
'''

class ProducerController:
    def __init__(self, movie_repository):
        self.movie_repository = movie_repository

    def get_producer_intervals(self):
        movies = self.movie_repository.get_winner_movies()
        if not movies:
            return {"detail": "Nenhum vencedor encontrado no banco de dados."}, 404

        return ProducerIntervalCalculator.calculate_intervals(movies), 200