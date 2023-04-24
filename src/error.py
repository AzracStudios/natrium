from utils import *

ERR_LEX = "Illegal Character"
ERR_PAR = "Parser Error"

class Error:

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def fmt(self, src, file_name):
        result = bright_red(
            f'{self.error_name} @ Ln {self.pos_start.ln + 1}, Col {self.pos_start.col}\n'
        )
        result += f"{bright_white(file_name)}: {self.details}\n\n"

        idx_start = max(src.rfind('\n', 0, self.pos_start.idx), 0)
        idx_end = src.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(src)

        line_count = self.pos_end.ln - self.pos_start.ln + 1
        max_ln_num_len = len(str(line_count))

        for i in range(line_count):
            line = src[idx_start:idx_end]
            col_start = self.pos_start.col if i == 0 else 0
            col_end = self.pos_end.col if i == line_count - 1 else len(
                line) - 1

            space_width = max_ln_num_len - len(str(i)) + 1
            result += bright_black(f"{i + 1}{' ' * space_width}| ")
            result += white(line + '\n')
            result += bright_red(' ' * (col_start + max_ln_num_len + 3) + '^' *
                                 (col_end - col_start))

            idx_start = idx_end
            idx_end = src.find('\n', idx_start + 1)
            if idx_end < 0: idx_end = len(src)

        return result.replace('\t', '')


class IllegalCharError(Error):

    def __init__(self, pos_start, pos_end, char):
        super().__init__(pos_start, pos_end, ERR_LEX, char)


class InvalidSyntaxError(Error):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, ERR_PAR, details)
