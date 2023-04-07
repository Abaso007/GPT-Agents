import unittest
from unittest.mock import patch
from GPTAgents.tools import *


class TestTools(unittest.TestCase):
    def test_get_tools(self):
        # Test that get_tools returns a non-empty list
        self.assertTrue(len(get_tools()) > 0)

    def test_Shell_use(self):
        # Test the Shell class's use method with a simple shell command
        output = Shell.use('echo "Hello, world!"')
        self.assertEqual(output, '"Hello, world!"\n')

    def test_Shell_use_cd(self):
        # Test the Shell class's use method with the 'cd' command
        output = Shell.use("cd /nonexistent")
        # Test changing to a non-existent directory
        self.assertEqual(output, "Directory not found")

        # Test changing to the home directory
        with patch.object(os, "chdir") as mock_chdir:
            output = Shell.use("cd")
            mock_chdir.assert_called_once_with(os.path.expanduser("~"))
            self.assertEqual(output, "")

        # Test changing to a valid directory
        with patch.object(os, "chdir") as mock_chdir:
            output = Shell.use("cd /tmp")
            mock_chdir.assert_called_once_with("/tmp")
            self.assertEqual(output, "")

    def test_Shell_use_command_not_found(self):
        # Test the Shell class's use method with a non-existent command
        output = Shell.use("nonexistentcommand")
        self.assertEqual(output, "Command not found")

    def test_RunPython_use(self):
        # Test the RunPython class's use method with a simple Python expression
        output = RunPython.use('print("Hello, world!")')
        self.assertEqual(output, "")

    def test_RunPython_use_exception(self):
        # Test the RunPython class's use method with code that raises an exception
        code = "print(1/0)"  # generate a long code that raises an exception
        output = RunPython.use(code)
        self.assertTrue("ZeroDivisionError" in output)

    def test_WebCrawler_use(self):
        # Test the WebCrawler class's use method with a simple URL
        output = WebCrawler.use("https://example.com")
        self.assertTrue("Example Domain" in output)

    def test_WebCrawler_use_exception(self):
        # Test the WebCrawler class's use method with a non-existent URL
        output = WebCrawler.use("https://nonexistent.example.com")
        self.assertTrue("Error" in output)

    def test_WebSearch_use(self):
        # Test the WebSearch class's use method with a simple search query
        output = WebSearch.use("example.com")
        self.assertTrue("example.com" in output)


if __name__ == "__main__":
    unittest.main()
