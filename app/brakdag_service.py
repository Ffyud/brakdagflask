from brakdag_models import bronModel

class bronService:
    def __init__(self):
        self.model = bronModel()
        
    def create(self, params):
        return self.model.create(params)

    def selectAll(self):
        return self.model.selectAll()    