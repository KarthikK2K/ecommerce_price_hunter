# from selenium import webdriver

# #chrome_driver ='D:\MineDown\Python_Selenium\chromedriver'
# driver = webdriver.Chrome()
# driver.get('https://www.google.com')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from pathlib import Path

source1 = "https://www.flipkart.com/apple-iphone-13-green-128-gb/p/itm18a55937b2607?pid=MOBGC9VGSU9DWGJZ&lid=LSTMOBGC9VGSU9DWGJZUXUVYB&marketplace=FLIPKART&q=Apple+iPhone+13+%28128GB%29+-+Green&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=9c541389-0368-4314-a58f-7f15121ed8d0.MOBGC9VGSU9DWGJZ.SEARCH&ppt=hp&ppn=homepage&ssid=4kqgzvn4280000001708452111903&qH=404cfe293d89f773"
source2 = "https://www.sangeethamobiles.com/product-details/iPhone-13-128GB-Midnight-Apple/8540?utm_source=google&utm_campaign=T1-Apple&gad_source=1&gclid=EAIaIQobChMIksKw7pW_hAMVz6lmAh2asACjEAQYASABEgKjn_D_BwE"
source3 = "https://www.croma.com/apple-iphone-13-128gb-alpine-green-/p/249840"
wait_imp = 10
CO = webdriver.ChromeOptions()
CO.add_experimental_option('useAutomationExtension',False)
CO.add_argument('--ignore-certificate-errors')
CO.add_argument('--start-maximized')
wd = webdriver.Chrome()
list=[]
print("************************************************\n")
print("Starting Program Please Wait.....\n")
print("------------------------------------------------")
print("Connectig to Flipkart")
wd.get(source1)
time.sleep(5) 
wd.implicitly_wait(wait_imp)

flipkart_soup = BeautifulSoup(wd.page_source, 'html.parser')
f_price = flipkart_soup.find("div", class_="_30jeq3 _16Jk6d")   #price extraction
product_name = flipkart_soup.find('span', class_='B_NuCI').text.strip() #product name extraction
r_price = f_price.text 
print("Successfully Retrieved The price from Flipkart ")
print(r_price[1:],"\n")
flip_price = r_price[1:]
list.append(flip_price)
print("Product Name:", product_name)
print("------------------------------------------------")
time.sleep(2)

print("Connecting to Sangeetha")
wd.get(source2)
wd.implicitly_wait(wait_imp)
time.sleep(5) 
amazon_soup = BeautifulSoup(wd.page_source, 'html.parser')
#a_price = amazon_soup.find("span", class_="a-price-whole") 
a_price = amazon_soup.find("div", class_="new-price")
raw_p = a_price.text
#print(raw_p[1:8])
print("Successfully Retrieved the price from Sangeetha")
print(raw_p[1:],"\n")
san_price = raw_p[1:]
list.append(san_price)
print("------------------------------------------------")
time.sleep(2)

print("Connecting to Croma")
wd.get(source3)
wd.implicitly_wait(wait_imp)
time.sleep(5) 
# c_price = wd.find_element_by_xpath("/html/body/main/div[5]/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/span")
croma_soup = BeautifulSoup(wd.page_source, 'html.parser')
c_price = croma_soup.find("span", class_="amount", id="pdp-product-price")
raw_c = c_price.text
print("Successfully Retrieved The Price From Croma")
print(raw_c.encode('ascii', 'ignore').decode('ascii'))
print("------------------------------------------------\n")
time.sleep(2)

print(product_name)
print("All Prices : ")
print(int(flip_price.replace(",","").replace(".","")))

san_price = san_price.split(".")
san_price=san_price[0].replace(",","")
print(san_price)

raw_c=raw_c.encode('ascii', 'ignore').decode('ascii')
new_raw=raw_c.split(".")
#print(raw_c)
new_raw=new_raw[0].replace(",","")
print(new_raw)
list.append(new_raw)

# Iterate over the list and encode each string element as UTF-8
encoded_list = [item.encode('utf-8') if isinstance(item, str) else item for item in list]

# Print the encoded list
print(encoded_list)
print("------------------------------------------------------------------------")
print("Product Name:", product_name)
print("\n")
from tabulate import tabulate

# Define your data
data = [
    ["Flipkart", flip_price],
    ["Sangeetha", san_price],
    ["Croma", new_raw]
]

min_price = min(data, key=lambda x: float(x[1].replace(',', '').replace('\u20b9', '').strip()))
#min_price = min(data, key=lambda x: float(str(x[1]).replace(',', '').replace('\u20b9', '').strip()))


min_price_source, min_price_value = min_price

# Display data in a tabular format
print(tabulate(data, headers=["Source", "Price"]))

print("\n------------------------------------------------------------------------\n")

print(f"The Minimum Price of the Product '{product_name}' is: {min(encoded_list)} from {min_price_source}")

print("=============================================================================================")

import smtplib
from email.mime.text import MIMEText

def send_email(min_price, min_price_source):
    send_email = 'karthik.19dbca@cmr.edu.in'
    receiver_email = 'kams22mca@cmrit.ac.in'
    app_password ='bbad7886'

    subject ='Alert Price of Particular product'
    body = f'The Least Price of the Product {product_name} is \n\nMinimum Price: {min_price} from {min_price_source}'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = send_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(send_email, app_password)
        server.sendmail(send_email, [receiver_email], msg.as_string())

# Call the function with the minimum price and its source
send_email(min_price_value, min_price_source)




#To display The Prices in graph Format 
#Ex the below code is using bargraph

import matplotlib.pyplot as plt

x_values = ['Flipkart','Sangeetha','Croma']
y_values = list
# Convert byte strings to float
# Define bar colors
colors = ['blue', 'orange', 'green']

plt.figure(figsize=(10, 6))
bars = plt.bar(y_values, x_values, color=colors)

# Attach price values to the top of each bar
for bar, price in zip(bars, y_values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, str(price), ha='center')

plt.xlabel('Source')
plt.ylabel('Price (in INR)')
plt.title('Price Comparison')
plt.grid(True)
plt.show()