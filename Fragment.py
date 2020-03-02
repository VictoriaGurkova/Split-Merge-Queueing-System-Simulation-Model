class Fragment:
    count = 0

    def __init__(self, parent_id):
        Fragment.count += 1
        self.id = Fragment.count
        self.parent_id = parent_id

    def __str__(self):
        return 'Parent id: ' + str(self.parent_id) + ". Fragment id: " + str(self.id)
