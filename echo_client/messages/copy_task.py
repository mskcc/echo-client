import uuid


class CopyTask(object):

    def __init__(self, source, destination, id=uuid.uuid4()):
        self.id = id
        self.source = source
        self.destination = destination

    @classmethod
    def from_json(cls, obj):
        obj.pop("type")
        return cls(**obj)

    def to_json(self):
        return {
            "id": str(self.id),
            "type": "COPY",
            "source": self.source,
            "destination": self.destination
        }

    def __str__(self):
        return f"{self.id}: COPY {self.source} -> {self.destination}"
