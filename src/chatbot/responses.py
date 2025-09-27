from typing import List, Dict, Optional

class ChatBotResponses:
    def __init__(self):
        self.language = 'vi'
    
    def set_language(self, language):
        """Set response language"""
        self.language = language

    def get_text(self, key, **kwargs):
        """Multi-language text getter"""
        texts = {
            'vi': {
                'welcome': """🌟 Chào mừng bạn đến với BookStore! 🌟

Tôi có thể giúp bạn:
📚 Tìm kiếm sách
🛒 Đặt mua sách  
📋 Kiểm tra đơn hàng
❓ Hỗ trợ và tư vấn

Bạn cần tôi hỗ trợ gì?""",
                'no_books_found': f"❌ Không tìm thấy sách với từ khóa '{kwargs.get('query', '')}'\n\n💡 Thử từ khóa khác hoặc mở Danh mục sách",
                'books_found': f"🔍 Tìm thấy **{kwargs.get('count', 0)}** sách với '{kwargs.get('query', '')}':\n\n",
                'order_success': """✅ **ĐẶT HÀNG THÀNH CÔNG!** ✅

🎉 Cảm ơn bạn đã tin tưởng BookStore!

📋 **THÔNG TIN ĐƠN HÀNG**
🆔 Mã đơn hàng: **{order.get('order_id', 'N/A')}**
📅 Ngày đặt: {order.get('created_at', 'N/A')}
👤 Khách hàng: {order.get('customer_name', 'N/A')}
📞 SĐT: {order.get('phone', 'N/A')}
🏠 Địa chỉ: {order.get('address', 'N/A')}

📚 **CHI TIẾT SẢN PHẨM**
📖 Tên sách: {order.get('book_title', 'N/A')}
🔢 Số lượng: {order.get('quantity', 0)} cuốn
💰 Đơn giá: {order.get('unit_price', 0):,}đ
💵 **Tổng tiền: {order.get('total_price', 0):,}đ**

📦 **THÔNG TIN GIAO HÀNG**
📋 Trạng thái: {order.get('status', 'N/A')}
🚚 Dự kiến giao: {order.get('estimated_delivery', 'N/A')}
⏰ Thời gian giao: 9:00 - 18:00 (T2-T7)

💳 **THANH TOÁN**
💰 Thanh toán khi nhận hàng (COD)
🏦 Hoặc chuyển khoản: MB Bank - 123456789

📞 **HỖ TRỢ 24/7**
📱 Hotline: 1900-xxxx
📧 Email: support@bookstore.com
💬 Chat: Dùng ô "Kiểm tra đơn hàng" để theo dõi

🙏 Cảm ơn bạn đã mua sắm tại BookStore! 🌟""",
                'order_status': """📋 **THÔNG TIN ĐƠN HÀNG**

🆔 Mã: {order['order_id']}
👤 Khách hàng: {order['customer_name']}
📚 Sách: {order['book_title']}
💵 Tổng tiền: {order['total_price']:,}đ
📋 **Trạng thái: {order['status']}**
🚚 Dự kiến giao: {order['estimated_delivery']}""",
                'help': """🆘 **HƯỚNG DẪN SỬ DỤNG**

🔍 **Tìm kiếm:**
• "tìm [từ khóa]"
• "sách về [chủ đề]"

🛒 **Đặt mua:**
• "mua [tên sách]"
• "mua [mã sách]"
• Dùng ô "Mua nhanh"

📋 **Đơn hàng:**
• "đơn hàng [mã]"

💡 **Tính năng:**
• Click phải để copy
• Danh mục sách đầy đủ
• Mua nhanh theo mã

📞 **Hỗ trợ:** 1900-xxxx""",
                'default': """❓ Xin lỗi, tôi không hiểu yêu cầu của bạn.

💡 **GỢI Ý SỬ DỤNG:**
• **"tìm [tên sách]"** để tìm kiếm sách
• **"mua [tên sách]"** để đặt mua sách
• **"kiểm tra đơn [mã]"** để xem đơn hàng
• **"giúp"** để xem hướng dẫn chi tiết

🔍 **VÍ DỤ CỤ THỂ:**
• "tìm sách lập trình"
• "mua Đắc Nhân Tâm" 
• "kiểm tra đơn hàng ORD000001"

🤖 Tôi luôn sẵn sàng hỗ trợ bạn!""",
            },
            'en': {
                'welcome': """🌟 Welcome to BookStore! 🌟

I can help you with:
📚 Search books
🛒 Purchase books  
📋 Check orders
❓ Support and advice

How can I assist you?""",
                'no_books_found': f"❌ No books found with keyword '{kwargs.get('query', '')}'\n\n💡 Try different keywords or open Book Catalog",
                'books_found': f"🔍 Found **{kwargs.get('count', 0)}** books with '{kwargs.get('query', '')}':\n\n",
                'order_success': """✅ **ORDER PLACED SUCCESSFULLY!** ✅

🆔 Order ID: {order['order_id']}
👤 Customer: {order['customer_name']}
📞 Phone: {order['phone']}
📍 Address: {order['address']}

📚 **Details:**
📖 Book: {order['book_title']}
🔢 Quantity: {order['quantity']} pcs
💵 **Total: {order['total_price']:,}đ**

📋 Status: {order['status']}
🚚 Estimated delivery: {order['estimated_delivery']}

Thank you for shopping at BookStore! 🌟""",
                'order_status': """📋 **ORDER INFORMATION**

🆔 ID: {order['order_id']}
👤 Customer: {order['customer_name']}
📚 Book: {order['book_title']}
💵 Total: {order['total_price']:,}đ
📋 **Status: {order['status']}**
🚚 Estimated delivery: {order['estimated_delivery']}""",
                'help': """🆘 **HOW TO USE**

🔍 **Search:**
• "find [keyword]"
• "book about [topic]"

🛒 **Purchase:**
• "buy [book name]"
• "buy [book id]"
• Use "Quick Buy" box

📋 **Order:**
• "order [id]"

💡 **Features:**
• Right-click to copy
• Full book catalog
• Quick buy by code

📞 **Support:** 1900-xxxx""",
                'default': """❓ Sorry, I don't understand your request.

💡 **Suggestions:**
• "find [book name]" to search
• "buy [book name]" to purchase  
• "help" to see instructions
• Open "Book Catalog" to browse

🤖 I'm always ready to assist!""",
            }
        }
        return texts[self.language].get(key, key)

    def greeting_response(self) -> str:
        return self.get_text('welcome')
    
    def search_books_response(self, query: str, books: List[Dict]) -> str:
        if not books:
            return self.get_text('no_books_found', query=query)
        
        # Check for error responses
        if len(books) == 1 and 'error' in books[0]:
            return f"""⚠️ **Lỗi API Google Books**

{books[0]['message']}

💡 **Thử lại:**
• Kiểm tra kết nối internet
• Thử từ khóa khác
• Liên hệ hỗ trợ nếu lỗi kéo dài

📞 Hotline: 1900-xxxx"""
        
        response = self.get_text('books_found', query=query, count=len(books))
        
        for i, book in enumerate(books, 1):
            stock_status = f"✅ Còn {book['stock']}" if book['stock'] > 0 else "❌ Hết hàng"
            
            response += f"""📚 **{i}. {book['title']}**
👤 Tác giả: {book['authors']}
🏢 NXB: {book['publisher']}
💰 Giá: {book['price']:,}đ
⭐ Đánh giá: {book['rating']}/5
📦 Tình trạng: {stock_status}
🆔 Mã sách: {book['book_id']}

{'─' * 40}
"""
        
        response += f"\n💡 **Để mua:** `mua {books[0]['book_id']}` hoặc dùng ô Mua nhanh"
        return response
    
    def order_success_response(self, order: Dict) -> str:
        return f"""✅ **ĐẶT HÀNG THÀNH CÔNG!** ✅

🎉 Cảm ơn bạn đã tin tưởng BookStore!

📋 **THÔNG TIN ĐƠN HÀNG**
🆔 Mã đơn hàng: **{order.get('order_id', 'N/A')}**
📅 Ngày đặt: {order.get('created_at', 'N/A')}
👤 Khách hàng: {order.get('customer_name', 'N/A')}
📞 SĐT: {order.get('phone', 'N/A')}
🏠 Địa chỉ: {order.get('address', 'N/A')}

📚 **CHI TIẾT SẢN PHẨM**
📖 Tên sách: {order.get('book_title', 'N/A')}
🔢 Số lượng: {order.get('quantity', 0)} cuốn
💰 Đơn giá: {order.get('unit_price', 0):,}đ
💵 **Tổng tiền: {order.get('total_price', 0):,}đ**

📦 **THÔNG TIN GIAO HÀNG**
📋 Trạng thái: {order.get('status', 'N/A')}
🚚 Dự kiến giao: {order.get('estimated_delivery', 'N/A')}
⏰ Thời gian giao: 9:00 - 18:00 (T2-T7)

💳 **THANH TOÁN**
💰 Thanh toán khi nhận hàng (COD)
🏦 Hoặc chuyển khoản: MB Bank - 123456789

📞 **HỖ TRỢ 24/7**
📱 Hotline: 1900-xxxx
📧 Email: support@bookstore.com
💬 Chat: Dùng ô "Kiểm tra đơn hàng" để theo dõi

🙏 Cảm ơn bạn đã mua sắm tại BookStore! 🌟"""

    def order_status_response(self, order: Optional[Dict]) -> str:
        if not order:
            return """❌ **Không tìm thấy đơn hàng**

Vui lòng kiểm tra lại mã đơn hàng.

💡 **Lưu ý:**
• Mã đơn hàng có dạng ORD000001
• Nhập chính xác mã đơn hàng
• Dùng ô "Kiểm tra đơn hàng" ở trên

📧 Kiểm tra email để tìm mã đơn hàng
📞 Liên hệ hỗ trợ: 1900-xxxx"""
        
        return f"""📋 **THÔNG TIN ĐƠN HÀNG** 📋

🆔 Mã đơn hàng: **{order.get('order_id', 'N/A')}**
📅 Ngày đặt: {order.get('created_at', 'N/A')}
👤 Khách hàng: {order.get('customer_name', 'N/A')}
📞 SĐT: {order.get('phone', 'N/A')}
🏠 Địa chỉ: {order.get('address', 'N/A')}

📚 **CHI TIẾT ĐƠN HÀNG**
📖 Sách: {order.get('book_title', 'N/A')}
🔢 Số lượng: {order.get('quantity', 0)} cuốn
💵 Tổng tiền: {order.get('total_price', 0):,}đ

📦 **TRẠNG THÁI GIAO HÀNG**
🔄 **Trạng thái: {order.get('status', 'N/A')}**
🚚 Dự kiến giao: {order.get('estimated_delivery', 'N/A')}
⏰ Thời gian giao: 9:00 - 18:00 (T2-T7)

📞 **Cần hỗ trợ?**
📱 Hotline: 1900-xxxx (24/7)
📧 Email: support@bookstore.com"""

    def help_response(self) -> str:
        return self.get_text('help')
    
    def default_response(self) -> str:
        return """❓ Xin lỗi, tôi không hiểu yêu cầu của bạn.

💡 **GỢI Ý SỬ DỤNG:**
• **"tìm [tên sách]"** để tìm kiếm sách
• **"mua [tên sách]"** để đặt mua sách
• **"kiểm tra đơn [mã]"** để xem đơn hàng
• **"giúp"** để xem hướng dẫn chi tiết

🔍 **VÍ DỤ CỤ THỂ:**
• "tìm sách lập trình"
• "mua Đắc Nhân Tâm" 
• "kiểm tra đơn hàng ORD000001"

🤖 Tôi luôn sẵn sàng hỗ trợ bạn!"""