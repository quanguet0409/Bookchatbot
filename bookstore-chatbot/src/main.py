import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.gui import GUI

def main():
    print("🌟" * 20)
    print("    📚 BOOKSTORE CHATBOT 📚")
    print("🌟" * 20)
    print("\n🎨 Khởi động GUI...")
    
    try:
        gui = GUI()
        gui.run()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()
