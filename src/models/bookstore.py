from typing import List, Dict, Optional
from api.book_api import BookAPI, OrderAPI

class BookStore:
    def __init__(self):
        self.book_api = BookAPI()
        self.order_api = OrderAPI()
    
    def search_books(self, query: str, max_results: int = 10) -> List[Dict]:
        return self.book_api.search_books(query, max_results)
    
    def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        return self.book_api.get_book_details(book_id)
    
    def create_order(self, customer_name: str, phone: str, address: str, 
                    book_id: str, book_title: str, quantity: int, unit_price: float,
                    email: str = "") -> Dict:
        order_data = {
            'customer_name': customer_name,
            'phone': phone,
            'email': email,
            'address': address,
            'book_id': book_id,
            'book_title': book_title,
            'quantity': quantity,
            'unit_price': unit_price
        }
        return self.order_api.create_order(order_data)
    
    def get_order_info(self, order_id: str) -> Optional[Dict]:
        return self.order_api.get_order(order_id)