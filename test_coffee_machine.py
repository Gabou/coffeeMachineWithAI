import unittest

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
                self.assertEqual(self.machine.make_drink(drink), expected)

    def test_sugar_includes_a_stick_only_when_needed(self):
        for drink, code in (("tea", "T"), ("coffee", "C"), ("chocolate", "H")):
            for sugars, suffix in ((0, "::"), (1, ":1:0"), (2, ":2:0")):
                with self.subTest(drink=drink, sugars=sugars):
                    self.assertEqual(
                        self.machine.make_drink(drink, sugars), code + suffix
                    )

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
