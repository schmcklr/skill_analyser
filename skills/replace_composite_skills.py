def replace_strings_in_column(df, column_name, old_strings):
    for old_string in old_strings:
        new_string = old_string.replace(" ", "-")
        print(new_string)
        df[column_name] = df[column_name].replace(old_string, new_string, regex=True)
    return df
