class bronService:
    def __init__(self):
        self.model = bronModel()
        
    def create(self, params):
        self.model.create(params["name"], params["link"])