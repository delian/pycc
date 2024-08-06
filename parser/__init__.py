from ply import lex
import tokenization
import ply.yacc as yacc
from tokenization import tokens


class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf

    def __str__(self):
        return (
            f"{self.type}({', '.join(str(child) for child in self.children)})"
            if self.children
            else f"{self.type}({self.leaf})"
        )


def p_expression_plus(p):
    """expression : expression PLUS term"""
    p[0] = Node("PLUS", [p[1], p[3]], p[2])


def p_expression_minus(p):
    """expression : expression MINUS term"""
    p[0] = Node("MINUS", [p[1], p[3]], p[2])


def p_expression_term(p):
    """expression : term"""
    p[0] = Node("TERM", [p[1]])


def p_term_times(p):
    """term : term TIMES factor"""
    p[0] = Node("MULTIPLY", [p[1], p[3]], p[2])


def p_term_div(p):
    """term : term DIVIDE factor"""
    p[0] = Node("DIVIDE", [p[1], p[3]], p[2])


def p_term_factor(p):
    """term : factor"""
    p[0] = Node("FACTOR", [p[1]])


def p_factor_num(p):
    """factor : NUMBER"""
    p[0] = Node("NUMBER", leaf=p[1])


def p_factor_expr(p):
    """factor : LPAREN expression RPAREN"""
    p[0] = Node("EXPRESSION", [p[2]])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


lex.lex(module=tokenization)
parser = yacc.yacc()


def run():
    while True:
        try:
            s = input("calc > ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        # breakpoint()
        print(result)
