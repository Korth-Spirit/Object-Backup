# Copyright (c) 2021 Johnathan P. Irvin
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
from korth_spirit import Instance
from korth_spirit.coords import Coordinates

from utilities import (and_do, append_to_file, load_saved_file, on_each,
                       try_add, try_delete)

with Instance(name="Portal Mage") as bot:
    try:
        bot.login(
            citizen_number=(int(input("Citizen Number: "))),
            password=input("Password: ")
        ).enter_world(
            world_name=input("World: ")
        ).move_to(Coordinates(x=0, y=0, z=0))

        on_each(bot.query(), lambda obj: and_do(
            funcs=[
                lambda: try_delete(obj),
                lambda: append_to_file("backup.txt", obj),
                lambda: print(f'Attempting to delete {obj.model} at {obj.x}, {obj.y}, {obj.z}'),
                lambda: append_to_file("log.txt", f'Attempting to delete {vars(obj)}'),
            ]
        ))

        on_each(load_saved_file("backup.txt"), lambda obj: and_do(
            funcs=[
                lambda: try_add(obj),
                lambda: print(f'Attempting to add {obj.model} at {obj.x}, {obj.y}, {obj.z}'),
                lambda: append_to_file("log.txt", f'Attempting to add {vars(obj)}'),
            ]
        ))

    except Exception as e:
        print("An error occurred:", e)
        exit()

