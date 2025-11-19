grammar MatLang;

//  Reglas de parser 

program
    : stmtList EOF
    ;

stmtList
    : stmtList stmt SEMI
    | stmt SEMI
    ;

stmt
    : matrixDecl
    | assign
    | printStmt
    ;

matrixDecl
    : MAT ID LBRACK INT COMMA INT RBRACK EQ matrixLit
    ;

assign
    : ID EQ expr
    ;

printStmt
    : PRINT ID
    ;

expr
    : multExpr
    ;

multExpr
    : primary (MUL primary)*
    ;

primary
    : ID
    | matrixLit
    | LPAREN expr RPAREN
    ;

matrixLit
    : LBRACK row (COMMA row)* RBRACK
    ;

row
    : LBRACK num (COMMA num)* RBRACK
    ;

num
    : INT
    | FLOAT
    ;

//  Reglas léxicas 

MAT      : 'mat';
PRINT    : 'print';

MUL      : '*';
EQ       : '=';
COMMA    : ',';
SEMI     : ';';

LBRACK   : '[';
RBRACK   : ']';
LPAREN   : '(';
RPAREN   : ')';

INT      : [0-9]+;
FLOAT    : [0-9]+ '.' [0-9]+;

ID       : [a-zA-Z_][a-zA-Z_0-9]*;

WS       : [ \t\r\n]+ -> skip;
LINE_COMMENT
         : '//' ~[\r\n]* -> skip;
