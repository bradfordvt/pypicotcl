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

set r "Hello 1234567 , world!"
puts [string replace $r 5 13]
puts [string replace $r 5 13 " John"]

puts -nonewline [string first "123" $r]
puts " must equal 6"
puts -nonewline [string first " " $r 14]
puts " must equal 15"

set str1 "We are abc working at abc company"
set str2 "Find Tutorial at Tutorial Gateway"
puts [string last "abc" $str1]
puts [string last "abc" $str1 5]
puts [string last "abc" $str1 12]
puts [string last "Tutorial" $str2]
puts [string last "Tutorial" $str2 21]

set s1 "test@test.com"
set s2 "*@*.com"
puts "Matching pattern s2 in s1"
puts [string match "*@*.com" $s1 ]
puts "Matching pattern tcl in s1"
puts [string match {tcl} $s1]

puts [string map {abc 1 ab 2 a 3 1 0} 1abcaababcabababc]
puts [string map {1 0 ab 2 a 3 abc 1} 1abcaababcabababc]

puts "Starting to test \"string is\" command."

set res1 ""
if [string is alnum "123abc"] { puts "alnum passes"; } else { puts "alnum fails"; }
if [string is alnum "123!abc"] { puts "alnum fails"; } else { puts "alnum passes"; }
if [string is alnum -failindex res1 "123!abc"] { puts "alnum fails"; } else { puts "alnum passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is alpha "abc"] { puts "alpha passes"; } else { puts "alpha fails"; }
if [string is alpha "abc123"] { puts "alpha fails"; } else { puts "alpha passes"; }
if [string is alpha -failindex res1 "abcd123"] { puts "alpha fails"; } else { puts "alpha passes"; }
if [string compare $res1 4] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is digit "123"] { puts "digit passes"; } else { puts "digit fails"; }
if [string is digit "123!abc"] { puts "digit fails"; } else { puts "digit passes"; }
if [string is digit -failindex res1 "123!abc"] { puts "digit fails"; } else { puts "digit passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is ascii "abc"] { puts "ascii passes"; } else { puts "ascii fails"; }
if [string is ascii "abc\x80"] { puts "ascii fails"; } else { puts "ascii passes"; }
if [string is ascii -failindex res1 "abcd\x083"] { puts "ascii fails"; } else { puts "ascii passes"; }
if [string compare $res1 4] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is control "123\x01abc"] { puts "control passes"; } else { puts "control fails"; }
if [string is control "123!abc"] { puts "control fails"; } else { puts "control passes"; }
if [string is control -failindex res1 "123!abc"] { puts "control fails"; } else { puts "control passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is boolean true] { puts "boolean passes"; } else { puts "boolean fails"; }
if [string is boolean None] { puts "boolean fails"; } else { puts "boolean passes"; }
if [string is boolean -failindex res1 None] { puts "boolean fails"; } else { puts "boolean passes"; }
if [string compare $res1 4] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is double "123.5"] { puts "double passes"; } else { puts "double fails"; }
if [string is double "0x123"] { puts "double fails"; } else { puts "double passes"; }
if [string is double -failindex res1 "123abc"] { puts "double fails"; } else { puts "double passes"; }
puts "res1 = $res1"
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is entier "123"] { puts "entier passes"; } else { puts "entier fails"; }
if [string is entier "123abcx"] { puts "entier fails"; } else { puts "entier passes"; }
if [string is entier -failindex res1 "123xabc"] { puts "entier fails"; } else { puts "entier passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is false false] { puts "false passes"; } else { puts "false fails"; }
if [string is false None] { puts "false fails"; } else { puts "false passes"; }
if [string is false -failindex res1 None] { puts "false fails"; } else { puts "false passes"; }
if [string compare $res1 0] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is integer "123"] { puts "integer passes"; } else { puts "integer fails"; }
if [string is integer "123abcx"] { puts "integer fails"; } else { puts "integer passes"; }
if [string is integer -failindex res1 "123xabc"] { puts "integer fails"; } else { puts "integer passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is lower "abc"] { puts "lower passes"; } else { puts "lower fails"; }
if [string is lower "abcDEF"] { puts "lower fails"; } else { puts "lower passes"; }
if [string is lower -failindex res1 "abcDEF"] { puts "lower fails"; } else { puts "lower passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is print "abc"] { puts "print passes"; } else { puts "print fails"; }
if [string is print "abc_\x01"] { puts "print fails"; } else { puts "print passes"; }
if [string is print -failindex res1 "abc_\x01"] { puts "print fails"; } else { puts "print passes"; }
if [string compare $res1 4] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is graph "123abc"] { puts "graph passes"; } else { puts "graph fails"; }
if [string is graph "123!abc"] { puts "graph fails"; } else { puts "graph passes"; }
if [string is graph -failindex res1 "123!abc"] { puts "graph fails"; } else { puts "graph passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is punct ";."] { puts "punct passes"; } else { puts "punct fails"; }
if [string is punct "abc123"] { puts "punct fails"; } else { puts "punct passes"; }
if [string is punct -failindex res1 "abcd123"] { puts "punct fails"; } else { puts "punct passes"; }
if [string compare $res1 0] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is space " "] { puts "space passes"; } else { puts "space fails"; }
if [string is space " 123!abc"] { puts "space fails"; } else { puts "space passes"; }
if [string is space -failindex res1 " 123!abc"] { puts "space fails"; } else { puts "space passes"; }
if [string compare $res1 1] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is true true] { puts "true passes"; } else { puts "true fails"; }
if [string is true false] { puts "true fails"; } else { puts "true passes"; }
if [string is true -failindex res1 false] { puts "true fails"; } else { puts "true passes"; }
if [string compare $res1 0] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is upper "ABC"] { puts "upper passes"; } else { puts "upper fails"; }
if [string is upper "ABCdef"] { puts "upper fails"; } else { puts "upper passes"; }
if [string is upper -failindex res1 "ABCdef"] { puts "upper fails"; } else { puts "upper passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is unicode abc] { puts "unicode passes"; } else { puts "unicode fails"; }
if [string is unicode None] { puts "unicode fails"; } else { puts "unicode passes"; }
if [string is unicode -failindex res1 None] { puts "unicode fails"; } else { puts "unicode passes"; }
if [string compare $res1 4] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is wordchar "abc"] { puts "wordchar passes"; } else { puts "wordchar fails"; }
if [string is wordchar "123@"] { puts "wordchar fails"; } else { puts "wordchar passes"; }
if [string is wordchar -failindex res1 "123@"] { puts "wordchar fails"; } else { puts "wordchar passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
if [string is xdigit "123abcdef"] { puts "xdigit passes"; } else { puts "xdigit fails"; }
if [string is xdigit "123abcx"] { puts "xdigit fails"; } else { puts "xdigit passes"; }
if [string is xdigit -failindex res1 "123xabc"] { puts "xdigit fails"; } else { puts "xdigit passes"; }
if [string compare $res1 3] { puts "res1 fails"; } else { puts "res1 passed"; }
puts "res1 = $res1"
