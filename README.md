# bf-interpreter
A line-by-line interpreter for the BF language.

# Basics
BF was developed to have the smallest compiler possible, and as such only has 8 commands. Instead of memorizing thousands of use cases as in other languages, BF encourages you to do more with less. To facilitate this, BF operates much like a Turing Machine, doing operations on an infinitely long tape of values, and a movable pointer to a single one of those values. Each of these values can be anything from 0-255, making BF (slightly) esaier to use and implement than pure Turing language. Despite this, BF is completely Turing Complete.

# Commands
+ : Increment value at current pointer position
- : Decrement value at current pointer position
< : Move pointer left one index
> : Move pointer right one index
\[ : If value is zero, skip to corresponding \]
\] : If value is NOT zero, return to corresponding \[
, : Gather ASCII input from the user and store it at the current location
. : Print the current value as an ASCII character

In addition to the official BF commands listed above, the interpreter also supports the following:
d : Displays the values of all active memory cells and pointer location

# Interpreter Specifics
...
