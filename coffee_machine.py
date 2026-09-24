class CoffeeMachine:
    """Translate customer orders into drink maker protocol commands."""

    def make_drink(self, drink: str, sugars: int = 0) -> str:
        codes = {"tea": "T", "coffee": "C", "chocolate": "H"}
        if drink not in codes:
            raise ValueError("Drink must be tea, coffee or chocolate")
        if type(sugars) is not int or sugars not in (0, 1, 2):
            raise ValueError("Sugars must be an integer between 0 and 2")
        code = codes[drink]
        return f"{code}:{sugars}:0" if sugars else f"{code}::"

    def message(self, content: str) -> str:
        return "M:" + content
