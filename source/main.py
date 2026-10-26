import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import algorithms

tong_khung_nho = 0
danh_sach_truy_xuat = []
nhat_ky_mo_phong = []
vi_tri_buoc = 0
dem_loi_trang = 0

def tai_file_du_lieu():
    global tong_khung_nho, danh_sach_truy_xuat
    duong_dan_tep = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not duong_dan_tep: return
    try:
        with open(duong_dan_tep, 'r', encoding='utf-8') as f:
            cac_dong = list(csv.reader(f))
            tong_khung_nho = int(cac_dong[0][0].strip())
            danh_sach_truy_xuat = [int(ky_tu.strip()) for ky_tu in cac_dong[1] if ky_tu.strip() != ""]
            if tong_khung_nho <= 0 or len(danh_sach_truy_xuat) == 0:
                raise ValueError()
        lbl_file.config(text=f"Đã tải: {tong_khung_nho} Khung | Chuỗi: {danh_sach_truy_xuat}", fg="green")
        thiet_lap_chuong_trinh()
    except:
        messagebox.showerror("Lỗi dữ liệu", "Cấu trúc file CSV không hợp lệ!")

def thiet_lap_chuong_trinh():
    global nhat_ky_mo_phong, vi_tri_buoc, dem_loi_trang
    if tong_khung_nho <= 0: return
    
    lua_chon_tt = cb_algo.get()
    if lua_chon_tt == "FIFO": 
        nhat_ky_mo_phong, dem_loi_trang = algorithms.thuat_toan_fifo(tong_khung_nho, danh_sach_truy_xuat)
    elif lua_chon_tt == "LRU": 
        nhat_ky_mo_phong, dem_loi_trang = algorithms.thuat_toan_lru(tong_khung_nho, danh_sach_truy_xuat)
    elif lua_chon_tt == "OPT": 
        nhat_ky_mo_phong, dem_loi_trang = algorithms.thuat_toan_opt(tong_khung_nho, danh_sach_truy_xuat)
    else: 
        nhat_ky_mo_phong, dem_loi_trang = algorithms.thuat_toan_second_chance(tong_khung_nho, danh_sach_truy_xuat)

    vi_tri_buoc = 0
    bang.delete(*bang.get_children())
    hien_thi_khung_ram([], "-", "-", "-")
    lbl_kq.config(text="Đã sẵn sàng mô phỏng.")

def hien_thi_khung_ram(ds_frame, trang_yeu_cau, trang_thai, victim):
    for w in khung_ram.winfo_children():
        w.destroy()

    mau_nen = "#ffcccc" if trang_thai == "FAULT" else ("#ccffcc" if trang_thai == "HIT" else "#eeeeee")
    tk.Label(khung_ram, text=f"Yêu cầu: {trang_yeu_cau}\nTrạng thái: {trang_thai}\nVictim: {victim}", 
             font=("Arial", 10, "bold"), bg=mau_nen, width=16, height=4, relief="solid", bd=1).pack(side="left", padx=10)

    for idx, gia_tri in enumerate(ds_frame):
        mau_o = "#ffd966" if gia_tri == trang_yeu_cau else "white"
        tk.Label(khung_ram, text=f"Slot {idx+1}\n\n{gia_tri}", 
                 font=("Arial", 11, "bold"), bg=mau_o, width=10, height=4, relief="ridge", bd=2).pack(side="left", padx=5)

def xu_ly_tung_buoc():
    global vi_tri_buoc
    if not nhat_ky_mo_phong:
        messagebox.showwarning("Cảnh báo", "Hãy nạp file CSV trước tiên!")
        return
    if vi_tri_buoc >= len(nhat_ky_mo_phong):
        messagebox.showinfo("Thông báo", "Đã chạy hết toàn bộ tiến trình!")
        return

    b = nhat_ky_mo_phong[vi_tri_buoc]
    hien_thi_khung_ram(b["frames"], b["trang"], b["trang_thai"], b["victim"])
    
    row_id = bang.insert("", "end", values=(b["buoc"], b["trang"], str(b["frames"]), b["trang_thai"], b["victim"]))
    bang.see(row_id)
    
    vi_tri_buoc += 1
    lbl_kq.config(text=f"Bước: {vi_tri_buoc}/{len(nhat_ky_mo_phong)} | Tổng lỗi trang (Page Faults): {dem_loi_trang}")

def chay_toan_bo():
    if not nhat_ky_mo_phong:
        messagebox.showwarning("Cảnh báo", "Hãy nạp file CSV trước tiên!")
        return
    while vi_tri_buoc < len(nhat_ky_mo_phong):
        xu_ly_tung_buoc()

def ghi_ra_file_csv():
    if not nhat_ky_mo_phong: return
    duong_dan = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if duong_dan:
        with open(duong_dan, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["Bước", "Trang yêu cầu", "Trạng thái RAM", "Kết quả", "Trang thay thế"])
            for b in nhat_ky_mo_phong:
                writer.writerow([b["buoc"], b["trang"], str(b["frames"]), b["trang_thai"], b["victim"]])
        messagebox.showinfo("Hoàn tất", "Đã xuất file kết quả thành công!")

# Thiết kế cửa sổ GUI
root = tk.Tk()
root.title("Mô phỏng Thay thế trang (OS_VME_13)")
root.geometry("780x560")

khung_nut = tk.Frame(root, pady=8)
khung_nut.pack()

tk.Button(khung_nut, text="1. Chọn file CSV", command=tai_file_du_lieu, bg="#d9edf7", width=14).grid(row=0, column=0, padx=4)
cb_algo = ttk.Combobox(khung_nut, values=["FIFO", "LRU", "OPT", "Second-Chance"], state="readonly", width=14)
cb_algo.current(0)
cb_algo.grid(row=0, column=1, padx=4)
cb_algo.bind("<<ComboboxSelected>>", lambda e: thiet_lap_chuong_trinh())

tk.Button(khung_nut, text="2. Chạy từng bước", command=xu_ly_tung_buoc, bg="#fcf8e3", width=16).grid(row=0, column=2, padx=4)
tk.Button(khung_nut, text="3. Chạy tất cả", command=chay_toan_bo, bg="#dff0d8", width=13).grid(row=0, column=3, padx=4)
tk.Button(khung_nut, text="4. Đặt lại", command=thiet_lap_chuong_trinh, width=10).grid(row=0, column=4, padx=4)
tk.Button(khung_nut, text="5. Xuất CSV", command=ghi_ra_file_csv, bg="#f2dede", width=11).grid(row=0, column=5, padx=4)

lbl_file = tk.Label(root, text="Chưa nạp tệp dữ liệu", fg="gray")
lbl_file.pack()

khung_ram_ngoai = tk.LabelFrame(root, text="Trực quan hóa Khung nhớ RAM", padx=10, pady=10)
khung_ram_ngoai.pack(fill="x", padx=15, pady=8)
khung_ram = tk.Frame(khung_ram_ngoai, height=90)
khung_ram.pack()

cot = ("Bước", "Trang yêu cầu", "Trạng thái RAM", "Kết quả (Hit/Fault)", "Trang bị thay (Victim)")
bang = ttk.Treeview(root, columns=cot, show="headings", height=11)
for c in cot:
    bang.heading(c, text=c)
    bang.column(c, width=140, anchor="center")
bang.pack(expand=True, fill="both", padx=15, pady=5)

lbl_kq = tk.Label(root, text="Tổng lỗi trang (Page Faults): 0", font=("Arial", 11, "bold"), fg="red")
lbl_kq.pack(pady=8)

root.mainloop()