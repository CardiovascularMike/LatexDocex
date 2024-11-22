from LatexParser import LatexParser
from DocFormatter import DocFormatter
from FigureParser import FigureParser

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
        # Step 2: Parse formatting metadata
        formatting = self.parser.parse_formatting()
        figureNumber = 0
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
                    elif fmt['type'] == 'bold' and len(line) < 50:
                        self.formatter.add_bold(fmt['text'])
                        matched = True

            if not matched:
                if line.strip().startswith('*'):
                    self.formatter.add_bulleted_line(line)
                elif line.strip().startswith('< g r'):
                    print('Graphic Found in plain text')
                    figures = self.figureparse.parse_figures(self.latex_code, plain_text)
                    self.formatter.add_figure(figures[figureNumber])
                    figureNumber = figureNumber + 1
                    self.formatter.add_paragraph('Graphic Goes Here!')
                else:
                    self.formatter.add_paragraph(line)

    def save(self, filename):
        """Saves the generated Word document."""
        self.formatter.save(filename)
