from mrjob.job import MRJob


class MRRatingCounter(MRJob):
    """
    Remember to set the data in the python runner
    1st arg. ../Data/movies/u.data
    """

    def mapper(self, key, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        self.increment_counter("movies", "number of ratings", 1)
        yield userID, movieID

    def reducer(self, userID, movies):
        self.increment_counter("movies", "number of unique users", 1)
        yield userID, sum(1 for _ in movies)


if __name__ == '__main__':
    MRRatingCounter.run()
