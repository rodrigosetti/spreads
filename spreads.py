#! /usr/bin/env python
# coding: utf-8

from __future__ import division

import atexit
import math
import re
import readline
import os

IDENTIFIER_RE = re.compile(r'^[a-zA-Z_]\w*$')

class Expressions(object):

    def __init__(self):
        self.expressions = {}
        self.values = {}

    def __getitem__(self, name):
        expression = str(self.expressions[name])
        value = str(self.values[name])

        if expression == value:
            return expression
        else:
            return "%s => %s" % (expression, value)

    def evaluate(self, expression):
        "Return the evaluated value of the expression in this context"
        if type(expression) == str:
            # try to parse the expression. if an error is found,
            # just ignore and use the unevaluated form
            try:
                return eval(expression, math.__dict__, self.values)
            except:
                return expression
        else:
            return expression

    def update(self, name):
        "Updates just the expression with given name"
        self.values[name] = self.evaluate(self.expressions[name])

    def __setitem__(self, name, expression):
        """
        Set an expression value, and then update all others to the new
        values.
        """
        self.expressions[name] = expression
        # updates itself first
        self.update(name)

        # update all others
        self.update_all()

    def __delitem__(self, name):
        del self.expressions[name]
        del self.values[name]

    def update_all(self, print_changed=True):
        """
        Evaluates all expressions to yield the new values within they own
        scope.
        """
        for name in self.expressions:
            before_value = str(self.values[name])

            self.update(name)

            value = str(self.values[name])
            if print_changed and before_value != value:
                print "%s => %s" % (name, value)

    def show(self):
        for name, expression in self.expressions.iteritems():
            value = str(self.values[name])

            if expression == value:
                print "%s => %s" % (name, expression)
            else:
                print "%s = %s => %s" % (name, expression, value)

if __name__ == "__main__":

    histfile = os.path.join(os.path.expanduser("~"), ".spreads-hist")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)

    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set blink-matching-paren on")

    expressions = Expressions()

    while True:
        try:
            # get input
            text = raw_input(">>  ").strip()

            # do some simple parsing.
            # if text starts with "del", remove name
            if text.startswith('del'):
                words = text.split()
                if len(words) != 2:
                    raise Exception('Error: del form should be "del <name>"')
                expressions.__delitem__(words[1])
            # if text has a "=", then it's an attribution
            elif '=' in text:
                words = text.split('=')
                if len(words) != 2:
                    raise Exception('Error: attribution form should be "<name> = <expression>"')
                name, expression = words[0].strip(), words[1].strip()
                expressions[name] = expression
                value = str(expressions.values[name])
                if value != expression:
                    print value
            elif text == '?':
                for name, value in expressions.values.iteritems():
                    print "%s => %s" % (name, value)
            elif text == '??':
                expressions.show()
            elif text.endswith('?'):
                words = text.split('?')
                if len(words) != 2:
                    raise Exception('Error: query format shoule be "<name>?"')
                name = words[0].strip()
                if not IDENTIFIER_RE.match(name):
                    raise Exception('Left hand of attribution should be a valid identifier')
                try:
                    print expressions[name]
                except KeyError:
                    raise Exception('"%s" is not defined' % name)

            elif IDENTIFIER_RE.match(text):
                # input is an identifier
                try:
                    print expressions.values[text]
                except KeyError:
                    raise Exception('"%s" is not defined' % text)
            elif text:
                # input is an expression: evaluates and print output
                print expressions.evaluate(text)

        except EOFError:
            break
        except KeyboardInterrupt:
            print "\ninterrupt."
        except Exception as e:
            print e.message

