
class C:
    def method(self, x, y=2, *args, **kwargs):
        return x + y

def foo(a, b, c=3):
    return a*b*c

foo(1)
foo(1,2,3,4)
C().method(1)
C().method(1,2,3, z=5)
