from item_model import ItemModel

class ItemService:
    def __init__(self):
        self.model = ItemModel()
        
    def create(self, params):
        return self.model.create(params)

    def selectAll(self):
        return self.model.selectAll()

    def selectByDay(self, param):
        return self.model.selectByDay(param)

    def selectBySource(self, param):
        return self.model.selectBySource(param)

    def selectStatistics(self):
        return self.model.selectStatistics()

    def selectByUitgelicht(self):
        return self.model.selectByUitgelicht()

    def selectBySearch(self, param):
        return self.model.selectBySearch(param)