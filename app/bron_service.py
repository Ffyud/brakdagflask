from bron_model import BronModel

class BronService:
    def __init__(self):
        self.model = BronModel()
        
    def create(self, params):
        return self.model.create(params)

    def selectAll(self):
        return self.model.selectAll() 