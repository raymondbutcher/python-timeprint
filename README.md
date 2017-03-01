# Timeprint
Python context manager and decorator for showing time elapsed.

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
