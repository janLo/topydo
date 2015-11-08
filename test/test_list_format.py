# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from collections import namedtuple
from freezegun import freeze_time
from six import u

from test.command_testcase import CommandTest
from test.facilities import load_file_to_todolist
from topydo.commands.ListCommand import ListCommand
from topydo.lib.Config import config

# We're searching for 'mock'
# pylint: disable=no-name-in-module
try:
    from unittest import mock
except ImportError:
    import mock

class ListFormatTest(CommandTest):
    def setUp(self):
        super(ListFormatTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListFormat.txt")
        self.terminal_size = namedtuple('terminal_size', ['columns', 'lines'])

    def test_list_format01(self):
        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %s %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-03 Lorem ipsum dolorem sit amet. Red @fox +jumped over the and jar due:2015-11-05 lazy:bar t:2015-11-04
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1 key:value
|  5| Drink beer @ home ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.PrettyPrinterFilter.get_terminal_size')
    def test_list_format02(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(80, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-03 Lorem ipsum dolore... due:2015-11-05 lazy:bar t:2015-11-04
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1 key:value
|  5| Drink beer @ home ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.PrettyPrinterFilter.get_terminal_size')
    def test_list_format03(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2 due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-03 Lorem ipsum dolorem sit amet. Red @fox... due:2015-11-05 lazy:bar t:2015-11-04
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1 key:value
|  5| Drink beer @ home ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.PrettyPrinterFilter.get_terminal_size')
    def test_list_format04(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S	%K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2                            due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-03 Lorem ipsum dolorem sit amet. Red @fox... due:2015-11-05 lazy:bar t:2015-11-04
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1                                                         key:value
|  5| Drink beer @ home                                                        ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with                                               date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @mock.patch('topydo.lib.PrettyPrinterFilter.get_terminal_size')
    def test_list_format05(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(80, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %{(}p{)} %c %S	%K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| (D) 2015-08-31 Bar @Context1 +Project2        due:2015-09-30 t:2015-09-29
|  2| (Z) 2015-11-03 Lorem ipsum dolore... due:2015-11-05 lazy:bar t:2015-11-04
|  3| (C) 2015-07-12 Foo @Context2 Not@Context +Project1 Not+Project
|  4| (C) Baz @Context1 +Project1                                     key:value
|  5| Drink beer @ home                                    ical:foobar id:1 p:2
|  6| x 2014-12-12 Completed but with                           date:2014-12-12
"""

    @freeze_time("2015, 11, 03")
    @mock.patch('topydo.lib.PrettyPrinterFilter.get_terminal_size')
    def test_list_format06(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %p %S %k	%{(}H{)}'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| D Bar @Context1 +Project2                (3 months ago, due a month ago, started a month ago)
|  2| Z Lorem ipsum dolorem sit amet. Red @f... lazy:bar (just now, due in 2 days, starts in a day)
|  3| C Foo @Context2 Not@Context +Project1 Not+Project                              (4 months ago)
|  4| C Baz @Context1 +Project1 key:value
|  5| Drink beer @ home
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @freeze_time("2015, 11, 03")
    @mock.patch('topydo.lib.PrettyPrinterFilter.get_terminal_size')
    def test_list_format07(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '|%I| %x %p %S %k	%{(}h{)}'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| D Bar @Context1 +Project2                              (due a month ago, started a month ago)
|  2| Z Lorem ipsum dolorem sit amet. Red @fox +jumped... lazy:bar (due in 2 days, starts in a day)
|  3| C Foo @Context2 Not@Context +Project1 Not+Project
|  4| C Baz @Context1 +Project1 key:value
|  5| Drink beer @ home
|  6| x 2014-12-12 Completed but with date:2014-12-12
"""
        self.assertEqual(self.output, result)

    @freeze_time("2015, 11, 03")
    @mock.patch('topydo.lib.PrettyPrinterFilter.get_terminal_size')
    def test_list_format08(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '%c %d %t %x'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""2015-08-31 2015-09-30 2015-09-29
2015-11-03 2015-11-05 2015-11-04
2015-07-12


x 2014-12-12
"""
        self.assertEqual(self.output, result)

    @freeze_time("2015, 11, 03")
    @mock.patch('topydo.lib.PrettyPrinterFilter.get_terminal_size')
    def test_list_format09(self, mock_terminal_size):
        mock_terminal_size.return_value = self.terminal_size(100, 25)

        config(p_overrides={('ls', 'list_format'): '%C | %D | %T | %X'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""3 months ago | a month ago | a month ago |
just now | in 2 days | in a day |
4 months ago | | |
| | |
| | |
| | | x 11 months ago
"""
        self.assertEqual(self.output, result)

    def test_list_format10(self):
        config(p_overrides={('ls', 'list_format'): '|%i| %k'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|1|
|2| lazy:bar
|3|
|4| key:value
|5|
|6| date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format11(self):
        config(p_overrides={('ls', 'list_format'): '|%I| %K'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| due:2015-09-30 t:2015-09-29
|  2| due:2015-11-05 lazy:bar t:2015-11-04
|  3|
|  4| key:value
|  5| ical:foobar id:1 p:2
|  6| date:2014-12-12
"""
        self.assertEqual(self.output, result)

    def test_list_format12(self):
        config(p_overrides={('ls', 'list_format'): '|%I| %%'})
        command = ListCommand(["-x"], self.todolist, self.out, self.error)
        command.execute()

        result = u"""|  1| %
|  2| %
|  3| %
|  4| %
|  5| %
|  6| %
"""
        self.assertEqual(self.output, result)
