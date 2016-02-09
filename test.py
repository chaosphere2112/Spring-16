import functools

def myfunc(person, msg):
     print ("Hey %s!" % person), msg

bryce_func = functools.partial(myfunc, "Bryce")
bryce_func("This is a partial function!")
