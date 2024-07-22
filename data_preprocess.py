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


input_file_path = output_file
# 1. 데이터 로드
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 2. 필요한 키 정의 (메뉴명, 재료, 제조법, 저감 비법)
required_keys = {
    "RCP_PARTS_DTLS",
    "ATT_FILE_NO_MAIN",
    "RCP_NM",
    "RCP_NA_TIP"
}

# MANUAL01부터 MANUAL06까지의 키를 포함한 집합 생성
manual_keys = [f'MANUAL{i:02}' for i in range(1, 7)]

# 3. 데이터 필터링
filtered_data = []
for item in data:
    # 필요한 키만 포함
    filtered_item = {key: item[key] for key in required_keys if key in item}
    
    # MANUAL01부터 MANUAL06까지의 항목 추가
    for manual_key in manual_keys:
        if manual_key in item:
            filtered_item[manual_key] = item[manual_key]
    
    filtered_data.append(filtered_item)
    
# 메뉴명, 재료, 제조법, 저감비법만 필터링한 파일 생성  
with open("data_preprocess_complete.json", 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=4)

print(f'필터링된 데이터가 data_preprocess_complete.json에 저장되었습니다.')


# 제조법 소팅.    
def sort_manual_steps(recipe,manual_keys):
    steps = {k: recipe[k] for k in manual_keys if k in recipe}
    for key in steps.keys():
        del recipe[key]
    
    recipe.update(steps)
    return recipe

# JSON 데이터의 각 레시피에 대해 순서 정렬 적용
sorted_data = [sort_manual_steps(data,manual_keys) for data in filtered_data]

# 결과를 새로운 JSON 파일로 저장
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=4)