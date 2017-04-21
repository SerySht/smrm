import unittest
import trash
import os
import shutil


class TestTrash(unittest.TestCase):

	def test_add_slash(self):
		self.assertEqual(trash.add_slash("/check"), "/check")
		self.assertEqual(trash.add_slash("check"), "/check")

	def test_get_name(self):		
		self.assertEqual(trash.get_name("folder1/folder2/file"),("/folder1/folder2/","file"))
		self.assertEqual(trash.get_name("file"),("","file"))


	def test_location_check(self):
		self.assertEqual(trash.location_check("/home/sergey", "test"), "/home/sergey/test")
		self.assertEqual(trash.location_check("/home/sergey", "/home/sergey/test"), "/home/sergey/test")

	
	def test_conflict_solver(self):
		self.assertEqual(trash.conflict_solver('bekmek', 'filename'), 'filename(1)')
		self.assertEqual(trash.conflict_solver('bekmek', 'filename(2)'), 'filename(3)')
		self.assertEqual(trash.conflict_solver('replace', 'filename(2)'), 'filename(2)')


	def test_remove_to_trash(self):
		#os.mkdir('test')
		#f = open("test/abc", 'w')
		#f.close()
		
		pass
		#shutil.rmtee('test')



if __name__ == '__main__':
	unittest.main()