#!/usr/bin/env python
"""
    Tool Command Language (Tcl) interpreter written in Python.
    Copyright (C) 2021  Bradford G. Van Treuren

    Tool Command Language (Tcl) interpreter written in Python.
    The interpreter is just a core interpreter and not a comprehensive
    implementation of the complete command language.  This was written
    to be able to extend to create an interpreter for IEEE Std 1687
    Procedural Description Language (PDL) for EDA tools.

    The inspiration for this code is based on the C code located at:
    http://oldblog.antirez.com/post/PICOTCL.html.  Major changes different
    from this code include making the parser and interpreter class based.
    Enhancements to the Tcl commands like puts and if are also to be included
    to make them more compliant to Tcl.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__authors__ = ["Bradford G. Van Treuren"]
__contact__ = "bradvt59@gmail.com"
__copyright__ = "Copyright 2021, VT Enterprises Consulting Services"
__credits__ = ["Bradford G. Van Treuren"]
__date__ = "2021/07/06"
__deprecated__ = False
__email__ = "bradvt59@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "Bradford G. Van Treuren"
__status__ = "Alpha/Experimental"
__version__ = "0.0.1"

import sys
from argparse import ArgumentError
from enum import Enum


class PICOTCL(Enum):
    PICOTCL_OK = 0
    PICOTCL_ERR = 1
    PICOTCL_RETURN = 2
    PICOTCL_BREAK = 3
    PICOTCL_CONTINUE = 4


class TOKEN_TYPES(Enum):
    PT_ESC = 0
    PT_STR = 1
    PT_CMD = 2
    PT_VAR = 3
    PT_SEP = 4
    PT_EOL = 5
    PT_EOF = 6


class picotclParser(object):
    def __init__(self, _text):  # picotclInitParser
        self.text = _text
        self.p = 0  # current text position
        self.length = len(_text)  # remaining length
        self.start = 0  # token start
        self.end = 0  # token end
        self.type = TOKEN_TYPES.PT_EOL  # token type, PT_...
        self.insidequote = False  # True if inside " "

    def parse_sep(self):
        self.start = self.p
        while self.p < len(self.text) and self.text[self.p] in [' ', '\t', '\n', '\r']:
            self.p += 1
            self.length -= 1
        self.end = self.p
        self.type = TOKEN_TYPES.PT_SEP
        return PICOTCL.PICOTCL_OK

    def parse_eol(self):
        self.start = self.p
        if self.p >= len(self.text):
            AssertionError("parse_eol() called with no more tokens available.")
        while self.text[self.p] in [' ', '\t', '\n', '\r', ';']:
            self.p += 1
            self.length -= 1
            if self.length == 0:
                break
            # if self.p >= len(self.text):
            #     raise AssertionError("self.length does not detect out of bound condition.")
        self.end = self.p
        self.type = TOKEN_TYPES.PT_EOL
        return PICOTCL.PICOTCL_OK

    def parse_command(self):
        level = 1
        blevel = 0
        self.p += 1  # Skip "["
        self.length -= 1
        self.start = self.p
        while self.p < len(self.text):
            if self.length == 0:
                break
            elif self.text[self.p] == '[' and blevel == 0:
                level += 1
            elif self.text[self.p] == ']' and blevel == 0:
                level -= 1
                if not level:
                    break
            elif self.text[self.p] == '\\':
                self.p += 1
                self.length -= 1
            elif self.text[self.p] == '{':
                blevel += 1
            elif self.text[self.p] == '}':
                if blevel != 0:
                    blevel -= 1
            self.p += 1
            self.length -= 1
        self.end = self.p
        self.type = TOKEN_TYPES.PT_CMD
        if self.text[self.p] == ']':
            self.p += 1
            self.length -= 1
        return PICOTCL.PICOTCL_OK

    def parse_var(self):
        # skip the '$'
        self.p += 1
        self.length -= 1
        self.start = self.p

        while self.p < len(self.text):
            c = self.text[self.p]
            if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9') or c == '_':
                self.p += 1
                self.length -= 1
                continue
            break
        if self.start == self.p:  # It's just a single char string "$"
            self.start = self.p - 1
            self.end = self.p
            self.type = TOKEN_TYPES.PT_STR
        else:
            self.end = self.p
            self.type = TOKEN_TYPES.PT_VAR
        return PICOTCL.PICOTCL_OK

    def parse_brace(self):
        level = 1
        self.p += 1
        self.start = self.p
        self.length -= 1
        while True:
            if self.length >= 2 and self.text[self.p] == '\\':
                self.p += 1
                self.length -= 1
            elif self.length == 0 or self.text[self.p] == '}':
                level -= 1
                if level == 0 or self.length == 0:
                    self.end = self.p
                    if self.length:
                        # Skip final closed brace
                        self.p += 1
                        self.length -= 1
                    self.type = TOKEN_TYPES.PT_STR
                    return PICOTCL.PICOTCL_OK
            elif self.text[self.p] == '{':
                level += 1
            self.p += 1
            self.length -= 1

    def parse_string(self):
        newword = (self.type == TOKEN_TYPES.PT_SEP or self.type == TOKEN_TYPES.PT_EOL or self.type == TOKEN_TYPES.PT_STR)
        if newword and self.text[self.p] == '{':
            return self.parse_brace()
        elif newword and self.text[self.p] == '"':
            self.insidequote = True
            self.p += 1
            self.length -= 1
        self.start = self.p
        while True:
            if self.length == 0:
                self.end = self.p
                self.type = TOKEN_TYPES.PT_ESC
                return PICOTCL.PICOTCL_OK
            c = self.text[self.p]
            if c == '\\':
                if self.length >= 2:
                    self.p += 1
                    self.length -= 1
            elif c == '$' or c == '[':
                self.end = self.p
                self.type = TOKEN_TYPES.PT_ESC
                return PICOTCL.PICOTCL_OK
            elif c == ' ' or c == '\t' or c == '\n' or c == '\r' or c == ';':
                if not self.insidequote:
                    self.end = self.p
                    self.type = TOKEN_TYPES.PT_ESC
                    return PICOTCL.PICOTCL_OK
            elif c == '"':
                if self.insidequote:
                    self.end = self.p
                    self.type = TOKEN_TYPES.PT_ESC
                    self.p += 1
                    self.length -= 1
                    self.insidequote = False
                    return PICOTCL.PICOTCL_OK
            self.p += 1
            self.length -= 1

    def parse_comment(self):
        while self.length and self.text[self.p] != '\n':
            self.p += 1
            self.length -= 1
        return PICOTCL.PICOTCL_OK

    def get_token(self):
        while True:
            if not self.length:
                if self.type != TOKEN_TYPES.PT_EOL and self.type != TOKEN_TYPES.PT_EOF:
                    self.type = TOKEN_TYPES.PT_EOL
                else:
                    self.type = TOKEN_TYPES.PT_EOF
                return PICOTCL.PICOTCL_OK
            assert(self.p < len(self.text))
            c = self.text[self.p]
            if c == ' ' or c == '\t' or c == '\r':
                if self.insidequote:
                    return self.parse_string()
                return self.parse_sep()
            elif c == '\n' or c == ';':
                if self.insidequote:
                    return self.parse_string()
                if self.p >= len(self.text):
                    raise AssertionError("Attempting to get a token beyond the string.")
                return self.parse_eol()
            elif c == '[':
                return self.parse_command()
            elif c == '$':
                return self.parse_var()
            elif c == '#':
                if self.type == TOKEN_TYPES.PT_EOL:
                    self.parse_comment()
                    continue
                return self.parse_string()
            else:
                return self.parse_string()
        return PICOTCL.PICOTCL_OK


class picolVar(object):
    def __init__(self):
        self.name = ""
        self.val = ""


class picolCmd(object):
    def __init__(self):
        self.name = ""
        self.function = None
        self.privdata = None


class picolCallFrame(object):
    def __init__(self):
        self.vars = []  # picolVar
        self.parent = None  # parent is None at top level


class picolInterp(object):
    def __init__(self):
        self.level = 0  # Level of nesting
        self.callframe = picolCallFrame()
        self.commands = []
        self.result = ""

    def set_result(self, s):
        self.result = s

    def get_result(self):
        return self.result

    def get_var(self, name):
        for _v in self.callframe.vars:
            if _v.name == name:
                return _v
        return None

    def set_var(self, _name, _val):
        _v = self.get_var(_name)
        if _v:
            _v.val = _val
        else:
            _v = picolVar()
            _v.name = _name
            _v.val = _val
            self.callframe.vars.append(_v)
        return PICOTCL.PICOTCL_OK

    def get_command(self, _name):
        for _c in self.commands:
            if _c.name == _name:
                return _c
        return None

    def register_command(self, _name, f, privdata):
        _c = self.get_command(_name)
        if _c:
            errbuf = "Command '{:s}' already defined".format(_name)
            self.set_result(errbuf)
            return PICOTCL.PICOTCL_ERR
        _c = picolCmd()
        _c.name = _name
        _c.function = f
        _c.privdata = privdata
        self.commands.append(_c)
        return PICOTCL.PICOTCL_OK

    def is_boolean_expr(self, expr):
        ret = -1
        try:
            val = int(expr)
            ret = 1 if (val != 0) else 0
        except ValueError:
            ret = -1
        return ret

    def get_bool_from_expression(self, expr):
        retcode = self.eval(expr)
        bret = -1
        if retcode == PICOTCL.PICOTCL_OK:
            x = self.is_boolean_expr(self.get_result())
            if x == 0:
                bret = 0
            elif x == 1:
                bret = 1
            else:
                retcode = PICOTCL.PICOTCL_ERR
        return retcode, bret

    def eval(self, _t):
        argc = 0
        argv = []
        retcode = PICOTCL.PICOTCL_OK
        self.set_result("")
        parser = picotclParser(_t)
        while True:
            # if not len(_t):
            #     raise AssertionError("Evaluating an empty string expression.")
            prevtype = parser.type
            parser.get_token()
            if parser.type == TOKEN_TYPES.PT_EOF:
                break
            if parser.start == parser.end:
                _t = ""
            else:
                _t = parser.text[parser.start:parser.end]
            if parser.type == TOKEN_TYPES.PT_VAR:
                _v = self.get_var(_t)
                if not _v:
                    errbuf = "No such variable '{:s}'".format(_t)
                    self.set_result(errbuf)
                    retcode = PICOTCL.PICOTCL_ERR
                    return retcode
                _t = _v.val
            elif parser.type == TOKEN_TYPES.PT_CMD:
                retcode = self.eval(_t)
                if retcode != PICOTCL.PICOTCL_OK:
                    return retcode
                _t = self.result
            elif parser.type == TOKEN_TYPES.PT_ESC:
                # TBD: escape handling missing!
                pass
            elif parser.type == TOKEN_TYPES.PT_SEP:
                prevtype = parser.type
                continue
            # We have a complete command + args. Call it!
            if parser.type == TOKEN_TYPES.PT_EOL:
                _c = picolCmd()
                prevtype = parser.type
                if argc:
                    _c = self.get_command(argv[0])
                    if _c is None:
                        bret = self.is_boolean_expr(argv[0])
                        if bret != -1:
                            self.set_result(argv[0])
                            return PICOTCL.PICOTCL_OK
                        else:
                            errbuf = "No such command '{:s}'".format(argv[0])
                            self.set_result(errbuf)
                            retcode = PICOTCL.PICOTCL_ERR
                            return retcode
                    retcode = _c.function(argv, _c.privdata)
                    if retcode != PICOTCL.PICOTCL_OK:
                        return retcode
                # Prepare for the next command
                argv = []
                argc = 0
                continue
            # We have a new token, append to the previous or as new arg?
            if prevtype == TOKEN_TYPES.PT_SEP or prevtype == TOKEN_TYPES.PT_EOL:
                argv.append(_t)
                argc += 1
            else:  # Interpolation
                argv[argc - 1] = argv[argc - 1] + _t
        return retcode

    def arity_err(self, _name):
        buf = "Wrong number of args for {:s}".format(_name)
        self.set_result(buf)
        return PICOTCL.PICOTCL_ERR

    def command_math(self, argv, pd):
        if len(argv) != 3:
            return self.arity_err(argv[0])
        _a = int(argv[1])
        _b = int(argv[2])
        if argv[0] == '+':
            _c = _a + _b
        elif argv[0] == '-':
            _c = _a - _b
        elif argv[0] == '*':
            _c = _a * _b
        elif argv[0] == '/':
            _c = _a // _b
        elif argv[0] == '>':
            _c = _a > _b
        elif argv[0] == '>=':
            _c = _a >= _b
        elif argv[0] == '<':
            _c = _a < _b
        elif argv[0] == '<=':
            _c = _a <= _b
        elif argv[0] == '==':
            _c = _a == _b
        elif argv[0] == '!=':
            _c = _a != _b
        else:
            _c = False  # I hate warnings
        if isinstance(_c, bool):
            self.set_result('1' if _c else '0')
        else:
            buf = "{:d}".format(_c)
            self.set_result(buf)
        return PICOTCL.PICOTCL_OK

    def command_set(self, argv, pd):
        if len(argv) != 3:
            return self.arity_err(argv[0])
        self.set_var(argv[1], argv[2])
        self.set_result(argv[2])
        return PICOTCL.PICOTCL_OK

    def command_puts(self, argv, pd):
        current = 1
        argc = len(argv)
        channel_id = sys.stdout
        end_val = "\n"
        if argc >= 2:
            # Far not enough arguments given!
            if current >= argc:
                return self.arity_err(argv[0] + ": ?-nonewline? ?channelId? string")
            if argv[current].lower() == "-nonewline":
                end_val = ""
                current += 1
            if current >= argc:
                return self.arity_err(argv[0] + ": ?-nonewline? ?channelId? string")
            if argv[current].lower() == "stdout":
                channel_id = sys.stdout
                current += 1
            elif argv[current].lower() == "stderr":
                channel_id = sys.stderr
                current += 1
            elif argv[current][0] == "$":  # a variable with file descriptor detected as a channel
                channel_id = self.get_var(argv[current])
                if isinstance(channel_id, str) and channel_id == "stdout":
                    channel_id = sys.stdout
                elif isinstance(channel_id, str) and channel_id == "stderr":
                    channel_id = sys.stderr
                current += 1
            if current >= argc:
                return self.arity_err(argv[0] + ": ?-nonewline? ?channelId? string")
            print("{:s}".format(argv[current]), end=end_val, file=channel_id)
            return PICOTCL.PICOTCL_OK
        return self.arity_err(argv[0] + ": ?-nonewline? ?channelId? string")

    def command_if(self, argv, pd):
        current = 1
        argc = len(argv)
        if argc >= 3:
            while True:
                # Far not enough arguments given!
                if current >= argc:
                    return self.arity_err(argv[0] + ": condition ?then? trueBody ?elseif ...? ?else? falseBody")
                retval, boolean = self.get_bool_from_expression(argv[current])
                current += 1
                if retval != PICOTCL.PICOTCL_OK:
                    return retval
                # There lacks something, isn't it?
                if current >= argc:
                    return self.arity_err(argv[0] + ": condition ?then? trueBody ?elseif ...? ?else? falseBody")
                if argv[current].lower() == "then":
                    current += 1
                # Tsk tsk, no then-clause?
                if current >= argc:
                    return self.arity_err(argv[0] + ": condition ?then? trueBody ?elseif ...? ?else? falseBody")
                if boolean:
                    return self.eval(argv[current])
                # Ok: no else-clause follows
                current += 1
                if current >= argc:
                    self.set_result("")
                    return PICOTCL.PICOTCL_OK
                falsebody = current
                current += 1
                if argv[falsebody].lower() == "else":
                    # IIICKS - else-clause isn't last cmd?
                    if current != (argc - 1):
                        return self.arity_err(argv[0] + ": condition ?then? trueBody ?elseif ...? ?else? falseBody")
                    return self.eval(argv[current])
                elif argv[falsebody].lower() == "elseif":
                    # Ok: elseif follows meaning all the stuff
                    # again (how boring...)
                    continue
                # OOPS - else-clause is not last cmd?
                elif falsebody != (argc - 1):
                    return self.arity_err(argv[0] + ": condition ?then? trueBody ?elseif ...? ?else? falseBody")
                return self.eval(argv[falsebody])
            return PICOTCL.PICOTCL_OK
        return self.arity_err(argv[0] + ": condition ?then? trueBody ?elseif ...? ?else? falseBody")

    def command_while(self, argv, pd):
        if len(argv) != 3:
            self.arity_err(argv[0])
        while True:
            retcode = self.eval(argv[1])
            if retcode != PICOTCL.PICOTCL_OK:
                return retcode
            if int(self.result):
                retcode = self.eval(argv[2])
                if retcode == PICOTCL.PICOTCL_CONTINUE:
                    continue
                elif retcode == PICOTCL.PICOTCL_OK:
                    continue
                elif retcode == PICOTCL.PICOTCL_BREAK:
                    return PICOTCL.PICOTCL_OK
                else:
                    return retcode
            else:
                return PICOTCL.PICOTCL_OK

    def command_retcodes(self, argv, pd):
        if len(argv) != 1:
            return self.arity_err(argv[0])
        if argv[0] == "break":
            return PICOTCL.PICOTCL_BREAK
        elif argv[0] == "continue":
            return PICOTCL.PICOTCL_CONTINUE
        return PICOTCL.PICOTCL_OK

    def drop_callframe(self):
        self.callframe = self.callframe.parent

    def command_proc(self, argv, pd):
        if len(argv) != 4:
            return self.arity_err(argv[0])
        # argv[2] => argument list
        # argv[3] => procedure body
        return self.register_command(argv[1], self.command_callproc, argv[2:])

    def command_return(self, argv, pd):
        if len(argv) != 1 and len(argv) != 2:
            return self.arity_err(argv[0])
        self.set_result(argv[1] if len(argv) == 2 else "")
        return PICOTCL.PICOTCL_RETURN

    def register_core_commands(self):
        name = ["+", "-", "*", "/", ">", ">=", "<", "<=", "==", "!="]
        for j in name:
            self.register_command(j, self.command_math, None)
        self.register_command("set", self.command_set, None)
        self.register_command("puts", self.command_puts, None)
        self.register_command("if", self.command_if, None)
        self.register_command("while", self.command_while, None)
        self.register_command("break", self.command_retcodes, None)
        self.register_command("continue", self.command_retcodes, None)
        self.register_command("proc", self.command_proc, None)
        self.register_command("return", self.command_return, None)
        self.register_command("string", self.command_string, None)

    def command_callproc(self, argv, _pd):
        x = _pd
        alist = x[0]
        body = x[1]
        _p = 0  # index in alist
        cf = picolCallFrame()
        arity = 0
        done = 0
        errcode = PICOTCL.PICOTCL_OK
        cf.parent = self.callframe
        self.callframe = cf
        while True:
            start = _p
            while _p < len(alist) and alist[_p] != ' ':
                _p += 1
            if _p < len(alist) and _p == start:
                _p += 1
                continue
            if _p == start:
                break
            if _p == len(alist):
                done = 1
            else:
                alist[_p] = ""
            arity += 1
            if arity > len(argv) - 1:
                self.set_result("Proc '{:s}' called with wrong arg num".format(argv[0]))
                self.drop_callframe()  # remove the called proc callframe
                return PICOTCL.PICOTCL_ERR
            self.set_var(alist[start], argv[arity])
            _p += 1
            if done:
                break
        if arity != len(argv) - 1:
            self.set_result("Proc '{:s}' called with wrong arg num".format(argv[0]))
            self.drop_callframe()  # remove the called proc callframe
            return PICOTCL.PICOTCL_ERR
        errcode = self.eval(body)
        if errcode == PICOTCL.PICOTCL_RETURN:
            errcode = PICOTCL.PICOTCL_OK
        self.drop_callframe()  # remove the called proc callframe
        return errcode

    def command_string(self, argv, pd):
        current = 1
        argc = len(argv)
        if argc >= 2:
            if argv[current].lower() == "cat":
                return self.__command_string_cat(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "compare":
                return self.__command_string_compare(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "equal":
                return self.__command_string_equal(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "index":
                return self.__command_string_index(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "length":
                return self.__command_string_length(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "range":
                return self.__command_string_range(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "repeat":
                return self.__command_string_repeat(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "reverse":
                return self.__command_string_reverse(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "tolower":
                return self.__command_string_tolower(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "toupper":
                return self.__command_string_toupper(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "trim":
                return self.__command_string_trim(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "trimright":
                return self.__command_string_trimright(argv[0], argc - 2, argv[2:], pd)
            elif argv[current].lower() == "trimleft":
                return self.__command_string_trimleft(argv[0], argc - 2, argv[2:], pd)

        else:
            return self.arity_err(argv[0] + ": see manual page for syntax")

    def __command_string_cat(self, cmd, argc, argv, pd):
        current = 0
        length = argc
        s = ""
        while length:
            s += argv[current]
            current += 1
            length -= 1
        self.set_result(s)
        return PICOTCL.PICOTCL_OK

    def __command_string_compare(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        nocase = 0
        lensize = None
        if largc >= 2:
            if argv[current].lower() == "-nocase":
                nocase = 1
                current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            if argv[current].lower() == "-length":
                current += 1
                if current >= largc:
                    return self.arity_err(cmd + ": see manual page for syntax")
                lensize = int(argv[current])
                if lensize < 0:
                    lensize = None
                current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            if argv[current].lower() == "-nocase":
                nocase = 1
                current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            s1 = argv[current]
            current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            s2 = argv[current]
            if nocase:
                s1 = s1.upper()
                s2 = s2.upper()
            if lensize is not None:
                if len(s1) < lensize:
                    lensize = len(s1)
                if len(s2) < lensize:
                    lensize = len(s2)
                if s1[:lensize] == s2[:lensize]:
                    self.set_result('0')
                    return PICOTCL.PICOTCL_OK
                elif s1[:lensize] < s2[:lensize]:
                    self.set_result('-1')
                    return PICOTCL.PICOTCL_OK
                elif s1[:lensize] > s2[:lensize]:
                    self.set_result('1')
                    return PICOTCL.PICOTCL_OK
                else:
                    return self.arity_err(cmd + ": see manual page for syntax")
            elif s1 == s2:
                self.set_result('0')
                return PICOTCL.PICOTCL_OK
            elif s1 < s2:
                self.set_result('-1')
                return PICOTCL.PICOTCL_OK
            elif s1 > s2:
                self.set_result('1')
                return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_equal(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        nocase = 0
        lensize = None
        if largc >= 2:
            if argv[current].lower() == "-nocase":
                nocase = 1
                current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            if argv[current].lower() == "-length":
                current += 1
                if current >= largc:
                    return self.arity_err(cmd + ": see manual page for syntax")
                lensize = int(argv[current])
                if lensize < 0:
                    lensize = None
                current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            if argv[current].lower() == "-nocase":
                nocase = 1
                current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            s1 = argv[current]
            current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            s2 = argv[current]
            if nocase:
                s1 = s1.upper()
                s2 = s2.upper()
            if lensize is not None:
                if len(s1) < lensize:
                    lensize = len(s1)
                if len(s2) < lensize:
                    lensize = len(s2)
                for i in range(lensize):
                    if s1[i] != s2[i]:
                        self.set_result('0')
                        return PICOTCL.PICOTCL_OK
                self.set_result('1')
                return PICOTCL.PICOTCL_OK
            elif s1 == s2:
                self.set_result('1')
                return PICOTCL.PICOTCL_OK
            else:
                self.set_result('0')
                return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_index(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        index = None
        if largc >= 2:
            s = argv[current]
            current += 1
            if current >= largc:
                return self.arity_err(cmd + ": index <string> <index>")
            if argv[current].lower() == "end":
                current += 1
                index = len(s) - 1
                if current >= largc:
                    return self.arity_err(cmd + ": index <string> <index>")
            elif argv[current].find('+') != -1:
                # end+n, m+n construct
                current += 1
                return self.arity_err(cmd + ": index <string> " + argv[current - 1] + " not supported yet.")
            elif argv[current].find('-') != -1:
                # end-n, m-n construct
                current += 1
                return self.arity_err(cmd + ": index <string> " + argv[current - 1] + " not supported yet.")
            else:
                try:
                    index = int(argv[current])
                    if index < 0:
                        index = None
                except ValueError:
                    return self.arity_err(cmd + ": index <string> <index>")
            if current >= largc:
                return self.arity_err(cmd + ": index <string> <index>")
            if index is None:
                self.set_result("")
                return PICOTCL.PICOTCL_OK
            else:
                self.set_result(s[index])
                return PICOTCL.PICOTCL_OK

    def __command_string_length(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        if largc == 1:
            self.set_result(str(len(argv[current])))
            return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": length <string>")

    def __command_string_range(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        first = 0
        last = 0
        if largc == 3:
            s = argv[current]
            current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            try:
                first = int(argv[current])
                current += 1
            except ValueError:
                return self.arity_err(cmd + ": see manual page for syntax")
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            try:
                last = int(argv[current])
                current += 1
            except ValueError:
                return self.arity_err(cmd + ": see manual page for syntax")
            if first < 0:
                first = 0
            if last >= len(s):
                last = len(s)
            if first > last:
                self.set_result("")
                return PICOTCL.PICOTCL_OK
            self.set_result(s[first:last])
            return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_repeat(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        if largc == 2:
            count = 1
            s = argv[current]
            current += 1
            if current >= largc:
                return self.arity_err(cmd + ": see manual page for syntax")
            else:
                try:
                    count = int(argv[current])
                    current += 1
                except ValueError:
                    return self.arity_err(cmd + ": see manual page for syntax")
            sb = ""
            for i in range(0, count):
                sb = sb + s
            self.set_result(sb)
            return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_reverse(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        if largc == 1:
            self.set_result(argv[current][::-1])
            return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_tolower(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        first = 0
        if largc >= 1:
            s = argv[current]
            last = len(s)
            current += 1
            if current < largc:
                try:
                    first = int(argv[current])
                    current += 1
                except ValueError:
                    return self.arity_err(cmd + ": see manual page for syntax")
            if current < largc:
                try:
                    last = int(argv[current]) + 1
                except ValueError:
                    return self.arity_err(cmd + ": see manual page for syntax")
            if first < 0:
                first = 0
            if last >= len(s):
                last = len(s)
            if first > last:
                self.set_result("")
                return PICOTCL.PICOTCL_OK
            self.set_result(s[first:last].lower())
            return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_toupper(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        first = 0
        if largc >= 1:
            s = argv[current]
            last = len(s)
            current += 1
            if current < largc:
                try:
                    first = int(argv[current])
                    current += 1
                except ValueError:
                    return self.arity_err(cmd + ": see manual page for syntax")
            if current < largc:
                try:
                    last = int(argv[current]) + 1
                except ValueError:
                    return self.arity_err(cmd + ": see manual page for syntax")
            if first < 0:
                first = 0
            if last >= len(s):
                last = len(s)
            if first > last:
                self.set_result("")
                return PICOTCL.PICOTCL_OK
            self.set_result(s[first:last].upper())
            return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_trim(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        lc = 0
        targv = []
        if largc >= 1:
            targv.append(argv[current])
            ls = len(targv[current])
            current += 1
            if current < largc:
                targv.append(argv[current])
                lc = len(targv[current])
                current += 1
            if current < largc:
                return self.arity_err(cmd + ": wrong number of arguments.")
            ret = self.__command_string_trimleft(cmd, argc, targv, pd)
            if ret != PICOTCL.PICOTCL_OK:
                return ret
            targv[0] = self.get_result()
            ret = self.__command_string_trimright(cmd, argc, targv, pd)
            if ret != PICOTCL.PICOTCL_OK:
                return ret
            self.set_result(self.get_result())
            return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_trimleft(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        chars = None
        lc = 0
        if largc >= 1:
            s = argv[current]
            ls = len(s)
            current += 1
            if current < largc:
                chars = argv[current]
                lc = len(chars)
                current += 1
            if current < largc:
                return self.arity_err(cmd + ": wrong number of arguments.")
            if chars is not None:
                if s[:lc] == chars:
                    self.set_result(s[lc:])
                else:
                    self.set_result(s)
                return PICOTCL.PICOTCL_OK
            else:
                self.set_result(s.lstrip())
                return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")

    def __command_string_trimright(self, cmd, argc, argv, pd):
        current = 0
        largc = len(argv)
        chars = None
        lc = 0
        if largc >= 1:
            s = argv[current]
            ls = len(s)
            current += 1
            if current < largc:
                chars = argv[current]
                lc = len(chars)
                current += 1
            if current < largc:
                return self.arity_err(cmd + ": wrong number of arguments.")
            if chars is not None:
                if s[ls - lc:] == chars:
                    self.set_result(s[:-lc])
                else:
                    self.set_result(s)
                return PICOTCL.PICOTCL_OK
            else:
                self.set_result(s.rstrip())
                return PICOTCL.PICOTCL_OK
        else:
            return self.arity_err(cmd + ": see manual page for syntax")


def main(argc, argv):
    interp = picolInterp()
    interp.register_core_commands()
    if argc == 1:
        while True:
            clibuf = input("PICOTCL> ")
            if clibuf == "":
                return 0
            retcode = interp.eval(clibuf)
            if interp.result != "":
                print("{:s} {:s}\n".format(str(retcode), str(interp.result)))
    elif argc == 2:
        fp = open(argv[1], mode='r')
        if fp is None:
            raise ArgumentError("open")
        buf = fp.read()
        fp.close()
        if interp.eval(buf) != PICOTCL.PICOTCL_OK:
            print("{:s}\n".format(interp.result))
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv))
