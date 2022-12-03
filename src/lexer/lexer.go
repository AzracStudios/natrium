package lexer

import (
	u "natrium/src/utils"
)

const LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
const NUMBERS = "1234567890"

var KEYWORDS = [...]string{"task", "if", "else", "while", "for", "break", "continue", "return", "do", "end"}

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

func (l *Lexer) NumberToken() Token {
	var num string = ""
	var pos Position = l.currentPos.Copy()
	var c byte = l.currentChar
	var eof bool = false

	for u.ContainsByte([]byte(NUMBERS+"."), c) != 0 {
		if eof {
			break
		}

		if c == '.' {
			if u.ContainsByte([]byte(num), '.') != 0 {
				//TODO: LOG ILLEGAL CHARACTER ERROR
				eof = l.Advance()
				return NewToken("ERROR", "_", pos, pos)
			}
		}

		num += string(c)
		eof = l.Advance()
		c = l.currentChar
	}

	n := NewToken("NUMBER", num, pos, l.currentPos.Copy())

	return n
}

func (l *Lexer) IdentifierKeywordToken() Token {
	var str string = ""
	var pos Position = l.currentPos.Copy()
	var c byte = l.currentChar
	var eof bool = false

	for {
		if eof || c == ' ' {
			break
		}

		str += string(c)
		eof = l.Advance()
		c = l.currentChar
	}

	tokenType := "IDENTIFIER"

	if u.ContainsString(KEYWORDS[:], str) {
		tokenType = "KEYWORD"
	}

	n := NewToken(tokenType, str, pos, l.currentPos.Copy())

	return n
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

	case '!':
		l.Advance()
		nPos := l.currentPos.Copy()

		if l.currentChar == '=' {
			token = NewToken("OPERATOR", "NE", pos.Copy(), nPos.Advance(c))
		} else {
			token = NewToken("OPERATOR", "NOT", pos.Copy(), pos.Advance(c))
		}

	case '<':
		l.Advance()
		nPos := l.currentPos.Copy()

		if l.currentChar == '=' {
			token = NewToken("OPERATOR", "LTE", pos.Copy(), nPos.Advance(c))
		} else {
			token = NewToken("OPERATOR", "LT", pos.Copy(), pos.Advance(c))
		}

	case '>':
		l.Advance()
		nPos := l.currentPos.Copy()

		if l.currentChar == '=' {
			token = NewToken("OPERATOR", "GTE", pos.Copy(), nPos.Advance(c))
		} else {
			token = NewToken("OPERATOR", "GT", pos.Copy(), pos.Advance(c))
		}

	case '=':
		l.Advance()
		nPos := l.currentPos.Copy()

		if l.currentChar == '=' {
			token = NewToken("OPERATOR", "EE", pos.Copy(), nPos.Advance(c))
		} else {
			token = NewToken("OPERATOR", "EQL", pos.Copy(), pos.Advance(c))
		}

	case '&':
		token = NewToken("OPERATOR", "AND", pos.Copy(), pos.Advance(c))

	case '|':
		token = NewToken("OPERATOR", "OR", pos.Copy(), pos.Advance(c))

	case u.ContainsByte([]byte(NUMBERS+"."), c):
		token = l.NumberToken()

	case u.ContainsByte([]byte(LETTERS), c):
		token = l.IdentifierKeywordToken()
	}

	return token
}

func (l *Lexer) Advance() bool {
	l.currentPos.Advance(l.currentChar)

	if !(l.currentPos.Idx < len(l.src)) {
		return true
	}

	l.currentChar = l.src[l.currentPos.Idx]
	return false
}

func (l *Lexer) Tokenize() []Token {
	var tokens []Token
	l.currentPos = NewPosition(-1, -1, 0)

	var eof bool = l.Advance()

	for {
		if eof {
			break
		}

		var next Token = l.Next()

		if next.Type != "SPACE" {
			tokens = append(tokens, next)
		}

		eof = l.Advance()
	}

	tokens = append(tokens, NewToken("FILE", "EOF", l.currentPos.Copy(), l.currentPos.Copy()))
	return tokens
}
