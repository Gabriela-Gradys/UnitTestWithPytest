"""File for mocking part."""
import os
import requests


class BritishGentleman:
    """Class for greeting."""

    def __init__(self):
        pass

    def greeting(self):
        """Wish everything best!"""

        self.destroy_the_world()
        return "Have a nice day!"

    def destroy_the_world(self):
        """Hahaha!"""

        raise ValueError

    def show_me_your_variable(self):
        """Get environment variable"""

        return os.getenv("OUR_MISTERIOUS_ENV", "None")

    def check_file(self, filepath):
        """Get text from file."""

        with open(filepath, encoding="utf-8") as file:
            return file.readline()

    def get_website_text(self, website):
        """Get code text from the website."""

        req = requests.get(str(website), timeout=15)
        return req.text
