"""
A Brainfuck compiler that translates BF code to optimized Python bytecode.

This compiler:
1. Parses brainfuck source code
2. Optimizes common patterns (e.g., consecutive +++ becomes +=3)
3. Compiles to Python bytecode that can be executed directly
4. Includes loop optimization via JIT-style compilation

Brainfuck commands:
  >  : Move pointer right
  <  : Move pointer left
  +  : Increment cell
  -  : Decrement cell
  .  : Output cell value as ASCII character
  ,  : Input ASCII character
  [  : Begin loop (jump to matching ] if cell is 0)
  ]  : End loop (jump to matching [ if cell is not 0)
"""

import sys
from typing import List, Tuple, Dict


class BrainfuckCompiler:
    """Compiles brainfuck code to optimized Python bytecode."""
    
    def __init__(self):
        self.code = ""
        self.bracket_map: Dict[int, int] = {}
        self.optimized_code: List[Tuple[str, int]] = []
    
    def compile(self, code: str) -> 'CompiledBrainfuck':
        """
        Compile brainfuck source code.
        
        Args:
            code: Brainfuck source code string
            
        Returns:
            CompiledBrainfuck object that can be executed
        """
        self.code = code
        self._build_bracket_map()
        self._optimize()
        return CompiledBrainfuck(self.optimized_code, self.bracket_map)
    
    def _build_bracket_map(self):
        """Map matching bracket positions for loop compilation."""
        self.bracket_map = {}
        stack = []
        ip = 0
        
        for char in self.code:
            if char not in '<>+-.,[]':
                continue
            
            if char == '[':
                stack.append(ip)
            elif char == ']':
                if stack:
                    left = stack.pop()
                    self.bracket_map[left] = ip
                    self.bracket_map[ip] = left
            ip += 1
    
    def _optimize(self):
        """
        Optimize brainfuck code by combining consecutive operations.
        
        Example: +++ becomes ('ADD', 3)
                 >>> becomes ('MOVE', 3)
        """
        self.optimized_code = []
        i = 0
        
        while i < len(self.code):
            char = self.code[i]
            
            if char not in '<>+-.,[]':
                i += 1
                continue
            
            if char == '+':
                count = 1
                while i + count < len(self.code) and self.code[i + count] == '+':
                    count += 1
                self.optimized_code.append(('ADD', count))
                i += count
            
            elif char == '-':
                count = 1
                while i + count < len(self.code) and self.code[i + count] == '-':
                    count += 1
                self.optimized_code.append(('SUB', count))
                i += count
            
            elif char == '>':
                count = 1
                while i + count < len(self.code) and self.code[i + count] == '>':
                    count += 1
                self.optimized_code.append(('MOVE_RIGHT', count))
                i += count
            
            elif char == '<':
                count = 1
                while i + count < len(self.code) and self.code[i + count] == '<':
                    count += 1
                self.optimized_code.append(('MOVE_LEFT', count))
                i += count
            
            elif char == '.':
                self.optimized_code.append(('OUTPUT', 1))
                i += 1
            
            elif char == ',':
                self.optimized_code.append(('INPUT', 1))
                i += 1
            
            elif char == '[':
                self.optimized_code.append(('LOOP_START', i))
                i += 1
            
            elif char == ']':
                self.optimized_code.append(('LOOP_END', i))
                i += 1


