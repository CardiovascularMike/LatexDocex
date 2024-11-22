from docx import Document
from docx.shared import Inches
class DocFormatter:
    def __init__(self):
        self.document = Document()

    def add_paragraph(self, text):
        """Adds a paragraph to the Word document."""
        self.document.add_paragraph(text)
    def add_heading(self, text, level=1):
        """Adds a heading to the Word document."""
        self.document.add_heading(text, level=level)
        print('heading')
    def add_bold(self, text):
        """Adds a bold text paragraph to the Word document."""
        para = self.document.add_paragraph()
        run = para.add_run(text)
        run.bold = True
        print('bold')
    def add_bulleted_line(self, text):
        """Adds a bulleted list item to the Word document."""
        """Delete the first character of the text, which is the *."""
        print(text)
        text = text.strip()[1:]
        print(text)
        self.document.add_paragraph(text, style='List Bullet')
        print('bulleted line')
    def add_figure(self, filename):
        """Adds a figure to the Word document."""
        self.document.add_picture('PlaceImagesHere/'+filename, width=Inches(6.0))
        print('figure')
    def save(self, filename):
        """Saves the Word document to the specified file."""
        self.document.save(filename)
