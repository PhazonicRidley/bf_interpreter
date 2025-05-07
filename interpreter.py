#!/usr/bin/python3
import os
import sys
import argparse
from enum import Enum

class Token(Enum):
    SHIFT_LEFT = 0
    SHIFT_RIGHT = 1
    INCREMENT = 2
    DECREMENT = 3
    OUT = 4
    IN = 5
    START_LOOP = 6
    END_LOOP = 7

class LexException(Exception):
    def __init__(self, msg: str, *args):
        self.msg = msg
        super().__init__(*args)

ALLOWED_CHARS = {'<': Token.SHIFT_LEFT, '>': Token.SHIFT_RIGHT, '+': Token.INCREMENT, 
                 '-': Token.DECREMENT, '.': Token.OUT, ',': Token.IN, 
                 '[': Token.START_LOOP, ']': Token.END_LOOP}

assert len(ALLOWED_CHARS) == 8

def lex(raw: str) -> list[Token]:
    program = []
    open_bracket_stack = []
    line_no = 0
    for idx, c in enumerate(raw):
        if not c in ALLOWED_CHARS.keys():
            if c == '\n':
                line_no += 1
            continue
        elif c == '[':
            open_bracket_stack.append((line_no, idx))
        elif c == ']':
            try:
                open_bracket_stack.pop()
            except IndexError:
                raise LexException(f"Error on line {line_no}, column {idx}: Closing ] without corresponding open [")
            
        program.append(ALLOWED_CHARS[c])
    
    if open_bracket_stack:
        err_str = ""
        for offending_bracket in open_bracket_stack:
            err_str += f"Error on line number: {offending_bracket[0]}, Column number {offending_bracket[1]}: Starting '[' loop is never closed with a ']"

        raise LexException(err_str)       
    
    return program


def skip_loop(ip: int, token_stream: list[Token]) -> int:
    stack = []
    stack.append(ip)
    while stack:
        ip += 1
        match token_stream[ip]:
            case Token.START_LOOP:
                stack.append(ip)
            case Token.END_LOOP:
                stack.pop()

    return ip

def parse_and_execute(token_stream: list[Token], memory_state: list[int], print_as_nums: bool = False):
    ptr = 0
    mem_size = len(memory_state)
    loop_stack = []
    instruction_length = len(token_stream)
    ip = 0
    while ip < instruction_length:
        token = token_stream[ip]
        match token:
            case Token.SHIFT_LEFT:
                ptr = (ptr - 1) % mem_size
            case Token.SHIFT_RIGHT:
                ptr = (ptr + 1) % mem_size
            case Token.INCREMENT:
                memory_state[ptr] = (memory_state[ptr] + 1) % 256
            case Token.DECREMENT:
                memory_state[ptr] = (memory_state[ptr] - 1) % 256
            case Token.OUT:
                print(chr(memory_state[ptr]), end="") if not print_as_nums else print(memory_state[ptr], end="")
            case Token.IN:
                try:
                    memory_state[ptr] = ord(input("Input a single character: ")) if not print_as_nums else input("Input a number from 0-255: ")
                except TypeError:
                    print("Invalid character given, terminated")
                    sys.exit(1)
                    
            case Token.START_LOOP:
                if memory_state[ptr] == 0:
                    ip = skip_loop(ip, token_stream)
                else:
                    loop_stack.append(ip)
            
            case Token.END_LOOP:
                if memory_state[ptr] == 0:
                    loop_stack.pop()
                else:
                    ip = loop_stack[-1]

        ip += 1
    
    print("\nDone!")


def main():
    arg_parser = argparse.ArgumentParser(
        prog="bf interpreter",
        description="An interpreter for the brainf**k language"
    )
    arg_parser.add_argument("script")
    arg_parser.add_argument('-m', '--memory_size', type=int)
    arg_parser.add_argument('-n', '--nums', action='store_true')
    args = arg_parser.parse_args()

    path: str = args.script
    if not os.path.isfile(path) or path.split("/")[-1][-3:] != '.bf':
        print("Invalid path or file given.")
    
    raw_text = None
    with open(path) as f:
        raw_text = f.read()
    
    mem_size = args.memory_size if args.memory_size is not None else 30000
    mem_state = [0] * mem_size
    try:
        token_stream = lex(raw_text)
    except LexException as e:
        print(e.msg)
        sys.exit(1)

    try:
        parse_and_execute(token_stream, mem_state, args.nums)
    except KeyboardInterrupt:
        print("Interrupted")


main()