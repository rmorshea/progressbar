import sys
from contextlib import contextmanager

try:
    from IPython.display import clear_output
except ImportError:
    clear_output = None

class ProgressBar(object):

    _default = {'pre':'' if clear_output else '\r',
                'left':"[", 'symbol':'=', 'right':']',
                'post':" %d%%"}

    def __init__(self, length=20, **kwargs):
        self.current = None
        self.length = length
        traits = self._merge(kwargs)
        for key,value in traits.items():
            setattr(self, key, value)
        self.form = self._make_form(length)

    def _merge(self, kwargs):
        traits = self._default
        for key,value in kwargs.items():
            if key in traits:
                value = '' if value is None else str(value)
                traits[key] = value
            else:
                raise ValueError('style argument "%s"'
                                 ' not recognized'%key)
        return traits

    def _make_form(self, length):
        left = self.pre+self.left
        inner = "%-"+str(length)+"s"
        right = self.right+self.post
        return left+inner+right

    render = lambda self,*args: self.form%args

    def printout(self, percent):
        num = round(percent*self.length)
        if num>self.current:
            if clear_output:
                clear_output()
            bar = self.symbol*int(num)
            prcnt = 100 if bar==self.length else percent*100
            rendered = self.render(bar, prcnt)
            sys.stdout.write(rendered)
            sys.stdout.flush()
            self.current = num
