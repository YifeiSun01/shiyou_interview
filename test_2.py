def replace_repeated_chars(input_str, k):
    modified_str = list(input_str)
    for i in range(len(input_str)):
        start_index = max(0, i - k)
        for j in range(start_index, i):
            if input_str[i] == input_str[j]:
                modified_str[i] = '-'
                break
    return ''.join(modified_str)

print(replace_repeated_chars("abcdefaxc", 10))
print(replace_repeated_chars("abcdefaxcqwertba", 10))