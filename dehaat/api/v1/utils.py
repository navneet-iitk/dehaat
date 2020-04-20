import tabula
import copy
import pandas as pd


def get_area_and_column_coordinates_dict(json_data):
    area_coordinates = list()
    columns_coordinates = list()
    if json_data:
        table = json_data[0]
        top = table['top']
        left = table['left']
        bottom = table['bottom']
        right = table['right']
        found_top_left_corner = False
        for row in table['data']:
            if row[0]['text'] != 'Particulars':
                continue
            for column in row:
                if not found_top_left_corner:
                    top = column['top']
                    left = column['left']
                    found_top_left_corner = True
                columns_coordinates.append(column['left'])
            if found_top_left_corner:
                break
        area_coordinates = (top, left, bottom, right)
    return {'area_coordinates': area_coordinates, 'columns_coordinates': columns_coordinates}


def extract_data_from_df(df, query_variable, query_year):
    column_extensions = ['', '.1']
    for column_ext in column_extensions:
        variable_column_name = 'Particulars' + column_ext
        value_column_name = str(query_year) + column_ext
        if variable_column_name in df:
            temp_df = df[df[variable_column_name].str.contains(query_variable, na=False, case=False)]
            if not temp_df.empty and value_column_name in df:
                value = temp_df[value_column_name].values[0]
                query = temp_df[variable_column_name].values[0][3:]
                return (query, value)
    return (None, None)


def get_df_from_pdf(pdf_file):
    json_data = tabula.read_pdf(copy.deepcopy(pdf_file), output_format="json")
    coordinates_dict = get_area_and_column_coordinates_dict(json_data)
    area_coordinates = coordinates_dict['area_coordinates']
    df = pd.DataFrame()
    if area_coordinates:
        df = tabula.read_pdf(copy.deepcopy(pdf_file),
                             area=area_coordinates,
                             columns=coordinates_dict['columns_coordinates'],
                             pages='all',
                             )
    return df


def clean_df(df):
    df = df.dropna(axis=1, how='all')
    df.columns = df.columns.str.replace(r'\.\d+', '')
    return df
