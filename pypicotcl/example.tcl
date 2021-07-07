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
