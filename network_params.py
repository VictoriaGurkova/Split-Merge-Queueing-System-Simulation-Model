from dataclasses import dataclass


@dataclass()
class Params:
    mu: float
    lambda1: float
    lambda2: float
    devices_amount: int
    fragments_amounts: list
    queues_capacities: list

    @property
    def combined_lambda(self) -> float:
        return self.lambda1 + self.lambda2
