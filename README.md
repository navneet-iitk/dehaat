# Dehaat

Balance Sheet Upload, Data Parsing Project :-

Steps to follow for setting up the project:
1. Create a vitual environment with python3 (preferrably 3.5.2) as development is done with Python version 3.5.2.
2. Activate the virtual environment.
3. On command interface, from project root directory, run command `pip install -r requirements/base.txt`.
   This will install all required dependencies.
4. Set environment variable with command, `export DJANGO_SETTINGS_MODULE="config.settings"`
5. Move file `.env.local` to root directory of project.
6. Postgresql database is being used which is hosted omline at AWS RDS and similarly media and static files are being
   saved at Amazon S3. So data is available globally without the limitations of local machine data storages.
6. Run migrations using `./manage.py migrate`.
7. Now, setup is finished. Run the server with `./manange.py runserver 0:{$PORT}`
8. In the browser, File upload page can be accessed at url - `http://localhost:{$PORT}/upload`
9. Tabula package is being used here for data parsing from pdf.
10. It is being assumed that query variable and query year either both of them are provided in the input form or None
    is provided. Necessary checks for these are in place. Partial matching of query variable is also possible. In case,
    if the matching data is not available in the balance sheet pdf, then response page doesn't render the output value
    statement.
11. Only PDF files are allowed as input for file uploading.
12. If a table is not found in the PDF, error is raised stating 'No table found'.
13. CSV will always be generated provided file is in correct format containing the required data.
14. CSV file can be downloaded from the `Download CSV` button in the response page.
15. A statement displaying the result for the query is displayed in the response page.
16. Query result is found for the first match in the balance sheet. Only one result is being displayed at the moment.
    Futher releases can take care of mulitple query results.
