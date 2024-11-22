import glob
import re

class FigureParser:
    def __init__(self):
        #self.latex_code = latex_code
        #self.plain_text = plain_text
        self.ImageList = []
        self.ImageLoc = '/PlaceImagesHere'
    
    def parse_figures(self, latex_code, plain_text):
        """Parses LaTeX code to extract figure filenames."""
        # Extract figure filenames
        #figure_pattern = re.compile(r'\\includegraphics{(.*)}')
        figure_pattern = re.compile(r'\\includegraphics(?:\[[^\]]*\])?{([^}]*)}')
        for match in figure_pattern.finditer(latex_code):
            #-Only include the text after / character
            text = match.group(1)
            text = text[text.rfind('/')+1:]
            self.ImageList.append(text)
        print(self.ImageList)
        return self.ImageList