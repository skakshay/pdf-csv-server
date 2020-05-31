This repository consists of 
1. Django project 
2. Independent script for converting a pdf file to a csv : **pdf_csv.py**


## Django Project

### Instructions to run on local
1. Clone the repo
2. Create new python3 environment
3. Install dependencies from requirements.txt using pip
4. Change value of DATABASES in pdftocsv/settings.py and create a new database if required
5. `python manage.py migrate`
6. `python manage.py runserver`


### APIs : 
* `/api/uploadFile/` : GET request 
  	Returns the page for the user to enter input query and upload file

* `/api/uploadFile/` : POST request 
  	body : {"*query_variable*":"", "*query_year*":"", "*pdf_file*":""}
	  redirects to `/api/getValue/`

* `/api/getValue/` : GET request
	  displays the value of *query_variable* for *query_year* and link to generated csv to download
    

### Assumption : 
The combination of a **Particular name** and **Year** in a pdf file must be unique. This has been enforced on database 
level(refer `coreapp/models.py`). So once you have successfully uploaded a pdf make sure the next pdf that you 
upload has different **Year** or **Particular name** to maintain the integrity of db table. 



## Independent script `pdf_csv.py`

* Dependency : **tabula-py==2.1.0**
* Provide the path to corresponding pdf file while running the module eg : `python pdf_csv.py /path/to/file.pdf`
* Generates corresponding file named **output.csv** file in present working directory
