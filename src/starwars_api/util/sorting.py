from typing import List, Optional

from starwars_api.enums.order_enum import Order


class DataSorter:

    @staticmethod
    def sort(data: List[dict], sort_by: Optional[str] = None, order: Order = Order.ASC) -> List[dict]:
        if not sort_by:
            return data
        
        reverse_order = (order == Order.DESC)
        return sorted(data, key=lambda item: str(item.get(sort_by, '')), reverse=reverse_order)