# sec-edgar
A Python package for automatically downloading & updating data from the SEC Edgar database

#### Install
    pip install sec-edgar

#### Downloads all zip files and unzips them to package folder
    from sec_edgar.financial_statements import financial_statements
    financial_statements.download()
    
#### Specify a directory
    from sec_edgar.financial_statements import financial_statements
    financial_statements.download(dest_path='/home/username/destination')

- This will automatically keep track of downloaded files and only download new files 
when run at a later date
