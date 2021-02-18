from unittest import TestCase

from network_params import Params


class TestParams(TestCase):

    def test_combined_lambda(self):
        lambda1 = 1
        lambda2 = 1.5
        params = Params(mu=0,
                        lambda1=lambda1, lambda2=lambda2,
                        devices_amount=0,
                        fragments_amounts=[],
                        queues_capacities=[])

        self.assertEqual(params.combined_lambda, params.lambda1 + params.lambda2)
        self.assertEqual(params.combined_lambda, lambda1 + lambda2)
