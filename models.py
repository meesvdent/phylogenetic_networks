import numpy as np


class Node:
    def __init__(self, sequences, species, features, parent=None, missing_links=0):
        self.sequences = np.array(sequences)
        self.features = np.array(features)
        self.species = np.array(species)
        self.order_features()
        self.parent = parent
        self.children = []
        self.connections = []
        self.name = None

    def order_features(self):
        colsums = np.array([])
        for i in range(self.sequences.shape[1]):
            colsums = np.hstack((colsums, np.sum(self.sequences[:, i])))
        order = np.argsort(-colsums)
        self.sequences = self.sequences[:, order]
        self.features = self.features[order]


    def find_hierarchy(self):

        self.check_if_node()
        if self.name is not None:
            return self
        else:
            self.order_features()
            branch_mask = self.sequences[:, 0] == 1
            branch_species = self.species[branch_mask]
            branch_sequences = self.sequences[branch_mask, 1:self.sequences.shape[1]]

            self.sequences = self.sequences[~branch_mask, 1:self.sequences.shape[1]]
            self.features = self.features[1:len(self.features)]
            self.species = self.species[~branch_mask]

            branch = Node(branch_sequences, branch_species, self.features, parent=self)
            self.children.append(branch)

            branch.find_hierarchy()
            self.find_hierarchy()

            self.connections = self.connections + [(self.name, branch.name)] + branch.connections

            return self

    def check_if_node(self):
        if len(self.species) == 1 and np.count_nonzero(self.sequences) == 0:
            self.name = self.species[0]
        elif len(self.species) == 0:
            self.name = "Missing link for " + ' '.join([x.name for x in self.children])


class PhylogeneticNetwork(Node):
    pass

