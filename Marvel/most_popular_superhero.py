from mrjob.job import MRJob
from mrjob.step import MRStep


class MostPopularSuperhero(MRJob):
    """
    Remember to set the data in the python runner
    1st arg. ../Data/marvel/Marvel-graph.txt
    2nd arg. --names ../Data/marvel/Marvel-names.txt
    """

    def configure_args(self):
        super(MostPopularSuperhero, self).configure_args()
        self.add_file_arg('--names', help="Path to ../Data/marvel/Marvel-names.txt")

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(mapper=self.mapper_inverter,
                   mapper_init=self.mapper_init,
                   reducer=self.reduce_sort)
        ]

    def mapper(self, _, line):
        (heroId, *friends) = line.split()
        yield int(heroId), len(friends)

    def reducer(self, heroId, friends_count):
        yield heroId, sum(friends_count)

    def mapper_inverter(self, heroId, friends_count):
        heroName = self.marvelNames[heroId]
        yield None, (friends_count, heroName)

    def mapper_init(self):
        self.marvelNames = {}

        with open("Marvel-names.txt", encoding='ascii', errors='ignore') as f:
            for line in f:
                (heroId, name, *_) = line.split('"')
                self.marvelNames[int(heroId)] = name

    def reduce_sort(self, _, tuples):
        yield max(tuples)


if __name__ == "__main__":
    MostPopularSuperhero.run()
