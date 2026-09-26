from decimal import Decimal


class CoffeeMachine:
    """Translate customer orders into drink maker protocol commands."""

    def make_drink(
        self, drink: str, sugars: int = 0, money: int | float | Decimal = 0
    ) -> str:
        """Return a drink command or a missing-payment message; money is in euros."""
        codes = {"tea": "T", "coffee": "C", "chocolate": "H"}
        if drink not in codes:
            raise ValueError("Drink must be tea, coffee or chocolate")
        if type(sugars) is not int or sugars not in (0, 1, 2):
            raise ValueError("Sugars must be an integer between 0 and 2")
        if type(money) not in (int, float, Decimal):
            raise ValueError("Money must be a non-negative amount in whole cents")
        payment = Decimal(str(money))
        if (
            not payment.is_finite()
            or payment < 0
            or payment * 100 != (payment * 100).to_integral_value()
        ):
            raise ValueError("Money must be a non-negative amount in whole cents")
        prices = {"tea": Decimal("0.40"), "coffee": Decimal("0.60"), "chocolate": Decimal("0.50")}
        missing = prices[drink] - payment
        if missing > 0:
            return self.message(f"Missing {missing:.2f} EUR")
        code = codes[drink]
        return f"{code}:{sugars}:0" if sugars else f"{code}::"

    def message(self, content: str) -> str:
        return "M:" + content
