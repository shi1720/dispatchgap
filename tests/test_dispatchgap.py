import itertools
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from dispatchgap import Contact, temporal_masks, oracle, route, critical_gap


class ExactnessTests(unittest.TestCase):
    def test_exhaustive_three_contact_streams(self):
        nodes = ['a', 'b', 'c']
        choices = [Contact(t, a, b, str(i)) for i, (t, a, b) in
                   enumerate(itertools.product(range(3), nodes, nodes)) if a != b]
        checked = 0
        for length in range(4):
            for stream in itertools.product(choices, repeat=length):
                for gap in range(3):
                    masks = temporal_masks(stream, nodes, gap)
                    for i, source in enumerate(nodes):
                        expected = oracle(stream, source, gap)
                        got = {n for j, n in enumerate(nodes) if masks[j] & (1 << i)}
                        self.assertEqual(got, expected)
                        for target in nodes:
                            witness = route(stream, source, target, gap)
                            self.assertEqual(witness is not None, target in expected)
                            if witness:
                                self.assertEqual(witness[0].author, source)
                                self.assertEqual(witness[-1].recipient, target)
                                for e, f in zip(witness, witness[1:]):
                                    self.assertEqual(e.recipient, f.author)
                                    self.assertGreaterEqual(f.day - e.day, gap)
                        checked += 1
        print('Exhaustive origin-stream-gap checks:', checked)

    def test_terminal_leg_has_no_horizon_delay_penalty(self):
        e = [Contact(365, 'a', 'b', 'last-day')]
        self.assertEqual(temporal_masks(e, ['a', 'b'], 1000)[1], 3)
        self.assertEqual(critical_gap(e, 'a', 'b'), 'direct')

    def test_same_day_order_and_monotonicity(self):
        rng = random.Random(20406)
        nodes = list('abcd')
        for _ in range(100):
            contacts = [Contact(rng.randrange(6), *rng.sample(nodes, 2), str(i))
                        for i in range(20)]
            last = None
            for gap in range(7):
                masks = temporal_masks(contacts, nodes, gap)
                shuffled = contacts.copy(); rng.shuffle(shuffled)
                self.assertEqual(masks, temporal_masks(shuffled, nodes, gap))
                if last is not None:
                    self.assertTrue(all(new & old == new for new, old in zip(masks, last)))
                last = masks

    def test_critical_gap(self):
        e = [Contact(2, 'a', 'b', 'x'), Contact(7, 'b', 'c', 'y')]
        self.assertEqual(critical_gap(e, 'a', 'c'), 5)
        self.assertIsNone(critical_gap(e, 'c', 'a'))


if __name__ == '__main__':
    unittest.main()
