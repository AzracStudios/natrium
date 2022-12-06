package error

import l "natrium/src/lexer"

type Error struct {
	ErrorDetails string
	Start        l.Position
	End          l.Position
}

func NewError(details string, start l.Position, end l.Position) Error {
	return Error{ErrorDetails: details, Start: start, End: end}
}

func (e *Error) True() bool {
	if e.ErrorDetails == "" {
		return false
	}

	return true
}
