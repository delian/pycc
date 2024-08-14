__all__ = ["tokens"]

tokens = (
    "NUMBER",
    "NAME",
    "LET",
)

t_LET = r"let"
t_NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

literals = ["=", "+", "-", "*", "/", "(", ")", "{", "}", ";"]

t_ignore = " \t"
t_ignore_COMMENT = r"\/\/.*"


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
