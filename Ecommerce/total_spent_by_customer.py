from mrjob.job import MRJob
from mrjob.step import MRStep

class MRTotalSpentByCustomer(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(mapper=self.invert_mapper, reducer=self.sort_reducer)
        ]

    def mapper(self, _, line):
        (id, _, spent) = line.split(",")
        yield id, float(spent)

    def reducer(self, customerId, orders):
        yield customerId, sum(orders)

    def invert_mapper(self, customerId, spent):
        yield "%08.02f" % float(spent), customerId

    def sort_reducer(self, spent, customers):
        for customer in customers:
            yield spent, customer



if __name__ == "__main__":
    MRTotalSpentByCustomer.run()