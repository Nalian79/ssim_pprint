import os
import unittest

from utils import is_file_compressed, uncompress

class UncompressTests(unittest.TestCase):
    def testUncompressFile(self):
        file = './sample_data/hr.ssim.dat.gz'
        expected_filename = './sample_data/hr.ssim.dat'
        new_filename = uncompress(file)
        self.assertEqual(new_filename, expected_filename)

    def testIsCompressedTrue(self):
        file = './sample_data/hr.ssim.dat.gz'
        answer = is_file_compressed(file)
        self.assertTrue(answer)

    def testIsCompressedFalse(self):
        file = './sample_data/hr.ssim.dat.gz'
        newfile = uncompress(file)
        answer = is_file_compressed(newfile)
        self.assertFalse(answer)

    def tearDown(self):
        #Clean up the sample data directory
        file = './sample_data/hr.ssim.dat'
        if os.path.exists(file):
            os.remove(file)

if __name__ == "__main__":
    unittest.main()
