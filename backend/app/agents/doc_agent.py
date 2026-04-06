"""Document processing agent: extract and preprocess documents."""
from backend.app.tools.pdf_parser import extract_text

class DocumentAgent:
    def run(self, file):
        return extract_text(file)