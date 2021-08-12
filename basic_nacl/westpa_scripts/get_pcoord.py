import mdtraj
import numpy
import sys

if __name__ == "__main__":
	dist = mdtraj.compute_distances(mdtraj.load(sys.argv[1], top=sys.argv[2]), [[0,1]], periodic=True)[0][0]*10
	print(f"{dist:.4f}")
