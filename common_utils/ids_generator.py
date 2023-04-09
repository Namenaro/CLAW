class IdsGenerator:
    def __init__(self):
        self.id = -1

    def generate_id(self):
        self.id += 1
        return self.id