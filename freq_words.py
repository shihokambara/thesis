# 頻出単語

filename = 'quaran'
f = open(filename+'_readable.dict')
lines = f.read().split('\n')
f.close()


new_file = open(filename+'_freq.txt', 'w')
freq_words = []

for line in lines:
  row = line.split('\t')
  if len(row) == 3:
    if int(row[2]) > 50: # 何回以上登場するかの閾値
        word = row[1]
        freq_words.append(word) # 単語を追加
        print(word + '    ' + row[2] , file=new_file)




