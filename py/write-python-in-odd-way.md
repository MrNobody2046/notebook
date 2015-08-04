
造Class
----

    NewClass = lambda *args, **kwargs: \
        type.__new__(type("mcs", (type,), {}),"NewClass",(),
                     { "print_self": lambda ins: ins.__dict__,  "__init__":
                         lambda ins, *args, **kwargs:
                         (ins.__dict__.update(kwargs), None)[1] } )(*args, **kwargs)
                         
    print  NewClass(ss=1,aa=2).print_self()                     
----



----



----
