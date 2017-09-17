import unittest
import smrm.trash as trash
import os
import shutil
import json
import tempfile
from smrm.utils import confirmed, get_size, conflict_solver, Progress


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp() 


    def tearDown(self):
        shutil.rmtree(self.test_dir)

    
    def test_conflict_solver(self):
        self.assertEqual(conflict_solver("name"), "name(1)")
        self.assertEqual(conflict_solver("name(1)"), "name(2)")
        self.assertEqual(conflict_solver("name(2)"), "name(3)")
        self.assertEqual(conflict_solver("1(1)"), "1(2)")


    def test_get_size(self):
        files = ["a", "b", "c"]
        for filename in files:
            with open("{}".format(os.path.join(self.test_dir, filename)), 'w+') as f: 
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
        self.test_trash = trash.Trash(trash_path = self.test_dir + "/Trash")
        self.file1 = self.test_dir + "/1"
        self.file2 = self.test_dir + "/2"
        self.file3 = self.test_dir + "/kek"   
        with open(self.file1, "w"):pass
        with open(self.file2, "w"):pass
        with open(self.file3, "w"):pass


    def tearDown(self):
        shutil.rmtree(self.test_dir)
        

    def test_delete_to_trash(self):        
        self.test_trash.delete_to_trash(self.file1)
        f = open(self.test_dir +"/Trash/filelist", 'r')         
        d = json.load(f)
        self.assertNotEqual(d, {}) 
        self.assertFalse(os.path.exists(self.file1))


    def test_exit_code_of_delete_to_trash_zero(self):
        lst = self.test_trash.delete_to_trash(self.file1)
        self.assertEqual(lst[0][1], 0)


    def test_exit_code_of_delete_to_trash_three(self):   
        lst = self.test_trash.delete_to_trash(self.test_dir + '/not_existing')
        self.assertEqual(lst[0][1], 3)


    def test_recover_from_trash(self):        
        self.test_trash.delete_to_trash(self.file1)
        self.test_trash.delete_to_trash(self.file2)
        self.test_trash.recover_from_trash("1")
        self.test_trash.recover_from_trash("2")
        self.assertEqual(os.path.exists(self.file1), True)
        self.assertEqual(os.path.exists(self.file2), True)

    
    def test_recover_from_trash_name_conflict(self):
        self.test_trash.delete_to_trash(self.file1)
        with open(self.file1, "w"):pass
        self.test_trash.delete_to_trash(self.file1)        
        self.test_trash.recover_from_trash("1")      
        self.test_trash.recover_from_trash("1")  
        self.assertEqual(os.path.exists(self.file1), True)
        self.assertEqual(os.path.exists(self.file1 + "(1)"), True)


    def test_exit_code_of_recover_from_trash(self):
        self.test_trash.delete_to_trash(self.file1)
        text, code = self.test_trash.recover_from_trash("1")
        self.assertEqual(code, 0)
        text, code = self.test_trash.recover_from_trash("3")
        self.assertEqual(code, 3)

    
    def test_wipe_trash(self):
        self.test_trash.wipe_trash()
        self.assertEqual(os.path.exists(self.test_dir + "/Trash/filelist"), False)


    def test_delete_to_trash_by_reg(self):
        self.test_trash.delete_to_trash_by_reg('\d+', self.test_dir)
        self.assertEqual(os.path.exists(self.file1), False)
        self.assertEqual(os.path.exists(self.file2), False)     

    
    def test_delete_to_trash_force(self):
        self.test_trash = trash.Trash(trash_path = self.test_dir + "/Trash",force=True)
        self.assertEqual(self.test_trash.delete_to_trash(self.test_dir + "/not_existing"), [("",0)])


    def test_dry_run(self):
        self.test_trash = trash.Trash(trash_path = self.test_dir + "/Trash", dry_run=True)
        self.test_trash .delete_to_trash(self.file1)
        self.assertTrue(os.path.exists(self.file1))


if __name__ == '__main__':
    unittest.main()
