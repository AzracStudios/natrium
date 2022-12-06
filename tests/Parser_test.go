package tests

import (
	l "natrium/src/lexer"
	p "natrium/src/parser"
	"testing"
)

type ParserTest struct {
	src      string
	expected p.ASTNode
}

var parserTests []ParserTest = []ParserTest{
	// CHECK SIMPLE BINARY OPERATOR
	{
		src:      "1 + 1",
		expected: 
			p.NewBinaryOperatorNode(
				p.NewNumberNode(
					l.NewToken("NUMBER", "1", l.NewPosition(0, 0, 0), l.NewPosition(1, 1, 0)), 
				),

				l.NewToken("OPERATOR", "PLUS", l.NewPosition(2, 2, 0), l.NewPosition(3, 3, 0)),

				p.NewNumberNode(
					l.NewToken("NUMBER", "1", l.NewPosition(4, 4, 0), l.NewPosition(5, 5, 0)), 
				),
			),
	},
}

func TestParser(t *testing.T) {
	var i int = 0

	for _, test := range parserTests {
		i++
		lexer := l.NewLexer(test.src)
		tokens := lexer.Tokenize()

		parser := p.NewParser(tokens)
		ast := parser.GenerateAbstractSyntaxTree().Node

		if ast != test.expected {
			t.Errorf("\nTest %v: Abstract Syntax Tree was incorrect, \ngot: %v, \nwant: %v", i, ast, test.expected)
		}

	}
}
