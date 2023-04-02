from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta
from selenium.webdriver.common.by import By
import mysql.connector
db = mysql.connector.connect(host="localhost",
                             user="root",
                             password="root",
                             database="dolar_db"
                             )

mycursor = db.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS dolar_db")
mycursor.execute("CREATE TABLE IF NOT EXISTS posts (fecha DATE PRIMARY KEY, valor float)")

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2015, 7, 22)
end_date = date.today()

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(r"C:\Users\FelipePC\Downloads\Projects\chromedriver.exe"), options=chrome_options)

chrome_options.add_extension(r"C:\Users\FelipePC\Downloads\Otros\ChromeDriver\adblock.crx")
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
        mycursor.execute("INSERT IGNORE INTO posts (fecha, valor) VALUES (%s, %s)", (fecha_db, valor_db))
        db.commit()




