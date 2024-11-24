import glob
import re

class FigureParser:
    def __init__(self):
        #self.latex_code = latex_code
        #self.plain_text = plain_text
        self.ImageList = []
        self.CaptionList = []
        self.ImageLoc = '/PlaceImagesHere'
    
    def parse_figures(self, latex_code, plain_text):
        """Parses LaTeX code to extract figure filenames."""
        # Extract figure filenames
        #figure_pattern = re.compile(r'\\includegraphics{(.*)}')
        figure_pattern = re.compile(r'\\includegraphics(?:\[[^\]]*\])?{([^}]*)}')
        caption_pattern = re.compile(r'\\caption{(.*)}')
        for match in figure_pattern.finditer(latex_code):
            #-Only include the text after / character
            text = match.group(1)
            text = text[text.rfind('/')+1:]
            self.ImageList.append(text)
        print(self.ImageList)
        for match in caption_pattern.finditer(latex_code):
            #-Add caption to caption list if the caption is starts within 6 lines of the figure-#
            if plain_text.find(match.group(1)) < plain_text.find(match.group(1)) + 6:
                self.CaptionList.append(match.group(1))
            else:
                self.CaptionList.append('')
        return self.ImageList, self.CaptionList