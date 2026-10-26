#thuật toán fifo này là mẫu nên ai phụ trách phải viết lại
def thuat_toan_fifo(tong_khung, danh_sach_page):
    khung_trang_hien_tai = []
    ket_qua_chi_tiet = []
    tong_so_loi = 0
    con_tro_fifo = 0

    for chi_so, trang in enumerate(danh_sach_page):
        trang_bi_thay_the = "-"
        if trang in khung_trang_hien_tai:
            trang_thai = "HIT"
        else:
            trang_thai = "FAULT"
            tong_so_loi += 1
            if len(khung_trang_hien_tai) < tong_khung:
                khung_trang_hien_tai.append(trang)
            else:
                trang_bi_thay_the = khung_trang_hien_tai[con_tro_fifo]
                khung_trang_hien_tai[con_tro_fifo] = trang
                con_tro_fifo = (con_tro_fifo + 1) % tong_khung

        ket_qua_chi_tiet.append({
            "buoc": chi_so + 1,
            "trang": trang,
            "frames": list(khung_trang_hien_tai),
            "trang_thai": trang_thai,
            "victim": trang_bi_thay_the
        })

    return ket_qua_chi_tiet, tong_so_loi

def thuat_toan_lru(tong_khung, danh_sach_page):
    # thuật toán lru
    return thuat_toan_fifo(tong_khung, danh_sach_page)

def thuat_toan_opt(tong_khung, danh_sach_page):
    # thuật toán opt
    return thuat_toan_fifo(tong_khung, danh_sach_page)

def thuat_toan_second_chance(tong_khung, danh_sach_page):
    # thuật toán second chance
    return thuat_toan_fifo(tong_khung, danh_sach_page)