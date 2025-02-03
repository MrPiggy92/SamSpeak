TokenType = [
    "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
    "LEFT_BRACKET", "RIGHT_BRACKET",
    "COMMA", "DOT", "MINUS", "PLUS", "SEMICOLON", "SLASH", "STAR",
    "MODULO", "UP_ARROW",

    # One or two character tokens.
    "BANG", "BANG_EQUAL",
    "EQUAL", "EQUAL_EQUAL",
    "GREATER", "GREATER_EQUAL",
    "LESS", "LESS_EQUAL",

    # Literals.
    "IDENTIFIER", "STRING", "NUMBER",

    # Keywords.
    "AND", "CLASS", "ELSE", "FALSE", "FN", "FOR", "IF", "NIL", "OR",
    "RETURN", "SUPER", "THIS", "TRUE", "VAR", "WHILE",
    
    # EOF
    "EOF"
]
