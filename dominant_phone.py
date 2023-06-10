class Phone:
    """
    Phone class represents a phone with attributes such as name, cost, RAM, and processor.
    """

    name = ""
    cost = 0
    ram = 0
    processor = 0

    def __init__(self, name, cost, ram, processor) -> None:
        """
        Initializes a Phone object with the specified attributes.

        Args:
            name (str): The name of the phone.
            cost (int): The cost of the phone.
            ram (int): The RAM of the phone.
            processor (int): The processor of the phone.
        """
        self.cost = cost
        self.ram = ram
        self.processor = processor
        self.name = name


def _is_better(phone, other) -> bool:
    """
    Determines if the given phone is better than the other phone based on cost, RAM, and processor.

    Args:
        phone (Phone): The phone to compare.
        other (Phone): The other phone to compare.

    Returns:
        bool: True if the phone is better than the other phone, False otherwise.
    """
    if (
        phone.cost > other.cost
        or phone.ram < other.ram
        or phone.processor < other.processor
    ):
        return False

    if (
        phone.cost == other.cost
        and phone.ram == other.ram
        and phone.processor == other.processor
    ):
        return False
    return True


def get_dominant_phones(phones) -> list[Phone]:
    """
    Finds the dominant phones from the given list based on cost, RAM, and processor.

    Args:
        phones (list[Phone]): The list of phones to check.

    Returns:
        list[Phone]: The list of dominant phones.
    """
    phones_count: int = len(phones)
    is_dominant: list[int] = [True] * phones_count

    for i in range(phones_count):
        for j in range(phones_count):
            if i != j and _is_better(phones[i], phones[j]):
                is_dominant[j] = False

    dominant_phones: list[int] = [
        phones[i] for i in range(phones_count) if is_dominant[i]
    ]
    return dominant_phones
