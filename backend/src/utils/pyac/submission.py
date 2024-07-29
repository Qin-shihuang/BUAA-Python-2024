import io
import zlib
import re

from typing import Optional
from dataclasses import dataclass

from antlr4 import *
from utils.pyac.lexer.PythonLexer import PythonLexer
from utils.pyac.lexer.PythonParser import PythonParser
from antlr4.error.ErrorListener import ConsoleErrorListener

dummy_code = "n=1"


@dataclass
class Submission:
    root: ParserRuleContext
    content: str
    compressed_size: Optional[int] = None

    def __init__(self, content: str):
        self.root = parse(content)
        self.content = content

    def getCompSize(self) -> int:
        if self.compressed_size is None:
            self.compressed_size = len(zlib.compress(self.root.toStringTree(recog=self.root.parser).encode()))
        return self.compressed_size
    
def parse(content):
    lexer = PythonLexer(InputStream(content))
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)
    parser.removeErrorListener(ConsoleErrorListener.INSTANCE)
    try:
        tree = parser.file_input()
    except:
        lexer = PythonLexer(InputStream(dummy_code))
        stream = CommonTokenStream(lexer)
        parser = PythonParser(stream)
        tree = parser.file_input()
    finally:
        return tree