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
    khung_trang_hien_tai = []   # các trang trong khung (giữ nguyên vị trí để hiển thị)
    thu_tu_su_dung = []         # đầu = ít dùng gần đây nhất, cuối = vừa dùng
    ket_qua_chi_tiet = []
    tong_so_loi = 0

    for chi_so, trang in enumerate(danh_sach_page):
        trang_bi_thay_the = "-"

        if trang in khung_trang_hien_tai:
            trang_thai = "HIT"
            # cập nhật: chuyển trang này xuống cuối (vừa dùng xong)
            thu_tu_su_dung.remove(trang)
            thu_tu_su_dung.append(trang)
        else:
            trang_thai = "FAULT"
            tong_so_loi += 1

            if len(khung_trang_hien_tai) < tong_khung:
                # còn khung trống
                khung_trang_hien_tai.append(trang)
            else:
                # khung đầy: chọn trang ít dùng gần đây nhất (đầu danh sách)
                trang_bi_thay_the = thu_tu_su_dung.pop(0)
                vi_tri = khung_trang_hien_tai.index(trang_bi_thay_the)
                khung_trang_hien_tai[vi_tri] = trang

            thu_tu_su_dung.append(trang)

        ket_qua_chi_tiet.append({
            "buoc": chi_so + 1,
            "trang": trang,
            "frames": list(khung_trang_hien_tai),
            "trang_thai": trang_thai,
            "victim": trang_bi_thay_the
        })
    return thuat_toan_fifo(tong_khung, danh_sach_page)

def thuat_toan_opt(tong_khung, danh_sach_page):
    if tong_khung <= 0:
        raise ValueError("Tổng số khung trang phải lớn hơn 0.")
 
    khung = []
    ket_qua_chi_tiet = []
    tong_so_loi = 0
 
    for chi_so, trang in enumerate(danh_sach_page):
        trang_bi_thay_the = "-"
        if trang in khung:
            trang_thai = "HIT"
        else:
            trang_thai = "FAULT"
            tong_so_loi += 1
            if len(khung) < tong_khung:
                khung.append(trang)
            else:
                # Phần chuỗi còn lại phía sau bước hiện tại
                tuong_lai = danh_sach_page[chi_so + 1:]
                xa_nhat = -1
                for t in khung:
                    if t not in tuong_lai:
                        # Không bao giờ dùng lại -> chọn luôn
                        trang_bi_thay_the = t
                        break
                    vi_tri = tuong_lai.index(t)
                    if vi_tri > xa_nhat:
                        xa_nhat = vi_tri
                        trang_bi_thay_the = t
                khung[khung.index(trang_bi_thay_the)] = trang
 
        ket_qua_chi_tiet.append({
            "buoc": chi_so + 1,
            "trang": trang,
            "frames": list(khung),
            "trang_thai": trang_thai,
            "victim": trang_bi_thay_the
        }) 
    return ket_qua_chi_tiet, tong_so_loi

def thuat_toan_second_chance(tong_khung, danh_sach_page):
    # thuật toán second chance
    return thuat_toan_fifo(tong_khung, danh_sach_page)
