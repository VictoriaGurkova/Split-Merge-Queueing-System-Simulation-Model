class Fragment:
    """Class describing the essence of the fragments that make up the demands in a split-merge system."""

    __COUNT = 0

    def __init__(self, parent_id: int):
        """

        :param parent_id: demand id
        """
        Fragment.__COUNT += 1
        self.id = Fragment.__COUNT
        self.parent_id = parent_id

    def __str__(self):
        return 'Demand parent id: ' + str(self.parent_id) + ". Fragment id: " + str(self.id)
