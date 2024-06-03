import sys

def process_text(text):
    # ここにテキスト処理ロジックを実装
    return text.upper()

if __name__ == '__main__':
    input_text = sys.argv[1]
    output_text = process_text(input_text)
    print(output_text)