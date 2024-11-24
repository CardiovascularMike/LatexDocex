import re

class MathParser:
    def __init__(self):
        pass
    def parse_math(self, line):
        """Parses LaTeX math expressions."""
        math_pattern = re.compile(r'\$(.*?)\$')
        math_parts = []
        last_end = 0
        for match in math_pattern.finditer(line):
            if match.start() > last_end:
                math_parts.append((line[last_end:match.start()], None))
            math_parts.append((None, match.group(1)))
            last_end = match.end()
        if last_end < len(line):
            math_parts.append((line[last_end:], None))
        return math_parts