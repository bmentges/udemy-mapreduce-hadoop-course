from mrjob.job import MRJob
from mrjob.step import MRStep


class MostPopularMovie(MRJob):
    """
    Remember to set the data in the python runner
    1st arg. ../Data/movies/u.data
    2nd arg. --items ../Data/movies/u.item
    """

    def configure_args(self):
        super(MostPopularMovie, self).configure_args()
        self.add_file_arg('--items', help="Path to u.item")

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer_init=self.reducer_init,
                   reducer=self.reducer),
            MRStep(reducer=self.reduce_max)
        ]

    def mapper(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        self.increment_counter("movies", "number of ratings", 1)
        yield movieID, 1

    def reducer_init(self):
        self.movieNames = {}

        with open("u.item", encoding='ascii', errors='ignore') as f:
            for line in f:
                (id, name, *_) = line.split("|")
                self.movieNames[id] = name

    def reducer(self, movieId, values):
        yield None, (sum(values), self.movieNames[movieId])

    def reduce_max(self, _, values):
        yield max(values)


if __name__ == "__main__":
    MostPopularMovie.run()
