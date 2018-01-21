from mrjob.job import MRJob


class MRMaxTemperature(MRJob):
    """
    Remember to set the data in the python runner
    1st arg. ../Data/temperatures/1800.csv
    """

    def mapper(self, _, line):
        (location, _, type, data, *_) = line.split(',')
        if type == 'TMAX':
            temperature = data
            yield location, temperature

    def reducer(self, location, temps):
        yield location, "{}C".format(max(temps))


if __name__ == '__main__':
    MRMaxTemperature.run()
