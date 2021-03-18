class Fragment:
    """The class describes the essence of the fragments that make up the demands entered the system."""
    __COUNT = 0

    def __init__(self, parent_id: int) -> None:
        """

        @param parent_id: demand id
        """
        self.id = Fragment.__COUNT
        self.parent_id = parent_id

        Fragment.__COUNT += 1

    @staticmethod
    def _reset_counter():
        Fragment.__COUNT = 0

    def __str__(self) -> str:
        return 'Demand parent id: ' + str(self.parent_id) + ". Fragment id: " + str(self.id)
