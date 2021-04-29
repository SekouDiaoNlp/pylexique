from dataclasses import dataclass
from pprint import pprint
from inspect import getmembers
from types import FunctionType


def attributes(obj):
    disallowed_names = {
      name for name, value in getmembers(type(obj))
        if isinstance(value, FunctionType)}
    return {
      name: getattr(obj, name) for name in dir(obj)
        if name[0:1] != '_' and name not in disallowed_names and hasattr(obj, name)}

def show_attributes(object):
    temp = vars(object)
    for item in temp:
        print(item, ':', temp[item])

def print_attributes(obj):
    pprint(attributes(obj))


def vdir(obj):
    """
    | This function pretty-display the lexical items in Lexique383.

    :param obj:
    :return:
    """
    return [x for x in dir(obj) if not x.startswith('__')]


def dataclass_with_default_init(_cls=None, *args, **kwargs):
    """
    | This class allows to define Frozen Dataclasses by bypassing the __init__.
    | It is useful when the attributes of the Dataclass are dynamically generated,
    | while still allowing the attributes of the class to be frozen after initialisation.

    :rtype: object
    """
    def wrap(cls):
        # Save the current __init__ and remove it so dataclass will
        # create the default __init__.
        user_init = getattr(cls, "__init__")
        delattr(cls, "__init__")

        # let dataclass process our class.
        result = dataclass(cls, *args, **kwargs)

        # Restore the user's __init__ save the default init to __default_init__.
        setattr(result, "__default_init__", result.__init__)
        setattr(result, "__init__", user_init)

        # Just in case that dataclass will return a new instance,
        # (currently, does not happen), restore cls's __init__.
        if result is not cls:
            setattr(cls, "__init__", user_init)

        return result

    # Support both dataclass_with_default_init() and dataclass_with_default_init
    if _cls is None:
        return wrap
    else:
        return wrap(_cls)

