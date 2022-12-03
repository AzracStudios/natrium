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
		// CHECK IDENTIFICATION
		{src: "++--", expected: []l.Token{
			l.NewToken("OPERATOR", "PLUS", l.NewPosition(0, 0, 0), l.NewPosition(1, 1, 0)),
			l.NewToken("OPERATOR", "PLUS", l.NewPosition(1, 1, 0), l.NewPosition(2, 2, 0)),
			l.NewToken("OPERATOR", "MINUS", l.NewPosition(2, 2, 0), l.NewPosition(3, 3, 0)),
			l.NewToken("OPERATOR", "MINUS", l.NewPosition(3, 3, 0), l.NewPosition(4, 4, 0)),
			l.NewToken("FILE", "EOF", l.NewPosition(4, 4, 0), l.NewPosition(4, 4, 0)),
		}},

		// CHECK NEW LINE
		{src: "* /\n+", expected: []l.Token{
			l.NewToken("OPERATOR", "MULTIPLY", l.NewPosition(0, 0, 0), l.NewPosition(1, 1, 0)),
			l.NewToken("OPERATOR", "DIVIDE", l.NewPosition(2, 2, 0), l.NewPosition(3, 3, 0)),
			l.NewToken("FILE", "NL", l.NewPosition(3, 3, 0), l.NewPosition(3, 3, 0)),
			l.NewToken("OPERATOR", "PLUS", l.NewPosition(4, 1, 1), l.NewPosition(5, 2, 1)),
			l.NewToken("FILE", "EOF", l.NewPosition(5, 2, 1), l.NewPosition(5, 2, 1)),
		}},

		// CHECK NUMBERS
		{src: "465484.05 + 5465 - 3", expected: []l.Token{
			l.NewToken("NUMBER", "465484.05", l.NewPosition(0, 0, 0), l.NewPosition(9, 9, 0)),
			l.NewToken("OPERATOR", "PLUS", l.NewPosition(10, 10, 0), l.NewPosition(11, 11, 0)),
			l.NewToken("NUMBER", "5465", l.NewPosition(12, 12, 0), l.NewPosition(16, 16, 0)),
			l.NewToken("OPERATOR", "MINUS", l.NewPosition(17, 17, 0), l.NewPosition(18, 18, 0)),
			l.NewToken("NUMBER", "3", l.NewPosition(19, 19, 0), l.NewPosition(20, 20, 0)),
			l.NewToken("FILE", "EOF", l.NewPosition(21, 21, 0), l.NewPosition(21, 21, 0)),
		}},

		// CHECK INVALID NUMBERS
		{src: "30.5.2", expected: []l.Token{
			l.NewToken("ERROR", "_", l.NewPosition(0, 0, 0), l.NewPosition(0, 0, 0)),
			l.NewToken("FILE", "EOF", l.NewPosition(6, 6, 0), l.NewPosition(6, 6, 0)),
		}},

		// CHECK KEYWORD AND IDENTIFIER
		{src: "task x", expected: []l.Token{
			l.NewToken("KEYWORD", "task", l.NewPosition(0, 0, 0), l.NewPosition(4, 4, 0)),
			l.NewToken("IDENTIFIER", "x", l.NewPosition(5, 5, 0), l.NewPosition(6, 6, 0)),
			l.NewToken("FILE", "EOF", l.NewPosition(7, 7, 0), l.NewPosition(7, 7, 0)),
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
