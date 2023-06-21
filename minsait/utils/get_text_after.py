def get_text_after(snippet: str, text: str) -> str:
    list_text = text.split(' ')
    list_snippet = snippet.split(' ')
    words_in_snippet = len(list_snippet)

    for i, word in enumerate(list_text):
        word = word.lower()

        if word == list_snippet[0].lower():
            matches = 0

            for j, snippet_word in enumerate(list_snippet):
                if list_text[i + j].lower() != snippet_word.lower():
                    break

                matches += 1
            
            if matches == words_in_snippet:
                return ' '.join(list_text[i + matches:])

    return ''