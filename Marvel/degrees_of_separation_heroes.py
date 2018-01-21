from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import RawValueProtocol


class Node:
    def __init__(self):
        self.characterID = ''
        self.connections = []
        self.distance = 9999
        self.color = 'WHITE'

    def from_line(self, line):
        """
        :param line: string, Format is ID|EDGES|DISTANCE|COLOR
        :return:
        """
        fields = line.split('|')
        if len(fields) == 4:
            (self.characterID, self.connections, self.distance, self.color) = fields
            self.connections = self.connections.split(',')

    def get_line(self):
        connections = ','.join(self.connections)
        return '|'.join((self.characterID, connections, str(self.distance), self.color))


class DegreeOfSeparation(MRJob):
    """
    To run:
    python degrees_of_separation_heroes.py --target=100 ../Data/marvel/BFS-iteration-0.txt > ../DATA/marvel/BFS-iteration-1.txt
    where target is a hero.
    """

    INPUT_PROTOCOL = RawValueProtocol
    OUTPUT_PROTOCOL = RawValueProtocol

    def configure_options(self):
        super(DegreeOfSeparation, self).configure_options()
        self.add_passthrough_option(
            '--target', help="ID of character we are searching for")

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer)
        ]

    def mapper(self, _, line):
        node = Node()
        node.from_line(line)
        # If this node needs to be expanded...
        if node.color == 'GRAY':
            for connection in node.connections:
                vnode = Node()
                vnode.characterID = connection
                vnode.distance = int(node.distance) + 1
                vnode.color = 'GRAY'
                if self.options.target == connection:
                    counterName = ("Target ID " + connection +
                                   " was hit with distance " + str(vnode.distance))
                    self.increment_counter('Degrees of Separation',
                                           counterName, 1)
                yield connection, vnode.get_line()

            # We've processed this node, so color it black
            node.color = 'BLACK'

        # Emit the input node so we don't lose it.
        yield node.characterID, node.get_line()

    def reducer(self, key, values):
        edges = []
        distance = 9999
        color = 'WHITE'

        for value in values:
            node = Node()
            node.from_line(value)

            if len(node.connections) > 0:
                edges.extend(node.connections)

            if int(node.distance) < int(distance):
                distance = node.distance

            if node.color == 'BLACK':
                color = 'BLACK'

            if node.color == 'GRAY' and color == 'WHITE':
                color = 'GRAY'

        node = Node()
        node.characterID = key
        node.distance = distance
        node.color = color
        node.connections = edges

        yield key, node.get_line()


if __name__ == '__main__':
    DegreeOfSeparation.run()