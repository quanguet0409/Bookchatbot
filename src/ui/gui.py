import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import datetime
import re
from chatbot.bot import ChatBot

class GUI:
    def __init__(self):
        self.chatbot = ChatBot()
        self.root = tk.Tk()
        self.message_queue = queue.Queue()
        self.typing_animation_active = False
        self.input_placeholder_active = False
        
        self.setup_window()
        self.setup_colors()
        self.setup_fonts()
        self.create_ui()
        self.process_queue()
    
    def setup_window(self):
        self.root.title("BookStore - Hệ thống quản lý sách")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        x = (self.root.winfo_screenwidth() // 2) - 600
        y = (self.root.winfo_screenheight() // 2) - 400
        self.root.geometry(f"1200x800+{x}+{y}")
    
    def setup_colors(self):
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db', 
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'white': '#ffffff',
            'text': '#2c3e50',
            'text_light': '#7f8c8d'
        }
        self.root.configure(bg=self.colors['light'])
    
    def setup_fonts(self):
        self.fonts = {
            'title': ('Segoe UI', 20, 'bold'),
            'subtitle': ('Segoe UI', 12),
            'chat': ('Segoe UI', 11),
            'input': ('Segoe UI', 11),
            'button': ('Segoe UI', 10, 'bold')
        }
    
    def create_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors['light'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_header()
        self.create_chat_area()
        self.create_input_area()
        self.create_status_bar()
        
        self.add_welcome_message()
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(header_content, bg=self.colors['primary'])
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = tk.Label(left_frame,
                              text="BookStore",
                              font=self.fonts['title'],
                              bg=self.colors['primary'],
                              fg=self.colors['white'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(left_frame,
                                 text="Hệ thống tìm kiếm và đặt mua sách trực tuyến",
                                 font=self.fonts['subtitle'],
                                 bg=self.colors['primary'],
                                 fg='#bdc3c7')
        subtitle_label.pack(anchor='w')
        
        right_frame = tk.Frame(header_content, bg=self.colors['primary'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons frame
        button_frame = tk.Frame(left_frame, bg=self.colors['primary'])
        button_frame.pack(fill='x', pady=(10, 0))
        
        catalog_btn = tk.Button(button_frame,
                               text="Danh mục sách",
                               font=self.fonts['button'],
                               bg=self.colors['secondary'],
                               fg=self.colors['white'],
                               relief='flat',
                               command=self.show_catalog,
                               cursor='hand2')
        catalog_btn.pack(side='left', padx=(0, 5))
        
        orders_btn = tk.Button(button_frame,
                              text="Đơn hàng",
                              font=self.fonts['button'],
                              bg=self.colors['secondary'],
                              fg=self.colors['white'],
                              relief='flat',
                              command=self.show_orders,
                              cursor='hand2')
        orders_btn.pack(side='left', padx=5)
        
        help_btn = tk.Button(button_frame,
                            text="Trợ giúp",
                            font=self.fonts['button'],
                            bg=self.colors['secondary'],
                            fg=self.colors['white'],
                            relief='flat',
                            command=self.show_help,
                            cursor='hand2')
        help_btn.pack(side='left', padx=5)

    def create_chat_area(self):
        chat_frame = tk.Frame(self.main_frame, bg=self.colors['light'])
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=self.fonts['chat'],
            bg=self.colors['white'],
            fg=self.colors['text'],
            state=tk.DISABLED,
            cursor='xterm'  # Change cursor to allow text selection
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        self.setup_text_tags()
        self.chat_display.bind('<Button-3>', self.show_context_menu)
        
        # Enable text selection when disabled
        self.chat_display.bind('<Button-1>', self.enable_selection)
        self.chat_display.bind('<B1-Motion>', self.enable_selection)
        self.chat_display.bind('<ButtonRelease-1>', self.enable_selection)

    def setup_text_tags(self):
        self.chat_display.tag_configure("user",
                                       background='#e3f2fd',
                                       foreground=self.colors['text'],
                                       font=self.fonts['chat'],
                                       lmargin1=20, lmargin2=20,
                                       spacing1=5, spacing3=5)
        
        self.chat_display.tag_configure("bot",
                                       background='#f8f9fa',
                                       foreground=self.colors['text'],
                                       font=self.fonts['chat'],
                                       lmargin1=20, lmargin2=20,
                                       spacing1=5, spacing3=5)
        
        self.chat_display.tag_configure("timestamp",
                                       foreground=self.colors['text_light'],
                                       font=('Segoe UI', 9))
        
        self.chat_display.tag_configure("book_id",
                                       background='#fff3cd',
                                       foreground=self.colors['warning'],
                                       font=('Consolas', 10, 'bold'))

    def create_input_area(self):
        input_frame = tk.Frame(self.main_frame, bg=self.colors['light'])
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Quick purchase area
        quick_frame = tk.Frame(input_frame, bg=self.colors['white'], relief=tk.SOLID, borderwidth=1)
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        quick_content = tk.Frame(quick_frame, bg=self.colors['white'])
        quick_content.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(quick_content,
                text="⚡ Mua nhanh theo mã sách:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).pack(side=tk.LEFT)
        
        self.quick_entry = tk.Entry(quick_content,
                                   font=('Consolas', 10),
                                   width=20)
        self.quick_entry.pack(side=tk.LEFT, padx=(10, 5))
        self.quick_entry.bind('<Return>', self.quick_buy)
        
        tk.Button(quick_content,
                 text="🛒 Mua ngay",
                 font=self.fonts['button'],
                 bg=self.colors['success'],
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 command=self.quick_buy).pack(side=tk.LEFT, padx=5)
        
        # Order check area
        check_frame = tk.Frame(quick_content, bg=self.colors['white'])
        check_frame.pack(side=tk.RIGHT)
        
        tk.Label(check_frame,
                text="📋 Kiểm tra đơn hàng:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).pack(side=tk.LEFT)
        
        self.order_entry = tk.Entry(check_frame,
                                   font=('Consolas', 10),
                                   width=15)
        self.order_entry.pack(side=tk.LEFT, padx=(10, 5))
        self.order_entry.bind('<Return>', self.check_order)
        
        tk.Button(check_frame,
                 text="🔍 Kiểm tra",
                 font=('Segoe UI', 9, 'bold'),
                 bg=self.colors['secondary'],
                 fg='white',
                 relief=tk.FLAT,
                 cursor='hand2',
                 command=self.check_order).pack(side=tk.LEFT)
        
        # Main input area
        main_input_frame = tk.Frame(input_frame, bg=self.colors['white'], relief=tk.SOLID, borderwidth=1)
        main_input_frame.pack(fill=tk.X)
        
        input_content = tk.Frame(main_input_frame, bg=self.colors['white'])
        input_content.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(input_content,
                text="💬 Nhập tin nhắn của bạn:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['white']).pack(anchor='w', pady=(0, 10))
        
        input_row = tk.Frame(input_content, bg=self.colors['white'])
        input_row.pack(fill=tk.X)
        
        self.input_text = tk.Text(input_row,
                                 height=3,
                                 font=self.fonts['input'],
                                 bg='#f8f9fa',
                                 wrap=tk.WORD)
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        button_frame = tk.Frame(input_row, bg=self.colors['white'])
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.send_button = tk.Button(button_frame,
                                    text="Gửi",
                                    font=self.fonts['button'],
                                    bg=self.colors['secondary'],
                                    fg='white',
                                    relief=tk.FLAT,
                                    cursor='hand2',
                                    width=8,
                                    command=self.send_message)
        self.send_button.pack(fill=tk.Y, pady=2)
        
        clear_btn = tk.Button(button_frame,
                             text="🗑️",
                             font=('Segoe UI', 10),
                             bg=self.colors['danger'],
                             fg='white',
                             relief=tk.FLAT,
                             cursor='hand2',
                             width=8,
                             command=self.clear_chat)
        clear_btn.pack(fill=tk.X, pady=2)
        
        self.input_text.bind('<Return>', self.handle_enter)
        self.input_text.bind('<Shift-Return>', lambda e: None)
        self.input_text.bind('<KeyRelease>', self.on_typing)
        
        self.add_placeholder()

    def create_status_bar(self):
        self.status_frame = tk.Frame(self.main_frame, bg=self.colors['primary'], height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame,
                                   text="✅ Sẵn sàng | Nhấn Enter để gửi tin nhắn",
                                   font=('Segoe UI', 9),
                                   bg=self.colors['primary'],
                                   fg='#bdc3c7',
                                   anchor='w')
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        online_label = tk.Label(self.status_frame,
                              text="🟢 Online | 🔗 Google Books API",
                              font=('Segoe UI', 9),
                              bg=self.colors['primary'],
                              fg=self.colors['success'])
        online_label.pack(side=tk.RIGHT, padx=15, pady=5)

    def add_placeholder(self):
        placeholder = """💡 Ví dụ các câu hỏi bạn có thể hỏi:

• "Tìm sách lập trình Python"
• "Mua sách Đắc Nhân Tâm"
• "Sách về kinh doanh" 
• "Kiểm tra đơn hàng ORD000001"

⌨️ Nhấn Enter để gửi, Shift+Enter để xuống dòng"""
        
        self.input_text.insert('1.0', placeholder)
        self.input_text.configure(fg=self.colors['text_light'])
        self.input_placeholder_active = True
        
        self.input_text.bind('<FocusIn>', self.on_focus_in)
        self.input_text.bind('<FocusOut>', self.on_focus_out)

    def on_focus_in(self, event):
        if self.input_placeholder_active:
            self.input_text.delete('1.0', tk.END)
            self.input_text.configure(fg=self.colors['text'])
            self.input_placeholder_active = False
    
    def on_focus_out(self, event):
        if not self.input_text.get('1.0', tk.END).strip():
            self.add_placeholder()

    def handle_enter(self, event):
        self.send_message()
        return 'break'

    def on_typing(self, event):
        if event.keysym == 'Return':
            return
        
        text = self.input_text.get('1.0', tk.END).strip()
        if text and not self.input_placeholder_active:
            self.send_button.configure(bg=self.colors['success'])
            self.status_label.configure(text="⌨️ Đang nhập...")
        else:
            self.send_button.configure(bg=self.colors['secondary'])
            self.status_label.configure(text="✅ Sẵn sàng | Nhấn Enter để gửi tin nhắn")

    def add_welcome_message(self):
        welcome = """🌟 Chào mừng bạn đến với BookStore AI Chatbot! 🌟

Tôi là trợ lý thông minh với API Google Books, sẵn sàng giúp bạn:

📚 **Tìm kiếm sách:** Từ hàng triệu đầu sách trên thế giới
🛒 **Đặt mua sách:** Quy trình đơn giản, thanh toán linh hoạt
📋 **Theo dõi đơn hàng:** Kiểm tra trạng thái real-time
💬 **Tư vấn chuyên nghiệp:** Gợi ý sách phù hợp với sở thích

🚀 **Tính năng nổi bật:**
• Tra cứu sách online qua Google Books API
• Mua nhanh theo mã sách
• Kiểm tra đơn hàng nhanh chóng
• Danh mục sách đầy đủ với copy dễ dàng
• Hỗ trợ đặt hàng từ A-Z

💡 Hãy bắt đầu bằng cách nhập câu hỏi hoặc sử dụng các chức năng phía trên!"""
        
        self.add_bot_message(welcome)

    def add_user_message(self, message):
        self.chat_display.configure(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        self.chat_display.insert(tk.END, f"\n👤 Bạn ({timestamp})\n", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n", "user")
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def add_bot_message(self, message):
        self.chat_display.configure(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        self.chat_display.insert(tk.END, f"\n🤖 BookStore AI ({timestamp})\n", "timestamp")
        
        lines = message.split('\n')
        for line in lines:
            if '🆔' in line and re.search(r'[A-Za-z0-9_-]{8,}', line):
                parts = re.split(r'([A-Za-z0-9_-]{8,})', line)
                for part in parts:
                    if re.match(r'^[A-Za-z0-9_-]{8,}$', part):
                        self.chat_display.insert(tk.END, part, "book_id")
                    else:
                        self.chat_display.insert(tk.END, part, "bot")
                self.chat_display.insert(tk.END, '\n', "bot")
            else:
                self.chat_display.insert(tk.END, line + '\n', "bot")
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        user_input = self.input_text.get('1.0', tk.END).strip()
        
        if not user_input or self.input_placeholder_active:
            return
        
        self.add_user_message(user_input)
        
        self.input_text.delete('1.0', tk.END)
        self.input_text.configure(fg=self.colors['text'])
        self.input_placeholder_active = False
        
        self.status_label.configure(text="🔄 Đang xử lý...")
        self.send_button.configure(state='disabled')
        
        if user_input.lower() in ['quit', 'exit', 'thoát']:
            self.add_bot_message("👋 Cảm ơn bạn đã sử dụng BookStore! Hẹn gặp lại! 🌟")
            self.root.after(2000, self.root.quit)
            return
        
        threading.Thread(target=self.process_message, args=(user_input,), daemon=True).start()

    def process_message(self, user_input):
        try:
            response = self.chatbot.process_message(user_input)
            self.message_queue.put(("response", response))
        except Exception as e:
            error_msg = f"❌ Có lỗi xảy ra: {str(e)}\nVui lòng thử lại!"
            self.message_queue.put(("response", error_msg))

    def process_queue(self):
        if not hasattr(self, 'root') or not self.root.winfo_exists():
            return
            
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                if msg_type == "response":
                    self.show_response(data)
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Queue processing error: {e}")
        
        try:
            self.root.after(100, self.process_queue)
        except tk.TclError:
            pass

    def show_response(self, response):
        self.add_bot_message(response)
        self.status_label.configure(text="✅ Sẵn sàng | Nhấn Enter để gửi tin nhắn")
        self.send_button.configure(state='normal', bg=self.colors['secondary'])
        self.input_text.focus_set()

    def quick_buy(self, event=None):
        book_id = self.quick_entry.get().strip()
        if book_id:
            if self.input_placeholder_active:
                self.input_text.delete('1.0', tk.END)
                self.input_placeholder_active = False
            else:
                self.input_text.delete('1.0', tk.END)
                
            self.input_text.insert('1.0', f"mua {book_id}")
            self.input_text.configure(fg=self.colors['text'])
            self.quick_entry.delete(0, tk.END)
            
            self.status_label.configure(text=f"⚡ Mua nhanh: {book_id}")
            self.send_message()
            
            self.root.after(3000, lambda: self.status_label.configure(text="✅ Sẵn sàng | Nhấn Enter để gửi tin nhắn"))

    def check_order(self, event=None):
        order_id = self.order_entry.get().strip()
        if order_id:
            if self.input_placeholder_active:
                self.input_text.delete('1.0', tk.END)
                self.input_placeholder_active = False
            else:
                self.input_text.delete('1.0', tk.END)
                
            self.input_text.insert('1.0', f"kiểm tra đơn hàng {order_id}")
            self.input_text.configure(fg=self.colors['text'])
            self.order_entry.delete(0, tk.END)
            
            self.status_label.configure(text=f"🔍 Kiểm tra đơn: {order_id}")
            self.send_message()
            
            self.root.after(3000, lambda: self.status_label.configure(text="✅ Sẵn sàng | Nhấn Enter để gửi tin nhắn"))

    def clear_chat(self):
        """Clear chat conversation"""
        if messagebox.askyesno("Xác nhận", "🗑️ Bạn có chắc muốn xóa toàn bộ cuộc trò chuyện?"):
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.delete('1.0', tk.END)
            self.chat_display.configure(state=tk.DISABLED)
            self.add_welcome_message()

    def enable_selection(self, event=None):
        """Enable text selection in chat display"""
        try:
            self.chat_display.configure(state=tk.NORMAL)
            self.root.after_idle(lambda: self.chat_display.configure(state=tk.DISABLED))
        except:
            pass

    def copy_selected_text(self, event=None):
        """Copy selected text to clipboard with better handling"""
        try:
            # Try to get selection first
            try:
                selected = self.chat_display.selection_get()
                if selected:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(selected)
                    self.status_label.configure(text="📋 Đã sao chép text được chọn!")
                    self.root.after(2000, lambda: self.status_label.configure(text="✅ Sẵn sàng"))
                    return
            except tk.TclError:
                pass
            
            # If no selection, try to copy from cursor position
            try:
                # Get current cursor position
                cursor_pos = self.chat_display.index(tk.INSERT)
                # Get the line containing cursor
                line_start = cursor_pos.split('.')[0] + '.0'
                line_end = cursor_pos.split('.')[0] + '.end'
                line_text = self.chat_display.get(line_start, line_end)
                
                if line_text.strip():
                    self.root.clipboard_clear()
                    self.root.clipboard_append(line_text.strip())
                    self.status_label.configure(text="📋 Đã sao chép dòng hiện tại!")
                    self.root.after(2000, lambda: self.status_label.configure(text="✅ Sẵn sàng"))
                    return
            except:
                pass
            
            # Fallback: copy all chat
            chat_content = self.chat_display.get('1.0', tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(chat_content)
            self.status_label.configure(text="📋 Đã sao chép toàn bộ chat!")
            self.root.after(2000, lambda: self.status_label.configure(text="✅ Sẵn sàng"))
            
        except Exception as e:
            print(f"Copy error: {e}")

    def show_context_menu(self, event):
        try:
            context_menu = tk.Menu(self.root, tearoff=0)
            
            # Check if there's a selection
            try:
                selected = self.chat_display.selection_get()
                if selected:
                    context_menu.add_command(label="📋 Sao chép text được chọn", 
                                           command=self.copy_selected_text)
                    context_menu.add_separator()
            except tk.TclError:
                pass
            
            context_menu.add_command(label="📋 Sao chép tất cả", 
                                   command=self.copy_all_chat)
            context_menu.add_command(label="📚 Sao chép mã sách", 
                                   command=self.copy_book_ids)
            context_menu.add_separator()
            context_menu.add_command(label="🔍 Danh mục sách", 
                                   command=self.open_catalog)
            context_menu.add_separator()
            context_menu.add_command(label="🔄 Làm mới", 
                                   command=self.refresh_chat)
            
            context_menu.tk_popup(event.x_root, event.y_root)
        except Exception as e:
            print(f"Context menu error: {e}")

    def copy_all_chat(self):
        """Copy entire chat content"""
        try:
            chat_content = self.chat_display.get('1.0', tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(chat_content)
            self.status_label.configure(text="📋 Đã sao chép toàn bộ cuộc trò chuyện!")
            self.root.after(2000, lambda: self.status_label.configure(text="✅ Sẵn sàng"))
        except Exception as e:
            print(f"Copy all error: {e}")

    def refresh_chat(self):
        """Refresh chat display"""
        try:
            self.chat_display.configure(state=tk.NORMAL)
            self.root.after(100, lambda: self.chat_display.configure(state=tk.DISABLED))
            self.status_label.configure(text="🔄 Đã làm mới chat display")
            self.root.after(2000, lambda: self.status_label.configure(text="✅ Sẵn sàng"))
        except Exception as e:
            print(f"Refresh error: {e}")

    def open_catalog(self):
        """Open book catalog window"""
        BookCatalogWindow(self.root, self.chatbot.bookstore)

    def show_help(self):
        """Show help message"""
        help_msg = """🆘 **HƯỚNG DẪN SỬ DỤNG BOOKSTORE CHATBOT**

🔍 **TÌM KIẾM SÁCH:**
• "tìm [từ khóa]" - Tìm theo tên, tác giả
• "sách về [chủ đề]" - Tìm theo thể loại

🛒 **ĐẶT MUA SÁCH:**
• "mua [tên sách]" - Đặt mua bằng tên
• "mua [ID sách]" - Đặt mua bằng mã sách
• Dùng ô "Mua nhanh" ở trên

📋 **KIỂM TRA ĐƠN HÀNG:**
• "kiểm tra đơn hàng [mã]" - Kiểm tra trạng thái
• "đơn hàng [mã]" - Xem thông tin đơn hàng
• Dùng ô "Kiểm tra đơn hàng" ở trên

💡 **TÍNH NĂNG KHÁC:**
• Click phải để mở menu copy
• "Danh mục sách" để duyệt toàn bộ
• Shift+Enter để xuống dòng

📞 **HỖ TRỢ:** Hotline 1900-xxxx (24/7)"""
        
        self.add_bot_message(help_msg)

    def copy_book_ids(self):
        """Copy all book IDs from chat"""
        try:
            chat_content = self.chat_display.get('1.0', tk.END)
            book_ids = re.findall(r'([A-Za-z0-9_-]{8,})', chat_content)
            if book_ids:
                unique_ids = list(set(book_ids))
                ids_text = '\n'.join(unique_ids)
                self.root.clipboard_clear()
                self.root.clipboard_append(ids_text)
                self.status_label.configure(text=f"📋 Đã sao chép {len(unique_ids)} mã sách!")
                self.root.after(2000, lambda: self.status_label.configure(text="✅ Sẵn sàng"))
        except:
            pass

    def run(self):
        """Run the GUI application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"GUI Error: {e}")
        finally:
            try:
                if hasattr(self, 'root'):
                    self.root.quit()
                    self.root.destroy()
            except:
                pass

class BookCatalogWindow:
    def __init__(self, parent, bookstore):
        self.parent = parent
        self.bookstore = bookstore
        self.window = tk.Toplevel(parent)
        self.setup_catalog()
    
    def setup_catalog(self):
        self.window.title("📚 Danh Mục Sách BookStore")
        self.window.geometry("900x600")
        self.window.configure(bg='#f8f9fa')
        
        header = tk.Frame(self.window, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header,
                text="📚 DANH MỤC SÁCH BOOKSTORE",
                font=('Segoe UI', 16, 'bold'),
                bg='#2c3e50',
                fg='white').pack(pady=15)
        
        main_frame = tk.Frame(self.window, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = tk.Frame(main_frame, bg='white', width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame,
                text="📂 DANH MỤC",
                font=('Segoe UI', 12, 'bold'),
                bg='white').pack(pady=10)
        
        categories = [
            ("🔤 Tất cả sách", ""),
            ("💼 Kinh doanh", "business"),
            ("💻 Lập trình", "programming"),
            ("📖 Văn học", "literature"),
            ("🧠 Kỹ năng sống", "self help"),
            ("🤖 AI & Công nghệ", "artificial intelligence")
        ]
        
        for cat_name, cat_query in categories:
            btn = tk.Button(left_frame,
                           text=cat_name,
                           font=('Segoe UI', 10),
                           bg='#ecf0f1',
                           fg='#2c3e50',
                           relief=tk.FLAT,
                           anchor='w',
                           width=20,
                           command=lambda q=cat_query: self.load_category(q))
            btn.pack(fill=tk.X, padx=5, pady=2)
        
        right_frame = tk.Frame(main_frame, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        search_frame = tk.Frame(right_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame,
                text="🔍 Tìm kiếm:",
                bg='white').pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(search_frame, font=('Segoe UI', 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        list_frame = tk.Frame(right_frame, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns = ('ID', 'Tên sách', 'Tác giả', 'Giá', 'Đánh giá')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.tree.heading('ID', text='Mã sách')
        self.tree.heading('Tên sách', text='📚 Tên sách')
        self.tree.heading('Tác giả', text='👤 Tác giả')
        self.tree.heading('Giá', text='💰 Giá')
        self.tree.heading('Đánh giá', text='⭐ Đánh giá')
        
        self.tree.column('ID', width=80)
        self.tree.column('Tên sách', width=300)
        self.tree.column('Tác giả', width=150)
        self.tree.column('Giá', width=100)
        self.tree.column('Đánh giá', width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<Double-1>', self.copy_book_id)
        
        btn_frame = tk.Frame(right_frame, bg='white')
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame,
                 text="📋 Copy mã",
                 bg='#3498db',
                 fg='white',
                 relief=tk.FLAT,
                 command=self.copy_selected).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="🛒 Mua ngay",
                 bg='#27ae60',
                 fg='white',
                 relief=tk.FLAT,
                 command=self.buy_selected).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="ℹ️ Chi tiết",
                 bg='#f39c12',
                 fg='white',
                 relief=tk.FLAT,
                 command=self.show_details).pack(side=tk.LEFT)
        
        self.load_category("")
    
    def load_category(self, query):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        books = self.bookstore.search_books(query if query else "bestseller", 30)
        
        for book in books:
            book_id = book.get('book_id', 'unknown')
            title = book.get('title', 'Tên không rõ')
            authors = book.get('authors', 'Tác giả không rõ')
            price = book.get('price', 0)
            rating = book.get('rating', 0)
            
            self.tree.insert('', 'end', values=(
                book_id,
                title[:40] + "..." if len(title) > 40 else title,
                authors[:20] + "..." if len(authors) > 20 else authors,
                f"{price:,}đ",
                f"{rating}/5"
            ))
    
    def on_search(self, event):
        query = self.search_entry.get().strip()
        if len(query) >= 2:
            self.load_category(query)
        elif len(query) == 0:
            self.load_category("")
    
    def copy_book_id(self, event):
        self.copy_selected()
    
    def copy_selected(self):
        selection = self.tree.selection()
        if selection:
            book_id = self.tree.item(selection[0])['values'][0]
            self.window.clipboard_clear()
            self.window.clipboard_append(book_id)
            messagebox.showinfo("Thành công", f"Đã copy mã sách: {book_id}")
    
    def buy_selected(self):
        selection = self.tree.selection()
        if selection:
            book_id = self.tree.item(selection[0])['values'][0]
            book_title = self.tree.item(selection[0])['values'][1]
            self.window.clipboard_clear()
            self.window.clipboard_append(f"mua {book_id}")
            messagebox.showinfo("Mua hàng", f"Đã copy 'mua {book_id}' vào clipboard!\n\nDán vào chat để mua sách:\n{book_title}")
    
    def show_details(self):
        selection = self.tree.selection()
        if selection:
            book_id = self.tree.item(selection[0])['values'][0]
            book = self.bookstore.get_book_by_id(book_id)
            if book:
                details = f"""📚 CHI TIẾT SÁCH

🆔 Mã: {book.get('book_id', 'N/A')}
📖 Tên: {book.get('title', 'N/A')}
👤 Tác giả: {book.get('authors', 'N/A')}
🏢 NXB: {book.get('publisher', 'N/A')}
📅 Năm XB: {book.get('published_date', 'N/A')}
📄 Số trang: {book.get('page_count', 'N/A')}
📂 Thể loại: {book.get('categories', 'N/A')}
💰 Giá: {book.get('price', 0):,}đ
⭐ Đánh giá: {book.get('rating', 0)}/5
📦 Tồn kho: {book.get('stock', 0)} cuốn

📝 Mô tả:
{book.get('description', 'Không có mô tả')[:300]}..."""
                
                messagebox.showinfo("Chi tiết sách", details)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin sách!")