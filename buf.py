from io import BytesIO

class BytesIOWithName(BytesIO):
    def __init__(self, buf, name=None, **kwargs):
        super().__init__(buf, **kwargs)
        self.name = name