import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import datetime
import re
from chatbot.bot import ChatBot

class BookCatalogWindow:
    def __init__(self, parent, bookstore):
        self.parent = parent
        self.bookstore = bookstore
        self.window = tk.Toplevel(parent)
        self.setup_catalog()
    
    def setup_catalog(self):
        self.window.title("Danh Mục Sách BookStore")
        self.window.geometry("900x600")
        self.window.configure(bg='#f8f9fa')
        
        header = tk.Frame(self.window, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header,
                text="DANH MỤC SÁCH BOOKSTORE",
                font=('Segoe UI', 16, 'bold'),
                bg='#2c3e50',
                fg='white').pack(pady=15)
        
        main_frame = tk.Frame(self.window, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_frame = tk.Frame(main_frame, bg='white', width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame,
                text="DANH MỤC",
                font=('Segoe UI', 12, 'bold'),
                bg='white').pack(pady=10)
        
        categories = [
            ("Tất cả sách", ""),
            ("Kinh doanh", "business"),
            ("Lập trình", "programming"),
            ("Văn học", "literature"),
            ("Kỹ năng sống", "self help"),
            ("Công nghệ", "technology")
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
                text="Tìm kiếm:",
                bg='white').pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(search_frame, font=('Segoe UI', 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        list_frame = tk.Frame(right_frame, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        columns = ('ID', 'Tên sách', 'Tác giả', 'Giá', 'Đánh giá')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.tree.heading('ID', text='Mã sách')
        self.tree.heading('Tên sách', text='Tên sách')
        self.tree.heading('Tác giả', text='Tác giả')
        self.tree.heading('Giá', text='Giá')
        self.tree.heading('Đánh giá', text='Đánh giá')
        
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
                 text="Copy mã",
                 bg='#3498db',
                 fg='white',
                 relief=tk.FLAT,
                 command=self.copy_selected).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Mua ngay",
                 bg='#27ae60',
                 fg='white',
                 relief=tk.FLAT,
                 command=self.buy_selected).pack(side=tk.LEFT, padx=(0, 5))
        
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

class GUI:
    def __init__(self):
        self.chatbot = ChatBot()
        self.root = tk.Tk()
        self.message_queue = queue.Queue()
        self.typing_animation_active = False
        self.input_placeholder_active = False
        self.user_has_chatted = False  # Track if user has started chatting
        
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
            'primary': '#1a1a1a',      # Dark black
            'secondary': '#8b5cf6',     # Purple accent
            'success': '#10b981',       # Green
            'warning': '#f59e0b',       # Orange
            'danger': '#ef4444',        # Red
            'background': '#0f0f0f',    # Very dark background
            'card': '#1e1e1e',         # Dark cards
            'light': '#2a2a2a',        # Light dark
            'white': '#ffffff',        # White
            'text': '#ffffff',         # White text
            'text_light': '#9ca3af'    # Gray text
        }
        self.root.configure(bg=self.colors['background'])
    
    def setup_fonts(self):
        self.fonts = {
            'title': ('Segoe UI', 20, 'bold'),
            'subtitle': ('Segoe UI', 12),
            'chat': ('Segoe UI', 11),
            'input': ('Segoe UI', 11),
            'button': ('Segoe UI', 10, 'bold')
        }
    
    def create_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'])
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
                                 text="Hệ thống tìm kiếm và quản lý sách",
                                 font=self.fonts['subtitle'],
                                 bg=self.colors['primary'],
                                 fg=self.colors['text_light'])
        subtitle_label.pack(anchor='w')
        
        right_frame = tk.Frame(header_content, bg=self.colors['primary'])
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        button_frame = tk.Frame(right_frame, bg=self.colors['primary'])
        button_frame.pack(fill='both', expand=True)
        
        catalog_btn = tk.Button(button_frame,
                               text="Danh mục",
                               font=self.fonts['button'],
                               bg=self.colors['secondary'],
                               fg=self.colors['white'],
                               relief='flat',
                               command=self.show_catalog,
                               cursor='hand2',
                               padx=10, pady=5)
        catalog_btn.pack(side='left', padx=5)
        
        help_btn = tk.Button(button_frame,
                            text="Trợ giúp",
                            font=self.fonts['button'],
                            bg=self.colors['secondary'],
                            fg=self.colors['white'],
                            relief='flat',
                            command=self.show_help,
                            cursor='hand2',
                            padx=10, pady=5)
        help_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(button_frame,
                             text="Xóa chat",
                             font=self.fonts['button'],
                             bg=self.colors['warning'],
                             fg=self.colors['white'],
                             relief='flat',
                             command=self.clear_chat,
                             cursor='hand2',
                             padx=10, pady=5)
        clear_btn.pack(side='left', padx=5)

    def create_chat_area(self):
        chat_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=self.fonts['chat'],
            bg=self.colors['card'],
            fg=self.colors['text'],
            state=tk.NORMAL,
            cursor='xterm',
            selectbackground=self.colors['secondary'],
            selectforeground=self.colors['white']
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Block editing but allow selection
        self.chat_display.bind('<KeyPress>', self.on_chat_keypress)
        self.chat_display.bind('<Control-c>', self.copy_selection)
        self.chat_display.bind('<Control-a>', self.select_all)
        
        self.setup_text_tags()
        self.chat_display.focus_set()
    
    def on_chat_keypress(self, event):
        if event.state & 0x4:  # Ctrl pressed
            if event.keysym in ['c', 'C', 'a', 'A']:
                return None
        return 'break'
    
    def copy_selection(self, event=None):
        try:
            if self.chat_display.tag_ranges(tk.SEL):
                selected_text = self.chat_display.selection_get()
                self.root.clipboard_clear()
                self.root.clipboard_append(selected_text)
                self.status_label.configure(text="Đã copy text được chọn!")
                self.root.after(2000, lambda: self.status_label.configure(text="Sẵn sàng"))
        except tk.TclError:
            pass
        return 'break'
    
    def select_all(self, event=None):
        self.chat_display.tag_add(tk.SEL, "1.0", tk.END)
        return 'break'

    def setup_text_tags(self):
        self.chat_display.tag_configure("user",
                                       background='#374151',
                                       foreground=self.colors['text'],
                                       font=self.fonts['chat'],
                                       lmargin1=20, lmargin2=20,
                                       spacing1=5, spacing3=5)
        
        self.chat_display.tag_configure("bot",
                                       background='#1f2937',
                                       foreground=self.colors['text'],
                                       font=self.fonts['chat'],
                                       lmargin1=20, lmargin2=20,
                                       spacing1=5, spacing3=5)
        
        self.chat_display.tag_configure("timestamp",
                                       foreground=self.colors['text_light'],
                                       font=('Segoe UI', 9))

    def create_input_area(self):
        input_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Quick actions
        quick_frame = tk.Frame(input_frame, bg=self.colors['card'], relief=tk.SOLID, borderwidth=1)
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        quick_content = tk.Frame(quick_frame, bg=self.colors['card'])
        quick_content.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(quick_content,
                text="Mua nhanh theo mã sách:",
                font=self.fonts['button'],
                fg=self.colors['text'],
                bg=self.colors['card']).pack(side=tk.LEFT)
        
        self.quick_entry = tk.Entry(quick_content,
                                   font=('Consolas', 10),
                                   bg=self.colors['background'],
                                   fg=self.colors['text'],
                                   insertbackground=self.colors['text'],
                                   width=20)
        self.quick_entry.pack(side=tk.LEFT, padx=(10, 5))
        self.quick_entry.bind('<Return>', self.quick_buy)
        
        tk.Button(quick_content,
                 text="Mua ngay",
                 font=self.fonts['button'],
                 bg=self.colors['success'],
                 fg=self.colors['white'],
                 relief='flat',
                 command=self.quick_buy,
                 cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))
        
        # Order check
        order_frame = tk.Frame(quick_content, bg=self.colors['card'])
        order_frame.pack(side=tk.RIGHT)
        
        tk.Label(order_frame,
                text="Kiểm tra đơn hàng:",
                font=self.fonts['button'],
                fg=self.colors['text'],
                bg=self.colors['card']).pack(side=tk.LEFT)
        
        self.order_entry = tk.Entry(order_frame,
                                   font=('Consolas', 10),
                                   bg=self.colors['background'],
                                   fg=self.colors['text'],
                                   insertbackground=self.colors['text'],
                                   width=15)
        self.order_entry.pack(side=tk.LEFT, padx=(10, 5))
        self.order_entry.bind('<Return>', self.check_order)
        
        tk.Button(order_frame,
                 text="Kiểm tra",
                 font=self.fonts['button'],
                 bg=self.colors['secondary'],
                 fg=self.colors['white'],
                 relief='flat',
                 command=self.check_order,
                 cursor='hand2').pack(side=tk.LEFT)
        
        # Main input
        input_content = tk.Frame(input_frame, bg=self.colors['card'], relief=tk.SOLID, borderwidth=1)
        input_content.pack(fill=tk.X)
        
        input_header = tk.Frame(input_content, bg=self.colors['card'])
        input_header.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        tk.Label(input_header,
                text="Nhập tin nhắn của bạn:",
                font=self.fonts['button'],
                fg=self.colors['text'],
                bg=self.colors['card']).pack(side=tk.LEFT)
        
        input_row = tk.Frame(input_content, bg=self.colors['card'])
        input_row.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.input_text = tk.Text(input_row,
                                 height=3,
                                 font=self.fonts['input'],
                                 bg=self.colors['background'],
                                 fg=self.colors['text'],
                                 insertbackground=self.colors['text'],
                                 wrap=tk.WORD,
                                 selectbackground=self.colors['secondary'],
                                 selectforeground=self.colors['white'])
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        button_frame = tk.Frame(input_row, bg=self.colors['card'])
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.send_button = tk.Button(button_frame,
                                    text="Gửi",
                                    font=self.fonts['button'],
                                    bg=self.colors['secondary'],
                                    fg=self.colors['white'],
                                    relief='flat',
                                    command=self.send_message,
                                    cursor='hand2',
                                    width=8, height=2)
        self.send_button.pack()
        
        self.input_text.bind('<Return>', self.handle_enter)
        self.input_text.bind('<Shift-Return>', lambda e: None)
        self.input_text.bind('<KeyRelease>', self.on_typing)
        self.input_text.bind('<FocusIn>', self.on_focus_in)
        self.input_text.bind('<FocusOut>', self.on_focus_out)
        
        self.add_placeholder()

    def create_status_bar(self):
        status_frame = tk.Frame(self.main_frame, bg=self.colors['background'], height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                    text="Sẵn sàng",
                                    font=('Segoe UI', 9),
                                    bg=self.colors['background'],
                                    fg=self.colors['text_light'],
                                    anchor='w')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

    def add_placeholder(self):
        # Only show placeholder if input is empty
        if not self.input_text.get('1.0', tk.END).strip():
            self.input_text.insert('1.0', 'Nhập tin nhắn của bạn...')
            self.input_text.configure(fg=self.colors['text_light'])
            self.input_placeholder_active = True

    def on_focus_in(self, event):
        if self.input_placeholder_active:
            self.input_text.delete('1.0', tk.END)
            self.input_text.configure(fg=self.colors['text'])
            self.input_placeholder_active = False

    def on_focus_out(self, event):
        # Add placeholder if input is empty
        if not self.input_text.get('1.0', tk.END).strip():
            self.add_placeholder()

    def handle_enter(self, event):
        if not (event.state & 0x1):  # No Shift
            self.send_message()
            return 'break'
        return None

    def on_typing(self, event):
        # If placeholder is active and user starts typing, remove it
        if self.input_placeholder_active:
            # Check if user is actually typing (not just navigating)
            if event.keysym not in ['Left', 'Right', 'Up', 'Down', 'Home', 'End']:
                self.input_text.delete('1.0', tk.END)
                self.input_text.configure(fg=self.colors['text'])
                self.input_placeholder_active = False
            return
        
        if not self.typing_animation_active:
            self.typing_animation_active = True
            self.send_button.configure(bg=self.colors['success'])
            self.status_label.configure(text="Đang soạn tin nhắn...")
            self.root.after(3000, self.stop_typing_animation)

    def stop_typing_animation(self):
        self.send_button.configure(bg=self.colors['secondary'])
        self.status_label.configure(text="Sẵn sàng | Nhấn Enter để gửi tin nhắn")
        self.typing_animation_active = False

    def add_welcome_message(self):
        welcome = """Chào mừng bạn đến với BookStore!

Tôi có thể giúp bạn:

Tìm kiếm sách: Từ hàng triệu đầu sách
Đặt mua sách: Quy trình đơn giản
Theo dõi đơn hàng: Kiểm tra trạng thái
Tư vấn sách: Gợi ý phù hợp

Tính năng:
• Tra cứu sách online
• Mua nhanh theo mã sách
• Kiểm tra đơn hàng nhanh chóng
• Danh mục sách đầy đủ
• Hỗ trợ đặt hàng từ A-Z

Hãy bắt đầu bằng cách nhập câu hỏi!"""
        
        self.add_bot_message(welcome)

    def add_user_message(self, message):
        self.chat_display.unbind('<KeyPress>')
        
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"\nBạn ({timestamp})\n", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n", "user")
        
        self.chat_display.bind('<KeyPress>', self.on_chat_keypress)
        self.chat_display.see(tk.END)

    def add_bot_message(self, message):
        self.chat_display.unbind('<KeyPress>')
        
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"\nBookStore ({timestamp})\n", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n", "bot")
        
        self.chat_display.bind('<KeyPress>', self.on_chat_keypress)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        user_input = self.input_text.get('1.0', tk.END).strip()
        if user_input and not self.input_placeholder_active:
            self.add_user_message(user_input)
            self.input_text.delete('1.0', tk.END)
            self.input_text.configure(fg=self.colors['text'])
            self.input_placeholder_active = False
            self.user_has_chatted = True  # Mark that user has started chatting
            
            # Don't add placeholder anymore after first chat
            
            self.status_label.configure(text="Đang xử lý...")
            threading.Thread(target=self.process_message, args=(user_input,), daemon=True).start()

    def process_message(self, user_input):
        try:
            response = self.chatbot.process_message(user_input)
            self.message_queue.put(('bot', response))
        except Exception as e:
            self.message_queue.put(('bot', f"Xin lỗi, có lỗi xảy ra: {str(e)}"))

    def process_queue(self):
        try:
            while True:
                msg_type, message = self.message_queue.get_nowait()
                if msg_type == 'bot':
                    self.add_bot_message(message)
                    self.status_label.configure(text="Sẵn sàng")
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)

    def quick_buy(self, event=None):
        book_id = self.quick_entry.get().strip()
        if book_id:
            self.add_user_message(f"mua {book_id}")
            self.quick_entry.delete(0, tk.END)
            self.user_has_chatted = True  # Mark that user has started chatting
            threading.Thread(target=self.process_message, args=(f"mua {book_id}",), daemon=True).start()

    def check_order(self, event=None):
        order_id = self.order_entry.get().strip()
        if order_id:
            self.add_user_message(f"kiểm tra đơn hàng {order_id}")
            self.order_entry.delete(0, tk.END)
            self.user_has_chatted = True  # Mark that user has started chatting
            threading.Thread(target=self.process_message, args=(f"kiểm tra đơn hàng {order_id}",), daemon=True).start()

    def show_catalog(self):
        """Show catalog window"""
        BookCatalogWindow(self.root, self.chatbot.bookstore)

    def show_help(self):
        """Show help window"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Hướng dẫn sử dụng BookStore")
        help_window.geometry("600x500")
        help_window.configure(bg=self.colors['background'])
        
        # Header
        header = tk.Frame(help_window, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header,
                text="HƯỚNG DẪN SỬ DỤNG BOOKSTORE",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colors['primary'],
                fg=self.colors['text']).pack(pady=15)
        
        # Content
        content_frame = tk.Frame(help_window, bg=self.colors['card'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        help_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=self.colors['card'],
            fg=self.colors['text'],
            state=tk.NORMAL
        )
        help_text.pack(fill=tk.BOTH, expand=True)
        
        help_content = """TÌM KIẾM SÁCH:
