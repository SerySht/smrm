import unittest
import smrm.trash as trash
import os
import shutil
import json
import tempfile
from smrm.utils import confirmed, get_size, conflict_solver, Progress


test_dir = tempfile.mkdtemp()
#print test_dir


class TestUtils(unittest.TestCase):
    
    def test_conflict_solver(self):
         self.assertEqual(conflict_solver("name"), "name(1)")
         self.assertEqual(conflict_solver("name(1)"), "name(2)")
         self.assertEqual(conflict_solver("name(2)"), "name(3)")


    def test_get_size(self):
        if not os.path.exists(test_dir):
            os.mkdir(test_dir)

        files = ["a", "b", "c"]
        for filename in files:
            with open("%s"%os.path.join(test_dir, filename), 'wb') as f: 
                f.seek(11111-1)
                f.write("\0")
            
        self.assertEqual(get_size(test_dir), 33333)        
        shutil.rmtree(test_dir)


    def test_confirmed(self):
        original_raw_input = __builtins__.raw_input
        __builtins__.raw_input = lambda _: 'yes'
        self.assertEqual(confirmed("kek"), True)
        __builtins__.raw_input = lambda _: 'no'
        self.assertEqual(confirmed("kek"), False)
        __builtins__.raw_input = original_raw_input



class TestTrash(unittest.TestCase):
    if not os.path.exists(test_dir):
        os.mkdir(test_dir)
    
    t = trash.Trash(trash_path = test_dir + "/Trash" , current_directory = test_dir, silent=True)

    def setUp(self):
        self.t.wipe_trash()
        self.file1 = test_dir + "/1"
        self.file2 = test_dir + "/2"
        self.file3 = test_dir + "/kek"   
        with open(self.file1, "w"):pass
        with open(self.file2, "w"):pass
        with open(self.file3, "w"):pass


    def test_delete_to_trash(self):        
        self.t.delete_to_trash(self.file1)
        f = open(test_dir +"/Trash/filelist", 'r')         
        d = json.load(f)
        self.assertNotEqual(d, {}) 


    def test_recover_from_trash_unique_file(self):        
        self.t.delete_to_trash(self.file1)
        self.t.recover_from_trash("1")
        self.assertEqual(os.path.exists(self.file1), True)

    
    def test_recover_from_trash_not_unique_file(self):
        self.t.delete_to_trash(self.file1)
        with open(self.file1, "w"):pass
        self.t.delete_to_trash(self.file1)

        original_raw_input = __builtins__.raw_input
        __builtins__.raw_input = lambda : 1
        self.t.recover_from_trash("1")        
        __builtins__.raw_input = original_raw_input
        
        self.t.recover_from_trash("1")
        self.assertEqual(os.path.exists(self.file1), True)
        self.assertEqual(os.path.exists(self.file1 + "(1)"), True)


    def test_wipe_trash(self):
        self.t.wipe_trash()
        self.assertEqual(os.path.exists(test_dir + "/Trash/filelist"), False)


    def test_delete_to_trash_by_reg(self):
        self.t.delete_to_trash_by_reg('\d+', test_dir)
        self.assertEqual(os.path.exists(self.file1), False)
        self.assertEqual(os.path.exists(self.file2), False)


if __name__ == '__main__':
    unittest.main()