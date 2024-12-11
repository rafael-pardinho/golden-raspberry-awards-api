from collections import defaultdict

class ProducerIntervalCalculator:
    @staticmethod
    def calculate_intervals(movies):
        producer_years = defaultdict(list)
        
        # Agrupar anos de vitória por produtor
        for movie in movies:
            producers = [producer.strip() for producer in movie.producers.split(",")]
            for producer in producers:
                producer_years[producer].append(movie.year)

        # Calcular intervalos para cada produtor
        intervals = []
        for producer, years in producer_years.items():
            years.sort()
            for i in range(len(years) - 1):
                intervals.append({
                    "producer": producer,
                    "interval": years[i + 1] - years[i],
                    "previousWin": years[i],
                    "followingWin": years[i + 1]
                })

        return filter_and_format_intervals(intervals)

def filter_and_format_intervals(intervals):
    # Ordenar por intervalos para identificar os menores e maiores
    sorted_intervals = sorted(intervals, key=lambda x: x["interval"])
    
    # Selecionar os menores intervalos
    min_intervals = []
    for interval in sorted_intervals:
        if len(min_intervals) >= 2:
            break
        min_intervals.append(interval)

    # Selecionar os maiores intervalos
    max_intervals = []
    unique_producers = set()
    for interval in sorted_intervals[::-1]:
        if len(max_intervals) >= 2:
            break
        if interval["producer"] not in unique_producers:
            max_intervals.append(interval)
            unique_producers.add(interval["producer"])

    return {"min": min_intervals, "max": max_intervals}
