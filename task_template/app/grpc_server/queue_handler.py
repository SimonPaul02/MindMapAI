import queue


class QueueHandler:
    def __init__(self):
        self.start_queue = queue.Queue()
        self.task_queue = queue.Queue()
        self.finish_queue = queue.Queue()
        self.response_queues = {}

    def add_response_queue(self, sessionID):
        if sessionID not in self.response_queues:
            self.response_queues[sessionID] = queue.Queue()

    def get_response_queue(self, sessionID) -> queue.Queue:
        if sessionID not in self.response_queues:
            self.response_queues[sessionID] = queue.Queue()
        return self.response_queues[sessionID]

    def remove_response_queue(self, sessionID):
        if sessionID in self.response_queues:
            self.response_queues.pop(sessionID)


queue_handler = QueueHandler()
