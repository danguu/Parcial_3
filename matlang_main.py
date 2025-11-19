import sys
from antlr4 import FileStream, CommonTokenStream
from MatLangLexer import MatLangLexer
from MatLangParser import MatLangParser
from matlang_semantics import EvalVisitor


def main(input_path: str):
    # Crear flujo de entrada
    input_stream = FileStream(input_path, encoding="utf-8")

    # Lexer y parser
    lexer = MatLangLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = MatLangParser(token_stream)

    tree = parser.program()

    # Visitor de evaluación
    visitor = EvalVisitor()
    visitor.visit(tree)


path = "program.mt"
if len(sys.argv) > 1:
    path = sys.argv[1]

main(path)
