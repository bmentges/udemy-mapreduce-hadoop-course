from mrjob.job import MRJob


class MRMinTemperature(MRJob):
    """
    Remember to set the data in the python runner
    1st arg. ../Data/temperatures/1800.csv
    """

    def mapper(self, _, line):
        (location, _, type, data, *_) = line.split(',')
        if type == 'TMIN':
            temperature = data
            yield location, temperature

    def reducer(self, location, temps):
        yield location, "{}C".format(min(temps))


if __name__ == '__main__':
    MRMinTemperature.run()
