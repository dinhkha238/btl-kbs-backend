# main.py
import uvicorn
from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware


# Thay đổi các thông tin kết nối tương ứng với cơ sở dữ liệu của bạn
host = 'localhost'
user = 'root'
password = 'anhkha123'
database = 'chtdttt'

# Kết nối đến MySQL
conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
# Tạo đối tượng cursor để thực hiện các truy vấn SQL
cursor = conn.cursor()






# Đóng cursor và kết nối
# cursor.close()
# conn.close()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/list-dieu-luat")
async def root():
    select_data_query = "SELECT * FROM tbldieuluat"
    cursor.execute(select_data_query)
    result = cursor.fetchall()
    rows_as_dict = [{"id": row[0], "tieuDe": row[1]} for row in result]
    return rows_as_dict


@app.get("/thacmac/{thac_mac_cha_value}")
async def get_thac_mac(thac_mac_cha_value: str):
        # Thực hiện truy vấn SQL
        select_query = f"SELECT * FROM tblthacmac WHERE thacMacCha = '{thac_mac_cha_value}'"
        cursor.execute(select_query)
        # Lấy kết quả
        result = cursor.fetchall()
        # Chuyển đổi kết quả thành danh sách các từ điển
        rows_as_dict = [{"id": row[0], "moTa": row[1], "thacMacCha": row[2]} for row in result]
        return rows_as_dict

@app.get("/suydien/{thac_mac_value}")
async def get_suy_dien(thac_mac_value: str):
        # Thực hiện truy vấn SQL
        select_query = f"SELECT * FROM tblsuydien WHERE idThacMac = '{thac_mac_value}'"
        cursor.execute(select_query)
        # Lấy kết quả
        result = cursor.fetchall()
        # Chuyển đổi kết quả thành danh sách các từ điển
        rows_as_dict = [{"id": row[1], "idThacMac": row[2], "idChiTietLuat": row[3]} for row in result]
        print(rows_as_dict)
        answers = []
        for row in rows_as_dict:
            select_query = f"SELECT * FROM tblchitietluat WHERE id = '{row['idChiTietLuat']}'"
            cursor.execute(select_query)
            result = cursor.fetchall()
            answers.append({"id": result[0][0], "dieuLuat": result[0][1], "tieuDe": result[0][2], "moTaChiTiet": result[0][3]})
        return answers

@app.get("/dieuluat/{id}")
async def get_dieu_luat(id: str):
       # Thực hiện truy vấn SQL
        select_query = f"SELECT * FROM tblchitietluat WHERE dieuluat = '{id}'"
        cursor.execute(select_query)
        # Lấy kết quả
        result = cursor.fetchall()
        # Chuyển đổi kết quả thành danh sách các từ điển
        rows_as_dict = [{"id": row[0],'dieuluat':row[1], "tieuDe": row[2], "moTaChiTiet": row[3]} for row in result]
        return rows_as_dict

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)