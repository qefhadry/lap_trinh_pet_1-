import tkinter as tk
from PIL import Image, ImageTk
import random

cua_so = tk.Tk()
cua_so.overrideredirect(True)
cua_so.config(bg='black')
cua_so.wm_attributes("-transparentcolor", "black")
cua_so.wm_attributes("-topmost", True)

# Kích thước màn hình
man_hinh_rong = cua_so.winfo_screenwidth()
man_hinh_cao = cua_so.winfo_screenheight()

# Load ảnh
kich_thuoc = (200, 200)
anh_trai = Image.open("mahiru_bth.png").resize(kich_thuoc, Image.LANCZOS)
anh_keo = Image.open("mahiru_k.png").resize(kich_thuoc, Image.LANCZOS)
anh_phai = Image.open("mahiru_bth_right.png").resize(kich_thuoc, Image.LANCZOS)

tk_anh_trai = ImageTk.PhotoImage(anh_trai)
tk_anh_keo = ImageTk.PhotoImage(anh_keo)
tk_anh_phai = ImageTk.PhotoImage(anh_phai)

nhan = tk.Label(cua_so, image=tk_anh_trai, bg="black")
nhan.pack()

# Vị trí ban đầu (dưới cùng màn hình)
cua_so.geometry(f"+100+{man_hinh_cao - kich_thuoc[1]}")

# ==================== CÁC HÀM ====================

def bat_dau_keo(su_kien):
    """Khi bắt đầu kéo"""
    global dang_roi, dem_thoi_gian, tu_dong_di
    dem_thoi_gian = 0
    dang_roi = False
    tu_dong_di = False  # tắt auto move khi kéo
    cua_so.x = su_kien.x
    cua_so.y = su_kien.y
    nhan.config(image=tk_anh_keo)

def keo(su_kien):
    """Khi đang kéo"""
    global dem_thoi_gian
    dem_thoi_gian = 0
    x = cua_so.winfo_x() + su_kien.x - cua_so.x
    y = cua_so.winfo_y() + su_kien.y - cua_so.y
    cua_so.geometry(f"+{x}+{y}")

def tha_chuot(su_kien):
    """Khi thả chuột"""
    global van_toc, dem_thoi_gian, dang_roi, tu_dong_di
    dem_thoi_gian = 0
    van_toc = 0
    dang_roi = True
    tu_dong_di = True
    nhan.config(image=tk_anh_trai)
    roi_xuong()

def roi_xuong():
    """Hiệu ứng rơi"""
    global van_toc, dang_roi, dem_thoi_gian
    dem_thoi_gian = 0
    if not dang_roi:
        return
    x = cua_so.winfo_x()
    y = cua_so.winfo_y()
    muc_dat = man_hinh_cao - (kich_thuoc[1] + 10)

    if y < muc_dat:
        y += van_toc
        van_toc += 1
        cua_so.geometry(f"+{x}+{y}")
        cua_so.after(10, roi_xuong)
    elif y > muc_dat:
        nay_duoi()

def nay_duoi():
    """Nảy khi chạm đất"""
    global van_toc, dang_roi, dem_thoi_gian
    dem_thoi_gian = 0
    if not dang_roi:
        return
    x = cua_so.winfo_x()
    y = cua_so.winfo_y()
    muc_dat = man_hinh_cao - (kich_thuoc[1] + 10)

    y += van_toc
    van_toc += 1

    if y >= muc_dat:
        y = muc_dat
        van_toc = -van_toc // 2
        if abs(van_toc) < 10:
            van_toc = 0
            dang_roi = False
            cua_so.geometry(f"+{x}+{y}")
            return

    cua_so.geometry(f"+{x}+{y}")
    cua_so.after(10, nay_duoi)

def kiem_tra_thoi_gian():
    """Đếm thời gian idle"""
    global dem_thoi_gian
    dem_thoi_gian += 100
    if dem_thoi_gian >= 3000:  # 3 giây
        dem_thoi_gian = 0
        tu_dong_di_chuyen()
    cua_so.after(100, kiem_tra_thoi_gian)

def tu_dong_di_chuyen():
    """Chọn điểm đích mới"""
    global tu_dong_di
    if not tu_dong_di:
        return
    x = cua_so.winfo_x()
    dich_moi = random.randint(50, man_hinh_rong - 200)
    if abs(dich_moi - x) < 50:
        return
    bat_dau_di_chuyen(dich_moi)

def bat_dau_di_chuyen(dich_moi):
    """Di chuyển tới điểm đích"""
    global dem_thoi_gian
    if not tu_dong_di:
        return
    x = cua_so.winfo_x()
    y = cua_so.winfo_y()

    if dich_moi > x:
        toc_do = 3
        nhan.config(image=tk_anh_phai)
    else:
        toc_do = -3
        nhan.config(image=tk_anh_trai)

    if abs(x - dich_moi) > 10:
        x += toc_do
        cua_so.geometry(f"+{x}+{y}")
        cua_so.after(10, lambda: bat_dau_di_chuyen(dich_moi))
        dem_thoi_gian = 0
    else:
        cua_so.geometry(f"+{dich_moi}+{y}")

# ==================== BIẾN TOÀN CỤC ====================
dem_thoi_gian = 0
tu_dong_di = True
dang_roi = False
van_toc = 0

kiem_tra_thoi_gian()

# ==================== BIND SỰ KIỆN ====================
nhan.bind("<Button-1>", bat_dau_keo)
nhan.bind("<B1-Motion>", keo)
nhan.bind("<ButtonRelease-1>", tha_chuot)

cua_so.mainloop()
