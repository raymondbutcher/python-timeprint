from __future__ import print_function

import functools
import re
import sys
import timeprint
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def assert_output_matches(*lines):
    pattern = re.compile('\n'.join(lines))

    def decorator(func):

        @functools.wraps(func)
        def test(self, *args, **kwargs):
            stderr = sys.stderr
            stdout = sys.stdout
            sys.stderr = sys.stdout = StringIO()
            try:
                result = func(self, *args, **kwargs)
                output = sys.stdout.getvalue()
            finally:
                sys.stderr = stderr
                sys.stdout = stdout
            match = pattern.search(output)
            error_message = '\n'.join((
                'Output did not match.',
                'Regex pattern: {}'.format(repr(pattern.pattern)),
                'Output: {}'.format(repr(output)),
            ))
            self.assertTrue(match, error_message)
            return result

        return test
    return decorator


class TestTimeprint(unittest.TestCase):

    def test_format_message(self):
        ms = 1.0 / 1000
        self.assertEqual(timeprint.format_message('it', 0.05 * ms), 'it took 0.0500 ms')
        self.assertEqual(timeprint.format_message('it', 0.5 * ms), 'it took 0.5000 ms')
        self.assertEqual(timeprint.format_message('it', 5 * ms), 'it took 5.00 ms')
        self.assertEqual(timeprint.format_message('it', 50 * ms), 'it took 50.00 ms')
        self.assertEqual(timeprint.format_message('it', 500 * ms), 'it took 500 ms')
        self.assertEqual(timeprint.format_message('it', 1), 'it took 1.0 s')
        self.assertEqual(timeprint.format_message('it', 1.5), 'it took 1.5 s')
        self.assertEqual(timeprint.format_message('it', 2), 'it took 2.0 s')


class TestTimeprintContext(unittest.TestCase):

    @assert_output_matches(
        'it worked',
        'it took \d+\.\d+ ms',
    )
    def test_not_called(self):
        with timeprint:
            print('it worked')

    @assert_output_matches(
        'it worked',
        'it took \d+\.\d+ ms',
    )
    def test_called(self):
        with timeprint():
            print('it worked')

    @assert_output_matches(
        'it worked',
        'calling context with name took \d+\.\d+ ms',
    )
    def test_called_with_name(self):
        with timeprint('calling context with name'):
            print('it worked')

    @assert_output_matches(
        'one a',
        'two',
        'two took \d+\.\d+ ms',
        'one b',
        'one took \d+\.\d+ ms',
    )
    def test_nested(self):
        with timeprint('one'):
            print('one a')
            with timeprint('two'):
                print('two')
            print('one b')


class TestTimeprintDecorator(unittest.TestCase):

    @assert_output_matches(
        'it worked',
        'func1 took \d+\.\d+ ms',
    )
    def test_not_called(self):

        @timeprint
        def func1():
            print('it worked')
            return 1

        self.assertEqual(func1(), 1)

    @assert_output_matches(
        'it worked',
        'func2 took \d+\.\d+ ms',
    )
    def test_called(self):

        @timeprint()
        def func2():
            print('it worked')
            return 2

        self.assertEqual(func2(), 2)

    @assert_output_matches(
        'it worked',
        'calling as decorator with name took \d+\.\d+ ms',
    )
    def test_called_with_name(self):

        @timeprint('calling as decorator with name')
        def func3():
            print('it worked')
            return 3

        self.assertEqual(func3(), 3)


class TestTimeprintDecoratorMore(unittest.TestCase):

    @assert_output_matches(
        '1 2 3',
        'func4 took \d+\.\d+ ms',
    )
    def test_not_called(self):

        @timeprint
        def func4(x, y, z):
            print(x, y, z)
            return 4

        self.assertEqual(func4(1, 2, z=3), 4)

    @assert_output_matches(
        '1 2 3',
        'func5 took \d+\.\d+ ms',
    )
    def test_called(self):

        @timeprint()
        def func5(x, y, z):
            print(x, y, z)
            return 5

        self.assertEqual(func5(1, 2, z=3), 5)

    @assert_output_matches(
        '1 2 3',
        'calling as decorator with name took \d+\.\d+ ms',
    )
    def test_called_with_name(self):

        @timeprint('calling as decorator with name')
        def func6(x, y, z):
            print(x, y, z)
            return 6

        self.assertEqual(func6(1, 2, z=3), 6)


if __name__ == '__main__':
    unittest.main()
