import sys

try:
    from IPython.display import clear_output as _clear_output
except ImportError:
    _clear_output = None

from ipywidgets import widgets
from IPython.display import display as ipydisplay

try:
    # IPython 4
    from traitlets import Unicode, Dict, Float, Tuple, CUnicode
except ImportError:
    # IPython 3
    from IPython.utils.traitlets import Unicode, Dict, Float, Tuple, CUnicode

class Px(CUnicode):

    def validate(self, obj, value):
        """Converts all length inputs to px, ex, em, and %"""
        if isinstance(value,int):
            return unicode(value)+u"px"
        if isinstance(value,str):
            return unicode(value)
        if isinstance(value,unicode):
            return value
        if value is None and self.allow_none is True:
            return value
        else:
            raise TraitError('invalid value for type: %r' % value)

class DivBar(widgets.DOMWidget):

    _view_module = Unicode('nbextensions/progressbar/js/bar', sync=True)
    _view_name = Unicode('ProgressView', sync=True)

    outer_style = Dict({"border":"1px solid gray",
                        "width":"200px",
                        "height":"10px",
                        "margin":"4px"},
                        sync=True)

    inner_style = Dict({"height":"8px",
                      "background-color":"#0063a3"},
                      sync=True)

    _inner_attr = Tuple(allow_none=False, sync=True)
    _outer_attr = Tuple(allow_none=False, sync=True)

    max_width = Px(sync=True)

    value = Float(allow_none=True, sync=True)

    def __init__(self, max_value=None, max_width=None, incrament=None,
                border_style=None, bar_style=None, *args, **kwargs):
    	"""A progressbar implamented with Divs using widgets"""
        super(DivBar,self).__init__(*args, **kwargs)
        if border_style:
            self.border_style = border_style
        if bar_style:
            self.bar_style = bar_style
        if not max_width:
            max_width = '198px'
        self.max_width = max_width
        self.max_value = max_value
        self.incrament = incrament or -1
        self.value = 0

    def inner_attr(self, name, value):
        self._inner_attr = (name, value)
        self.inner_style[name] = value

    def outer_attr(self, name, value):
        self._outer_attr = (name, value)
        self.outer_style[name] = value

    def update(self, value):
        max_val = (self.max_value or 1)
        new = float(value)/max_val
        i = float(self.incrament)/max_val
        if new-self.value>=i:
            self.value = new
        elif round((1-new)/i)==1:
            self.value = 1.0
        elif new<i:
            self.value = new

    def display(self):
        ipydisplay(self)

class PyBar(object):

    _clear = True

    _default = {'pre':'' if _clear_output else '\r',
                'left':"[", 'symbol':'=', 'right':']',
                'post':" %d%%"}

    def __init__(self, length=20, limit=None, **kwargs):
    	"""A progressbar implamented in pure python"""
        self._current = None
        self.limit = limit
        self.length = length
        traits = self._merge_styles(kwargs)
        for key,value in traits.items():
            setattr(self, key, value)
        self.form = self._make_form(length)

    def _merge_styles(self, kwargs):
        traits = self._default.copy()
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
        spaces = length*len(self.symbol)
        inner = "%-"+str(spaces)+"s"
        right = self.right+self.post
        return left+inner+right

    render = lambda self,*args: self.form%args

    def printout(self, value):
        percent = float(value)/(self.limit or 1)
        num = int(round(percent*self.length))
        if num!=self._current:
            if self._clear and _clear_output:
                _clear_output()
            bar = self.symbol*num
            prcnt = 100 if num==self.length else percent*100
            rendered = self.render(bar, prcnt)
            sys.stdout.write(rendered)
            sys.stdout.flush()
            self._current = num