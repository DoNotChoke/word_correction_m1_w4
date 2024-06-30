import streamlit as st


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words


vocabs = load_vocab(file_path='./vocab.txt')


def levenshtein_distance(token1, token2):
    n = len(token1)
    m = len(token2)
    dp = [[0 for _ in range(m+1)] for _ in range(2)]
    for j in range(m+1):
        dp[0][j] = j
    for i in range(n+1):
        for j in range(m+1):
            if j == 0:
                dp[1][j] = i
            else:
                x = dp[0][j]+1
                y = dp[1][j-1]+1
                z = dp[0][j-1]
                if token1[i-1] != token2[j-1]:
                    z += 1
                d = min(x, y)
                d = min(d, z)
                dp[1][j] = d
        for j in range(m+1):
            dp[0][j] = dp[1][j]
    distance = dp[1][m]
    return distance


def main():
    st.title("Word correction using levenshtein distance")
    st.markdown('''
        :red[Type] :orange[your] :green[word] :blue[here]''')
    word = st.text_input('Word:')
    if st.button("Compute"):
        diction = dict()
        for vocab in vocabs:
            diction[vocab] = levenshtein_distance(word, vocab)
        sort_dict = dict(sorted(diction.items(), key=lambda item: item[1]))
        matching_word = list(sort_dict.keys())[0]
        st.write('Correct word: ', matching_word)
        col1, col2 = st.columns(2)
        col1.write("Vocabulary: ")
        col2.write("Distance: ")
        for item in sort_dict:
            col1.write(item)
            col2.write(sort_dict[item])

if __name__== "__main__":
    main()
