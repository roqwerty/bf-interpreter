# Toolkit for BF
# Features:
#   Reducer - Removes all unnecessary characters from a BF file
#   Obsfucator - (not spelled correctly) Reduces, but also adds tons of unneeded
#       characters (+-+-, <><>, <<>>, [] when == 0, etc)
#   Stringer - Does ASCII magic to transform a string into a list of +-. chars
#       such that one may start at any 0 or -1 and output the message without
#       changing the value of the currently pointed memory cell
# C Ethan Brucker
# Version 11-20-19

def reduce():
    # Get the code into data
    data = ''
    while True:
        try:
            file = input("Filepath: ")
            with open(file, 'r', encoding='utf-8') as f:
                data = f.read()
                break
        except:
            print("Enter valid filepath.")
    # Format the data
    scrubbed = ''
    for char in data:
        # FUTURE add option for simplified BF
        if char in ['+', '-', '>', '<', '[', ']', ',', '.']: # Full list
            scrubbed += char
    # Write the data to file
    with open('output.txt', 'w+') as f:
        f.write(scrubbed)
    print("Saved code to output.txt.")

def stringer(add_newline=True, message=None):
    # Get the input string
    if message is None:
        message = input("Input string: ")
    if add_newline:
        message += '\n'
    # Get the final data value
    data_v = int(input("Finishing value: "))
    # The BF output (reset to 0 at beginning)
    output = '[-]'
    # The last value that has been stored
    last = 0
    
    for char in message:
        # Get the ASCII numeral of each character as an offset from previous
        offset = ord(char)
        offset -= last
        last = ord(char)
        # Add the code
        if offset == 0:
            output += '.'
            continue # Issa same character
        elif offset > 0:
            output += '+' * offset
            output += '.'
        else: # Negative character
            output += '-' * abs(offset)
            output += '.'

    # Account for initial offset
    # FUTURE make cleaner? (remove '[-]')
    if data_v > 0: # Starting value above 0
        output += '[-]' + ('+' * data_v)
        #output = ('-' * data_v) + output + '[-]' + ('+' * data_v)
    elif data_v < 0: # Starting value was negative
        output += '[-]' + ('-' * abs(data_v))
        #output = ('+' * abs(data_v)) + output + '[-]' + ('-' * abs(data_v))
    else: # Finish value is 0
        output += '[-]'
    
    return output

def ml_stringer(add_newline=True): # Stringer, but also multiline
    # Get the input string over many lines
    message = ''
    print("Input string, line by line. Enter a newline to finish.")
    while True:
        line = input()
        if line != '':
            message += line + '\n'
        else:
            break

    #message = message.strip() # Remove redundant whitespace
    message = message[:-1] # Remove the last newline
    if add_newline:
        message += '\n'

    # Get the final data value
    data_v = int(input("Finishing value: "))
    # The BF output (reset to 0 at beginning)
    output = '[-]'
    # The last value that has been stored
    last = 0
    
    for char in message:
        # Get the ASCII numeral of each character as an offset from previous
        offset = ord(char)
        offset -= last
        last = ord(char)
        # Add the code
        if offset == 0:
            output += '.'
            continue # Issa same character
        elif offset > 0:
            output += '+' * offset
            output += '.'
        else: # Negative character
            output += '-' * abs(offset)
            output += '.'

    # Account for initial offset
    # FUTURE make cleaner? (remove '[-]')
    if data_v > 0: # Starting value above 0
        output += '[-]' + ('+' * data_v)
        #output = ('-' * data_v) + output + '[-]' + ('+' * data_v)
    elif data_v < 0: # Starting value was negative
        output += '[-]' + ('-' * abs(data_v))
        #output = ('+' * abs(data_v)) + output + '[-]' + ('-' * abs(data_v))
    else: # Finish value is 0
        output += '[-]'
    
    return output
