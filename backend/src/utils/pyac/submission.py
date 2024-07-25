import io
import zlib
import re

from typing import Optional
from dataclasses import dataclass

from antlr4 import *
from utils.pyac.lexer.PythonLexer import PythonLexer
from utils.pyac.lexer.PythonParser import PythonParser

@dataclass
class Submission:
    root: ParserRuleContext
    content: str
    compressed_size: Optional[int] = None

    def __init__(self, content: str):
        self.root = content
        self.content = self.root.toStringTree(recog=self.root.parser)

    @staticmethod
    def from_string(content: str):
        return Submission(parse(content))

    def getCompSize(self) -> int:
        if self.compressed is None:
            self.compressed_size = len(zlib.compress(self.content.encode()))
        return self.compressed_size
    
def parse(content):
    lexer = PythonLexer(InputStream(content))
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)
    try:
        tree = parser.file_input()
    except Exception as e:
        tree = '0'
    finally:
        return tree