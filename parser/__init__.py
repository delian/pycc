from ply import lex
import tokenization
import ply.yacc as yacc
from tokenization import tokens
import history


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


def p_program(p):
    """program : functions
    | glob_variables ';' functions
    """
    p[0] = Node("PROGRAM", [p[1]])


def p_glob_variables(p):
    """glob_variables : glob_variable
    | glob_variables ';' glob_variable"""
    if len(p) == 2:
        p[0] = Node("GLOB_VARIABLES", [p[1]])
    else:
        p[0] = Node("GLOB_VARIABLES", [p[1], p[3]])


def p_glob_variable(p):
    """glob_variable : NAME '=' expression"""
    p[0] = Node("GLOB_VARIABLE", [p[3]], p[1])


def p_functions(p):
    """functions : function
    | functions ';' function"""
    if len(p) == 2:
        p[0] = Node("FUNCTIONS", [p[1]])
    else:
        p[0] = Node("FUNCTIONS", [p[1], p[3]])


def p_function(p):
    """function : NAME '(' ')' block"""
    p[0] = Node("FUNCTION", [p[4]], p[1])


def p_block(p):
    """block : '{' statements '}'
    | '{' statements ';' '}'
    | '{' '}'
    """
    if p[2] == "}":
        p[0] = Node("BLOCK", [])
    else:
        p[0] = Node("BLOCK", [p[2]])


def p_statements(p):
    """statements : statement
    | statements ';' statement"""
    if len(p) == 2:
        p[0] = Node("STATEMENTS", [p[1]])
    else:
        p[0] = Node("STATEMENTS", [p[1], p[3]])


def p_statement(p):
    """statement : var_declare
    | var_assign
    | function_call
    | expression
    | block
    """
    p[0] = Node("STATEMENT", [p[1]])


def p_var_declare(p):
    """var_declare : LET NAME
    | LET NAME '=' expression
    """  # no expression yet
    if len(p) < 4:
        p[0] = Node("VAR_DECLARE", [], p[2])
    else:
        p[0] = Node("VAR_DECLARE", [p[4]], p[2])


def p_var_assign(p):
    """var_assign : NAME '=' expression"""
    p[0] = Node("VAR_ASSIGN", [p[3]], p[1])


def p_function_call(p):
    """function_call : NAME '(' ')'"""
    p[0] = Node("FUNCTION_CALL", [], p[1])


def p_expression(p):
    """expression : expression '+' term
            | expression '-' term
            | expression '+' function_call
            | expression '-' function_call
    term : term '*' factor
         | term '/' factor
         | term '*' function_call
         | term '/' function_call
    """
    match p[2]:
        case "+":
            p[0] = Node("PLUS", [p[1], p[3]], p[2])
        case "-":
            p[0] = Node("MINUS", [p[1], p[3]], p[2])
        case "*":
            p[0] = Node("MULTIPLY", [p[1], p[3]], p[2])
        case "/":
            p[0] = Node("DIVIDE", [p[1], p[3]], p[2])


def p_expression_term(p):
    """expression : term"""
    p[0] = Node("TERM", [p[1]])


def p_term_factor(p):
    """term : factor"""
    p[0] = Node("FACTOR", [p[1]])


def p_factor_num(p):
    """factor : NUMBER"""
    p[0] = Node("NUMBER", leaf=p[1])


def p_factor_variable(p):
    """factor : NAME"""
    p[0] = Node("VARIABLE", leaf=p[1])


def p_factor_expr(p):
    """factor : '(' expression ')'"""
    p[0] = Node("EXPRESSION", [p[2]])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)


lex.lex(module=tokenization)
parser = yacc.yacc()


def parse(s):
    return parser.parse(s)


def run():
    while True:
        try:
            s = input("input > ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        # breakpoint()
        print(result)
