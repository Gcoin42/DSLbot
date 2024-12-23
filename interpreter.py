import sys
import pandas as pd
from douban import fetch_douban
from lianjia import fetch_lianjia

def parse_range(range_str):
    try:
        start, end = map(int, range_str.split('-'))
        return start, end
    except ValueError:
        print("Invalid range format. Please enter in the format 'start-end'.")
        return None, None

def run_script(script_lines):
    variables = {}
    lines = script_lines.copy()
    i = 0
    labels = {}

    for idx, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) > 0 and parts[0] == 'LABEL':
            labels[parts[1]] = idx

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('#'):
            i += 1
            continue
        parts = line.split()
        cmd = parts[0]

        if cmd == 'SAY':
            message = ' '.join(parts[1:])
            print(message)
        elif cmd == 'ASK':
            message = ' '.join(parts[1:])
            answer = input(message)
            variables['$ANSWER'] = answer
        elif cmd == 'IF':
            var = parts[1]
            op = parts[2]
            value = parts[3]
            condition_true = False
            if op == '==':
                condition_true = variables.get(var, '') == value
            if 'THEN' in line:
                pass
            else:
                while i < len(lines) and 'THEN' not in lines[i]:
                    i += 1
            i_then = i
            endif_idx = i
            nest = 0
            while endif_idx < len(lines):
                if 'IF' in lines[endif_idx]:
                    nest += 1
                if 'ENDIF' in lines[endif_idx]:
                    if nest == 0:
                        break
                    else:
                        nest -= 1
                endif_idx += 1
            if condition_true:
                i = i_then
            else:
                else_idx = i_then
                found_else = False
                while else_idx < endif_idx:
                    if lines[else_idx].strip() == 'ELSE':
                        found_else = True
                        break
                    else_idx += 1
                if found_else:
                    i = else_idx + 1
                else:
                    i = endif_idx + 1
                continue
        elif cmd == 'ELSE':
            endif_idx = i + 1
            while endif_idx < len(lines) and 'ENDIF' not in lines[endif_idx]:
                endif_idx += 1
            i = endif_idx
        elif cmd == 'ENDIF':
            pass
        elif cmd == 'GOTO':
            label = parts[1]
            if label in labels:
                i = labels[label]
                continue
            else:
                print(f"Unknown label: {label}")
                sys.exit(1)
        elif cmd == 'LABEL':
            pass
        elif cmd == 'END':
            break
        elif cmd == 'PYTHON':
            python_code = []
            i += 1
            while i < len(lines) and lines[i].strip() != 'ENDPYTHON':
                python_code.append(lines[i])
                i += 1
            exec('\n'.join(python_code))
        elif cmd == 'FETCH_DOUBAN_RANGE':
            range_str = input("请输入电影排名范围 (例如 1-10): ")
            start, end = parse_range(range_str)
            if start is not None and end is not None:
                df = fetch_douban()
                df_range = df.iloc[start-1:end]
                print(df_range)
        elif cmd == 'FETCH_LIANJIA_PRICE':
            range_str = input("请输入楼盘均价范围 (例如 20000-25000): ")
            start, end = parse_range(range_str)
            if start is not None and end is not None:
                data, success = fetch_lianjia()
                if success:
                    df = pd.DataFrame(data, columns=['Name', 'Category', 'District', 'Area', 'Address', 'House Type', 'Area Size', 'Price per sqm', 'Total Price'])
                    df_filtered = df[(df['Price per sqm'] >= start) & (df['Price per sqm'] <= end)]
                    print(df_filtered)
                else:
                    print("Failed to fetch Lianjia property information.")
        else:
            print(f"Unknown command: {cmd}")
        i += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py script.txt")
        sys.exit(1)
    script_file = sys.argv[1]
    with open(script_file, 'r', encoding='utf-8') as f:
        script_lines = f.readlines()
    run_script(script_lines)