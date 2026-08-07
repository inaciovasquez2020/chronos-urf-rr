from __future__ import annotations

from dataclasses import dataclass, field


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class Budget:
    limits: dict[str, int]
    used: dict[str, int] = field(default_factory=dict)

    def consume(self, key: str, amount: int = 1) -> int:
        if amount < 0:
            raise ValueError("amount must be nonnegative")
        new_value = self.used.get(key, 0) + amount
        limit = self.limits.get(key)
        if limit is not None and new_value > limit:
            raise BudgetExceeded(f"{key} budget exceeded: {new_value}>{limit}")
        self.used[key] = new_value
        return new_value

    def remaining(self, key: str) -> int | None:
        limit = self.limits.get(key)
        if limit is None:
            return None
        return limit - self.used.get(key, 0)
