package lexer

type Position struct {
	Idx int // INDEX
	Col int // COLUMN
	Ln  int // LINE
}

func NewPosition(idx int, col int, ln int) Position {
	return Position{
		Idx: idx,
		Col: col,
		Ln:  ln,
	}
}

func (p *Position) Advance(char byte) Position {
	if char == '\n' {
		p.Col = 0
		p.Ln++
	}

	p.Idx++
	p.Col++

	return *p
}

func (p *Position) Copy() Position {
	return NewPosition(p.Idx, p.Col, p.Ln)
}
