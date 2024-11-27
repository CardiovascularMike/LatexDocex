import re
from pylatexenc.latex2text import LatexNodes2Text

class LatexParser:
    def __init__(self, latex_code):
        self.latex_code = latex_code
        self.plain_text = ""
        self.formatting = []

    def convert_to_text(self):
        """Converts LaTeX code to plain text using pylatexenc."""
        converter = LatexNodes2Text(keep_inline_math=True)
        self.plain_text = converter.latex_to_text(self.latex_code)
        return self.plain_text

    def parse_formatting(self):
        """Parses LaTeX code to extract headings, bold text, etc."""
        section_pattern = re.compile(r'\\section{(.*?)}')
        subsection_pattern = re.compile(r'\\subsection{(.*?)}')
        bold_pattern = re.compile(r'\\textbf{(.*?)}')
        align_pattern = re.compile(r'\\begin{align}(.*?)\\end{align}', re.DOTALL)
        align_pattern2 = re.compile(r'\\begin{align\*}(.*?)\\end{align\*}', re.DOTALL)

        # Extract formatting metadata
        for match in section_pattern.finditer(self.latex_code):
            line_start = self.latex_code.rfind('\n', 0, match.start()+1)
            if not '%' in self.latex_code[line_start:match.start()]:
                self.formatting.append({'type': 'section', 'text': match.group(1)})
        for match in subsection_pattern.finditer(self.latex_code):
            line_start = self.latex_code.rfind('\n', 0, match.start())
            if not '%' in self.latex_code[line_start:match.start()+1]:
                self.formatting.append({'type': 'subsection', 'text': match.group(1)})
        for match in bold_pattern.finditer(self.latex_code):
            line_start = self.latex_code.rfind('\n', 0, match.start())
            if not '%' in self.latex_code[line_start:match.start()+1]:
                self.formatting.append({'type': 'bold', 'text': match.group(1)})
        for match in align_pattern.finditer(self.latex_code):
            line_start = self.latex_code.rfind('\n', 0, match.start())
            if not '%' in self.latex_code[line_start:match.start()+1]:
                self.formatting.append({'type': 'align', 'text': match.group(1)})
        for match in align_pattern2.finditer(self.latex_code):
            line_start = self.latex_code.rfind('\n', 0, match.start())
            if not '%' in self.latex_code[line_start:match.start()+1]:
                self.formatting.append({'type': 'align', 'text': match.group(1)})

        return self.formatting