from typing import List, Optional

from starwars_api.enums.order_enum import Order


class DataSorter:
    @staticmethod
    def sort(
        data: List[dict], sort_by: Optional[str] = None, order: Order = Order.ASC
    ) -> List[dict]:
        if not sort_by:
            return data

        reverse_order = order == Order.DESC

        def sort_key(item):
            value = item.get(sort_by, "")
            if isinstance(value, str) and value.isdigit():
                return (
                    0,
                    int(value),
                )  # Números como tupla para evitar comparação direta
            try:
                return (0, float(value))
            except (ValueError, TypeError):
                return (1, str(value))  # Strings como tupla separada

        return sorted(data, key=sort_key, reverse=reverse_order)
