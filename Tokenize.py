def f_tokenize(words, token_len):
    tokens = []
    for word in words:
        if word:
            if len(word) >= token_len:
                word = word.lower()
                word = word.replace('ё', 'е') 
                for i in range(len(word)-token_len+1):
                    tokens.append(word[i:i+token_len])
    return tokens

def f_build_vocabulary(tokens):
    tokens_counts = collections.defaultdict(int)
    for token in tokens:
        tokens_counts[token] += 1
    # frequency
    tokens_counts = {token: cnt/len(tokens) for token, cnt in tokens_counts.items()}
    # sort
    tokens_counts = dict(sorted(tokens_counts.items(), reverse=True, key=lambda item: item[1]))
    return tokens_counts
    
def f_fill_tokens(word, tokens, token_len):
    fill = {}
    word_tokens = f_tokenize([word], token_len)
    for token in tokens:
        fill[token] = 1 if token in word_tokens else 0
    return fill

pd.DataFrame.from_records([x for x in df['word'].apply(f_fill_tokens, args=(tokens, token_len))], index = df.index)
    
def f_fill_tokens_df(words, tokens, token_len, indexes):
    words_tokens = pd.DataFrame(columns=tokens)
    if len(words) != len(indexes):
        return None
    for j in range(len(words)):
        word_tokens = []
        val = []
        if words[j]:
            if len(words[j]) >= token_len:
                word = words[j].lower().replace('ё', 'е') 
                for i in range(len(word)-token_len+1):
                    word_tokens.append(word[i:i+token_len])
        for token in tokens:
            val.append(1 if token in word_tokens else 0)       
        words_tokens.loc[indexes[j]] = val  
    return words_tokens

f_fill_tokens_df(list(df['word']), tokens, token_len, df.index)

def f_tokenize_df(words, token_len):
    tokens = []
    for word in words:
        word_tokens = []
        if word:
            if len(word) >= token_len:
                word = word.lower()
                word = word.replace('ё', 'е') 
                for i in range(len(word)-token_len+1):
                    word_tokens.append(word[i:i+token_len])
        tokens.append(word_tokens)
    return tokens

df['tokens'] = f_tokenize_df(list(df['word']), token_len)

for token in tokens:
    df[token] = 0
    
for i in df.index:
    for token in df.loc[i, 'tokens']:
        if token in tokens:
            df.loc[i, token] = 1



