import unittest
import smrm.trash as trash
import os
import shutil
import json
import tempfile
from smrm.utils import confirmed, get_size, conflict_solver, Progress


# delete work with console in Trash
# may be make separate logging
# ADD EXIT CODES!!!!!!!!
# deleting trash into trash???
#make predupre}\{ (notice)(exit code) about using default config
#add more tests (for directories)
#may be russian files?
#delete absolute import 


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp() 


    def tearDown(self):
        shutil.rmtree(self.test_dir)

    
    def test_conflict_solver(self):
         self.assertEqual(conflict_solver("name"), "name(1)")
         self.assertEqual(conflict_solver("name(1)"), "name(2)")
         self.assertEqual(conflict_solver("name(2)"), "name(3)")


    def test_get_size(self):
        files = ["a", "b", "c"]
        for filename in files:
            with open("%s"%os.path.join(self.test_dir, filename), 'wb') as f: 
                f.seek(11111-1)
                f.write("\0")
            
        self.assertEqual(get_size(self.test_dir), 33333)  
        


    def test_confirmed(self):
        original_raw_input = __builtins__.raw_input
        __builtins__.raw_input = lambda _: 'yes'
        self.assertEqual(confirmed("kek"), True)
        __builtins__.raw_input = lambda _: 'no'
        self.assertEqual(confirmed("kek"), False)
        __builtins__.raw_input = original_raw_input



class TestTrash(unittest.TestCase):
    
   
    def setUp(self):
        self.test_dir = tempfile.mkdtemp() 
        self.t = trash.Trash(trash_path = self.test_dir + "/Trash" , current_directory = self.test_dir, silent=True)
        self.t.wipe_trash()
        self.file1 = self.test_dir + "/1"
        self.file2 = self.test_dir + "/2"
        self.file3 = self.test_dir + "/kek"   
        with open(self.file1, "w"):pass
        with open(self.file2, "w"):pass
        with open(self.file3, "w"):pass

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_delete_to_trash(self):        
        self.t.delete_to_trash(self.file1)
        f = open(self.test_dir +"/Trash/filelist", 'r')         
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
        self.t.recover_from_trash("1")        
        self.t.recover_from_trash("1")
        self.assertEqual(os.path.exists(self.file1), True)
        self.assertEqual(os.path.exists(self.file1 + "(1)"), True)


    def test_wipe_trash(self):
        self.t.wipe_trash()
        self.assertEqual(os.path.exists(self.test_dir + "/Trash/filelist"), False)


    def test_delete_to_trash_by_reg(self):
        self.t.delete_to_trash_by_reg('\d+', self.test_dir)
        self.assertEqual(os.path.exists(self.file1), False)
        self.assertEqual(os.path.exists(self.file2), False)


if __name__ == '__main__':
    unittest.main()