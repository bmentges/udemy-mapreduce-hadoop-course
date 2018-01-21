from mrjob.job import MRJob


class MRFriendsCounter(MRJob):
    """
    Remember to set the data in the python runner
    1st arg. ../Data/socialnetwork/fakefriends.csv
    """

    def mapper(self, key, line):
        (userID, name, age, num_friends) = line.split(',')
        self.increment_counter("friends", "number of people", 1)
        yield age, float(num_friends)

    def reducer(self, age, num_friends):
        total = 0
        num_friends_length = 0
        for qty in num_friends:
            total += qty
            num_friends_length += 1

        yield age, total / num_friends_length


if __name__ == "__main__":
    MRFriendsCounter.run()
