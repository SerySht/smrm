import unittest
import trash
import os
import shutil
import json
from utils import confirmed, get_size, conflict_solver, Progress




class TestUtils(unittest.TestCase):
    
    def test_conflict_solver(self):
         self.assertEqual(conflict_solver("name"), "name(1)")
         self.assertEqual(conflict_solver("name(1)"), "name(2)")
         self.assertEqual(conflict_solver("name(2)"), "name(3)")


    def test_get_size(self):
        test_path = "/home/sergey/test"
        
        if not os.path.exists(test_path):
            os.mkdir(test_path)

        files = ["a", "b", "c"]
        for filename in files:
            with open("%s"%os.path.join(test_path, filename), 'wb') as f: 
                f.seek(11111-1)
                f.write("\0")
            
        self.assertEqual(get_size(test_path), 33333)        
        shutil.rmtree(test_path)


    def test_confirmed(self):
        original_raw_input = __builtins__.raw_input
        __builtins__.raw_input = lambda _: 'yes'
        self.assertEqual(confirmed("kek"), True)
        __builtins__.raw_input = lambda _: 'no'
        self.assertEqual(confirmed("kek"), False)
        __builtins__.raw_input = original_raw_input


# class TestTrash(unittest.TestCase):
    
#     t = trash.Trash(trash_path = "/home/sergey/Trash" , current_directory = "/home/sergey")

#     def setUp(self):
        
#         self.t.wipe_trash()
#         if not os.path.exists("/home/sergey/test"):
#             os.mkdir("/home/sergey/test")

#         self.file = "/home/sergey/test/1"
#         with open(self.file, "w"):
#             pass

#     # def tearDown(self):
#     #     if os.path.exists("test"):
#     #         shutil.rmtree("test") 
#     #     self.t.wipe_trash()


   
#     def test_delete_to_trash(self):
        
#         self.t.delete_to_trash(self.file)

#         f = open("/home/sergey/Trash/filelist", 'r')  
#         try:     
#             d = json.load(f)
#         except ValueError:
#             print "Failed to get dict"
#             return False
#         self.assertNotEqual(d.get(self.file), None) 

#     # def test_recover_from_trash(self):
#     #     self.t.recover_from_trash(["bekmek"])
#     #     self.assertTrue(os.path.exists("/home/sergey/labs/lab2/smrm/bekmek"))






if __name__ == '__main__':
    unittest.main()