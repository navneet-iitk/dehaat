import sys, os
from pdf_to_csv.api.v1 import utils as v1_utils

if __name__ == '__main__':
    '''
    Script file to convert a balance sheet PDF file of given format to CSV file in the same directory
    file input is given as the first argument when launching the script through the command line
    '''
    input_pdf_file = sys.argv[1]
    file_directory, file = os.path.split(input_pdf_file)
    file_name, extension = os.path.splitext(file)

    #check for valid file extension - Only PDF allowed
    if extension != '.pdf':
        raise SystemExit('PDF file required. Please run again with pdf file as command line argument')

    # get dataframe for the table in PDF. Empty dataframe returned in case no table is found.
    df = v1_utils.get_dataframe_from_pdf(input_pdf_file)
    if df.empty:
        raise SystemExit('No table found within the PDF file.')

    # Remove empty or na filled columns and rename the column names as required.
    df = v1_utils.clean_dataframe(df)
    csv_file_name = file_name + '.csv'
    csv_file_path = os.path.join(file_directory, csv_file_name)
    df.to_csv(csv_file_path, index=False)
    print('File converted successfully. File Path is {}'.format(csv_file_path))
