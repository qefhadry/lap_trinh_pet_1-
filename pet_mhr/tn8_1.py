import sys
import random
import os
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QMouseEvent

class MahiruWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Biến toàn cục
        self.dem_thoi_gian = 0
        self.tu_dong_di = True
        self.dang_roi = False
        self.van_toc = 0
        self.dragging = False
        self.drag_position = QPoint()
        self.dich_moi = 0
        
        # Thiết lập cửa sổ
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        
        # Kích thước màn hình
        screen = QApplication.primaryScreen().geometry()
        self.man_hinh_rong = screen.width()
        self.man_hinh_cao = screen.height()
        
        # Load ảnh với kiểm tra file
        self.kich_thuoc = 200  # Kích thước cố định
        
        # Tạo ảnh mặc định nếu không tìm thấy file
        self.tao_anh_mac_dinh()
        
        # Thử load ảnh từ file
        if not self.tai_anh_tu_file():
            print("Không thể tải ảnh từ file, sử dụng ảnh mặc định")
        
        # Tạo label hiển thị ảnh - QUAN TRỌNG: đặt kích thước cố định
        self.nhan = QLabel(self)
        self.nhan.setPixmap(self.anh_trai)
        self.nhan.setStyleSheet("background: transparent; border: none;")
        self.nhan.setFixedSize(self.kich_thuoc, self.kich_thuoc)  # QUAN TRỌNG
        
        # Đặt kích thước cửa sổ bằng kích thước ảnh
        self.setFixedSize(self.kich_thuoc, self.kich_thuoc)
        
        # Vị trí ban đầu (dưới cùng màn hình)
        self.move(100, self.man_hinh_cao - self.kich_thuoc - 10)
        
        # Timer cho các hiệu ứng
        self.timer_roi = QTimer()
        self.timer_roi.timeout.connect(self.roi_xuong)
        
        self.timer_nay = QTimer()
        self.timer_nay.timeout.connect(self.nay_duoi)
        
        self.timer_kiem_tra = QTimer()
        self.timer_kiem_tra.timeout.connect(self.kiem_tra_thoi_gian)
        self.timer_kiem_tra.start(100)
        
        self.timer_di_chuyen = QTimer()
        self.timer_di_chuyen.timeout.connect(self.di_chuyen_tu_dong)
        
    def tao_anh_mac_dinh(self):
        """Tạo ảnh mặc định nếu không tìm thấy file"""
        # Tạo ảnh tròn màu với chữ để dễ nhận biết
        pixmap = QPixmap(self.kich_thuoc, self.kich_thuoc)
        pixmap.fill(Qt.transparent)
        
        # Ảnh trái (xanh)
        self.anh_trai = QPixmap(self.kich_thuoc, self.kich_thuoc)
        self.anh_trai.fill(Qt.blue)
        
        # Ảnh kéo (đỏ)
        self.anh_keo = QPixmap(self.kich_thuoc, self.kich_thuoc)
        self.anh_keo.fill(Qt.red)
        
        # Ảnh phải (xanh lá)
        self.anh_phai = QPixmap(self.kich_thuoc, self.kich_thuoc)
        self.anh_phai.fill(Qt.green)
        
    def tai_anh_tu_file(self):
        """Thử tải ảnh từ file, trả về True nếu thành công"""
        try:
            # Kiểm tra file tồn tại và load với kích thước cố định
            if os.path.exists("mahiru_bth.png"):
                self.anh_trai = QPixmap("mahiru_bth.png").scaled(
                    self.kich_thuoc, self.kich_thuoc, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
            
            if os.path.exists("mahiru_k.png"):
                self.anh_keo = QPixmap("mahiru_k.png").scaled(
                    self.kich_thuoc, self.kich_thuoc,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            
            if os.path.exists("mahiru_bth_right.png"):
                self.anh_phai = QPixmap("mahiru_bth_right.png").scaled(
                    self.kich_thuoc, self.kich_thuoc,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            return True
        except Exception as e:
            print(f"Lỗi khi tải ảnh: {e}")
            return False
    
    def mousePressEvent(self, event: QMouseEvent):
        """Khi bắt đầu kéo"""
        if event.button() == Qt.LeftButton:
            self.dem_thoi_gian = 0
            self.dang_roi = False
            self.tu_dong_di = False  # tắt auto move khi kéo
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.nhan.setPixmap(self.anh_keo)
            
            # Dừng các timer
            self.timer_roi.stop()
            self.timer_nay.stop()
            self.timer_di_chuyen.stop()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Khi đang kéo"""
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.dem_thoi_gian = 0
            new_pos = event.globalPos() - self.drag_position
            self.move(new_pos)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Khi thả chuột"""
        if event.button() == Qt.LeftButton and self.dragging:
            self.dem_thoi_gian = 0
            self.van_toc = 0
            self.dang_roi = True
            self.tu_dong_di = True
            self.dragging = False
            self.nhan.setPixmap(self.anh_trai)
            
            # Bắt đầu hiệu ứng rơi
            self.timer_roi.start(10)
    
    def roi_xuong(self):
        """Hiệu ứng rơi"""
        self.dem_thoi_gian = 0
        if not self.dang_roi:
            self.timer_roi.stop()
            return
            
        x = self.x()
        y = self.y()
        muc_dat = self.man_hinh_cao - self.kich_thuoc - 10  # Cách đáy 10px

        if y < muc_dat:
            y += self.van_toc
            self.van_toc += 1
            self.move(x, y)
        else:
            self.timer_roi.stop()
            self.timer_nay.start(10)
    
    def nay_duoi(self):
        """Nảy khi chạm đất"""
        self.dem_thoi_gian = 0
        if not self.dang_roi:
            self.timer_nay.stop()
            return
            
        x = self.x()
        y = self.y()
        muc_dat = self.man_hinh_cao - self.kich_thuoc - 10

        y += self.van_toc
        self.van_toc += 1

        if y >= muc_dat:
            y = muc_dat
            self.van_toc = -self.van_toc // 2
            if abs(self.van_toc) < 5:  # Ngưỡng dừng nhỏ hơn
                self.van_toc = 0
                self.dang_roi = False
                self.move(x, y)
                self.timer_nay.stop()
                return

        self.move(x, y)
    
    def kiem_tra_thoi_gian(self):
        """Đếm thời gian idle"""
        self.dem_thoi_gian += 100
        if self.dem_thoi_gian >= 3000:  # 3 giây
            self.dem_thoi_gian = 0
            self.tu_dong_di_chuyen()
    
    def tu_dong_di_chuyen(self):
        """Chọn điểm đích mới"""
        if not self.tu_dong_di or self.dragging or self.dang_roi:
            return
            
        x = self.x()
        dich_moi = random.randint(50, self.man_hinh_rong - self.kich_thuoc - 50)
        if abs(dich_moi - x) < 50:
            return
            
        self.bat_dau_di_chuyen(dich_moi)
    
    def bat_dau_di_chuyen(self, dich_moi):
        """Di chuyển tới điểm đích"""
        if not self.tu_dong_di or self.dragging:
            return
            
        self.dich_moi = dich_moi
        self.timer_di_chuyen.start(10)
    
    def di_chuyen_tu_dong(self):
        """Hàm di chuyển được gọi bởi timer"""
        x = self.x()
        y = self.y()

        if self.dich_moi > x:
            toc_do = 3
            self.nhan.setPixmap(self.anh_phai)
        else:
            toc_do = -3
            self.nhan.setPixmap(self.anh_trai)

        if abs(x - self.dich_moi) > 10:
            x += toc_do
            self.move(x, y)
            self.dem_thoi_gian = 0
        else:
            self.move(self.dich_moi, y)
            self.timer_di_chuyen.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Kiểm tra và thông báo
    print("Đang khởi chạy ứng dụng...")
    print("Lưu ý: Đặt file ảnh trong cùng thư mục với script")
    print("Các file ảnh cần có: mahiru_bth.png, mahiru_k.png, mahiru_bth_right.png")
    print(f"Kích thước ảnh: 200x200 pixels")
    
    window = MahiruWindow()
    window.show()
    sys.exit(app.exec_())