def singleton(cls_):
    """单例类装饰器"""

    class wrap_cls(cls_):
        __instance = None

        def __new__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = super().__new__(cls, *args, **kwargs)
                cls.__instance.__init = False
            return cls.__instance

        def __init__(self, *args, **kwargs):
            if self.__init:
                return
            super().__init__(*args, **kwargs)
            self.__init = True

    wrap_cls.__name__ = cls_.__name__
    wrap_cls.__doc__ = cls_.__doc__
    wrap_cls.__qualname__ = cls_.__qualname__
    return wrap_cls
