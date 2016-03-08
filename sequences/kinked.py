"""
.. module:: kinked

.. moduleauthor:: modlab Alex Mueller <alex.mueller@pharma.ethz.ch>

This module incorporates methods for presumed kinked amphipathic alpha-helical peptide sequences:
Sequences are generated by placing basic residues along the sequence with distance 3-4 AA to each other.
The remaining spots are filled up by hydrophobic AAs. Then, a basic residue is replaced by proline, presumably
leading to a kink in the hydrophobic face of the amphipathic helices.
"""

from core.templates import mutate_AA, aminoacids, template, clean, save_fasta, filter_unnatural
import random
from itertools import cycle

__author__ = 'modlab'

class Kinked:
	"""
	Base class for peptide sequences probable to form helices with a kink.
	"""
	def __init__(self,lenmin,lenmax,seqnum,):
		'''
		:param lenmin: minimal sequence length
		:param lenmax: maximal sequence length
		:param seqnum: number of sequences to generate
		:return: defined self variables
		'''
		aminoacids(self)
		template(self,lenmin,lenmax,seqnum)

	def generate_kinked(self):
		"""
		Method to actually generate the presumed kinked sequences with features defined in the class instances.

		:return: sequence list with strings stored in object.sequences
		:Example:

		>>> K = Kinked(7,28,8)
		>>> K.generate_kinked()
		>>> K.sequences
		['IILRLHPIG','ARGAKVAIKAIRGIAPGGRVVAKVVKVG','GGKVGRGVAFLVRIILK','KAVKALAKGAPVILCVAKVI',
		'IGIRVWRAVIKVIPVAVRGLRL','RIGRVIVPVIRGL','AKAARIVAMLAR','LGAKGWRLALKGIPAAIKLGKV']
		"""
		clean(self)
		for s in range(self.seqnum): #for the number of sequences to generate
			poslist = [] #used to
			seq = ['X'] * random.choice(range(self.lenmin, self.lenmax + 1))
			basepos = random.choice(range(4)) #select spot for first basic residue from 0 to 3
			seq[basepos] = random.choice(self.AA_basic) #place first basic residue
			poslist.append(basepos)
			gap = cycle([3,4]).next #gap cycle of 3 & 4 --> 3,4,3,4,3,4...
			g = gap()
			while g+basepos < len(seq): #place more basic residues 3-4 positions further (changing between distance 3 and 4)
				basepos += g
				seq[basepos] = random.choice(self.AA_basic) #place more basic residues
				g = gap() #next gap
				poslist.append(basepos)

			for p in range(len(seq)):
				while seq[p] == 'X': #fill up remaining spots with hydrophobic AAs
					seq[p] = random.choice(self.AA_hyd)

			#place proline around the middle of the sequence
			propos = poslist[len(poslist) / 2]
			seq[propos] = 'P'

			self.sequences.append(''.join(seq))

	def mutate_AA(self,nr,prob):
		"""
		Method to mutate with **prob** probability a **nr** of positions per sequence randomly.

		:param nr: number of mutations to perform per sequence
		:param prob: probability of mutating a sequence
		:return: In *self.sequences*: mutated sequences
		:Example:

		>>> S.sequences
		['IAKAGRAIIK']
		>>> S.mutate_AA(3,1)
		>>> S.sequences
		['NAKAGRAWIK']
		"""
		mutate_AA(self,nr,prob)


	def save_fasta(self,filename):
		"""
		Method for saving sequences in the instance self.sequences to a file in FASTA format.

		:param filename: output filename (ending .fasta)
		:return: a FASTA formatted file containing the generated sequences
		"""
		save_fasta(self,filename)


	def filter_unnatrual(self):
		"""
		Method to filter out sequences with unnatural amino acids from :py:attr:`self.sequences` as well as duplicates.
		:return: Filtered sequence list in :py:attr:`self.sequences`
		"""
		filter_unnatural(self)