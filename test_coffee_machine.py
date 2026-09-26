import unittest
from decimal import Decimal

from coffee_machine import CoffeeMachine


class CoffeeMachineTests(unittest.TestCase):
    def setUp(self):
        self.machine = CoffeeMachine()

    def test_drinks_without_sugar_have_no_stick(self):
        for drink, expected in (
            ("tea", "T::"),
            ("coffee", "C::"),
            ("chocolate", "H::"),
        ):
            with self.subTest(drink=drink):
                self.assertEqual(self.machine.make_drink(drink, money=1), expected)

    def test_sugar_includes_a_stick_only_when_needed(self):
        for drink, code in (("tea", "T"), ("coffee", "C"), ("chocolate", "H")):
            for sugars, suffix in ((0, "::"), (1, ":1:0"), (2, ":2:0")):
                with self.subTest(drink=drink, sugars=sugars):
                    self.assertEqual(
                        self.machine.make_drink(drink, sugars, money=1), code + suffix
                    )

    def test_exact_payment_makes_each_drink(self):
        for drink, price, code in (
            ("tea", 0.4, "T"),
            ("coffee", 0.6, "C"),
            ("chocolate", 0.5, "H"),
        ):
            for sugars, suffix in ((0, "::"), (1, ":1:0"), (2, ":2:0")):
                with self.subTest(drink=drink, sugars=sugars):
                    self.assertEqual(
                        self.machine.make_drink(drink, sugars, money=price),
                        code + suffix,
                    )

    def test_insufficient_payment_reports_missing_amount(self):
        for drink, price in (("tea", "0.40"), ("coffee", "0.60"), ("chocolate", "0.50")):
            for money, missing in (
                (0, price),
                (Decimal(price) - Decimal("0.01"), "0.01"),
                (0.1, f"{Decimal(price) - Decimal('0.1'):.2f}"),
            ):
                with self.subTest(drink=drink, money=money):
                    self.assertEqual(
                        self.machine.make_drink(drink, 2, money=money),
                        f"M:Missing {missing} EUR",
                    )

    def test_omitted_payment_is_zero(self):
        self.assertEqual(self.machine.make_drink("tea"), "M:Missing 0.40 EUR")

    def test_orange_juice_payment(self):
        for money, expected in (
            (0, "M:Missing 0.60 EUR"),
            (0.5, "M:Missing 0.10 EUR"),
            (Decimal("0.59"), "M:Missing 0.01 EUR"),
            (0.6, "O::"),
            (1, "O::"),
        ):
            with self.subTest(money=money):
                self.assertEqual(
                    self.machine.make_drink("orange juice", money=money), expected
                )

    def test_extra_hot_drinks_keep_prices_and_sugar_protocol(self):
        for drink, price, code in (
            ("coffee", Decimal("0.60"), "Ch"),
            ("chocolate", Decimal("0.50"), "Hh"),
            ("tea", Decimal("0.40"), "Th"),
        ):
            for sugars, suffix in ((0, "::"), (1, ":1:0"), (2, ":2:0")):
                for money in (price, 1):
                    with self.subTest(drink=drink, sugars=sugars, money=money):
                        self.assertEqual(
                            self.machine.make_drink(drink, sugars, money, extra_hot=True),
                            code + suffix,
                        )
                with self.subTest(drink=drink, sugars=sugars, payment="insufficient"):
                    self.assertEqual(
                        self.machine.make_drink(
                            drink, sugars, price - Decimal("0.01"), extra_hot=True
                        ),
                        "M:Missing 0.01 EUR",
                    )

    def test_orange_juice_rejects_sugar_and_extra_heat(self):
        for sugars, extra_hot in ((1, False), (2, False), (0, True), (1, True)):
            with self.subTest(sugars=sugars, extra_hot=extra_hot):
                with self.assertRaises(ValueError):
                    self.machine.make_drink("orange juice", sugars, 1, extra_hot)

    def test_extra_hot_requires_a_boolean(self):
        for extra_hot in (0, 1, "true", None):
            with self.subTest(extra_hot=extra_hot):
                with self.assertRaises(ValueError):
                    self.machine.make_drink("coffee", money=1, extra_hot=extra_hot)

    def test_invalid_payment_is_rejected(self):
        for money in (-1, True, None, "0.60", float("nan"), float("inf"), 0.001):
            with self.subTest(money=money):
                with self.assertRaises(ValueError):
                    self.machine.make_drink("coffee", money=money)

    def test_messages_preserve_the_content(self):
        for content in ("Please collect your drink", "", "Info: café prêt !"):
            with self.subTest(content=content):
                self.assertEqual(self.machine.message(content), "M:" + content)

    def test_unknown_drink_is_rejected(self):
        with self.assertRaises(ValueError):
            self.machine.make_drink("juice")

    def test_invalid_sugar_amount_is_rejected(self):
        for sugars in (-1, 3, 1.5, "1", None, True):
            with self.subTest(sugars=sugars):
                with self.assertRaises(ValueError):
                    self.machine.make_drink("coffee", sugars)


if __name__ == "__main__":
    unittest.main()
