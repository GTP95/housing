class AlreadyReacted:
    def __init__(self):
        try:
            self.already_visited_file = open("already_visited.txt", "r+")
        except FileNotFoundError:
            self.already_visited_file = open("already_visited.txt", "w+")
        finally:
            self.already_visited_list = self.already_visited_file.read().splitlines()

    def get_list(self):
        """returns the list of URLs we already sent emails for"""
        return self.already_visited_list

    def addlisting(self, url):
        """Adds a URL to the list of reactions"""
        self.already_visited_file.write(
            url + '\n')  # a sensible thing to do could be to just write everything back in the close method, but I'm not doing it now to prevent an exception from messing with the file update
        self.already_visited_list.append(url)

    def close(self):
        """Close the underlying file"""
        self.already_visited_file.close()