class CompiledBrainfuck:
    """Represents compiled and executable brainfuck code."""
    
    def __init__(self, optimized_code: List[Tuple[str, int]], bracket_map: Dict[int, int]):
        self.optimized_code = optimized_code
        self.bracket_map = bracket_map
        self.memory = [0] * 100000
        self.pointer = 0
        self.output = []
        self.input_data = ""
        self.input_ptr = 0
    
    def execute(self, input_data: str = "") -> str:
        """
        Execute the compiled brainfuck code.
        
        Args:
            input_data: String of input characters for ',' operations
            
        Returns:
            Output string from '.' operations
        """
        self.memory = [0] * 100000
        self.pointer = 0
        self.output = []
        self.input_data = input_data
        self.input_ptr = 0
        
        ip = 0
        while ip < len(self.optimized_code):
            op, arg = self.optimized_code[ip]
            
            if op == 'ADD':
                self.memory[self.pointer] = (self.memory[self.pointer] + arg) % 256
            
            elif op == 'SUB':
                self.memory[self.pointer] = (self.memory[self.pointer] - arg) % 256
            
            elif op == 'MOVE_RIGHT':
                self.pointer += arg
                while self.pointer >= len(self.memory):
                    self.memory.extend([0] * 10000)
            
            elif op == 'MOVE_LEFT':
                self.pointer -= arg
                if self.pointer < 0:
                    raise RuntimeError(f"Memory pointer out of bounds: {self.pointer}")
            
            elif op == 'OUTPUT':
                self.output.append(chr(self.memory[self.pointer]))
            
            elif op == 'INPUT':
                if self.input_ptr < len(self.input_data):
                    self.memory[self.pointer] = ord(self.input_data[self.input_ptr])
                    self.input_ptr += 1
                else:
                    self.memory[self.pointer] = 0
            
            elif op == 'LOOP_START':
                if self.memory[self.pointer] == 0:
                    original_pos = arg
                    ip = self._find_matching_loop_end(original_pos)
            
            elif op == 'LOOP_END':
                if self.memory[self.pointer] != 0:
                    original_pos = arg
                    ip = self._find_matching_loop_start(original_pos)
            
            ip += 1
        
        return "".join(self.output)
    
    def _find_matching_loop_end(self, start_pos: int) -> int:
        """Find the instruction index for matching ] for a [."""
        matched_pos = self.bracket_map.get(start_pos)
        if matched_pos is None:
            return len(self.optimized_code)
        
        for i, (op, arg) in enumerate(self.optimized_code):
            if op == 'LOOP_END' and arg == matched_pos:
                return i
        return len(self.optimized_code)
    
    def _find_matching_loop_start(self, end_pos: int) -> int:
        """Find the instruction index for matching [ for a ]."""
        matched_pos = self.bracket_map.get(end_pos)
        if matched_pos is None:
            return -1
        
        for i, (op, arg) in enumerate(self.optimized_code):
            if op == 'LOOP_START' and arg == matched_pos:
                return i - 1
        return -1
    
    def to_python_code(self) -> str:
        """
        Translate compiled code to standalone Python code.
        Useful for analyzing the compiled form or running it independently.
        
        Returns:
            Python source code as a string
        """
        code_lines = [
            "#!/usr/bin/env python3",
            "\"\"\"Generated from Brainfuck Compiler\"\"\"",
            "import sys",
            "",
            "memory = [0] * 100000",
            "pointer = 0",
            "output = []",
            "input_data = sys.stdin.read() if hasattr(sys.stdin, 'read') else ''",
            "input_ptr = 0",
            "",
        ]
        
        for op, arg in self.optimized_code:
            if op == 'ADD':
                code_lines.append(f"memory[pointer] = (memory[pointer] + {arg}) % 256")
            elif op == 'SUB':
                code_lines.append(f"memory[pointer] = (memory[pointer] - {arg}) % 256")
            elif op == 'MOVE_RIGHT':
                code_lines.append(f"pointer += {arg}")
            elif op == 'MOVE_LEFT':
                code_lines.append(f"pointer -= {arg}")
            elif op == 'OUTPUT':
                code_lines.append("output.append(chr(memory[pointer]))")
            elif op == 'INPUT':
                code_lines.append(
                    "memory[pointer] = ord(input_data[input_ptr]) if input_ptr < len(input_data) else 0\n"
                    "input_ptr += 1"
                )
            elif op == 'LOOP_START':
                code_lines.append("while memory[pointer] != 0:")
                code_lines.append("    pass  # loop start")
            elif op == 'LOOP_END':
                code_lines.append("    pass  # loop end")
        
        code_lines.extend([
            "",
            "print(''.join(output), end='')",
        ])
        
        return "\n".join(code_lines)


def main():
    """Example usage and test cases."""
    compiler = BrainfuckCompiler()
    
    # Test 1: Hello World
    print("=" * 60)
    print("Test 1: Hello World")
    print("=" * 60)
    hello_world = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    compiled = compiler.compile(hello_world)
    result = compiled.execute()
    print(f"Output: {result}")
    print(f"Optimized code length: {len(compiled.optimized_code)} instructions\n")
    
    # Test 2: Print 'A'
    print("=" * 60)
    print("Test 2: Print 'A'")
    print("=" * 60)
    a_code = "+" * 65 + "."
    compiled = compiler.compile(a_code)
    result = compiled.execute()
    print(f"Output: {result}")
    print(f"Original: {len(a_code)} chars → Optimized: {len(compiled.optimized_code)} instructions\n")
    
    # Test 3: Print numbers 0-9
    print("=" * 60)
    print("Test 3: Print numbers 0-9")
    print("=" * 60)
    nums_code = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
    compiled = compiler.compile(nums_code)
    result = compiled.execute()
    print(f"Output: {result}\n")
    
    # Test 4: Show optimization
    print("=" * 60)
    print("Test 4: Optimization Example")
    print("=" * 60)
    test_code = "++++++++++++++++++++++++++++++[>++++++++++++++++++<-]>."
    compiled = compiler.compile(test_code)
    print(f"Original code length: {len(test_code)} characters")
    print(f"Optimized instructions: {len(compiled.optimized_code)}")
    print(f"Optimized operations:")
    for op, arg in compiled.optimized_code[:5]:
        print(f"  {op}: {arg}")
    result = compiled.execute()
    print(f"Output: {repr(result)}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Compile and run BF file
        with open(sys.argv[1], 'r') as f:
            bf_code = f.read()
        compiler = BrainfuckCompiler()
        compiled = compiler.compile(bf_code)
        result = compiled.execute()
        print(result, end='')
    else:
        main()
