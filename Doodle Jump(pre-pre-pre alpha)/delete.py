from MODULES import *


# delete list of trackers
def delete_trackers(trackers, errors_log):
    try:
        for o in trackers:
            del o.rect
            del o.text_func
            del o.param
            del o.text
            o.rect = None
            o.text_func = None
            o.param = 0
            o.text = None
            del o
    except AttributeError:
        errors_log[AttributeError] += "delete.py: delete_trackers(): try:...\n"
    except BaseException:
        raise RuntimeError("UNKNOWN UNHANDLED ERROR: delete.py: delete_trackers(): try:...")


# delete jumper and his handlers
def delete_jumper(keyup_handlers, keydown_handlers, jumper, errors_log):
    try:
        keydown_handlers[pygame.K_RIGHT].remove(jumper.handle)
        keydown_handlers[pygame.K_LEFT].remove(jumper.handle)
        keyup_handlers[pygame.K_RIGHT].remove(jumper.handle)
        keyup_handlers[pygame.K_LEFT].remove(jumper.handle)
    except AttributeError:
        errors_log[AttributeError] += "delete.py: delete_jumper(): try:...\n"
    except ValueError:
        errors_log[ValueError] += "delete.py: delete_jumper(): try:...\n"
    except BaseException:
        raise RuntimeError("UNKNOWN UNHANDLED ERROR: delete.py: delete_jumper(): try:...")
    del jumper


# delete object from object's list by it's ID
def delete_object_by_id(collection, identifier):
    for o in collection:
        if identifier == o.ID:
            collection.remove(o)
            del o


# the same as delete_object_by_id BUT with "try" construction
def try_delete_object_by_id(collection, identifier):
    try:
        for o in collection:
            if identifier == o.ID:
                collection.remove(o)
                del o
    except BaseException:
        raise RuntimeError("UNKNOWN UNHANDLED ERROR: delete.py: try_delete_object_by_id(): try:...")
