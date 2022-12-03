expression:
    NOT compare
    compare ((AND) compare)*

compare:
    arithemtic-expression ((EE | NE | LT | GT | LTE | GTE) arithemtic-expression)*

arithmetic-expression:
    term ((PLUS | MINUS) term)*

term:
    factor ((MULTIPLY | DIVIDE | MOD) factor)*

factor:
    (PLUS | MINUS) factor
    power

power:
    quark (POW factor)*

quark:
    NUMBER | STRING | IDENTIFIER | KEYWORD
    LPAREN expr RPAREN