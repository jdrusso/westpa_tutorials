import mdtraj
import numpy


##### This is no longer necessary, because pdb_to_xml.py will ensure a parent PDB always exists.
# try:
#     # If it's a  continuation, parent state is stored in an XML
#     parent = mdtraj.load('parent.xml', top='bstate.pdb')
# except OSError:
#     # If it's a new trajectory, then just reference the PDB
#     parent = mdtraj.load('bstate.pdb')
parent = mdtraj.load('parent.xml', top='bstate.pdb')

traj = mdtraj.load('seg.dcd', top='bstate.pdb')
dist_parent = mdtraj.compute_distances(parent, [[0,1]], periodic=True)
dist_traj = mdtraj.compute_distances(traj, [[0,1]], periodic=True)
dist = numpy.append(dist_parent,dist_traj)
d_arr = numpy.asarray(dist)
d_arr = d_arr*10
numpy.savetxt("dist.dat", d_arr)
