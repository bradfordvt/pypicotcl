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

set a "pu"
set b {ts}
$a$b "Hello World!"

puts "[- 20 1]"
puts "[- 20 2]"


proc fib {x} {
    if {<= $x 1} {
        return 1
    } else {
        + [fib [- $x 1]] [fib [- $x 2]]
    }
}

puts [fib 20]

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

puts [string cat "Hello, " "world!"]
set s1 "Hello, "
set s2 "world!!"
puts [string cat $s1 $s2]

set s3 "Hello, "
set s4 "hello, "

if [string compare $s1 $s3] { puts "compare fails"; } else { puts "s1 compares to s3"; }
if [string compare $s1 $s4] { puts "s1 does not compare to s4"; } else { puts "compare fails"; }
if [string compare -nocase $s1 $s4] { puts "compare fails"; } else { puts "s1 compares to s4"; }
if [string equal $s1 $s3] { puts "s1 equal to s3"; } else { puts "equal fails"; }

puts [string index $s1 4]
puts [string cat "length of s1 is " [string length $s1]]
puts [string cat "range(2,5) of s1 is " [string range $s1 2 5]]
puts [string repeat "X" 10]
puts [string reverse $s1]
puts [string tolower $s1]
puts [string toupper $s4]
puts [string tolower $s1 0 4]
puts [string toupper $s4 0 4]

set t1 "  space   "
set t2 "abcspaceabc"
puts -nonewline [string trimleft $t1]
puts ":"
puts -nonewline [string trimleft $t2 "abc"]
puts ":"
puts -nonewline [string trimright $t1]
puts ":"
puts -nonewline [string trimright $t2 "abc"]
puts ":"
puts -nonewline [string trim $t1]
puts ":"
puts -nonewline [string trim $t2 "abc"]
puts ":"
