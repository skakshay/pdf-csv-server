This repository consists of 
1. Django project 
2. Independent script for converting a pdf file to a csv : **pdf_csv.py**


## Django Project

### Instructions to run on local
1. Create new python3 environment : `python3 -m venv /path/to/new/virtual/environment`
2. Activate the newly create environment : `source /path/to/new/virtual/environment/bin/activate`
3. Clone the repo, and change directory into the project : `cd pdf-csv-server/`
4. Install dependencies from requirements.txt using pip
5. Change value of **DATABASES** in `pdftocsv/settings.py` and create a new database if required
6. Run : `python manage.py migrate`
7. Run : `python manage.py runserver`


### APIs : 
* `/api/uploadFile/` : GET request\
	         	Returns the page for the user to enter input query and upload file

* `/api/uploadFile/` : POST request\
  	                body : {"*query_variable*":"", "*query_year*":"", "*pdf_file*":""}\
	                redirects to `/api/getValue/`

* `/api/getValue/` : GET request\
		       displays the value of *query_variable* for *query_year* and link to the generated csv to download
    

### Assumption : 
The combination of a **Particular name** and **Year** in a pdf file must be unique. This has been enforced on database 
level(refer `coreapp/models.py`). So once you have successfully uploaded a pdf make sure the next pdf that you 
upload has different **Year** or **Particular name** to maintain the integrity of db table. 

In the sample **BalSheet.pdf** provided there are multiple values of `Total Rs.`. I am not able to understand what do they correspond to and which `Total Rs` is for which particulars. So I have not saved them in database. You can see the `Total Rs.` in the generated csv but not in the database. 



## Independent script `pdf_csv.py`

* Dependency : **tabula-py==2.1.0**
* Provide the path to corresponding pdf file while running the module eg : `python pdf_csv.py /path/to/file.pdf`
* Generates corresponding file named **output.csv** file in present working directory
