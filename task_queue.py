# https://docs.blender.org/api/current/bpy.app.timers.html
import queue

import bpy

__execution_queue: queue.Queue = queue.Queue()


# This function can safely be called in another thread.
# The function will be executed when the timer runs the next time.
def put(function):
    __execution_queue.put(function)


def __execute_queued_functions():
    while not __execution_queue.empty():
        function = __execution_queue.get()
        function()
    return 1.0


def register():
    if not bpy.app.timers.is_registered(__execute_queued_functions):
        bpy.app.timers.register(__execute_queued_functions)


def unregister():
    if bpy.app.timers.is_registered(__execute_queued_functions):
        bpy.app.timers.unregister(__execute_queued_functions)
