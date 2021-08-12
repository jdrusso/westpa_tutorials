import logging

from rich.logging import RichHandler

log = logging.getLogger(__name__)
log.setLevel("INFO")
log.propagate = False
log.addHandler(RichHandler())

import numpy as np
import mdtraj as md


def processCoordinates(self, coords):
        log.debug("Processing coordinates")

        if self.dimReduceMethod == "none":
            nC = np.shape(coords)
            nC = nC[0]
            ndim = 3 * self.nAtoms
            data = coords.reshape(nC, 3 * self.nAtoms)
            return data

        if self.dimReduceMethod == "pca" or self.dimReduceMethod == "vamp":

            ### Original dimensionality reduction
            # xt = md.Trajectory(xyz=coords, topology=None)
            # atom_selection_string = "resid 1"
            # indCA = self.reference_structure.topology.select("name CA")
            # pair1, pair2 = np.meshgrid(indCA, indCA, indexing="xy")
            # indUT = np.where(np.triu(pair1, k=1) > 0)
            # pairs = np.transpose(np.array([pair1[indUT], pair2[indUT]])).astype(int)
            # dist = md.compute_distances(xt, pairs, periodic=True, opt=True)

            ###

            ### NaCl dimensionality reduction
            #log.warning("Hardcoded selection: Doing dim reduction for Na, Cl. This is only for testing!")
            indNA = self.reference_structure.topology.select("element Na")
            indCL = self.reference_structure.topology.select("element Cl")

            diff = np.subtract(coords[:, indNA], coords[:, indCL])

            dist = np.array(np.sqrt(
                np.mean(
                    np.power(
                        diff,
                        2)
                , axis=-1)
            ))

            return dist

def reduceCoordinates(self, coords):
    """
    Defines the coordinate reduction strategy used.
    The reduced corodinates are stored in /auxdata for each iteration.

    Parameters
    ----------
    coords: array-like
        Array of coordinates to reduce.

    Returns
    -------
    Reduced data

    """

    log.debug("Reducing coordinates")

    if self.dimReduceMethod == "none":
        nC = np.shape(coords)
        nC = nC[0]
        ndim = 3 * self.nAtoms
        data = coords.reshape(nC, 3 * self.nAtoms)
        return data

    if self.dimReduceMethod == "pca" or self.dimReduceMethod == "vamp":
        coords = self.processCoordinates(coords)
        coords = self.coordinates.transform(coords)
        return coords

    raise Exception

log.info("Loading user-override functions for modelWE")
