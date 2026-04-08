"""
A Brainfuck interpreter in Python.

Brainfuck commands:
  >  : Move pointer right
  <  : Move pointer left
  +  : Increment cell
  -  : Decrement cell
  .  : Output cell value as ASCII character
  ,  : Input ASCII character
  [  : Jump forward to matching ] if cell is 0
  ]  : Jump backward to matching [ if cell is not 0
"""


class BrainfuckInterpreter:
    def __init__(self, memory_size=100000):
        self.memory = [0] * memory_size
        self.pointer = 0
        self.instruction_ptr = 0
        self.code = ""
        self.output = []
        self.input_data = ""
        self.input_ptr = 0
        
        # Pre-compute bracket matching for performance
        self.bracket_map = {}

    def _build_bracket_map(self):
        """Build a map of matching brackets for efficient jumping."""
        stack = []
        for i, char in enumerate(self.code):
            if char == '[':
                stack.append(i)
            elif char == ']':
                if stack:
                    left = stack.pop()
                    self.bracket_map[left] = i
                    self.bracket_map[i] = left

    def run(self, code, input_data=""):
        """
        Execute Brainfuck code.
        
        Args:
            code: Brainfuck source code string
            input_data: String of input characters
        """
        self.code = code
        self.input_data = input_data
        self.input_ptr = 0
        self.instruction_ptr = 0
        self.pointer = 0
        self.output = []
        self.memory = [0] * len(self.memory)
        
        self._build_bracket_map()
        
        while self.instruction_ptr < len(self.code):
            self._execute_instruction()
        
        return "".join(self.output)

    def _execute_instruction(self):
        """Execute the current instruction."""
        cmd = self.code[self.instruction_ptr]
        
        if cmd == '>':
            self.pointer += 1
            # Expand memory dynamically if needed
            while self.pointer >= len(self.memory):
                self.memory.extend([0] * 10000)
        
        elif cmd == '<':
            self.pointer -= 1
            if self.pointer < 0:
                raise RuntimeError(f"Memory pointer out of bounds: {self.pointer}")
        
        elif cmd == '+':
            self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256
        
        elif cmd == '-':
            self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256
        
        elif cmd == '.':
            self.output.append(chr(self.memory[self.pointer]))
        
        elif cmd == ',':
            if self.input_ptr < len(self.input_data):
                self.memory[self.pointer] = ord(self.input_data[self.input_ptr])
                self.input_ptr += 1
            else:
                self.memory[self.pointer] = 0
        
        elif cmd == '[':
            if self.memory[self.pointer] == 0:
                self.instruction_ptr = self.bracket_map.get(self.instruction_ptr, self.instruction_ptr)
        
        elif cmd == ']':
            if self.memory[self.pointer] != 0:
                self.instruction_ptr = self.bracket_map.get(self.instruction_ptr, self.instruction_ptr)
        
        self.instruction_ptr += 1


def main():
    """Example usage and test cases."""
    interpreter = BrainfuckInterpreter()
    
    # Test 1: Hello World
    hello_world = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    print("Test 1: Hello World")
    result = interpreter.run(hello_world)
    print(f"Output: {result}\n")
    
    # Test 2: Simple increment and print (ASCII 65 = 'A')
    print("Test 2: Print 'A'")
    a_code = "+" * 65 + "."
    result = interpreter.run(a_code)
    print(f"Output: {result}\n")
    
    # Test 3: Print newline
    print("Test 3: Print newline")
    newline_code = "+" * 10 + "."
    result = interpreter.run(newline_code)
    print(f"Output: {repr(result)}\n")
    
    # Test 4: Move right, increment, print (ABC)
    print("Test 4: Print 'B' on second cell")
    b_code = ">" + "+" * 66 + "."
    result = interpreter.run(b_code)
    print(f"Output: {result}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Read from file if provided
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        interpreter = BrainfuckInterpreter()
        result = interpreter.run(code)
        print(result, end='')
    else:
        main()
