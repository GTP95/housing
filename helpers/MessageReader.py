import random

class MessageReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.messages = self._read_messages()

    def _read_messages(self):
        """Reads messages from a file and returns a list of messages"""
        with open(self.file_path, 'r') as file:
            content = file.read()
        messages = content.split('---')
        return [message.strip() for message in messages if message.strip()]

    def get_random_message(self):
        """Returns a random message"""
        return random.choice(self.messages)

# Example usage:
# reader = MessageReader('Resources/messages_hendriks.txt')
# messages = reader.read_messages()
# for message in messages:
#     print(message)