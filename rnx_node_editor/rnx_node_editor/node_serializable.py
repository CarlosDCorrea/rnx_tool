class Serializable:
    def __init__(self):
        self.id = id(self)

    "These methods have to be in the children class too"
    def serialize(self):
        raise NotImplemented()

    def deserialize(self, data, dictionary=None):
        if dictionary is None:
            dictionary = {}
        raise NotImplemented()


