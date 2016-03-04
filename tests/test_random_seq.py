import unittest
from sequences.random_seq import RandomSeqs

class TestRandom(unittest.TestCase):

	S = RandomSeqs(10,30,10)
	S.generate_sequences('AMP')

	def test_seq_num(self):
		self.assertEqual(len(self.S.sequences),10)

	def test_seq_len(self):
		for seq in self.S.sequences:
			self.assertIn(len(seq),range(10,31))

if __name__ == '__main__':
	unittest.main()