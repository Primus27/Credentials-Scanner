"""
Title: Generates ASCII title art based on input parameters
Author: Primus27
"""

# Import packages
import re
from sys import exit
from time import sleep

try:
    from pyfiglet import Figlet
except ImportError:
    print("'pyfiglet' module is missing. Closing application (10s)")
    sleep(10)
    exit()


class TitleGen:
    def __init__(self, text, font="big", width=79, justify="left",
                 author="", target=2):
        """
        Constructor method
        :param text: Text used for the title card
        :param font: Ref: http://www.figlet.org/fontdb.cgi
        :param width: Character length that the title wraps at.
            Increase if too low
        :param justify: Align 'left', 'center' or 'right'
        :param author: Program/script author
        :param target: Which line displays the author. Value is n from last
        """

        # Cast to int, if not possible, set default width
        if not isinstance(width, int):
            try:
                width = int(width)
            except ValueError:
                width = 79
        self.width = width

        # Cast to int, if not possible set default target value
        default_target = 2
        if not isinstance(target, int):
            try:
                target = int(target)
            except ValueError:
                target = default_target
        # Assuming user entered int, assign if valid, else assign default
        self.target = target if target in [1, 2, 3] else default_target

        self.text = str(text)
        self.font = str(font)
        self.author = "By {}".format(author) if author else ""
        self.justify = justify if justify in ["left", "center", "right"] \
            else "left"
        self.title = self.create_title()  # ASCII title card

    def create_title(self):
        """
        Creates a title based on the parameters
        :return: Returns the ASCII title as a string
        """
        # Create Figlet object
        banner = Figlet(font=self.font, justify=self.justify,
                        width=self.width).renderText(self.text)

        # Split banner into a list
        banner_list = re.split("\n", banner)
        # Target the nth to last line
        target = len(banner_list) - self.target
        # Remove characters in target line
        banner_list[target] = banner_list[target][(len(self.author)):]
        # Add credits to target line
        banner_list[target] = re.sub("^", self.author, banner_list[target])

        # Create new banner with whitespace between title words removed
        new_banner = []
        for line in banner_list:
            if not line.isspace():
                new_banner.append(line)

        # Return banner as a string
        return "\n".join(new_banner)
