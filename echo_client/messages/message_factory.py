from . import CopyTask, DeleteTask, Response


class MessageFactory(object):

    @staticmethod
    def parse(msg):
        if "message" in msg.keys():
            return Response.from_json(msg)
        elif msg.get("type") == "COPY":
            return CopyTask.from_json(msg)
        elif msg.get("type") == "DELETE":
            return DeleteTask.from_json(msg)
