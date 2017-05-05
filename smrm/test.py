import unittest
import trash
import os
import shutil
import smrm 


class TestTrash(unittest.TestCase):

    def test_add_slash(self):
        os.mknod("bekmek1")
        smrm.main()



if __name__ == '__main__':
    unittest.main()