def transform_data(titles):
    output = [{}]
    dict_index = 0

    for title in titles:
        if all(value == 0 for value in title.values()):
            dict_index += 1
            continue

        next_line = []
        
        try:
            next_line = list(titles[titles.index(title) + 1].keys())
        except:
            continue

        current_line = list(title.keys())

    return output