import functools
import sys
import time
import types


class Timeprint(types.ModuleType):
    """
    Timeprint can be used as a context manager or decorator
    to print how much time things take to run.

    It pretends to be a module so it can be used directly,
    rather than making users import or reference something
    below the timeprint module.

    """

    # Keep a reference to these because messing with sys.modules
    # causes them to disappear from the module/global namespace.
    functools = functools
    sys = sys
    time = time
    __name__ = __name__

    def __init__(self, name=None):
        self._name = name
        self._stack = []
        super(self.__class__, self).__init__(self.__name__)

    def __enter__(self):
        self._stack.append((
            self._name,
            self.time.time(),
        ))

    def __exit__(self, *args, **kwargs):
        name, start = self._stack.pop()
        elapsed = (self.time.time() - start)
        self.sys.stderr.write(self.format_message(
            name=name or 'it', seconds=elapsed
        ) + '\n')

    def __call__(self, *args):
        func = args and args[0]
        if hasattr(func, '__call__'):
            return self.decorator(func)
        else:
            return self.contextmanager(*args)

    def format_message(self, name, seconds):
        if seconds < 0.001:
            return '{} took {:.4f} ms'.format(name, seconds * 1000)
        elif seconds < 0.1:
            return '{} took {:.2f} ms'.format(name, seconds * 1000)
        elif seconds < 1:
            return '{} took {:.0f} ms'.format(name, seconds * 1000)
        else:
            return '{} took {:.1f} s'.format(name, seconds)

    def contextmanager(self, name=None):
        return self.__class__(name or self._name)

    def decorator(self, func):

        context = self.contextmanager(self._name or func.__name__)

        @self.functools.wraps(func)
        def decorator(*args, **kwargs):
            with context:
                return func(*args, **kwargs)

        return decorator


# Replace the module with the fake module
# so it can be used directly.
sys.modules[__name__] = Timeprint()
