# pypicotcl
**Small Tool Command Language (Tcl) Interpreter written in Python**

Tool Command Language (Tcl) interpreter written in Python.
The interpreter is just a core interpreter and not a comprehensive
implementation of the complete command language.  This was written
to be able to extend to create an interpreter for IEEE Std 1687
Procedural Description Language (PDL) for EDA tools.

The inspiration for this code is based on the C code located at:
[http://oldblog.antirez.com/post/picol.html](http://oldblog.antirez.com/post/picol.html).  Major changes different
from this code include making the parser and interpreter class based.
Enhancements to the Tcl commands like puts and if are also to be included
to make them more compliant to Tcl.

## pypicotcl package
The pypicotcl package contains the pypicotcl.py module which contains all the
core classes and code for the interpreter.  Specialized classes
can be created to inherit the core interpreter and add additional
commands to the interpreter.  To add additional commands, the derived
class would call the ***register_command()*** method of the core interpreter
similar to how the ***register_core_commands()*** works.  The derived class
must also call the ***register_core_commands()*** of the core interpreter
to get the core commands installed.  A sample of the kind of Tcl code supported
is shown below:
```tcl
if [+ 1 2] {
   puts "+ 1 2 is true"
}
if [+ 7 -7] {
   puts "+ 7 -7 is true"
} else {
   puts "+ 7 -7 is false"
}
puts "Hello World!"
set v "foobar"
puts "v is $v"

puts -nonewline "First message..."
puts "ok"

puts stderr "This sent to stderr"

set b "stderr"
puts $b "b sent to stderr"
```
The parser is very similar to the Tcl one, pypicotcl supports interpolation as well, for example you can write:
```tcl
set a "pu"
set b {ts}
$a$b "Hello World!"
```
Note that **pypicotcl** has an interactive shell! so just launch
it without arguments to start to play
(to run just write ***python pypicotcl.py***).

To run a program stored in a file instead use ***python pypicotcl.py filename.tcl***.

A Raw list of the supported features:
+ Interpolation, as seen above. You can also write "2+2 = [+ 2 2]" or "My name is: $foobar".
+ Procedures, with return. Like Tcl if return is missing the result of the last command executed is returned.
+ If, if .. else .., while with break and continue
+ Recursion
+ Variables inside procedures are limited in scope like Tcl, i.e. there are real call frames in Picol.
+ The following other commands: set + - * / == != > < >= <= puts

This is an example of programs **pypicotcl** can run:
```tcl
proc fib {x} {
    if {<= $x 1} {
        return 1
    } else {
        + [fib [- $x 1]] [fib [- $x 2]]
    }
}

puts [fib 20]
```
Another example:
```tcl
proc square {x} {
    * $x $x
}

set a 1
while {<= $a 10} {
    if {== $a 5} {
        puts {Missing five!}
        set a [+ $a 1]
        continue
    }
    puts "I can compute that $a*$a = [square $a]"
    set a [+ $a 1]
}
```
