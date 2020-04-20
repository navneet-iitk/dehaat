# Dehaat

Balance Sheet Upload, Data Parsing Project :-

Steps to follow for setting up the project:
1. Create a virtual environment with python3 (preferably 3.5.2) as development is done with Python version 3.5.2.
2. Activate the virtual environment.
3. On command interface, from project root directory, run command `pip install -r requirements/base.txt`.
   This will install all required dependencies.
4. Set environment variable with command, `export DJANGO_SETTINGS_MODULE="config.settings"`
5. Move file `.env.local` to root directory of project.
6. PostgreSQL database is being used which is hosted online at AWS RDS and similarly media and static files are being
   saved at Amazon S3. So data is available globally without the limitations of local machine data storage.
   So no need to run migrations using `./manage.py migrate`.
7. Now, setup is finished. Run the server with `./manange.py runserver 0:{$PORT}`
8. In the browser, File upload page can be accessed at url - `http://localhost:{$PORT}/upload`
9. Tabula package is being used here for data parsing from pdf.
10. Given the format of all uploaded balance sheets remain same, Table is extracted through area coordinates after 
    finding the occurrence for 'Particular' string in the PDF. (This had to be done as the default table without area 
    coordinates was having jumbled data)
11. It is being assumed that query variable and query year either both of them are provided in the input form or None
    is provided. Necessary checks for these are in place. Partial matching of query variable is also possible. In case,
    if the matching data is not available in the balance sheet pdf, then response page doesn't render the output value
    statement.
12. Only PDF files are allowed as input for file uploading.
13. If a table is not found in the PDF, error is raised stating 'No table found'.
14. CSV will always be generated provided file is in correct format containing the required data.
15. CSV file can be downloaded from the `Download CSV` button in the response page.
16. A statement displaying the result for the query is displayed in the response page.
17. Query result is found for the first match in the balance sheet. Only one result is being displayed at the moment.
    Futher releases can take care of multiple query results.
18. Additionally, Another API to list all the uploads with respective queries and CSVs are available at 
    `http://localhost:{$PORT}/api/v1/balance_sheet/list`. This endpoint is commented at the present moment. If needed, 
    one can uncomment and look through the data.
