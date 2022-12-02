package lexer

type Lexer struct {
	src         string
	Tokens      []Token
	currentChar byte
	currentPos  Position
}

func NewLexer(src string) Lexer {
	return Lexer{
		src: src,
	}
}

func (l *Lexer) Next() Token {
	var pos Position = l.currentPos.Copy()
	var c byte = l.currentChar
	var token Token

	switch c {
	case ' ':
		return NewToken("SPACE", "", pos, pos)
	case '\n':
		return NewToken("FILE", "NL", pos, pos)
	case '+':
		token = NewToken("OPERATOR", "PLUS", pos.Copy(), pos.Advance(c))

	case '-':
		token = NewToken("OPERATOR", "MINUS", pos.Copy(), pos.Advance(c))

	case '*':
		token = NewToken("OPERATOR", "MULTIPLY", pos.Copy(), pos.Advance(c))

	case '/':
		token = NewToken("OPERATOR", "DIVIDE", pos.Copy(), pos.Advance(c))

	case '%':
		token = NewToken("OPERATOR", "MOD", pos.Copy(), pos.Advance(c))

	case '^':
		token = NewToken("OPERATOR", "POWER", pos.Copy(), pos.Advance(c))
	}

	return token
}

func (l *Lexer) Advance() bool {
	l.currentPos.Advance(l.currentChar)

	if l.currentPos.Idx == len(l.src) {
		return true
	}

	l.currentChar = l.src[l.currentPos.Idx]
	return false
}

func (l *Lexer) Tokenize() []Token {
	var tokens []Token
	l.currentPos = NewPosition(-1, -1, 0)

	var eof bool = l.Advance()

	for !eof {
		var next Token = l.Next()

		if next.Type != "SPACE" {
			tokens = append(tokens, next)
		}

		eof = l.Advance()
	}

	return tokens
}
