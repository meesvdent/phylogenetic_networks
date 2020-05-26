import numpy as np


class Node:
    def __init__(self, sequences, species, features, parent=None):
        self.sequences = np.array(sequences)
        self.features = np.array(features)
        self.species = np.array(species)
        self.order_features()
        self.parent = parent
        self.children = []
        self.name = None

    def order_features(self):
        colsums = np.array([])
        for i in range(self.sequences.shape[1]):
            colsums = np.hstack((colsums, np.sum(self.sequences[:, i])))
        order = np.argsort(-colsums)
        self.sequences = self.sequences[:, order]
        self.features = self.features[order]


    def find_hierarchy(self):

        branch_mask = self.sequences[:, 0] == 1

        branch_species = self.species[branch_mask]
        branch_sequences = self.sequences[branch_mask, 1:self.sequences.shape[1]]

        self.sequences = self.sequences[~branch_mask, 1:self.sequences.shape[1]]
        self.features = self.features[1:len(self.features)]
        self.species = self.species[~branch_mask]

        branch = Node(branch_sequences, branch_species, self.features, parent=self)

        branch.is_leaflet()
        if branch.name is None:
            branch.order_features()
            branch.find_hierarchy()

        self.is_leaflet()
        if self.name is None:
            branch.order_features()
            self.find_hierarchy()

        self.children.append(branch)

        return self

    def is_leaflet(self):
        if len(self.species) == 1:
            self.name = self.species[0]
        elif len(self.species) == 0:
            self.name = "Missing link"


class PhylogeneticNetwork(Node):
    pass

