package lexer

type Token struct {
	Type  string  // OPERATOR | FILE
	Value string
	Start Position
	End   Position
}

func NewToken(_type string, value string, start Position, end Position) Token {
	return Token{
		Type:  _type,
		Value: value,
		Start: start,
		End:   end,
	}
}