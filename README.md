# 📚 BookStore Chatbot

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/GUI-Tkinter-green.svg" alt="GUI Framework">
  <img src="https://img.shields.io/badge/API-Google%20Books-red.svg" alt="API Integration">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

<div align="center">
  <h3>🌟 Hệ thống quản lý và tìm kiếm sách thông minh với giao diện Dark Theme hiện đại</h3>
</div>

---

## ✨ Tính năng chính

### 🔍 **Tìm kiếm sách thông minh**
- Tìm kiếm theo tên sách, tác giả, thể loại
- Tích hợp Google Books API với hàng triệu đầu sách
- Gợi ý tìm kiếm thông minh
- Hiển thị thông tin chi tiết: giá, đánh giá, mô tả

### 🛒 **Quản lý đơn hàng**
- Đặt mua sách nhanh chóng bằng mã sách hoặc tên
- Theo dõi trạng thái đơn hàng real-time
- Hệ thống mã đơn hàng tự động
- Kiểm tra lịch sử mua hàng

### 💬 **Chat Interface thông minh**
- Giao diện chat tự nhiên, dễ sử dụng
- Hỗ trợ copy/paste text (Ctrl+C, Ctrl+V)
- Tự động gợi ý câu hỏi
- Xóa lịch sử chat tiện lợi

### 🎨 **Dark Theme hiện đại**
- Giao diện tối đẹp mắt, bảo vệ mắt
- Màu sắc tím (Purple) accent chuyên nghiệp
- Responsive design, thân thiện người dùng
- Animation và hiệu ứng mượt mà

---

## 🖥️ Giao diện ứng dụng

### 📱 Main Interface
```
┌─────────────────────────────────────────────────────────┐
│  📚 BookStore - Hệ thống tìm kiếm và quản lý sách        │
│  [Danh mục] [Trợ giúp] [Xóa chat]                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  💬 Chat Area (Dark theme với purple accents)          │
│     - Tìm kiếm sách thông minh                          │
│     - Đặt hàng nhanh chóng                              │
│     - Hỗ trợ 24/7                                       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  🛒 Mua nhanh: [Mã sách____] [Mua ngay]               │
│  📋 Kiểm tra: [Mã đơn hàng_] [Kiểm tra]               │
├─────────────────────────────────────────────────────────┤
│  💭 Nhập tin nhắn: [Text area______] [Gửi]            │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Cài đặt và chạy

### 📋 Yêu cầu hệ thống
- **Python 3.11+**
- **Tkinter** (có sẵn với Python)
- **Requests** library
- **Threading** support

### ⚡ Cài đặt nhanh

```bash
# Clone repository
git clone https://github.com/yourusername/BookStore-Chatbot.git
cd BookStore-Chatbot

# Cài đặt dependencies
pip install requests

# Chạy ứng dụng
cd src
python main.py
```

### 🛠️ Cấu trúc dự án
```
BookStore-Chatbot/
├── src/
│   ├── main.py              # Entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── book_api.py      # Google Books API integration
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── bot.py           # Core chatbot logic
│   │   └── responses.py     # Response handling
│   ├── models/
│   │   ├── __init__.py
│   │   └── bookstore.py     # Data models
│   └── ui/
│       ├── __init__.py
│       └── gui.py           # GUI interface (Dark theme)
├── README.md
└── requirements.txt
```

---

## 📖 Hướng dẫn sử dụng

### 🔍 **Tìm kiếm sách**
```
💬 "tìm sách lập trình Python"
💬 "sách về khoa học máy tính"
💬 "tác giả Nguyễn Nhật Ánh"
```

### 🛒 **Đặt mua sách**
```
💬 "mua BOOK123"
💬 "mua Đắc Nhân Tâm"
💬 Hoặc dùng form "Mua nhanh" ở trên
```

### 📋 **Kiểm tra đơn hàng**
```
💬 "kiểm tra đơn hàng ORDER123"
💬 Hoặc dùng form "Kiểm tra đơn hàng" ở trên
```

### ⚙️ **Tính năng khác**
- **Danh mục**: Xem toàn bộ sách có sẵn
- **Trợ giúp**: Hướng dẫn chi tiết trong cửa sổ riêng
- **Xóa chat**: Làm sạch lịch sử trò chuyện

---

## 🎯 Tính năng nổi bật

### 🤖 **AI-powered Search**
- Tìm kiếm ngữ nghĩa thông minh
- Gợi ý sách liên quan
- Lọc theo thể loại, giá cả, đánh giá

### 🎨 **Modern Dark UI**
- Smooth animations và transitions
- Responsive design cho mọi kích thước màn hình

### ⚡ **Performance**
- Multi-threading cho API calls
- Lazy loading cho danh sách sách lớn
- Caching để tăng tốc độ truy vấn
- Memory optimization

### 🔒 **User Experience**
- Auto-complete và suggestions
- Keyboard shortcuts (Enter, Ctrl+C/V)
- Error handling thông minh
- Status updates real-time

---

## 🛡️ Bảo mật và Hiệu năng

### 🔐 **Security Features**
- ✅ Input validation và sanitization
- ✅ Safe API key handling
- ✅ No sensitive data storage
- ✅ Thread-safe operations

### ⚡ **Performance Optimizations**
- ✅ Async API calls
- ✅ Response caching
- ✅ Lazy UI updates
- ✅ Memory leak prevention

---

## 🤝 Đóng góp

Chúng tôi rất hoan nghênh mọi đóng góp! 

### 📝 Các bước đóng góp:
1. **Fork** repository
2. Tạo **feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit** changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to branch: `git push origin feature/AmazingFeature`
5. Tạo **Pull Request**

### 🐛 Báo lỗi
Nếu bạn phát hiện lỗi, vui lòng tạo **Issue** với:
- Mô tả chi tiết lỗi
- Steps to reproduce
- Screenshots (nếu có)
- Environment info


## 📄 License

Dự án này được cấp phép theo **MIT License** - xem file [LICENSE](LICENSE) để biết chi tiết.

---

## 🌟 Acknowledgments

- **Google Books API** - Cung cấp dữ liệu sách phong phú
- **Python Tkinter** - Framework GUI mạnh mẽ
- **Contributors** - Cảm ơn tất cả những người đóng góp

---

</div>
