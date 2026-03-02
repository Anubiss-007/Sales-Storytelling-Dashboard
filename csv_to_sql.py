import pandas as pd
import sqlite3

df = pd.read_csv("Super_StoreOrders.csv")

conn = sqlite3.connect("superstore.db")
 # connect ไฟล์ csv -> sqlite และสร้างไฟล์ชื่อ "superstore.db"

df.to_sql("sales_table", conn , if_exists="replace", index=False)
#เอาข้อมูลลงใน Table ชื่อ 'sales_table'

print("✅ แปลงไฟล์สำเร็จ! คุณได้ฐานข้อมูล superstore.db เรียบร้อยแล้ว")
conn.close()