• "tìm [từ khóa]" - Tìm theo tên, tác giả
• "sách về [chủ đề]" - Tìm theo thể loại

ĐẶT MUA SÁCH:
• "mua [tên sách]" - Đặt mua bằng tên
• "mua [ID sách]" - Đặt mua bằng mã sách
• Dùng ô "Mua nhanh" ở trên

KIỂM TRA ĐƠN HÀNG:
• "kiểm tra đơn hàng [mã]" - Kiểm tra trạng thái
• "đơn hàng [mã]" - Xem thông tin đơn hàng
• Dùng ô "Kiểm tra đơn hàng" ở trên

VÍ DỤ SỬ DỤNG:
• "tìm sách lập trình Python"
• "mua Đắc Nhân Tâm"
• "kiểm tra đơn hàng ORD000001"

HỖ TRỢ:
• Hotline: 1900-xxxx (24/7)
• Email: support@bookstore.com

DANH MỤC SÁCH:
• Click nút "Danh mục" để duyệt toàn bộ sách
• Tìm kiếm theo thể loại
• Copy mã sách dễ dàng"""
        
        help_text.insert('1.0', help_content)
        help_text.configure(state=tk.DISABLED)
        
        # Close button
        btn_frame = tk.Frame(help_window, bg=self.colors['background'])
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(btn_frame,
                 text="Đóng",
                 font=('Segoe UI', 10, 'bold'),
                 bg=self.colors['secondary'],
                 fg=self.colors['white'],
                 relief='flat',
                 command=help_window.destroy,
                 cursor='hand2',
                 padx=20, pady=5).pack(side=tk.RIGHT)
    
    def clear_chat(self):
        """Clear chat history"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ lịch sử chat?"):
            # Clear chat display
            self.chat_display.unbind('<KeyPress>')
            self.chat_display.delete('1.0', tk.END)
            self.chat_display.bind('<KeyPress>', self.on_chat_keypress)
            
            # Clear input field first
            self.input_text.delete('1.0', tk.END)
            
            # Reset all states
            self.user_has_chatted = False
            self.input_placeholder_active = False
            
            # Add placeholder back to input
            self.add_placeholder()
            
            self.status_label.configure(text="Đã xóa lịch sử chat")

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