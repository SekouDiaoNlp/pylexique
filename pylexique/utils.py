import sys
from distutils.version import StrictVersion
import tables
from dataclasses import dataclass


def my_close_open_files(verbose):
    """

    :param verbose:
    """
    open_files = tables.file._open_files

    are_open_files = len(open_files) > 0

    if verbose and are_open_files:
        sys.stderr.write("Closing remaining open files:")

    if StrictVersion(tables.__version__) >= StrictVersion("3.1.0"):
        # make a copy of the open_files.handlers container for the iteration
        handlers = list(open_files.handlers)
    else:
        # for older versions of pytables, setup the handlers list from the
        # keys
        keys = open_files.keys()
        handlers = []
        for key in keys:
            handlers.append(open_files[key])

    for fileh in handlers:
        if verbose:
            sys.stderr.write("%s..." % fileh.filename)

        fileh.close()

        if verbose:
            sys.stderr.write("done")

    if verbose and are_open_files:
        sys.stderr.write("\n")


def dataclass_with_default_init(_cls=None, *args, **kwargs):
    """

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

