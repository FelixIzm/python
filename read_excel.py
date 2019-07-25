import xlrd 

#import pandas as pd
#from pandas import ExcelFile

#loc = ("E:\\Южное Кладбище\\VGD\\csv\\Нерльский_рн.xlsx") 
<<<<<<< HEAD
loc = ("E:\\Южное Кладбище\\VGD\\csv\\Московская_ПодвигНарода_Призыв.xlsx")
=======
loc = ("C:\\BackUp\\Docs\\Южное Кладбище\\Выгрузки\\москворецкий_рвк.xlsx") 
>>>>>>> 8d673ced1baf93a5857a61cc7b1adc73ac9a6dc3

#df = pd.read_excel(loc, sheetname='data')
#print("Column headings:")
#print(df.columns)


wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
# For row 0 and column 0 
sheet.cell_value(0, 0) 
# Extracting number of columns 
#for i in range(sheet.nrows):
for i in range(sheet.nrows):
    print(sheet.row(i)[0].value)
