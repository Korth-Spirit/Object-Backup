# Copyright (c) 2021-2022 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from korth_spirit import ConfigurableInstance
from korth_spirit.configuration import (AggregateConfiguration,
                                        InputConfiguration, JsonConfiguration)

from utilities import (and_do, append_to_file, load_saved_file, on_each,
                       try_add, try_delete)

with ConfigurableInstance(
    AggregateConfiguration({
        JsonConfiguration: ("configuration.json",),
    })
) as bot:
    on_each(bot.query(), lambda obj: and_do(
        funcs=[
            lambda: try_delete(obj),
            lambda: append_to_file("backup.txt", obj),
            lambda: print(f'Attempting to delete {obj.model} at {obj.x}, {obj.y}, {obj.z}'),
        ]
    ))

    on_each(load_saved_file("backup.txt"), lambda obj: and_do(
        funcs=[
            lambda: try_add(obj),
            lambda: print(f'Attempting to add {obj.model} at {obj.x}, {obj.y}, {obj.z}'),
        ]
    ))
