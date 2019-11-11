# This adds ASCII input/output to the base.py file
# C Ethan Brucker
# Version 11-8-19
# New Symbols:
#   , . : Get ASCII input, give ASCII output

from base import * # Main functions for Turing Machine
import sys # For advanced command-line tricks

def get_input(mem, index):
    # Sets the value of mem[index] to the ASCII number of 1st char of input
    mem[index] = ord(input()[0])

def set_output(mem, index):
    # Prints the value of mem[index] as ASCII
    print(str(chr(mem[index])), end='')

def parse_all(code):
    # Take a raw code and format it to be used with IO
    parsed = ''
    for char in code:
        if char in ['+', '-', '<', '>', '[', ']', ',', '.', 'd']:
            parsed += char
    return parsed

def main():
    # Help flag
    if "-h" in sys.argv:
        print()
        print("Activation: full.py <optional_code_file> <args>")
        print("Arguments:")
        print("   -h: This help menu")
        print("   -v: Verbose mode (telegraphs each step)")
        print('Can also make "d" part of the code at any time to view memory')
        print()
        exit()

    # Assemble the "infinite" memory
    mem = []
    index = 0
    layer = 0 # Layer for brackets
    code_index = 0
    mem.append(0) # Create index 0
    
    # Verbose flag
    verbose = False
    if "-v" in sys.argv: # Literally just checks to see if it exists
        verbose = True

    # Run a file if input by the user
    try: # If they added the name of a file
        with open(sys.argv[1], "r") as file:
            code = parse_all(file.read())

        while code_index < len(code): # End by going through entire program

            if verbose:
                display(mem, index) # Display each step if verbose
            
            if code[code_index] is '+':
                increment(mem, index)
            elif code[code_index] is '-':
                decrement(mem, index)
            elif code[code_index] is "<":
                index = left(mem, index)
            elif code[code_index] is ">":
                index = right(mem, index)
            elif code[code_index] is '[':
                code_index = open_bracket(mem, index, code, code_index)
            elif code[code_index] is ']':
                code_index = close_bracket(mem, index, code, code_index)
            elif code[code_index] is ',': # Input
                get_input(mem, index)
            elif code[code_index] is '.': # Output
                set_output(mem, index)

            code_index += 1
    except:
        pass

    
    # Get input line by line from the user
    while True:
        code = parse_all(input("Code: "))
        code_index = 0

        while code_index < len(code): # End by going through entire program
            
            if code[code_index] is '+':
                increment(mem, index)
            elif code[code_index] is '-':
                decrement(mem, index)
            elif code[code_index] is "<":
                index = left(mem, index)
            elif code[code_index] is ">":
                index = right(mem, index)
            elif code[code_index] is '[':
                code_index = open_bracket(mem, index, code, code_index)
            elif code[code_index] is ']':
                code_index = close_bracket(mem, index, code, code_index)
            elif code[code_index] is ',': # Input
                get_input(mem, index)
            elif code[code_index] is '.': # Output
                set_output(mem, index)

            elif code[code_index] is 'd': # Display
                display(mem, index)

            if verbose:
                display(mem, index) # Display each step if verbose
            
            code_index += 1

if __name__ == "__main__":
    main()
