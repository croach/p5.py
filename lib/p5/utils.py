"""A set of global helper functions.
"""

def processing_func_name(func_name):
    """Converts a python function name into its equivalent Processing name.
    """
    func_name = func_name.split('_')
    return ''.join(func_name[:1] + [s.capitalize() for s in func_name[1:]])
