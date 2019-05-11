class Memory:
    def __init__(self, name):
        self.name = name
        self.variables = {}

    def __contains__(self, variable):
        return variable in self.variables

    def __str__(self):
        return self.name

    def get(self, variable):
        return self.variables[variable]

    def put(self, variable, value):
        self.variables[variable] = value


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
