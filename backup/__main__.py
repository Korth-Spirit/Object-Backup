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
import json
from typing import Callable, Iterable, List

from korth_spirit import Instance, WorldEnum
from korth_spirit.aw_object import AWObject
from korth_spirit.coords import Coordinates
from korth_spirit.data import ObjectCreateData, ObjectDeleteData
from korth_spirit.sdk import aw_object_add, aw_object_delete


def ceil_div(a: int, b: int) -> int:
    """
    Returns the ceiling of a / b.

    Args:
        a (int): The dividend.
        b (int): The divisor.

    Returns:
        int: The ceiling of a / b.
    """
    return -(a // -b)

def query_world(bot: Instance) -> Iterable[AWObject]:
    """
    Queries the entire world. Assumes priveleges.
    It is important to remember that we're scanning sectors of 8x8 cells in a 3x3 grid.

    Args:
        bot (Instance): The instance who does the work.

    Returns:
        Iterable[AWObject]: A list of the objects queried.
    """
    world_size = bot.get_world().get_attribute(WorldEnum.AW_WORLD_SIZE)
    scan_range = ceil_div(world_size, 8)

    for x in range(-scan_range, scan_range + 1):
        for z in range(-scan_range, scan_range + 1):
            print(f"Querying sector {x * 8}, {z * 8}")
            for obj in bot.query(x * 8, z * 8):
                yield AWObject.from_cell_object(obj)

def append_to_file(file_name: str, data: str):
    """
    Appends the data to the file.

    Args:
        file_name (str): The name of the file to append to.
        data (str): The data to append.
    """    
    with open(file_name, "a") as f:
        f.write(data)

def and_do(funcs: List[Callable], *args, **kwargs) -> None:
    """
    Iterates over all objects in the world.

    Args:
        bot (Instance): The instance who does the work.
        funcs (List[Callable]): The list of functions to call.
        args (List[Any]): The list of arguments to pass to the functions.
        kwargs (Dict[str, Any]): The dictionary of keyword arguments to pass to the functions.
    """
    for each in funcs:
        each(*args, **kwargs)
    
def on_each(iterable: Iterable, callback: callable) -> None:
    """
    Iterates over all objects in the world.

    Args:
        callback (callable): The callback to call for each object.
    """
    for each in iterable:
        callback(each)

def try_delete(obj: AWObject) -> None:
    """
    Attempts to delete the object.

    Args:
        bot (Instance): The instance who does the work.
        obj (AWObject): The object to delete.
    """
    try:
        aw_object_delete(ObjectDeleteData(
            number=obj.number,
            x=obj.x,
            z=obj.z,
        ))
    except Exception as e:
        print(f"Failed to delete {obj} -- {e}")

def try_add(obj: AWObject) -> None:
    """
    Attempts to add the object.

    Args:
        bot (Instance): The instance who does the work.
        obj (AWObject): The object to add.
    """
    try:
        aw_object_add(ObjectCreateData(
            type=obj.type,
            x=obj.x,
            y=obj.y,
            z=obj.z,
            yaw=obj.yaw,
            tilt=obj.tilt,
            roll=obj.roll,
            model=obj.model,
            description=obj.description,
            action=obj.action,
            data=obj.data
        ))
    except Exception as e:
        print(f"Failed to add {obj} -- {e}")

def restore_from_file(bot: Instance, file_name: str) -> None:
    """
    Restores the objects from the file.

    Args:
        bot (Instance): The instance who does the work.
        file_name (str): The name of the file to restore from.
    """
    with open(file_name, "r") as f:
        for line in f:
            try_add(AWObject(
                **json.loads(line)
            ))

with Instance(name="Portal Mage") as bot:
    try:
        (
            bot
                .login(
                    citizen_number=(int(input("Citizen Number: "))),
                    password=input("Password: ")
                )
                .enter_world(input("World: "))
                .move_to(Coordinates(0, 0, 0))
        )

        on_each(query_world(bot), lambda obj: and_do(
            funcs=[
                lambda: try_delete(obj),
                lambda: append_to_file("backup.txt", json.dumps(obj.__dict__) + "\n"),
            ]
        ))
        restore_from_file(bot, "./backup.txt")

    except Exception as e:
        print("An error occurred:", e)
        exit()

