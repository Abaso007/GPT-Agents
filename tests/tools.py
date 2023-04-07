import unittest
from unittest.mock import patch
from GPTAgents.tools import *


class TestTools(unittest.TestCase):
    def test_get_tools(self):
        # Test that get_tools returns a non-empty list
        self.assertTrue(len(get_tools()) > 0)

    def test_Shell_use(self):
        # Test the Shell class's use method with a simple shell command
        shell = Shell()
        output = shell.use('echo "Hello, world!"')
        self.assertEqual(output, '"Hello, world!"\n')

    def test_Shell_use_cd(self):
        # Test the Shell class's use method with the 'cd' command
        shell = Shell()

        # Test changing to a non-existent directory
        output = shell.use("cd /nonexistent")
        self.assertEqual(output, "Directory not found")

        # Test changing to the home directory
        with patch.object(os, "chdir") as mock_chdir:
            output = shell.use("cd")
            mock_chdir.assert_called_once_with(os.path.expanduser("~"))
            self.assertEqual(output, "")

        # Test changing to a valid directory
        with patch.object(os, "chdir") as mock_chdir:
            output = shell.use("cd /tmp")
            mock_chdir.assert_called_once_with("/tmp")
            self.assertEqual(output, "")

    def test_Shell_use_command_not_found(self):
        # Test the Shell class's use method with a non-existent command
        shell = Shell()
        output = shell.use("nonexistentcommand")
        self.assertEqual(output, "Command not found")

    def test_RunPython_use(self):
        # Test the RunPython class's use method with a simple Python expression
        run_python = RunPython()
        output = run_python.use('print("Hello, world!")')
        self.assertEqual(output, "")

    def test_RunPython_use_exception(self):
        # Test the RunPython class's use method with code that raises an exception
        run_python = RunPython()
        code = "print(1/0)"  # generate a long code that raises an exception
        output = run_python.use(code)
        self.assertTrue("ZeroDivisionError" in output)


if __name__ == "__main__":
    unittest.main()
