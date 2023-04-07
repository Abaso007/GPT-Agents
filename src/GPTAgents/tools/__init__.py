"""
Tools that AI can interact with

Feel free to make a pull request and make more tools!
"""
import os
import subprocess
import inspect
import requests
import html2text


class Tools:
    """
    Template tools class
    """

    def __init__(self) -> None:
        pass


class Shell(Tools):
    """
    This tool allows the AI to interact with the shell and execute arbitrary bash commands
    """

    def use(self, command: str) -> str:
        """
        Execute a shell command
        """

        # Split the command into a list
        command = command.split()

        # Join quoted arguments
        i = 0
        while i < len(command):
            if command[i].startswith('"') and not command[i].endswith('"'):
                while not command[i].endswith('"'):
                    command[i] = command[i] + " " + command[i + 1]
                    del command[i + 1]
            i += 1

        # If the command is empty, return an empty string
        if not command:
            return ""

        # If the command is `cd` and there is a second argument, change the directory
        if command[0] == "cd" and len(command) > 1:
            try:
                os.chdir(command[1])
            except FileNotFoundError:
                return "Directory not found"
            return ""

        # If the command is `cd` and there is no second argument, change the directory to the home directory
        if command[0] == "cd" and len(command) == 1:
            os.chdir(os.path.expanduser("~"))
            return ""

        # Execute the command
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            return output.decode("utf-8")
        except subprocess.CalledProcessError as error:
            # If the command failed, return the error
            return error.output.decode("utf-8")
        except FileNotFoundError:
            # If the command was not found, return an error
            return "Command not found"


class RunPython(Tools):
    """
    Allows the AI to run Python code
    """

    def use(self, code: str) -> str:
        """
        Run Python code
        """

        # If the code is empty, return an empty string
        if not code:
            return ""
        try:
            # Evaluate the code
            exec(code)
            return ""
        except Exception as error:
            # Get error type
            error_type = type(error).__name__
            # Get error message
            error_message = str(error)
            # Return the error
            return f"{error_type}: {error_message}"


class WebSearch(Tools):
    """
    Use a search engine to search the web
    """

    def use(self, query: str) -> str:
        """
        Search the web
        """
        resp = requests.post(
            url="https://ddg-api.herokuapp.com/search",
            json={"query": query, "limit": 5},
            timeout=10,
        )
        resp.encoding = "utf-8" if resp.encoding is None else resp.encoding
        search_results = resp.text
        return search_results


class WebCrawler(Tools):
    """
    Gets the text from a web page (without HTML)
    """

    def use(self, url: str) -> str:
        """
        Gets the text from a web page (without HTML)
        """
        resp = requests.get(url, timeout=60)
        resp.encoding = "utf-8" if resp.encoding is None else resp.encoding
        html = resp.text
        text_maker = html2text.HTML2Text()
        text_maker.ignore_images = True

        text = text_maker.handle(html)
        return text


# Get a list of all the tools in this module and their docstrings
tools = []

for name in dir():
    obj = eval(name)
    if isinstance(obj, type) and issubclass(obj, Tools):
        for func_name, func_obj in obj.__dict__.items():
            if callable(func_obj) and func_obj.__qualname__.startswith(
                obj.__qualname__
            ):
                params = list(inspect.signature(func_obj).parameters.values())
                tools.append((name, obj.__doc__.strip(), func_name, params))


def get_tools() -> str:
    """
    Formats the tools into a string
    """
    # Format the tools
    output = ""
    for tool in tools:
        output += f"{tool[0]}: {tool[1]} \n"
        for param in tool[3]:
            output += f"    {tool[2]}({param.name}: {(param.annotation.__name__)})\n"
    return output


if __name__ == "__main__":
    # Print the tools
    print(get_tools())
