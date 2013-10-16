import unittest
import shutil
from test_common import *
from xml_compare import compare_xml_files

class Test_mvn_config(unittest.TestCase):

    def setUp(self):
        self.maxDiff = 2048
        dirpath = os.path.dirname(os.path.realpath(__file__))
        self.olddir = os.getcwd()
        self.workdir = os.path.join(dirpath, 'workdir')
        os.mkdir(self.workdir)
        os.chdir(self.workdir)

    def tearDown(self):
        try:
            shutil.rmtree(self.workdir)
        except OSError:
            pass
        os.chdir(self.olddir)

    @xmvnconfig('mvn_config', [])
    def test_run_no_args(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertEqual("Usage:", stderr[:6])

    @xmvnconfig('mvn_config', ['-h'])
    def test_help(self, stdout, stderr, return_value):
        self.assertTrue(stdout)

    @xmvnconfig('mvn_config',['aaa', ])
    def test_single(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', 'b', 'c', ])
    def test_more(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['aaa', 'bbb', ])
    def test_simple(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'simple'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a/b/c', 'xxx', ])
    def test_path(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'path'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b/>', ])
    def test_xml1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'xml1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b>c</b>', ])
    def test_xml2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'xml2'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b>c</b><d/>', ])
    def test_xml3(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'xml3'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b>c</b><d>e</d>', ])
    def test_xml4(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'xml4'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b><c>d</c></b>', ])
    def test_nested_xml1(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'nested_xml1'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b><c>d</c>d</b>', ])
    def test_nested_xml2(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'nested_xml2'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', '<b', ])
    def test_invalid_xml1(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', '<b>', ])
    def test_invalid_xml2(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', '<b><c></b>', ])
    def test_invalid_xml3(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', '<b></c></b>', ])
    def test_invalid_xml4(self, stdout, stderr, return_value):
        self.assertNotEqual(return_value, 0)
        self.assertTrue(stderr)

    @xmvnconfig('mvn_config',['a', '<b>c&lt;d</b>', ])
    def test_entity(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'entity'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

    @xmvnconfig('mvn_config',['a', 'f<b>c</b>d', ])
    def test_mixed(self, stdout, stderr, return_value):
        self.assertEquals(return_value, 0)
        filelist = get_config_file_list()
        self.assertEquals(len(filelist), 1)
        for file in filelist:
            report = compare_xml_files(get_actual_config(file),
                 get_expected_config(file, 'mvn_config', 'mixed'),
                 ['artifactGlob'])
            self.assertFalse(report, '\n' + report)

if __name__ == '__main__':
    unittest.main()
