import os
import sqlite3

# 데이터베이스 파일들이 있는 디렉토리 경로
directory_path = r'C:\Users\wp3wk\OneDrive\바탕 화면\국민대학교\3학년 여름방학\LLM_Project4\LLM_bootcamp-elecXsoft\test'  # 실제 경로로 변경하세요

# 병합할 최종 데이터베이스 파일 경로
merged_db_path = os.path.join(directory_path, 'merged_database.sqlite3')

# 병합할 데이터베이스 파일 목록 가져오기
db_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.sqlite3')]

# 최종 병합 데이터베이스 생성
merged_conn = sqlite3.connect(merged_db_path)
merged_cursor = merged_conn.cursor()

for db_file in db_files:
    print(f'병합 중: {db_file}')
    source_conn = sqlite3.connect(db_file)
    source_cursor = source_conn.cursor()
    
    # 소스 데이터베이스의 모든 테이블 가져오기
    source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = source_cursor.fetchall()
    
    for table_name in tables:
        table_name = table_name[0]
        print(f'  테이블 복사 중: {table_name}')
        
        # 테이블 스키마 가져오기
        source_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        create_table_sql = source_cursor.fetchone()[0]
        
        try:
            # 테이블 생성
            merged_cursor.execute(create_table_sql)
        except sqlite3.OperationalError:
            # 테이블이 이미 존재하는 경우 무시
            pass
        
        # 데이터 복사
        source_cursor.execute(f"SELECT * FROM {table_name};")
        rows = source_cursor.fetchall()
        
        if rows:
            placeholders = ', '.join(['?' for _ in rows[0]])
            insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            merged_cursor.executemany(insert_sql, rows)
        
    source_conn.close()

# 최종 병합 데이터베이스 저장 및 닫기
merged_conn.commit()
merged_conn.close()

print('병합 완료!')