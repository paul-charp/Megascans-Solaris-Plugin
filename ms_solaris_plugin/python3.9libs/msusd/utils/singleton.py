class Singleton(type):
    __instance = None
    def __call__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance
    
    def clear(cls):
        cls.__instance = None
