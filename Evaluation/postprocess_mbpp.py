import json
import re

def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [json.loads(line.strip()) for line in file]
    return lines

def write_jsonl(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(json.dumps(entry) + '\n')

def extract_code_blocks(solution):
    code_blocks = re.findall(r'```python(.*?)```', solution, re.DOTALL)
    return code_blocks

# 主函数
def process_files(file_path1, output_file):
    data1 = read_jsonl(file_path1)
    
    updated_data = []
    
    for entry in data1:
        new_entry = entry
        code_blocks = extract_code_blocks(entry['solution'])
        if len(code_blocks) > 0:
            cleaned_code = code_blocks[0].strip().strip()
            new_entry['solution'] = cleaned_code 
            updated_data.append(new_entry)
        else:
            new_entry['solution'] = "" 
            updated_data.append(new_entry)
    write_jsonl(updated_data, output_file)

file_path1 = 'AutoCoder_Mbpp+_new.jsonl'
output_file = 'AutoCoder_Mbpp+_new_wo_test-sanitized.jsonl'

process_files(file_path1, output_file)
