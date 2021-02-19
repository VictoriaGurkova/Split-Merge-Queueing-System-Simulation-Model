from unittest import TestCase

from network_params import Params


class TestParams(TestCase):

    def test_combined_lambda(self):
        lambda1 = 1
        lambda2 = 1.5
        params = Params(mu=0,
                        lambda1=lambda1, lambda2=lambda2,
                        servers_number=0,
                        fragments_numbers=[],
                        queues_capacities=[])

        self.assertEqual(params.combined_lambda, params.lambda1 + params.lambda2)
        self.assertEqual(params.combined_lambda, lambda1 + lambda2)
