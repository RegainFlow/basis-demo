from typing import Literal

ExpenseCategory = Literal[
    "Software",
    "Meals",
    "Travel",
    "Office Supplies",
    "Professional Services",
    "Uncategorized",
]

_CATEGORY_KEYWORDS: tuple[tuple[ExpenseCategory, tuple[str, ...]], ...] = (
    ("Software", ("software", "saas", "subscription", "license")),
    ("Meals", ("meal", "lunch", "dinner", "catering", "coffee")),
    ("Travel", ("flight", "hotel", "lodging", "taxi", "rideshare", "mileage")),
    ("Office Supplies", ("paper", "printer", "notebook", "pen", "desk")),
    ("Professional Services", ("consulting", "legal", "audit", "bookkeeping")),
)


def categorize_expense(description: str) -> ExpenseCategory:
    normalized = description.casefold()
    for category, keywords in _CATEGORY_KEYWORDS:
        if any(keyword in normalized for keyword in keywords):
            return category
    return "Uncategorized"
