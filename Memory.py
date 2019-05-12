class Memory:
    def __init__(self, segmentName):
        self.segmentName = segmentName
        self.variables = {}

    def __contains__(self, item):
        return item in self.variables

    def __str__(self):
        return self.segmentName

    def get(self, name):
        return self.variables[name]

    def put(self, name, value):
        self.variables[name] = value


class MemoryStack:
    def __init__(self, memory=None):
        self.stack = []
        if memory is not None:
            self.stack.append(memory)
        else:
            self.stack.append(Memory("Global Memory"))

    def get(self, name):
        for memory in self.stack:
            if name in memory:
                return memory.get(name)
        return None

    def insert(self, name, value):
        self.stack[0].put(name, value)

    def set(self, name, value):
        for memory in self.stack:
            if name in memory:
                memory.put(name, value)
                return

    def push(self, memory):
        self.stack.insert(0, memory)

    def pop(self):
        return self.stack.pop()
