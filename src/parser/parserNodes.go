package parser

import (
	l "natrium/src/lexer"
)

type ASTNode interface {
	GetType() string
	GetValue() []any
	GetPosition() []l.Position
}

type NumberNode struct {
	Val l.Token
	Start l.Position
	End l.Position
}

func NewNumberNode(val l.Token) NumberNode {
	return NumberNode{Val: val, Start: val.Start, End: val.End}
}

func (n NumberNode) GetType() string {
	return "NUMBER"
}

func (n NumberNode) GetValue() []any {
	return []any{n.Val}
}

func (n NumberNode) GetPosition() []l.Position {
	return []l.Position{n.Start, n.End}
}

type BinaryOperatorNode struct {
	Left ASTNode
	OP l.Token
	Right ASTNode

	Start l.Position
	End l.Position
}

func NewBinaryOperatorNode(left ASTNode, op l.Token, right ASTNode) BinaryOperatorNode {
	return BinaryOperatorNode{
		Left: left,
		OP: op,
		Right: right,
		Start: left.GetPosition()[0],
		End: right.GetPosition()[1],
	}
}

func (b BinaryOperatorNode) GetType() string {
	return "BINARY_OPERATOR"
}

func (b BinaryOperatorNode) GetValue() []any {
	return []any{b.Left.GetValue(), b.OP, b.Right.GetValue()}
}

func (b BinaryOperatorNode) GetPosition() []l.Position {
	return []l.Position{b.Start, b.End}
}

type UnaryOperatorNode struct {
	OP l.Token
	Val ASTNode

	Start l.Position
	End l.Position
}

func NewUnaryOperatorNode(op l.Token, val ASTNode) UnaryOperatorNode {
	return UnaryOperatorNode{OP: op, Val: val}
}

func (u UnaryOperatorNode) GetType() string {
	return "BINARY_OPERATOR"
}

func (u UnaryOperatorNode) GetValue() []any {
	return []any{u.OP, u.Val.GetValue()}
}

func (u UnaryOperatorNode) GetPosition() []l.Position {
	return []l.Position{u.Start, u.End}
}