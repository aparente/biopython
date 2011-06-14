# Copyright (C) 2011, Mikael Trellet (mikael.trellet@gmail.com)
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

"""Interface class, used in Structure objects."""

from Bio.PDB.Entity import Entity

class Interface(Entity):
    """
    The Interface object isn't automatically initialize during a PDB parsing,
    but can be guessed from an existing parsed structure in order to analyse
    the interface between 2 or more chains in a complex.
    """

    def __init__(self, id):
        self.level="I"
        self.id=id
        self.neighbors = {}
        self.uniq_pairs = []

        Entity.__init__(self, id)

    # Override Entity add method
    # Interface doesnt follow strictly
    # other Entity rules.
    #
    # Its childs are residues
    # but it may be useful
    # to list them by chain.
    
    def add(self, entity):
        "Add a child to the Entity."

        entity_id=entity.get_id()
        if not self.has_id(entity_id):

            self.child_list.append(entity)
            if entity.parent.id not in self.child_dict:
                self.child_dict[entity.parent.id] = []
            self.child_dict[entity.parent.id].append(entity)

    def get_chains(self):
        "Get the different chains involved in the Interface object"
        for chain in self.child_dict.keys():
            yield chain

    def get_neighbors(self):
        neighbors=self.neighbors
        for resA, resB in self.uniq_pairs:
        ## Checking for 1st residue (if his chain exist, then if 
        ## it is referenced and finally if his partner is already present)
            if resA.parent.id not in neighbors:
                neighbors[resA.parent.id]={}
                neighbors[resA.parent.id][resA]=[]
                neighbors[resA.parent.id][resA].append(resB)
            elif resA not in neighbors[resA.parent.id]:
                neighbors[resA.parent.id][resA]=[]
                neighbors[resA.parent.id][resA].append(resB)
            elif resB not in neighbors[resA.parent.id][resA]:
                neighbors[resA.parent.id][resA].append(resB)
        ## Checking for 2nd residue
            if resB.parent.id not in neighbors:
                neighbors[resB.parent.id]={}
                neighbors[resB.parent.id][resB]=[]
                neighbors[resB.parent.id][resB].append(resB)
            elif resB not in neighbors[resB.parent.id]:
                neighbors[resB.parent.id][resB]=[]
                neighbors[resB.parent.id][resB].append(resB)
            elif resA not in neighbors[resB.parent.id][resB]:
                neighbors[resB.parent.id][resB].append(resA)
        return neighbors
