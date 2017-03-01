# Timeprint
Python context manager and decorator for showing time elapsed.

# Setup

```
pip install timeprint
```

# Usage as a context manager

```python
import timeprint

with timeprint:
  do_stuff()

# it took 100ms

with timeprint('some stuff')
  do_stuff()

# some stuff took 100ms
```

# Usage as a decorator

```python
import timeprint

@timeprint
def first_function():
  do_stuff()

# first_function took 100ms

@timeprint('some other stuff')
def second_function():
  do_stuff()

# some other stuff took 100ms
```

# Is that it?

Yes. I was tired of finding and copying my old [Gist](https://gist.github.com/raymondbutcher/5168588) into files every time I wanted to measure a small chunk of code.
