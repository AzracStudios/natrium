package parser

import e "natrium/src/error"

type ParseRegister struct {
	Node  ASTNode
	Error e.Error 
}

func NewParseRegister() ParseRegister {
	return ParseRegister{}
}

func (p *ParseRegister) Register(res ParseRegister) ASTNode {
	if res.Error.True() {
		p.Error= res.Error
	}

	return res.Node
}

func (p *ParseRegister) Success(val ASTNode) ParseRegister {
	p.Node = val
	return *p
}

func (p *ParseRegister) Failure(err e.Error) ParseRegister {
	p.Error = err
	return *p
}