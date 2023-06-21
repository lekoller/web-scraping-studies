import pandas as pd


def process_xlsx_file(file_path: str):
    sheets = pd.read_excel(file_path, sheet_name=None)

    for sheet_name, df in sheets.items():
        if sheet_name == list(sheets.keys())[0]:
            continue

        if sheet_name == list(sheets.keys())[1]:

            documents = df.to_dict(orient='records')
            insert_dict = {}
            titles = []
            titles_index = 0
            table_index = 0
            
            for index, document in enumerate(documents):
                values = list(document.values())
                
                # check if all is nan
                if all([type(value) == float and value != value for value in values]):
                    continue

                if any([type(value) == float and value != value for value in values]):
                    big_one = ''
                    if type(values[0]) == str:
                        big_one = values[0]
                        insert_dict[big_one] = {}

                    string_values = []
                    
                    for value in values:
                        in_dict = {}

                        if type(value) == str and value != '' and value != big_one:
                            string_values.append(value.strip().replace(" ", ""))
                        elif value == big_one:
                            continue
                        else:
                            string_values.append('')

                    if len(string_values) > 1:
                        # check if all is empty string
                        if all([value == '' for value in string_values]):
                            continue

                        # title_values = string_values
                        title_values = {}

                        for i, value in enumerate(string_values):
                            if value != '':
                                title_values[value] = 0
                                continue

                            keys = list(title_values.keys())

                            if keys:
                                last_key = str(keys[-1])

                                title_values[last_key] += 1
                                
                        # print(title_values)
                        titles.append(title_values)
                        
                else:
                    titles_index += 1
                    keys = list(insert_dict.keys())

                    if keys:
                        last_key = str(keys[-1])

                        insert_dict[last_key][values[0]] = {}

                # check if at least one is nan
            print()
            print(titles)
            print()
            # print(json.dumps(insert_dict, indent=2))
            # print()

            # print(json.dumps(transform_data(titles), indent=2))


            # for insert_dict_key in insert_dict.keys():
            #     for item_key in insert_dict[insert_dict_key].keys():

        documents = df.to_dict(orient='records')
        # collection_name = sheet_name.replace(' ', '_').lower()

        # repository = GenericRepository(db_name='brutes', collection_name=collection_name)

        # for document in documents:
        #     print(document)
        #     repository.insert_document(document)
