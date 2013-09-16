class PVector(object):

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z


    def add(self, *args):
        x, y, z = (args[0].x, args[0].y, args[0].z) if len(args) == 1 else args
        self.x += x
        self.y += y
        self.z += z


    def sub(self, *args):
        x, y, z = (args[0].x, args[0].y, args[0].z) if len(args) == 1 else args
        self.x -= x
        self.y -= y
        self.z -= z


    def __add__(self, v):
        v1 = self.copy()
        v1.add(v)
        return v1

    def __sub__(self, v):
        v1 = self.copy()
        v1.sub(v)
        return v1


    def copy(self):
        return PVector(self.x, self.y, self.z)


    def get(self, target=None):
        if target is None:
            return self.copy()

        if len(target) >= 2:
            target[0] = self.x
            target[1] = self.y

        if len(target) >= 3:
            target[2] = self.z

        return target

