import unittest
import trash

class TestTrash(unittest.TestCase):

	def test_add_slash(self):
		self.assertEqual(trash.add_slash("/check"), "/check")
		self.assertEqual(trash.add_slash("check"), "/check")

	def test_get_name(self):		
		self.assertEqual(trash.get_name("folder1/folder2/file"),("/folder1/folder2/","file"))
		self.assertEqual(trash.get_name("file"),("","file"))



if __name__ == '__main__':
	unittest.main()