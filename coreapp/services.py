import tabula
import os
import csv 
import pandas as pd
import calendar, time

from django.core.files.storage import default_storage
from django.core.files import File
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .models import File as CsvFile
from .models import BalanceSheet
from .constants import *


def get_value(variable, year):
    """Gets the value of variable for year

        Parameters
        ----------
        variable: str
            the variable to be queried
        year: str
            the year for which variable needs to be queried

        Raises
        ------
        RuntimeError
            If the db qiery returns more than one result or returns no result

        Returns
        -------
        tuple
            a tuple with value and file name
        """

    try: 
        balance = BalanceSheet.objects.get(particular__iexact=variable, year=year)
        return balance.value, balance.file.file.name
    except (MultipleObjectsReturned, ObjectDoesNotExist) : 
        raise RuntimeError("Invalid query variable and year.")



def convert_and_save_data(pdf_file) :
    """Converts the pdf to csv, saves data present in csv and saves 
    the csv itself. Deletes all the intermediate files generated except
     the final csv.

        Parameters
        ----------
        pdf_fie: str
            The file location of the pdf

        Raises
        ------
        RuntimeError
            if the data in pdf violates the uniqueness constraint of database
        """

    file_name = default_storage.save(pdf_file.name, pdf_file)
    output_file_name, output1_file_name, output2_file_name = convert_pdf_to_csv(os.path.abspath(settings.MEDIA_URL+file_name))
    os.remove(output1_file_name)
    os.remove(output2_file_name)
    os.remove(settings.MEDIA_URL+file_name)
    try: 
        balances = save_data(output_file_name)
        csv_file = CsvFile()
        csv_file.file.save(output_file_name, File(open(output_file_name)))
        for balance in balances : 
            balance.file = csv_file
            balance.save()
    except IntegrityError : 
        raise RuntimeError("Invalid data in uploaded pdf file")
    finally : 
        os.remove(output_file_name)
    

def save_data(filename):
    """Parses and saves the data of csv file

        Parameters
        ----------
        filename: str
            path of the file whose data needs to be saved

        Returns
        -------
        list
            a list of data objects saved
        """

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        years = [int(field) for field in fields if field.isnumeric()]
        year1 = years[0]
        year2 = years[1];
        balances = []
        for row in csvreader:
            if row[0] and row[0] != 'Total Rs.':    # Since their are multiple values of 'Total Rs' I am completely ignoring them
                balance_sheet_year1 = BalanceSheet()
                balance_sheet_year2 = BalanceSheet()
                balance_sheet_year1.particular = row[0][3:].strip()
                balance_sheet_year1.year = year1
                balance_sheet_year1.value = row[1]
                balance_sheet_year1.save()
                balance_sheet_year2.particular = row[0][3:].strip()
                balance_sheet_year2.year = year2
                balance_sheet_year2.value = row[2]
                balance_sheet_year2.save()
                balances.append(balance_sheet_year1)
                balances.append(balance_sheet_year2)
            if(len(row)>3) and row[3] and row[3] != 'Total Rs.' :   # Since their are multiple values of 'Total Rs' I am completely ignoring them
                balance_sheet_year1 = BalanceSheet()
                balance_sheet_year2 = BalanceSheet()
                balance_sheet_year1.particular = row[3][3:].strip()
                balance_sheet_year1.year = year1
                balance_sheet_year1.value = row[5]
                balance_sheet_year1.save()
                balance_sheet_year2.particular = row[3][3:].strip()
                balance_sheet_year2.year = year2
                balance_sheet_year2.value = row[6]
                balance_sheet_year2.save()
                balances.append(balance_sheet_year1)
                balances.append(balance_sheet_year2)
        return balances


def convert_pdf_to_csv(path):
    """Gets the value of variable for year

        Parameters
        ----------
        path: str
            path of the pdf file to be converted to csv

        Returns
        -------
        tuple
            a tuple containing all the intermediate and final csvs generated
    """

    filename_wo_ext = os.path.splitext(os.path.basename(path))[0]

    filename_prefix = str(calendar.timegm(time.gmtime()))
    output1_file_name = filename_prefix + '_output1.csv'
    output2_file_name = filename_prefix + '_output2.csv'
    output_file_name = filename_prefix + '_output.csv'

    tabula.convert_into(path, output1_file_name, format='csv', stream=True , pages=1, area=(TOP1, LEFT1, TOP_HEIGHT1, LEFT_WIDTH1))
    tabula.convert_into(path, output2_file_name, format='csv', stream=True , pages=1, area=(TOP2, LEFT2, TOP_HEIGHT2, LEFT_WIDTH2))
    df1 = pd.read_csv(output1_file_name)
    df2 = pd.read_csv(output2_file_name, header=0, names=NAMES)
    pd.concat([df1, df2], axis=1).to_csv(output_file_name, index=False)
    return output_file_name, output1_file_name, output2_file_name

