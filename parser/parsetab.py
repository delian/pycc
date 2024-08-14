
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "LET NAME NUMBERprogram : functions\n    | glob_variables ';' functions\n    glob_variables : glob_variable\n    | glob_variables ';' glob_variableglob_variable : NAME '=' expressionfunctions : function\n    | functions ';' functionfunction : NAME '(' ')' blockblock : '{' statements '}'\n    | '{' statements ';' '}'\n    | '{' '}'\n    statements : statement\n    | statements ';' statementstatement : expression\n    | var_declare\n    | var_assign\n    var_declare : LET NAMEvar_assign : NAME '=' expressionfunction_call : NAME '(' ')'expression : expression '+' term\n            | expression '-' term\n            | expression '+' function_call\n            | expression '-' function_call\n    term : term '*' factor\n         | term '/' factor\n         | term '*' function_call\n         | term '/' function_call\n    expression : termterm : factorfactor : NUMBERfactor : NAMEfactor : '(' expression ')'"
    
_lr_action_items = {'NAME':([0,7,8,10,22,24,25,26,27,28,36,50,52,],[6,12,15,17,17,37,40,40,45,45,51,37,17,]),'$end':([1,2,4,11,13,23,31,49,54,],[0,-1,-6,-7,-2,-8,-11,-9,-10,]),';':([2,3,4,5,11,13,14,17,18,19,20,21,23,30,31,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47,48,49,51,54,55,56,57,],[7,8,-6,-3,-7,7,-4,-31,-5,-28,-29,-30,-8,50,-11,-12,-14,-15,-16,-31,-20,-22,-31,-21,-23,-24,-26,-31,-25,-27,-32,-9,-17,-10,-13,-18,-19,]),'(':([6,10,12,15,22,24,25,26,27,28,40,45,50,52,],[9,22,9,9,22,22,22,22,22,22,53,53,22,22,]),'=':([6,15,37,],[10,10,52,]),')':([9,17,19,20,21,29,38,39,40,41,42,43,44,45,46,47,48,53,57,],[16,-31,-28,-29,-30,48,-20,-22,-31,-21,-23,-24,-26,-31,-25,-27,-32,57,-19,]),'NUMBER':([10,22,24,25,26,27,28,50,52,],[21,21,21,21,21,21,21,21,21,]),'{':([16,],[24,]),'*':([17,19,20,21,37,38,40,41,43,44,45,46,47,48,57,],[-31,27,-29,-30,-31,27,-31,27,-24,-26,-31,-25,-27,-32,-19,]),'/':([17,19,20,21,37,38,40,41,43,44,45,46,47,48,57,],[-31,28,-29,-30,-31,28,-31,28,-24,-26,-31,-25,-27,-32,-19,]),'+':([17,18,19,20,21,29,33,37,38,39,40,41,42,43,44,45,46,47,48,56,57,],[-31,25,-28,-29,-30,25,25,-31,-20,-22,-31,-21,-23,-24,-26,-31,-25,-27,-32,25,-19,]),'-':([17,18,19,20,21,29,33,37,38,39,40,41,42,43,44,45,46,47,48,56,57,],[-31,26,-28,-29,-30,26,26,-31,-20,-22,-31,-21,-23,-24,-26,-31,-25,-27,-32,26,-19,]),'}':([17,19,20,21,24,30,32,33,34,35,37,38,39,40,41,42,43,44,45,46,47,48,50,51,55,56,57,],[-31,-28,-29,-30,31,49,-12,-14,-15,-16,-31,-20,-22,-31,-21,-23,-24,-26,-31,-25,-27,-32,54,-17,-13,-18,-19,]),'LET':([24,50,],[36,36,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'functions':([0,8,],[2,13,]),'glob_variables':([0,],[3,]),'function':([0,7,8,],[4,11,4,]),'glob_variable':([0,8,],[5,14,]),'expression':([10,22,24,50,52,],[18,29,33,33,56,]),'term':([10,22,24,25,26,50,52,],[19,19,19,38,41,19,19,]),'factor':([10,22,24,25,26,27,28,50,52,],[20,20,20,20,20,43,46,20,20,]),'block':([16,],[23,]),'statements':([24,],[30,]),'statement':([24,50,],[32,55,]),'var_declare':([24,50,],[34,34,]),'var_assign':([24,50,],[35,35,]),'function_call':([25,26,27,28,],[39,42,44,47,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> functions','program',1,'p_program','__init__.py',26),
  ('program -> glob_variables ; functions','program',3,'p_program','__init__.py',27),
  ('glob_variables -> glob_variable','glob_variables',1,'p_glob_variables','__init__.py',33),
  ('glob_variables -> glob_variables ; glob_variable','glob_variables',3,'p_glob_variables','__init__.py',34),
  ('glob_variable -> NAME = expression','glob_variable',3,'p_glob_variable','__init__.py',42),
  ('functions -> function','functions',1,'p_functions','__init__.py',47),
  ('functions -> functions ; function','functions',3,'p_functions','__init__.py',48),
  ('function -> NAME ( ) block','function',4,'p_function','__init__.py',56),
  ('block -> { statements }','block',3,'p_block','__init__.py',61),
  ('block -> { statements ; }','block',4,'p_block','__init__.py',62),
  ('block -> { }','block',2,'p_block','__init__.py',63),
  ('statements -> statement','statements',1,'p_statements','__init__.py',72),
  ('statements -> statements ; statement','statements',3,'p_statements','__init__.py',73),
  ('statement -> expression','statement',1,'p_statement','__init__.py',81),
  ('statement -> var_declare','statement',1,'p_statement','__init__.py',82),
  ('statement -> var_assign','statement',1,'p_statement','__init__.py',83),
  ('var_declare -> LET NAME','var_declare',2,'p_var_declare','__init__.py',89),
  ('var_assign -> NAME = expression','var_assign',3,'p_var_assign','__init__.py',94),
  ('function_call -> NAME ( )','function_call',3,'p_function_call','__init__.py',99),
  ('expression -> expression + term','expression',3,'p_expression','__init__.py',104),
  ('expression -> expression - term','expression',3,'p_expression','__init__.py',105),
  ('expression -> expression + function_call','expression',3,'p_expression','__init__.py',106),
  ('expression -> expression - function_call','expression',3,'p_expression','__init__.py',107),
  ('term -> term * factor','term',3,'p_expression','__init__.py',108),
  ('term -> term / factor','term',3,'p_expression','__init__.py',109),
  ('term -> term * function_call','term',3,'p_expression','__init__.py',110),
  ('term -> term / function_call','term',3,'p_expression','__init__.py',111),
  ('expression -> term','expression',1,'p_expression_term','__init__.py',125),
  ('term -> factor','term',1,'p_term_factor','__init__.py',130),
  ('factor -> NUMBER','factor',1,'p_factor_num','__init__.py',135),
  ('factor -> NAME','factor',1,'p_factor_variable','__init__.py',140),
  ('factor -> ( expression )','factor',3,'p_factor_expr','__init__.py',145),
]
