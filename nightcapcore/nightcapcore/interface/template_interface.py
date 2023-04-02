
# region Imports

# endregion

# regin Abstract Function Definition
def abstractfunc(func):
    func.__isabstract__ = True
    return func


# endregion


class Interface(type):
    """

    This class is used as a template interface using ABC

    """

    def __init__(self, name, bases, namespace) -> None:
        for base in bases:
            must_implement = getattr(base, "abstract_methods", [])
            class_methods = getattr(self, "all_methods", [])
            for method in must_implement:
                if method not in class_methods:
                    err_str = """Can't create abstract class {name}!
                    {name} must implement abstract method {method} of class {base_class}!""".format(
                        name=name, method=method, base_class=base.__name__
                    )
                    raise TypeError(err_str)

    def __new__(metaclass, name, bases, namespace):
        namespace["abstract_methods"] = Interface._get_abstract_methods(namespace)
        namespace["all_methods"] = Interface._get_all_methods(namespace)
        cls = super().__new__(metaclass, name, bases, namespace)
        return cls

    def _get_abstract_methods(namespace):
        return [
            name
            for name, val in namespace.items()
            if callable(val) and getattr(val, "__isabstract__", False)
        ]

    def _get_all_methods(namespace):
        return [name for name, val in namespace.items() if callable(val)]
