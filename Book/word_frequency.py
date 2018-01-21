from mrjob.job import MRJob
from mrjob.step import MRStep
import re

WORD_REGEXP = re.compile(r"[\w']+")


class MRWordFrequencyCount(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(mapper=self.mapper_invert_key_value,
                   reducer=self.sort_reducer)
        ]

    def mapper(self, _, line):
        words = WORD_REGEXP.findall(line)
        for word in words:
            self.increment_counter("words", "# of words", 1)
            yield word.lower(), 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)

    def mapper_invert_key_value(self, word, count):
        yield "%04d" % int(count), word

    def sort_reducer(self, count, words):
        for word in words:
            yield count, word


if __name__ == '__main__':
    MRWordFrequencyCount.run()
