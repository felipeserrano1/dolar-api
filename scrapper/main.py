from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta, datetime
from selenium.webdriver.common.by import By
import mysql.connector

db = mysql.connector.connect(host="localhost",
                             user="root",
                             password="root",
                             database="dolar_db"
                             )

mycursor = db.cursor()
cursor = db.cursor(buffered=True)
mycursor.execute("CREATE DATABASE IF NOT EXISTS dolar_db")
mycursor.execute("CREATE TABLE IF NOT EXISTS posts (id INT AUTO_INCREMENT PRIMARY KEY, fecha date, valor float)")

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

mycursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1")
last_date = mycursor.fetchone()

if last_date is None:
    start_date = date(2015, 7, 22)
else:
    start_date = last_date[1] + timedelta(days=1)

end_date = date.today()

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome(service=Service(r"C:\Users\FelipePC\Downloads\Projects\chromedriver.exe"), options=chrome_options)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\FelipePC\Downloads\Projects\chromedriver.exe", options=options)

options.add_extension(r"C:\Users\FelipePC\Downloads\Otros\ChromeDriver\adblock.crx")
driver.get('https://www.cotizacion-dolar.com.ar/dolar-blue-historico-2023.php')


for single_date in daterange(start_date, end_date):
    fecha = single_date.strftime("%d-%m-%y")
    year = single_date.strftime("%Y")
    driver.find_element(By.LINK_TEXT, year).click()
    element = driver.find_element(By.CLASS_NAME, 'fecha-historico')
    l = driver.find_element('name', "fecha")
    dropdown = Select(l)
    possibleDates = []
    for opt in dropdown.options:
        possibleDates.append(opt.text)
    if(fecha in possibleDates):
        dropdown.select_by_visible_text(fecha)
        element.submit()
        valor = driver.find_element('xpath', '//*[@id="article1"]/div[3]/div[4]/table/tbody/tr[2]/td').text
        valor_db = float(valor[2:])
        fecha_db = single_date.strftime("%Y-%m-%d")
        mycursor.execute("INSERT IGNORE INTO posts (fecha, valor) VALUES ( %s, %s)", (fecha_db, valor_db))
        db.commit()




