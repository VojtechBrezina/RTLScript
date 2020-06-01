# RTLScript

This scripting language is written from right to left. 
It is designed to make your eyes hurt if you are a true coder. 
On the other hand, it is tuing complete and going to have a nice library for all kinds of tasks.
In the future it might have a basic game library.

## Writing RTLScript programs
### Basic syntax
- every line ends with a command
- before that there are any arguments the command needs
- commands and expressions are not separated by anything
- string literals are closed in double qotes `""`
- reading a variable is done by `[]` (the variable name is the result of any expression inside the brackes, even a number)
- when a command needs an undefined number of arguments, the argument list is followed by END (`DNE` i the script)
- `DNE` is also used to terminate a block of commands
### Commands
|Command|meaning|number of arguments|number of blocks of code|
|-------|-------|-------------------|------------------------|
|PRINT&nbsp;-&nbsp;`TNIRP`|prints the argument to the console|1|0|
|STOP&nbsp;-&nbsp;`POTS`|immediately halts execution|0|0|
|SET&nbsp;-&nbsp;`TES`|set a variable to a value (use the first expression as name and the second as value)|2|0|
### Comments
There is no special syntax for comments, but any expression that is not an argument to a command can serve as a comment. It still gets evaluated because function calls with no return value are the same case, but it does the trick. If you do not want it to be evaluated, just close inside a condition that will always fail or inside some other unrechable space.
