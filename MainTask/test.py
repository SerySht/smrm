import unittest
import trash
import os
import shtutil


class TestTrash(unittest.TestCase):

	def test_add_slash(self):
		self.assertEqual(trash.add_slash("/check"), "/check")
		self.assertEqual(trash.add_slash("check"), "/check")

	def test_get_name(self):		
		self.assertEqual(trash.get_name("folder1/folder2/file"),("/folder1/folder2/","file"))
		self.assertEqual(trash.get_name("file"),("","file"))

	def test_remove_to_trash(self):
		os.mkdir('test')
		f = open("test/abc", 'w')
		f.close()
		

		shtutil.rmtee('test')



if __name__ == '__main__':
	unittest.main()