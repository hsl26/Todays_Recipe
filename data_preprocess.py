import json
# JSON 파일 경로
input_file = r'C:\Users\wp3wk\OneDrive\바탕 화면\국민대학교\3학년 여름방학\LLM_Project4\LLM_bootcamp-elecXsoft\data_rows.json' # 본인 파일 경로로 바꾸시면 됩니다.
output_file = 'data_preprocess.json'

# 비어있는 속성을 제거하는 함수
def remove_empty_properties(data):
    if isinstance(data, dict):
        return {k: remove_empty_properties(v) for k, v in data.items() if v}
    return data

# JSON 파일 읽기
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 리스트 내의 각 딕셔너리에서 비어있는 속성 제거
cleaned_data = [remove_empty_properties(item) for item in data] 

# 결과를 JSON 파일로 저장
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

print(f"비어있는 속성이 제거된 JSON 데이터를 '{output_file}' 파일로 저장했습니다.")