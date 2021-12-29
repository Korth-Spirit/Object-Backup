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
from typing import Callable, Iterable, List, Union

from korth_spirit.data import ObjectCreateData, ObjectDeleteData, CellObjectData
from korth_spirit.sdk import aw_object_add, aw_object_delete


def append_to_file(file_name: str, data: Union[CellObjectData, str]) -> None:
    """
    Appends the data to the file.

    Args:
        file_name (str): The name of the file to append to.
        data (Union[CellObjectData, str]): The data to append.
    """
    if type(data) == CellObjectData:
        data = json.dumps(data.__dict__)
    
    with open(file_name, "a") as f:
        f.write(f"{data}\n")

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

def load_saved_file(file_name: str) -> Iterable[CellObjectData]:
    """
    Load the CellObjectDatum saved as json objects separated by new lines.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        Iterable[CellObjectData]: The list of CellObjectData.
    """
    with open(file_name, "r") as f:
        for line in f:
            yield CellObjectData(
                **json.loads(line)
            )

def try_delete(obj: CellObjectData) -> None:
    """
    Attempts to delete the object.

    Args:
        bot (Instance): The instance who does the work.
        obj (CellObjectData): The object to delete.
    """
    try:
        aw_object_delete(ObjectDeleteData(
            number=obj.number,
            x=obj.x,
            z=obj.z,
        ))
    except Exception as e:
        print(f"Failed to delete {obj} -- {e}")

def try_add(obj: CellObjectData) -> None:
    """
    Attempts to add the object.

    Args:
        bot (Instance): The instance who does the work.
        obj (CellObjectData): The object to add.
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
