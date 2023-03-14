# ans = 199957220

from dataclasses import dataclass

@dataclass
class LeftParen:
    pass


@dataclass
class RightParen:
    pass


@dataclass
class Comma:
    pass


@dataclass
class Number:
    value: str


Token = LeftParen | RightParen | Comma | Number


class Lexer:
    def __init__(self, text) -> None:
        self.text = text
        self.index = 0
        self.tokens: list[Token] = []

    def get_tokens(self):
        while self.index < len(self.text):
            c = self.text[self.index]
            match c:
                case " " | "\t" | "\n":
                    self.index += 1
                case "[":
                    self.index += 1
                    self.tokens.append(LeftParen())
                case "]":
                    self.index += 1
                    self.tokens.append(RightParen())
                case ",":
                    self.index += 1
                    self.tokens.append(Comma())
                case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    self.consume_numbers()
                case _:
                    raise Exception(f"Unknown Value {c}")
        return self.tokens

    def consume_numbers(self):
        nums = ""
        while True:
            c = self.text[self.index]
            match c:
                case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    nums += c
                case _:
                    self.tokens.append(Number(nums))
                    return
            self.index += 1


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def parse(self) -> list[int]:
        result = []
        self.consume(LeftParen)
        while True:
            c = self.tokens[self.index]
            self.expect(c, Number)
            self.index += 1
            result.append(self.strtoint(c.value))
            lookahead = self.tokens[self.index]
            if not isinstance(lookahead, Comma):
                break
            else:
                self.consume(Comma)

        self.consume(RightParen)

        if self.index < len(self.tokens):
            raise "Found tokens after closing parens"
        return result

    @staticmethod
    def todigit(char):
        return ord(char) - 48

    @staticmethod
    def strtoint(input: str):
        total = 0
        for char in input:
            total = total * 10 + Parser.todigit(char)
        return total

    @staticmethod
    def expect(item, type):
        if not isinstance(item, type):
            raise Exception(f"expected: {type} found: {item}")

    def consume(self, type):
        c = self.tokens[self.index]
        self.expect(c, type)
        self.index += 1


def main():
    with open("largest-number/input.txt") as f:
        text = f.read()
    lexer = Lexer(text)
    tokens = lexer.get_tokens()
    parser = Parser(tokens)
    print(max(parser.parse()))


if __name__ == "__main__":
    main()
