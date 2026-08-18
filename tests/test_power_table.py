import hashlib
import json
import unittest

from power_table import POWER_TABLE


EXPECTED_TABLE_HASH = (
    "e773a82cc98ef1bd5ba86d3e5c61c444"
    "685ebb96f50034e6914605423fa09ddf"
)


class TestPowerTable(unittest.TestCase):

    def test_available_powers(self):
        self.assertEqual(
            sorted(POWER_TABLE.keys()),
            list(range(51)),
        )

    def test_each_row_has_11_entries(self):
        for power, row in POWER_TABLE.items():
            with self.subTest(power=power):
                self.assertEqual(len(row), 11)

    def test_roll_2_is_fumble_slot(self):
        for power, row in POWER_TABLE.items():
            with self.subTest(power=power):
                self.assertIsNone(row[0])

    def test_known_values(self):
        # 出目の添字:
        # 2 -> 0
        # 3 -> 1
        # ...
        # 12 -> 10

        self.assertEqual(
            POWER_TABLE[0],
            [None, 0, 0, 0, 1, 2, 2, 3, 3, 4, 4],
        )

        self.assertEqual(
            POWER_TABLE[25],
            [None, 2, 3, 4, 5, 6, 7, 8, 8, 9, 10],
        )

        self.assertEqual(
            POWER_TABLE[50],
            [None, 4, 6, 8, 10, 10, 12, 12, 13, 15, 15],
        )

    def test_entire_table_hash(self):
        table_data = [
            POWER_TABLE[power]
            for power in range(51)
        ]

        encoded = json.dumps(
            table_data,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

        actual_hash = hashlib.sha256(encoded).hexdigest()

        self.assertEqual(
            actual_hash,
            EXPECTED_TABLE_HASH,
        )


if __name__ == "__main__":
    unittest.main()
