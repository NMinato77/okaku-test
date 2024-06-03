import random
import sys
import os
import pickle

HISTORY_FILE = 'text_history.pkl'
ORIGINAL = ['2024年７月10日13:00 《space》は、', 
            'にかいだて', 
            'の建物に', 
            'もとのたてもの', 
            'とは', 
            'まったくことなる', 
            '空間、ガラス張りのホワイトキューブが', 
            'うめこまれて', 
            'います。コピー・アンド・ペーストのように、', 
            'もと', 
            'の空間の', 
            'いちぶ', 
            'が切り取られ、', 
            'あらた', 
            'な空間が', 
            'ぼうりょく', 
            '的な', 
            'ちから', 
            'を持って', 
            'はりつけられ', 
            'ています。近づいて', 
            'みる', 
            'と、', 
            'にかい', 
            'の窓は', 
            'えいかく', 
            'に、', 
            'きぞん', 
            'の', 
            'ゆか', 
            'は消え', 
            'さった', 
            'ように、ホワイトキューブの空間に', 
            'しんしょく', 
            'されています。建物の', 
            'うら', 
            '側に回ると', 
            'そとかいだん', 
            'が現れ、', 
            'そのかいだんを', 
            '上がって、ガラスの', 
            'とびら', 
            'を開けて中の空間に入ることができます。そこは十和田市現代美術館の展示室と同じく、外光が白い空間を満たしています。']

class Transform:
    def __init__(self, txt):
        self.txt = txt

    def _convert_to_base_hiragana(self, char):
        # 変換辞書を定義
        conversion_dict = {
            'が': 'か', 'ぎ': 'き', 'ぐ': 'く', 'げ': 'け', 'ご': 'こ',
            'ざ': 'さ', 'じ': 'し', 'ず': 'す', 'ぜ': 'せ', 'ぞ': 'そ',
            'だ': 'た', 'ぢ': 'ち', 'づ': 'つ', 'で': 'て', 'ど': 'と',
            'ば': 'は', 'び': 'ひ', 'ぶ': 'ふ', 'べ': 'へ', 'ぼ': 'ほ',
            'ぱ': 'は', 'ぴ': 'ひ', 'ぷ': 'ふ', 'ぺ': 'へ', 'ぽ': 'ほ',
            'ぁ': 'あ', 'ぃ': 'い', 'ぅ': 'う', 'ぇ': 'え', 'ぉ': 'お',
            'っ': 'つ', 'ゃ': 'や', 'ゅ': 'ゆ', 'ょ': 'よ', 'ゎ': 'わ'
        }
        # 濁点・半濁点・小文字を通常のひらがなに変換
        return conversion_dict.get(char, char)
    
    def _hiragana_to_number_map(self):
        hiragana_list = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
        return {char: i + 1 for i, char in enumerate(hiragana_list)}
    
    def _number_to_hiragana_map(self):
        hiragana_list = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
        return {i + 1: char for i, char in enumerate(hiragana_list)}
    
    def _transform_hiragana_string(self, input_text):
        input_txt = ''.join([self._convert_to_base_hiragana(char) for char in input_text])
        
        # Step 2: Create the mappings
        hira_to_num = self._hiragana_to_number_map()
        num_to_hira = self._number_to_hiragana_map()
    
        # Step 3: Calculate the sum of unique integers for the input string
        total_sum = sum(hira_to_num[char] for char in input_text if char in hira_to_num)
    
        # Step 4 & 5: Transform each character's unique integer
        new_numbers = [(hira_to_num[char] + total_sum) % 46 for char in input_text if char in hira_to_num]
        new_numbers = [num if num != 0 else 46 for num in new_numbers]  # Handle modulo 46 result 0
    
        # Step 6: Convert new numbers back to hiragana
        transformed_text = ''.join(num_to_hira[num] for num in new_numbers)
    
        return transformed_text
    
    def _transform_strings(self, original_list, search_string, replacement_string):
        hiragana_list = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
            
        # 各文字列を結合して1つの大きな文字列にする
        concatenated_string = ''.join(original_list)
        
        replace_string = []
        for search_char in search_string:
            index = hiragana_list.index(search_char)
            char = search_char
            while (not char in concatenated_string) or (char in replace_string):
                index =  index + 1
                char = hiragana_list[index]
            replace_string.append(char)

        search_string = replace_string
        
        # 変換用の辞書を作成
        conversion_dict = {search_char: replacement_char for search_char, replacement_char in zip(search_string, replacement_string)}
    
        # 検索文字のすべての位置を記録する辞書
        positions = {search_char: [] for search_char in search_string}
    
        # すべての検索文字の位置を収集する
        for index, char in enumerate(concatenated_string):
            if char in positions:
                positions[char].append(index)
        
        # 変換後の文字列を分割されたリストとして保持
        concatenated_string = list(concatenated_string)
    
        # すべての検索文字について処理する
        for search_char, replacement_char in conversion_dict.items():
            if positions[search_char]:
                # ランダムに位置を選択して変換する
                random_index = random.choice(positions[search_char])
                concatenated_string[random_index] = replacement_char
        
        # 元のリストの構造に従って文字列を再構築する
        new_original_list = []
        start_index = 0
        for string in original_list:
            new_original_list.append(''.join(concatenated_string[start_index:start_index + len(string)]))
            start_index += len(string)
    
        return new_original_list
    
    def transform(self, name):
        unchangeable_txt = [self.txt[2*i] for i in range(int(len(self.txt)/2)+1)]
        changeable_txt = [self.txt[2*i+1] for i in range(int(len(self.txt)/2))]
    
        changed_name = self._transform_hiragana_string(name)
        converted_txt = self._transform_strings(changeable_txt, changed_name, name)

        new_txt = [char for sublist in[[converted_txt[i], unchangeable_txt[i+1]] for i in range(len(converted_txt))] for char in sublist]
        new_txt = [unchangeable_txt[0]] + new_txt
        self.txt = new_txt

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'rb') as file:
            return pickle.load(file)
    return ORIGINAL  # 初期状態のoriginal_txtをリストで保持

def save_history(history):
    with open(HISTORY_FILE, 'wb') as file:
        pickle.dump(history, file)

if __name__ == '__main__':
    input_text = sys.argv[1]
    original = load_history()
    txt = Transform(original)
    txt.transform(input_text)
    save_history(txt.txt)
    print(''.join(txt.txt))
    print(''.join(original))