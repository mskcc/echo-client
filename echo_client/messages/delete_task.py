import uuid


class DeleteTask(object):

    def __init__(self, source, id=uuid.uuid4()):
        self.id = id
        self.source = source

    @classmethod
    def from_json(cls, obj):
        obj.pop("type")
        return cls(**obj)

    def to_json(self):
        return {
            "id": str(self.id),
            "type": "DELETE",
            "source": self.source
        }

    def __str__(self):
        return f"{self.id}: DELETE {self.source}"
