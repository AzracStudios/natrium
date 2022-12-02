package tests

import (
	l "natrium/src/lexer"
	"testing"
)

type LexerTest struct {
	src      string
	expected []l.Token
}

func TestLexer(t *testing.T) {
	var test []LexerTest = []LexerTest{
		{src: "++--", expected: []l.Token{
			l.NewToken("OPERATOR", "PLUS", l.NewPosition(0, 0, 0), l.NewPosition(1, 1, 0)),
			l.NewToken("OPERATOR", "PLUS", l.NewPosition(1, 1, 0), l.NewPosition(2, 2, 0)),
			l.NewToken("OPERATOR", "MINUS", l.NewPosition(2, 2, 0), l.NewPosition(3, 3, 0)),
			l.NewToken("OPERATOR", "MINUS", l.NewPosition(3, 3, 0), l.NewPosition(4, 4, 0)),
		}},
		{src: "* /\n+", expected: []l.Token{
			l.NewToken("OPERATOR", "MULTIPLY", l.NewPosition(0, 0, 0), l.NewPosition(1, 1, 0)),
			l.NewToken("OPERATOR", "DIVIDE", l.NewPosition(2, 2, 0), l.NewPosition(3, 3, 0)),
			l.NewToken("FILE", "NL", l.NewPosition(3, 3, 0), l.NewPosition(3, 3, 0)),
			l.NewToken("OPERATOR", "PLUS", l.NewPosition(4, 1, 1), l.NewPosition(5, 2, 1)),
		}},
	}

	for i := 0; i < len(test); i++ {
		var lexer l.Lexer = l.NewLexer(test[i].src)

		var tokens []l.Token = lexer.Tokenize()
		var expected []l.Token = test[i].expected

		if len(tokens) != len(expected) {
			t.Errorf("\nTest %v: Tokens were incorrect, \ngot: %v, \nwant: %v", i, tokens, expected)
		}

		for i := 0; i < len(tokens); i++ {
			if tokens[i] != expected[i] {
				t.Errorf("\nTest %v: Tokens were incorrect, \ngot: %v, \nwant: %v", i, tokens, expected)
			}
		}
	}
}
