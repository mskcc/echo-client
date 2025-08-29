class Response(object):

    def __init__(self, id, status, message):
        self.id = id
        self.status = status
        self.message = message

    @classmethod
    def from_json(cls, obj):
        return cls(**obj)

    def to_json(self):
        return {
            "id": str(self.id),
            "status": self.status,
            "message": self.message
        }

    def __str__(self):
        return f"{self.id}: {self.status} {self.message}"
