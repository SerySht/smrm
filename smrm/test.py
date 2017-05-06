import unittest
import trash
import os
import shutil
import json



class TestTrash(unittest.TestCase):
    tl = '/home/sergey/labs/lab2/smrm'

    t = trash.Trash(trash_location = tl ,current_directory = tl)
   
    def test_delete_to_trash(self):
        if not os.path.exists('bekmek'):      
            os.mkdir('bekmek') 

        self.t.delete_to_trash(["bekmek"])

        f = open(self.tl + "/Trash/filelist", 'a+')       
        d = json.load(f)
        self.assertNotEqual(d.get("bekmek"), None) 
    t.wipe_trash()       


if __name__ == '__main__':
    unittest.main()