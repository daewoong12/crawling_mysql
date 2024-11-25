import pymysql
import pandas as pd

# MySQL 연결 설정
db_config = {
    'host': 'localhost',        # MySQL 서버 주소
    'user': 'root',             # MySQL 사용자 이름
    'password': '1234',         # MySQL 비밀번호
    'port': 3306                # MySQL 포트 (기본값: 3306)
}

# CSV 파일 읽기
csv_file = 'products.csv'
data = pd.read_csv(csv_file)

# MySQL 연결
connection = pymysql.connect(
    host=db_config['host'],
    user=db_config['user'],
    password=db_config['password'],
    port=db_config['port']
)
cursor = connection.cursor()

# 데이터베이스 생성
cursor.execute("CREATE DATABASE IF NOT EXISTS product_db;")

# 데이터베이스 사용
cursor.execute("USE product_db;")

# 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255),
        url TEXT,
        price VARCHAR(50),
        rating VARCHAR(10)
    );
""")

# 데이터 삽입 쿼리
insert_query = """
    INSERT INTO products (product_name, url, price, rating)
    VALUES (%s, %s, %s, %s)
"""

# 데이터 삽입
# iterrows() -> pandas의 메서드로, DataFrame의 각 행(row)을 순회하며 (index, row) 형식의 튜플을 반환
for index, row in data.iterrows():
    cursor.execute(insert_query, (row['제품명'], row['URL'], row['가격'], row['평점']))

# 커밋
connection.commit()

# 연결 종료
cursor.close()
connection.close()
