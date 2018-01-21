# To run locally:
# !python MovieSimilarities.py --items=ml-100k/u.item ml-100k/u.data > sims.txt

from mrjob.job import MRJob
from mrjob.step import MRStep
from math import sqrt
from itertools import combinations


class MovieSimilarities(MRJob):
    """
    Remember to set the data in the python runner
    1st arg. ../Data/movies/u.data
    2nd arg. --items ../Data/movies/u.item
    """

    def configure_args(self):
        super(MovieSimilarities, self).configure_args()
        self.add_file_arg('--items', help="Path to u.item")

    def load_movie_names(self):
        # Load database of movie names.
        self.movie_names = {}

        with open("u.item", encoding='ascii', errors='ignore') as f:
            for line in f:
                fields = line.split('|')
                (id, name, *_) = fields
                self.movie_names[int(id)] = name

    def steps(self):
        return [
            MRStep(mapper=self.mapper_parse_input,
                   reducer=self.reducer_ratings_by_user),
            MRStep(mapper=self.mapper_create_item_pairs,
                   reducer=self.reducer_compute_similarity),
            MRStep(mapper=self.mapper_sort_similarities,
                   mapper_init=self.load_movie_names,
                   reducer=self.reducer_output_similarities)]

    def mapper_parse_input(self, key, line):
        # Outputs userID => (movieID, rating)
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield userID, (movieID, float(rating))

    def reducer_ratings_by_user(self, user_id, item_ratings):
        #Group (item, rating) pairs by userID

        ratings = []
        for movieID, rating in item_ratings:
            ratings.append((movieID, rating))

        yield user_id, ratings

    def mapper_create_item_pairs(self, _, item_ratings):
        # Find every pair of movies each user has seen, and emit
        # each pair with its associated ratings

        # "combinations" finds every possible pair from the list of movies
        # this user viewed.
        for itemRating1, itemRating2 in combinations(item_ratings, 2):
            movieID1 = itemRating1[0]
            rating1 = itemRating1[1]
            movieID2 = itemRating2[0]
            rating2 = itemRating2[1]

            # Produce both orders so sims are bi-directional
            yield (movieID1, movieID2), (rating1, rating2)
            yield (movieID2, movieID1), (rating2, rating1)

    def cosine_similarity(self, rating_pairs):
        # Computes the cosine similarity metric between two
        # rating vectors.
        numPairs = 0
        sum_xx = sum_yy = sum_xy = 0
        for ratingX, ratingY in rating_pairs:
            sum_xx += ratingX * ratingX
            sum_yy += ratingY * ratingY
            sum_xy += ratingX * ratingY
            numPairs += 1

        numerator = sum_xy
        denominator = sqrt(sum_xx) * sqrt(sum_yy)

        score = 0
        if (denominator):
            score = (numerator / (float(denominator)))

        return score, numPairs

    def reducer_compute_similarity(self, movie_pair, rating_pairs):
        # Compute the similarity score between the ratings vectors
        # for each movie pair viewed by multiple people

        # Output movie pair => score, number of co-ratings

        score, num_pairs = self.cosine_similarity(rating_pairs)

        # Enforce a minimum score and minimum number of co-ratings
        # to ensure quality
        if num_pairs > 10 and score > 0.95:
            yield movie_pair, (score, num_pairs)

    def mapper_sort_similarities(self, movie_pair, scores):
        # Shuffle things around so the key is (movie1, score)
        # so we have meaningfully sorted results.
        score, n = scores
        movie1, movie2 = movie_pair

        yield (self.movie_names[int(movie1)], score), \
            (self.movie_names[int(movie2)], n)

    def reducer_output_similarities(self, movieScore, similarN):
        # Output the results.
        # Movie => Similar Movie, score, number of co-ratings
        movie1, score = movieScore
        for movie2, n in similarN:
            yield movie1, (movie2, score, n)


if __name__ == '__main__':
    MovieSimilarities.run()
