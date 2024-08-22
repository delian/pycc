from ply import lex
import tokenization
import ply.yacc as yacc
from tokenization import tokens
import history
from node import Node


def p_program(p):
    """program : functions
    | glob_variables ';' functions
    |
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
    | functions ';' function
    | functions function
    """
    match len(p):
        case 2:
            p[0] = Node("FUNCTIONS", [p[1]])
        case 3:
            p[0] = Node("FUNCTIONS", [p[1], p[2]])
        case 4:
            p[0] = Node("FUNCTIONS", [p[1], p[3]])
        case _:
            raise SyntaxError(f"Incorrect function definition {p}")


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
    | compl_expression
    """
    p[0] = Node("STATEMENT", [p[1]])


def p_compl_expression(p):
    """compl_expression : var_assign
    | expression
    | if_statement
    | block
    | comp_andor_expression
    | comp_expression
    | bitwise_expression
    """
    p[0] = Node("COMPL_EXPRESSION", [p[1]])


def p_if_statement(p):
    """if_statement : IF '(' comp_andor_expression ')' block
    | IF '(' comp_andor_expression ')' block ELSE block
    """
    if len(p) == 6:
        p[0] = Node("IF_STATEMENT", [p[3], p[5]])
    else:
        p[0] = Node("IF_ELSE_STATEMENT", [p[3], p[5], p[7]])


def p_comparision_andor_expression(p):
    """comp_andor_expression : comp_expression AND comp_expression
    | comp_expression OR comp_expression
    | comp_expression XOR comp_expression
    | comp_expression OR not_expression
    | not_expression OR comp_expression
    | not_expression OR not_expression
    | comp_expression AND not_expression
    | not_expression AND comp_expression
    | not_expression AND not_expression
    | comp_expression XOR not_expression
    | not_expression XOR comp_expression
    | not_expression XOR not_expression
    """
    p[0] = Node("COMP_ANDOR_EXPRESSION", [p[1], p[3]], p[2])


def p_bitwise_expression(p):
    """bitwise_expression : expression '&' expression"""
    p[0] = Node("BITWISE_EXPRESSION", [p[1], p[3]], p[2])


def p_not_expression(p):
    """not_expression : '!' expression
    | NOT expression
    | '!' comp_expression
    | NOT comp_expression
    """
    p[0] = Node("NOT_EXPRESSION", [p[2]], p[1])
    pass


def p_comparision_expression(p):
    """comp_expression : expression '>' expression
    | expression '<' expression
    | expression LEQ expression
    | expression GEQ expression
    | expression EQ expression
    | expression NEQ expression
    """
    p[0] = Node("COMP_EXPRESSION", [p[1], p[3]], p[2])


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
    term : term '*' factor
         | term '/' factor
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
        case "%":
            p[0] = Node("MODULO", [p[1], p[3]], p[2])


def p_expression_term(p):
    """expression : term"""
    p[0] = Node("TERM", [p[1]])


def p_term_factor(p):
    """term : factor"""
    p[0] = Node("FACTOR", [p[1]])


def p_factor_num(p):
    """factor : NUMBER
    | '-' NUMBER
    | '+' NUMBER
    | '~' NUMBER
    """
    match len(p):
        case 3:
            match p[1]:
                case "+":
                    p[0] = Node("NUMBER", leaf=p[2])
                case "-":
                    p[0] = Node("NUMBER", leaf=-int(p[2]))
                case "~":
                    p[0] = Node("NUMBER", leaf=~int(p[2]))
        case 2:
            p[0] = Node("NUMBER", leaf=p[1])


def p_factor_variable(p):
    """factor : NAME"""
    p[0] = Node("VARIABLE", leaf=p[1])


def p_factor_expr(p):
    """factor : '(' compl_expression ')'"""
    p[0] = Node("EXPRESSION", [p[2]])


def p_factor_function_call(p):
    """factor : function_call"""
    p[0] = Node("FACTOR_FUNCTION_CALL", [p[1]])


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
