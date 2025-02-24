
def inner1(**kwargs):
    """
    Inner function 1.
    """
    kwargs.pop('key1', None)
    print(kwargs)
    return kwargs

def inner2(**kwargs):
    """
    Inner function 2.
    """
    print(kwargs)

def main(**kwargs):
    """
    Main function to run the script.
    """
    # Call inner functions with kwargs
    kwargs = inner1(**kwargs)
    inner2(**kwargs)

values = {'key1': 'value1', 'key2': 'value2'}
main(**values)