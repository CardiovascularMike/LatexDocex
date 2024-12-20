from LatexParser import LatexParser
from DocFormatter import DocFormatter
from FigureParser import FigureParser
#from MathParser import MathParser
import re
import matplotlib.pyplot as plt

class LatexToDocx:
    def __init__(self, latex_code):
        self.latex_code = latex_code
        self.parser = LatexParser(latex_code)
        self.formatter = DocFormatter()
        self.figureparse = FigureParser()

    def process(self):
        """Main method to process LaTeX code and generate a Word document."""
        # Step 1: Convert LaTeX to plain text
        plain_text = self.parser.convert_to_text()
        print(plain_text)
        # Step 2: Parse formatting metadata
        formatting = self.parser.parse_formatting()
        figureNumber = 0
        captionBuddy = False
        # Step 3: Add content to the Word document
        for line in plain_text.split('\n'):
            if not line.strip():
                continue  # Skip empty lines

            matched = False
            for fmt in formatting:
                #print(f"Checking if '{fmt['text'].lower()}' is in '{line.lower()}'")  # Debug statement
                if fmt['text'].lower() in line.lower():
                    if fmt['type'] == 'section' and len(line) < 50:
                        self.formatter.add_heading(fmt['text'], level=1)
                        matched = True
                    elif fmt['type'] == 'subsection' and len(line) < 50:
                        self.formatter.add_heading(fmt['text'], level=2)
                        matched = True
                    elif fmt['type'] == 'bold':
                        self.formatter.add_bold(line, fmt['text'])
                        matched = True
                    elif fmt['type'] == 'align':
                        self.formatter.add_math_as_figure(fmt['text'])

            if not matched:
                if line.strip().startswith('*'):
                    self.formatter.add_bulleted_line(line)
                elif line.strip().startswith('< g r'):
                    print('Graphic Found in plain text')
                    figures, captions = self.figureparse.parse_figures(self.latex_code, plain_text)
                    if captions[figureNumber] != '':
                        captionBuddy = True
                    self.formatter.add_figure(figures[figureNumber])
                    figureNumber = figureNumber + 1
                elif captionBuddy:
                    self.formatter.add_caption(captions[figureNumber], figureNumber)
                    captionBuddy = False
                else:
                    self.handle_math_expressions(line)

    def handle_math_expressions(self, line):
        #-Look for stuff between $ and add as math-#
        math_pattern = re.compile(r'\$\$(.*?)\$\$|\$(.*?)\$')
        #block_math_pattern = re.compile(r'')
        mathcheck = math_pattern.search(line)
        if mathcheck:
            math_parts = []
            last_end = 0
            if mathcheck.group(1):
                print('BLOCK MATH FOUND DEBUG STATEMENT')
                math_text = mathcheck.group(1)
                self.formatter.add_math_as_figure(math_text)
            else:
                for match in math_pattern.finditer(line):
                    text_before = line[last_end:match.start()]
                    math_text = match.group(2)
                    math_parts.append((text_before, math_text))
                    last_end = match.end()
                text_after = line[last_end:]
                math_parts.append((text_after, None))
                self.formatter.add_math_paragraph(math_parts)
        else:
            self.formatter.add_paragraph(line)
    
    def math_expressions_inline_with_formatting(self, line, para):
        return
    
    def save(self, filename):
        """Saves the generated Word document."""
        self.formatter.save(filename)
