from collections import defaultdict

class ProducerIntervalCalculator:
    @staticmethod
    def calculate_intervals(movies):
        producer_intervals = defaultdict(list)
        for movie in movies:
            for producer in movie.producers.split(","):
                producer = producer.strip()
                producer_intervals[producer].append(movie.year)
        
        min_intervals = []
        max_intervals = []

        for producer, years in producer_intervals.items():
            years.sort()
            intervals = [years[i + 1] - years[i] for i in range(len(years) - 1)]
            if intervals:
                min_interval = min(intervals)
                max_interval = max(intervals)
                min_intervals.append({
                    "producer": producer,
                    "interval": min_interval,
                    "previousWin": years[intervals.index(min_interval)],
                    "followingWin": years[intervals.index(min_interval) + 1]
                })
                max_intervals.append({
                    "producer": producer,
                    "interval": max_interval,
                    "previousWin": years[intervals.index(max_interval)],
                    "followingWin": years[intervals.index(max_interval) + 1]
                })

        return {
            "min": sorted(min_intervals, key=lambda x: x["interval"]),
            "max": sorted(max_intervals, key=lambda x: x["interval"], reverse=True)
        }