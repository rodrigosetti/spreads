#! /usr/bin/env python
# coding: utf-8

import atexit
import readline
import os

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

    def __setitem__(self, name, expression):
        """
        Set an expression value, and then update all others to the new
        values.
        """
        self.expressions[name] = expression

        # updates itself
        if type(expression) == str:
            # try to parse the expression. if an error is found,
            # just ignore and use the unevaluated form
            try:
                self.values[name] = eval(expression, self.values)
            except:
                self.values[name] = expression
        else:
            self.values[name] = expression

        # update all others
        self.update()

    def __delitem__(self, name):
        del self.expressions[name]
        del self.values[name]

    def update(self, print_changed=True):
        """
        Evaluates all expressions to yield the new values within they own
        scope.
        """
        for name, expression in self.expressions.iteritems():
            before_value = str(self.values[name])

            if type(expression) == str:
                # try to parse the expression. if an error is found,
                # just ignore and use the unevaluated form
                try:
                    self.values[name] = eval(expression, self.values)
                except:
                    self.values[name] = expression
            else:
                self.values[name] = expression

            value = str(self.values[name])
            if print_changed and before_value != value:
                if expression == value:
                    print "%s = %s" % (name, expression)
                else:
                    print "%s = %s => %s" % (name, expression, value)

    def show(self):
        for name, expression in self.expressions.iteritems():
            value = str(self.values[name])

            if expression == value:
                print "%s = %s" % (name, expression)
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
            elif text == '*':
                expressions.show()
            elif text:
                try:
                    print expressions[text]
                except KeyError:
                    raise Exception('"%s" is not defined' % text)

        except EOFError:
            break
        except KeyboardInterrupt:
            print "\ninterrupt."
        except Exception as e:
            print e.message

