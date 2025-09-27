from models.bookstore import BookStore
from chatbot.responses import ChatBotResponses
import re

class ChatBot:
    def __init__(self):
        self.bookstore = BookStore()
        self.responses = ChatBotResponses()
        self.current_state = "normal"
        self.order_data = {}
    
    def process_message(self, message: str) -> str:
        try:
            message = message.strip().lower()
            
            if self.current_state == "ordering":
                return self._process_order_flow(message)
            
            if self._is_greeting(message):
                return self.responses.greeting_response()
            elif self._is_search_query(message):
                return self._handle_search(message)
            elif self._is_order_query(message):
                return self._handle_order_start(message)
            elif self._is_order_status_query(message):
                return self._handle_order_status(message)
            elif self._is_help_query(message):
                return self.responses.help_response()
            else:
                return self.responses.default_response()
                
        except Exception as e:
            return f"❌ Lỗi xử lý: {str(e)}. Vui lòng thử lại!"
    
    def _is_greeting(self, message):
        greetings = ["xin chào", "chào", "hello", "hi"]
        return any(g in message for g in greetings)
    
    def _is_search_query(self, message):
        keywords = ["tìm", "search", "sách", "book"]
        return any(k in message for k in keywords)
    
    def _is_order_query(self, message):
        keywords = ["mua", "đặt", "order", "buy"]
        return any(k in message for k in keywords)
    
    def _is_order_status_query(self, message):
        keywords = ["đơn hàng", "order", "trạng thái", "kiểm tra đơn", "check order"]
        return any(k in message for k in keywords)
    
    def _is_help_query(self, message):
        keywords = ["help", "giúp", "hướng dẫn"]
        return any(k in message for k in keywords)
    
    def _handle_search(self, message):
        query = self._extract_search_query(message)
        books = self.bookstore.search_books(query)
        return self.responses.search_books_response(query, books)
    
    def _extract_search_query(self, message):
        words = ["tìm", "search", "sách", "book"]
        for word in words:
            if word in message:
                parts = message.split(word, 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return message
    
    def _handle_order_start(self, message):
        if "mua " in message:
            parts = message.split("mua", 1)
            if len(parts) > 1:
                book_id = parts[1].strip()
                
                # Debug: show what we're looking for
                print(f"Looking for book ID: '{book_id}'")
                
                # Try to get book details
                book = self.bookstore.get_book_by_id(book_id)
                if book:
                    self.current_state = "ordering"
                    self.order_data = {"step": "quantity", "book": book}
                    return f"""🛒 **MUA NHANH THEO MÃ SÁCH** 

📚 Bạn đã chọn: **{book['title']}**
👤 Tác giả: {book['authors']}
🏢 NXB: {book['publisher']}
💰 Giá: {book['price']:,}đ
⭐ Đánh giá: {book['rating']}/5 ⭐
📦 Còn lại: {book['stock']} cuốn
🆔 Mã sách: {book['book_id']}

🔢 **Số lượng bạn muốn mua?**
(Nhập số lượng, ví dụ: 1, 2, 3...)"""
                else:
                    return f"""❌ **Không tìm thấy sách với mã: {book_id}**

🔍 **Đang tìm kiếm tương tự...**

💡 **Có thể do:**
• Mã sách sai format (chữ hoa/thường)
• Sách không có trong Google Books API
• Lỗi kết nối tạm thời

🛠️ **Thử lại:**
• Copy chính xác mã từ danh mục
• Tìm kiếm bằng tên sách thay thế
• Mở lại **Danh mục sách**"""

        self.current_state = "ordering"
        self.order_data = {"step": "book_selection"}
        return "🛒 Bạn muốn mua sách gì? Vui lòng cho tôi biết tên sách hoặc mã sách."

    def _handle_order_status(self, message):
        order_match = re.search(r'ORD\d+', message.upper())
        if order_match:
            order_id = order_match.group()
            order = self.bookstore.get_order_info(order_id)
            return self.responses.order_status_response(order)
        else:
            # Extract any potential order ID from message
            words = message.split()
            for word in words:
                if len(word) >= 6 and (word.startswith('ord') or word.isdigit()):
                    order = self.bookstore.get_order_info(word.upper())
                    if order:
                        return self.responses.order_status_response(order)
            
            return """❓ **Cần mã đơn hàng để kiểm tra**

Vui lòng cung cấp mã đơn hàng để kiểm tra trạng thái.

💡 **Các cách kiểm tra:**
• "kiểm tra đơn hàng ORD000001"
• "đơn hàng ORD000001"
• Dùng ô "Kiểm tra đơn hàng" ở trên

📧 Mã đơn hàng được gửi qua email sau khi đặt hàng thành công."""
    
    def _process_order_flow(self, message):
        step = self.order_data.get("step")
        
        if step == "book_selection":
            return self._process_book_selection(message)
        elif step == "quantity":
            return self._process_quantity(message)
        elif step == "customer_info":
            return self._process_customer_info(message)
        elif step == "phone":
            return self._process_phone(message)
        elif step == "address":
            return self._process_address(message)
        
        return "Có lỗi xảy ra. Vui lòng thử lại."
    
    def _process_book_selection(self, message):
        try:
            if message.startswith('fb_') or len(message) > 8:
                book = self.bookstore.get_book_by_id(message)
                if book:
                    self.order_data["book"] = book
                    self.order_data["step"] = "quantity"
                    return f"""📚 Đã chọn: **{book['title']}**
👤 Tác giả: {book['authors']}
💰 Giá: {book['price']:,}đ
📦 Còn lại: {book['stock']} cuốn

🔢 **Số lượng bạn muốn mua?**"""
            else:
                books = self.bookstore.search_books(message, 5)
                if books:
                    if len(books) == 1:
                        book = books[0]
                        self.order_data["book"] = book
                        self.order_data["step"] = "quantity"
                        return f"""📚 Đã chọn: **{book['title']}**
👤 Tác giả: {book['authors']}
💰 Giá: {book['price']:,}đ

🔢 **Số lượng bạn muốn mua?**"""
                    else:
                        response = "📚 Tìm thấy nhiều sách phù hợp:\n\n"
                        for book in books:
                            response += f"🆔 {book['book_id']} - {book['title']}\n"
                        response += "\n💬 Vui lòng nhập **mã sách** để chọn mua."
                        return response
            
            return "❌ Không tìm thấy sách. Vui lòng thử lại với tên khác."
            
        except Exception as e:
            return f"❌ Lỗi tìm sách: {str(e)}. Vui lòng thử lại!"

    def _process_quantity(self, message):
        try:
            if message.isdigit() and int(message) > 0:
                quantity = int(message)
                book = self.order_data["book"]
                stock = book.get('stock', 0)
                
                if quantity > stock:
                    return f"❌ Xin lỗi, chỉ còn {stock} cuốn. Vui lòng nhập số lượng khác."
                
                self.order_data["quantity"] = quantity
                self.order_data["step"] = "customer_info"
                price = book.get('price', 0)
                total = price * quantity
                return f"""💰 **THÔNG TIN ĐƠN HÀNG**

📚 Sách: {book['title']}
🔢 Số lượng: {quantity} cuốn
💰 Đơn giá: {price:,}đ
💵 **Tổng tiền: {total:,}đ**

👤 **Vui lòng cung cấp họ tên của bạn:**"""
            else:
                return "❌ Vui lòng nhập số lượng hợp lệ (số nguyên dương)."
                
        except Exception as e:
            return f"❌ Lỗi xử lý số lượng: {str(e)}"

    def _process_customer_info(self, message):
        self.order_data["customer_name"] = message
        self.order_data["step"] = "phone"
        return "📞 **Vui lòng cung cấp số điện thoại:**"

    def _process_phone(self, message):
        if re.match(r'^[\d\s\-\+\(\)]+$', message) and len(message.replace(' ', '')) >= 10:
            self.order_data["phone"] = message
            self.order_data["step"] = "address"
            return "🏠 **Vui lòng cung cấp địa chỉ giao hàng:**"
        else:
            return "❌ Số điện thoại không hợp lệ. Vui lòng nhập lại số điện thoại (ít nhất 10 số):"

    def _process_address(self, message):
        try:
            self.order_data["address"] = message
            
            result = self.bookstore.create_order(
                self.order_data["customer_name"],
                self.order_data["phone"],
                self.order_data["address"],
                self.order_data["book"]["book_id"],
                self.order_data["book"]["title"],
                self.order_data["quantity"],
                self.order_data["book"]["price"]
            )
            
            self.current_state = "normal"
            self.order_data = {}
            
            if result["success"]:
                return self.responses.order_success_response(result["order"])
            else:
                return f"❌ Có lỗi khi tạo đơn hàng: {result['message']}"
                
        except Exception as e:
            self.current_state = "normal"
            self.order_data = {}
            return f"❌ Có lỗi khi xử lý đơn hàng: {str(e)}. Vui lòng thử lại từ đầu!"
