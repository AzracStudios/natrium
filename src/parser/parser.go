package parser

import (
	e "natrium/src/error"
	l "natrium/src/lexer"
	u "natrium/src/utils"
)

type Parser struct {
	Tokens  []l.Token
	Tree    []ASTNode
	tokIdx  int
	current l.Token
}

func NewParser(tokens []l.Token) Parser {
	var parser Parser = Parser{
		Tokens: tokens,
		tokIdx: -1,
	}

	parser.Advance()
	return parser
}

func (p *Parser) Advance() l.Token {
	p.tokIdx++

	if p.tokIdx < len(p.Tokens) {
		p.current = p.Tokens[p.tokIdx]
	}

	return p.current
}

func (p *Parser) GenerateAbstractSyntaxTree() ParseRegister {
	var res ParseRegister = p.Expression()

	if !res.Error.True() && p.current.Value != "EOF" {
		return res.Failure(e.NewError("", p.current.Start.Copy(), p.current.End.Copy()))
	}

	return res
}

func (p *Parser) Factor() ParseRegister {
	var res ParseRegister = NewParseRegister()
	var tok l.Token = p.current

	if u.ContainsString([]string{"PLUS", "MINUS"}, tok.Value) {
		p.Advance()
		var fac ASTNode = res.Register(p.Factor())
		if res.Error.True() {
			return res
		}

		return res.Success(NewUnaryOperatorNode(tok, fac))
	} else if  u.ContainsString([]string{"NUMBER"}, tok.Type) {
		p.Advance()
		return res.Success(NewNumberNode(tok))
	} else if tok.Value == "LPAREN" {
		p.Advance()
		var expr ASTNode = res.Register(p.Expression())
		if res.Error.True() {
			return res
		}

		if p.current.Value == "RPAREN" {
			p.Advance()
			return res.Success(expr)
		} else {
			// TODO: RETURN INVALID SYNTAX ERROR
		}
	}

	// TODO: RETURN INVALID SYNTAX ERROR
	return res
}

func (p *Parser) Term() ParseRegister {
	return p.BinOp(p.Factor, p.Factor, []string{"MULTIPLY", "DIVIDE"})
}

func (p *Parser) Expression() ParseRegister {
	return p.BinOp(p.Factor, p.Factor, []string{"PLUS", "MINUS"})
	
}

func (p *Parser) BinOp(lFunc func() ParseRegister, rFunc func() ParseRegister, op []string) ParseRegister {
	var res ParseRegister = NewParseRegister()
	var left ASTNode = res.Register(lFunc())
	if res.Error.True() {return res}

	for u.ContainsString(op, p.current.Value) {
		var operator l.Token = p.current
		p.Advance()

		var right ASTNode = res.Register(rFunc())
		if res.Error.True() {
			return res
		}

		left = NewBinaryOperatorNode(left, operator, right)
	}

	return res.Success(left)
}