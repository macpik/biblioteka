import json

class Books:
    def __init__(self):
        try:
            with open("library.json", "r") as f:
                self.library = json.load(f)
        except FileNotFoundError:
            self.library = []

    def all(self):
        return self.library
    
    def get(self, id):
        libraries = [libraries for libraries in self.all() if libraries['id'] == id]
        if libraries:
            return libraries[0]
        return []
    
    def create(self, data):
        self.library.append(data)
        self.save_all()

    def delete(self, id):
        libraries = self.get(id)
        if libraries:
            self.library.remove(libraries)
            self.save_all()
            return True
        return False
    
    def update(self, id, data):
        libraries = self.get(id)
        if libraries:
            index = self.library.index(libraries)
            self.library[index] = data
            self.save_all()
            return True
        return False
    
    def save_all(self):
        with open("library.json", "w") as f:
            json.dump(self.library, f)
    
library = Books()