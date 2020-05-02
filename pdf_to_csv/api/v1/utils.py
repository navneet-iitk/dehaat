import tabula
import copy
import pandas as pd


def get_area_and_column_coordinates_dict(json_data):
    '''
    Method to find the Area and Column coordinates of the table in the PDF
    Marks the cell containing text 'Particulars' as the top left corner of the table
    (This had to be done as the default table without area coordinates was having jumbled data)
    :param json_data:
    :return: dict with area_coordinates and column_coordinates as the keys.
    '''
    area_coordinates = list()
    columns_coordinates = list()
    if json_data:
        table = json_data[0]
        # Area under search
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
            # Loop breaks as soon as the header row and top left corner coordinates are found
            if found_top_left_corner:
                break
        area_coordinates = (top, left, bottom, right)
    return {'area_coordinates': area_coordinates, 'columns_coordinates': columns_coordinates}


def extract_data_from_dataframe(dataframe, query_variable, query_year):
    '''
    with given format of 6 columns balance sheet, this works well.
    for balance sheets having more columns, this would need update
    at present, gives one match only, the one found first. Can be refactored for multiple matchcases
    :param dataframe:
    :param query_variable:
    :param query_year:
    :return: tuple (query, value): found value for the given query_variable
    '''
    column_extensions = ['', '.1']
    for column_ext in column_extensions:
        variable_column_name = 'Particulars' + column_ext
        value_column_name = str(query_year) + column_ext
        if variable_column_name in dataframe:
            # Finding the query_variable (case-insensitive) in dataframe and corresponding whole row
            temp_dataframe = dataframe[dataframe[variable_column_name].str.contains(query_variable, na=False, case=False)]
            # check if corresponding row is found and column with the given year is present or not
            if not temp_dataframe.empty and value_column_name in dataframe:
                value = temp_dataframe[value_column_name].values[0]             # corresponding found value
                query = temp_dataframe[variable_column_name].values[0][3:]      # returned after removing 'To ' & 'By '
                return (query, value)
    return (None, None)


def get_dataframe_from_pdf(pdf_file):
    '''
    Extracts dataframes for the balancce sheet table present in the PDF file
    :param pdf_file:
    :return:
    '''
    # output format - json helps in finding coordinates of required cells
    # file deepcopied as in memory file corrupts after read_pdf operation
    json_data = tabula.read_pdf(copy.deepcopy(pdf_file), output_format="json")

    # coordinates_dict containing area coordinates and column coordinates extracted from json data
    coordinates_dict = get_area_and_column_coordinates_dict(json_data)
    area_coordinates = coordinates_dict['area_coordinates']

    # empty dataframe returned if no area coordinates found
    dataframe = pd.DataFrame()
    if area_coordinates:
        dataframe = tabula.read_pdf(copy.deepcopy(pdf_file),
                                    area=area_coordinates,
                                    columns=coordinates_dict['columns_coordinates'],
                                    pages='all',
                                    )
    return dataframe


def clean_dataframe(dataframe):
    '''
    cleans the dataframe so as to get CSV in the required format.
    :param dataframe:
    :return:
    '''
    # empty columns removed containing only na removed
    dataframe = dataframe.dropna(axis=1, how='all')

    #column names formatted - digits at end separated from name by dot removed
    dataframe.columns = dataframe.columns.str.replace(r'\.\d+', '')
    return dataframe
