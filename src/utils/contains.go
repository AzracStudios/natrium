package utils

func ContainsByte (arr []byte, char byte) byte {
	for i := 0; i < len(arr); i++ {
		if arr[i] == char {
			return char
		}
	}

	return 0
}

func ContainsString (arr []string, str string) bool {
	for i := 0; i < len(arr); i++ {
		if arr[i] == str {
			return true
		}
	}

	return false
}