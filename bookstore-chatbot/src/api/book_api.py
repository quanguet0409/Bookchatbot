import requests
import time
from typing import List, Dict, Optional

class BookAPI:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
        self.api_key = "AIzaSyDCtNN2okTUP2dUSXBKw4bUqBaeTDNXM0E"
        self.timeout = 5
        
    def get_book_details(self, book_id: str) -> Optional[Dict]:
        # Normalize book ID case for comparison
        book_id_lower = book_id.lower()
        
        # First check if it's in our current search results cache
        if hasattr(self, '_last_search_results'):
            for book in self._last_search_results:
                if book.get('book_id', '').lower() == book_id_lower:
                    return book
        
        try:
            # Use original case for API call
            url = f"{self.base_url}/{book_id}"
            params = {'key': self.api_key}
            
            response = requests.get(
                url, 
                params=params,
                timeout=3,
                headers={'User-Agent': 'BookStore-Chatbot/1.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_book_details(data)
                
        except Exception as e:
            print(f"⚠️ Error getting book details: {e}")
            
        return None

    def search_books(self, query: str, max_results: int = 10) -> List[Dict]:
        try:
            params = {
                'q': query if query.strip() else 'bestsellers',
                'maxResults': min(max_results, 40),
                'langRestrict': 'vi',
                'printType': 'books',
                'key': self.api_key,
                'orderBy': 'relevance'
            }
            
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeout,
                headers={'User-Agent': 'BookStore-Chatbot/1.0'}
            )
            
            if response.status_code == 200:
                data = response.json()
                api_books = self._parse_google_books_response(data)
                
                # Cache the results for get_book_details
                self._last_search_results = api_books
                
                return api_books[:max_results]
            elif response.status_code == 403:
                return [{'error': 'API quota exceeded', 'message': 'API đã hết quota, vui lòng thử lại sau'}]
            else:
                return [{'error': f'API error {response.status_code}', 'message': 'Không thể kết nối API'}]
            
        except Exception as e:
            return [{'error': str(e), 'message': 'Lỗi kết nối mạng'}]

    def _parse_google_books_response(self, data: Dict) -> List[Dict]:
        books = []
        
        if 'items' not in data:
            return books
            
        for item in data['items']:
            volume_info = item.get('volumeInfo', {})
            sale_info = item.get('saleInfo', {})
            
            price = 150000 + (abs(hash(item.get('id', ''))) % 300000)
            
            if sale_info.get('saleability') == 'FOR_SALE':
                retail_price = sale_info.get('retailPrice', {})
                if retail_price:
                    api_price = retail_price.get('amount', 0)
                    if retail_price.get('currencyCode') == 'USD':
                        price = int(api_price * 24000)
                    else:
                        price = int(api_price)
            
            # Use the actual Google Books ID
            book_id = item.get('id', '')
            
            book = {
                'book_id': book_id,  # Keep original Google Books ID
                'title': volume_info.get('title', 'Không có tên'),
                'authors': ', '.join(volume_info.get('authors', ['Tác giả không rõ'])),
                'publisher': volume_info.get('publisher', 'NXB không rõ'),
                'published_date': volume_info.get('publishedDate', ''),
                'description': (volume_info.get('description', 'Không có mô tả')[:200] + '...'),
                'page_count': volume_info.get('pageCount', 0),
                'categories': ', '.join(volume_info.get('categories', ['Chưa phân loại'])),
                'language': volume_info.get('language', 'vi'),
                'price': price,
                'currency': 'VND',
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                'availability': 'available',
                'stock': 10 + (abs(hash(book_id)) % 20),
                'rating': round(3.5 + (abs(hash(book_id)) % 150) / 100, 1)
            }
            books.append(book)
            
        return books

    def _parse_book_details(self, data: Dict) -> Dict:
        volume_info = data.get('volumeInfo', {})
        sale_info = data.get('saleInfo', {})
        
        price = 150000 + (abs(hash(data.get('id', ''))) % 300000)
        if sale_info.get('saleability') == 'FOR_SALE':
            retail_price = sale_info.get('retailPrice', {})
            if retail_price:
                api_price = retail_price.get('amount', 0)
                if retail_price.get('currencyCode') == 'USD':
                    price = int(api_price * 24000)
        
        # Use actual Google Books ID
        book_id = data.get('id', '')
        
        return {
            'book_id': book_id,  # Keep original Google Books ID
            'title': volume_info.get('title', 'Không có tên'),
            'authors': ', '.join(volume_info.get('authors', ['Tác giả không rõ'])),
            'publisher': volume_info.get('publisher', 'NXB không rõ'),
            'published_date': volume_info.get('publishedDate', ''),
            'description': volume_info.get('description', 'Không có mô tả'),
            'page_count': volume_info.get('pageCount', 0),
            'categories': ', '.join(volume_info.get('categories', ['Chưa phân loại'])),
            'language': volume_info.get('language', 'vi'),
            'price': price,
            'currency': 'VND',
            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'availability': 'available',
            'stock': 10 + (abs(hash(book_id)) % 20),
            'rating': round(3.5 + (abs(hash(book_id)) % 150) / 100, 1)
        }

class OrderAPI:
    def __init__(self):
        self.orders = []
        self.order_counter = 1
    
    def create_order(self, order_data: Dict) -> Dict:
        try:
            order = {
                'order_id': f"ORD{self.order_counter:06d}",
                'customer_name': order_data['customer_name'],
                'phone': order_data['phone'],
                'email': order_data.get('email', ''),
                'address': order_data['address'],
                'book_id': order_data['book_id'],
                'book_title': order_data['book_title'],
                'quantity': order_data['quantity'],
                'unit_price': order_data['unit_price'],
                'total_price': order_data['unit_price'] * order_data['quantity'],
                'status': 'Đã xác nhận',
                'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'estimated_delivery': self._calculate_delivery_date()
            }
            
            self.orders.append(order)
            self.order_counter += 1
            
            return {'success': True, 'order': order}
            
        except Exception as e:
            return {'success': False, 'message': f'Lỗi tạo đơn hàng: {str(e)}'}
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        for order in self.orders:
            if order['order_id'] == order_id:
                return order
        return None
    
    def _calculate_delivery_date(self) -> str:
        import datetime
        delivery_date = datetime.datetime.now() + datetime.timedelta(days=3)
        return delivery_date.strftime('%d/%m/%Y')
