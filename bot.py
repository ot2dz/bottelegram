#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import pandas as pd
import json
import datetime


# # Create buttons

# In[2]:


# first level buttons
button1 = telebot.types.KeyboardButton("Products manager")
button2 = telebot.types.KeyboardButton("Customers manager")
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1,selective=True ,one_time_keyboard=True)
keyboard.add(button1, button2)


# Create the second level of buttons
button1 = telebot.types.KeyboardButton("Add product")
button2 = telebot.types.KeyboardButton("Edit product")
button3 = telebot.types.KeyboardButton("Add product codes")
button4 = telebot.types.KeyboardButton("Delete product")
keyboard_product = telebot.types.ReplyKeyboardMarkup(row_width=1,selective=True ,one_time_keyboard=True)
keyboard_product.add(button1, button2, button3,button4)


# when user click on Add product 
button1 = telebot.types.KeyboardButton("بطاقات ببجي")
button2 = telebot.types.KeyboardButton("رايزر جولد")
button3 = telebot.types.KeyboardButton("شحن عبر الحساب")
button4 = telebot.types.KeyboardButton("خدمات ببجي")
button5 = telebot.types.KeyboardButton("ايتونز")
keyboard_category = telebot.types.ReplyKeyboardMarkup(row_width=2,selective=True ,one_time_keyboard=True)
keyboard_category.add(button1, button2, button3, button4, button5)



# بطاقات ببجي products
keyboard_pubg_cards = telebot.types.ReplyKeyboardMarkup(row_width=4,selective=True ,one_time_keyboard=True)
# رايزر جولد products
keyboard_gold = telebot.types.ReplyKeyboardMarkup(row_width=4,selective=True ,one_time_keyboard=True)
# شحن عبر الحساب products
keyboard_charge = telebot.types.ReplyKeyboardMarkup(row_width=4,selective=True ,one_time_keyboard=True)
# خدمات ببجي products
keyboard_pubg_services = telebot.types.ReplyKeyboardMarkup(row_width=4,selective=True ,one_time_keyboard=True)
# ايتونز products
keyboard_itunes = telebot.types.ReplyKeyboardMarkup(row_width=4,selective=True ,one_time_keyboard=True)


# confirm akeyboard_productns
button1 = telebot.types.KeyboardButton("نعم ، قم بشراء هذا المنتج")
button2 = telebot.types.KeyboardButton("لا ، إلغاء الشراء")
keyboard_confirm_purchase = telebot.types.ReplyKeyboardMarkup(row_width=1,selective=True ,one_time_keyboard=True)
keyboard_confirm_purchase.add(button1, button2)


# when user click on edit product
button1 = telebot.types.KeyboardButton("Edit Name")
button2 = telebot.types.KeyboardButton("Edit Description")
button3 = telebot.types.KeyboardButton("Edit Price")
button4 = telebot.types.KeyboardButton("Edit Image")
keyboard_edit_product= telebot.types.ReplyKeyboardMarkup(row_width=1,selective=True ,one_time_keyboard=True) 
keyboard_edit_product.add(button1, button2, button3, button4)


# customers 
button1 = telebot.types.KeyboardButton("Edit Balance")
button2 = telebot.types.KeyboardButton("Edit Loans")
button3 = telebot.types.KeyboardButton("ِShow customers details")
button4 = telebot.types.KeyboardButton("ِAdd customer")
keyboard_customers = telebot.types.ReplyKeyboardMarkup(row_width=1,selective=True ,one_time_keyboard=True) 
keyboard_customers.add(button1, button2, button3, button4)


# # check admin

# In[3]:


bot = telebot.TeleBot('6129430590:AAEOVwMOacd1FKikQEXuXnFD5y8De3qKvxY')

# Define the admin users who are authorized to access the admin panel
ADMIN_USERS = [1077656944]



@bot.message_handler(commands=['start'])
# Define a decorator function that can be used to restrict access to admin users only
def admin_only(func):
    def wrapper(message):
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'r') as file:
            customers_data = json.load(file)  
            
        if message.from_user.id in ADMIN_USERS:
            bot.send_message(message.chat.id, "Hi admin")
            return func(message)
        
        elif str(message.from_user.id) in customers_data:
            bot.send_message(message.chat.id, "مرحبا ايها العميل", reply_markup=keyboard_customer)
            
        else:
            bot.send_message(message.chat.id, "عليك أن تطلب من المسؤول إضافتك إلى مستخدمين البوت حتي تتمكن من استخدامه")
    return wrapper


# # choose button

# In[4]:


@bot.message_handler(func=lambda message: message.text in ["start", "No, start again"])
@admin_only
def choose_panel(message):
    bot.send_message(message.chat.id,"How can i help you?", reply_markup=keyboard)
    

@bot.message_handler(func=lambda message: message.text == "Products manager")
@admin_only
def open_product_manager(message):
    bot.send_message(message.chat.id,"Products manager is opened", reply_markup=keyboard_product)
    
    
@bot.message_handler(func=lambda message: message.text == "Customers manager")
@admin_only
def open_customers_manager(message):
    bot.send_message(message.chat.id,"Customers manager is opened", reply_markup = keyboard_customers)


# # Products manager

# # 1. Add product

# In[5]:


# Define a command that allows admin users to add a new product
@bot.message_handler(func=lambda message: message.text == "Add product")
@admin_only

def select_category(message):
    bot.send_message(message.chat.id, "Which category you want to add product to?", reply_markup=keyboard_category)
    bot.register_next_step_handler(message, add_product)

    
def add_product(message):
    category_name = message.text
    # Ask the user for the product name and price
    bot.reply_to(message, "What's the name of the product you want to add?")
    bot.register_next_step_handler(message, add_product_name, category_name)

def add_product_name(message, category_name):
    product_name = message.text
    bot.reply_to(message, "What's the description of the product?")
    bot.register_next_step_handler(message, add_product_description, product_name, category_name)
    
def add_product_description(message, product_name, category_name):
    product_description = message.text
    bot.reply_to(message, "What's the price of the product?")
    bot.register_next_step_handler(message, add_product_price, product_name, product_description, category_name)

def add_product_price(message, product_name, product_description, category_name):
    product_price = int(message.text)
    # Ask the user for the product image
    bot.register_next_step_handler(message, save_product, product_name, product_description, product_price, category_name)
    
def save_product(message, product_name, product_description, product_price ,category_name):
    try:
        products_excel = pd.read_excel(f"C:/Users/Shady Emad/Desktop/products bot/Excels/categories/{category_name}.xlsx")
        new_product = pd.DataFrame({"Name":[product_name],"Description": [product_description], "Price": [product_price]})
        # add the new row to the DataFrame
        products_excel = products_excel.append(new_product, ignore_index=True)
        # write the DataFrame back to an Excel file
        products_excel.to_excel(f"C:/Users/Shady Emad/Desktop/products bot/Excels/categories/{category_name}.xlsx", index=False)
        
        try:
            # create product list in json to add codes in it
            with open("C:/Users/Shady Emad/Desktop/products bot/Excels/products codes.json", 'r') as file:
                product_codes = json.load(file)
            # Add new list for new product
            product_codes[category_name][product_name]=[]
            # Write the updated data back to the JSON file
            with open('C:/Users/Shady Emad/Desktop/products bot/Excels/products codes.json', 'w') as file:
                json.dump(product_codes, file, indent=4)
        
        except Exception as e:
            # Notify the user that an error occurred
            bot.send_message(message.chat.id, f"An error occurred: {e}")
        
        # create products keyboard 
        if category_name == 'بطاقات ببجي':
            button = telebot.types.KeyboardButton(product_name)
            keyboard_pubg_cards.add(button)
        elif category_name == 'رايزر جولد':
            button = telebot.types.KeyboardButton(product_name)
            keyboard_gold.add(button)       
        elif category_name == 'شحن عبر الحساب':
            button = telebot.types.KeyboardButton(product_name)
            keyboard_charge.add(button)     
        elif category_name == 'خدمات ببجي':
            button = telebot.types.KeyboardButton(product_name)
            keyboard_pubg_services.add(button)       
        elif category_name =='ايتونز':
            button = telebot.types.KeyboardButton(product_name)
            keyboard_itunes.add(button)       
        
        
        bot.send_message(message.chat.id, "product is successfully saved")
        
    except Exception as e:
        # Notify the user that an error occurred
        bot.send_message(message.chat.id, f"An error occurred: {e}")


# # 2. Edit product

# In[6]:


# Define a command that allows admin users to change the price of an existing product
@bot.message_handler(func=lambda message: message.text == "Edit product") 
@admin_only

def edit_type(message):
    bot.reply_to(message, "What do you want to edit?", reply_markup=keyboard_edit_product)  


# # Edit Product name

# In[7]:


@bot.message_handler(func=lambda message: message.text == "Edit Name") 
@admin_only

def select_category(message):
    bot.send_message(message.chat.id, "Which category do you want to edit product in it?", reply_markup=keyboard_category)
    bot.register_next_step_handler(message, get_old_name)
    
def get_old_name(message):
    category_name = message.text
    bot.reply_to(message, "What's the name of the product that you want to edit") 
    bot.register_next_step_handler(message, get_new_name, category_name)
    
def get_new_name(message, category_name):
    old_name = message.text
    bot.reply_to(message, "What's the new name of the product") 
    bot.register_next_step_handler(message, change_product_name, old_name, category_name)

def change_product_name(message, old_name, category_name):
    new_name = message.text
    bot.register_next_step_handler(message, save_product_name, old_name, new_name, category_name)


def save_product_name(message, old_name, new_name, category_name):
    df = pd.read_excel(f"C:/Users/Shady Emad/Desktop/products bot/Excels/categories/{category_name}.xlsx")
    
    mask = df['Name'] == old_name

    # Replace the selected values with 'new_value'
    df.loc[mask, 'Name'] = new_name

    # Save the modified DataFrame back to the Excel file
    df.to_excel('products.xlsx', index=False)
    
    bot.send_message(message.chat.id, "The porduct name has been changed")


# # Edit product description

# In[8]:


@bot.message_handler(func=lambda message: message.text == "Edit Description") 
@admin_only

def select_category(message):
    bot.send_message(message.chat.id, "Which category do you want to edit product in it?", reply_markup=keyboard_category)
    bot.register_next_step_handler(message, get_old_name)

def get_old_name(message):
    category_name = message.text
    bot.reply_to(message, "What's the name of the product that you want to edit") 
    bot.register_next_step_handler(message, get_new_desc, category_name)
    
def get_new_desc(message, category_name):
    product_name = message.text
    bot.reply_to(message, "What's the new description of the product") 
    bot.register_next_step_handler(message, change_product_desc, product_name, category_name)

def change_product_desc(message, product_name, category_name):
    new_desc = message.text
    bot.register_next_step_handler(message, save_product_desc, product_name, new_desc, category_name)


def save_product_desc(message, product_name, new_desc, category_name):
    df = pd.read_excel(f"C:/Users/Shady Emad/Desktop/products bot/Excels/categories/{category_name}.xlsx")
    
    mask = df['Name'] == product_name

    # Replace the selected values with 'new_value'
    df.loc[mask, 'Description'] = new_desc

    # Save the modified DataFrame back to the Excel file
    df.to_excel(f"C:/Users/Shady Emad/Desktop/products bot/Excels/categories/{category_name}.xlsx", index=False)
    
    bot.send_message(message.chat.id, "The porduct description has been changed")


# # Edit product price

# In[9]:


@bot.message_handler(func=lambda message: message.text == "Edit Price") 
@admin_only

def select_category(message):
    bot.send_message(message.chat.id, "Which category do you want to edit product in it?", reply_markup=keyboard_category)
    bot.register_next_step_handler(message, get_old_name)

def get_old_name(message):
    category_name = message.text
    bot.reply_to(message, "What's the name of the product that you want to edit") 
    bot.register_next_step_handler(message, get_new_price, category_name)
    
def get_new_price(message, category_name):
    product_name = message.text
    bot.reply_to(message, "What's the new price of the product") 
    bot.register_next_step_handler(message, change_product_price, product_name, category_name)

def change_product_price(message, product_name, category_name):
    new_price = message.text
    save_product_price(product_name, new_price, category_name)


def save_product_price(ةmessage, product_name, new_price, category_name):
    df = pd.read_excel(f"C:/Users/Shady Emad/Desktop/products bot/Excels/categories/{category_name}.xlsx", index=False)
    
    mask = df['Name'] == product_name

    # Replace the selected values with 'new_value'
    df.loc[mask, 'Price'] = new_price

    # Save the modified DataFrame back to the Excel file
    df.to_excel(f"C:/Users/Shady Emad/Desktop/products bot/Excels/categories/{category_name}.xlsx", index=False)
    
    bot.send_message(message.chat.id, "The porduct price has been changed")


# # Edit product image

# In[10]:


@bot.message_handler(func=lambda message: message.text == "Edit Image") 
@admin_only

def select_category(message):
    bot.send_message(message.chat.id, "Which category do you want to edit product in it?", reply_markup=keyboard_category)
    bot.register_next_step_handler(message, get_product_name)

def get_product_name(message):
    category_name = message.text
    bot.reply_to(message, "What's the name of the product that you want to edit") 
    bot.register_next_step_handler(message, get_new_image, category_name)
    
    
def get_new_image(message, category_name):
    product_name = message.text
    bot.reply_to(message, "Send me the new image of the product") 
    bot.register_next_step_handler(message, change_product_image, product_name, category_name)

    
def change_product_image(message, product_name, category_name):
    # Get the file ID of the photo
    file_id = message.photo[-1].file_id
    # Download the photo from Telegram servers
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    # Set the file name for saving
    file_name = product_name + '.jpg'
    # Set the folder path for saving
    folder_path = f"C:/Users/Shady Emad/Desktop/products bot/products images/{category_name}"
    # Save the image to the folder on the PC
    with open(os.path.join(folder_path, file_name), 'wb') as f:
        f.write(file)
        
    bot.reply_to(message, "Image saved successfully") 


# # Add product codes

# In[11]:


@bot.message_handler(func=lambda message: message.text == "Add product codes") 
@admin_only


def select_category(message):
    bot.send_message(message.chat.id, "Which category do you want to edit product in it?", reply_markup=keyboard_category)
    global chat_id
    chat_id = message.chat.id
    bot.register_next_step_handler(message, select_product)


def select_product(message):
    category_name= message.text
    if category_name == 'بطاقات ببجي':
        bot.send_message(message.chat.id, "Which product do you want to add codes for?", reply_markup=keyboard_pubg_cards)
    elif category_name == 'رايزر جولد':
        bot.send_message(message.chat.id, "Which product do you want to add codes for?", reply_markup=keyboard_gold)     
    elif category_name == 'شحن عبر الحساب':
        bot.send_message(message.chat.id, "Which product do you want to add codes for?", reply_markup=keyboard_charge)     
    elif category_name == 'خدمات ببجي':
        bot.send_message(message.chat.id, "Which product do you want to add codes for?", reply_markup=keyboard_pubg_services)      
    else:
        pass
    bot.register_next_step_handler(message, get_codes,category_name)

    
def get_codes(message,category_name):
    product_name = message.text
    bot.send_message(chat_id, "send codes you want to add")
    bot.register_next_step_handler(message, save_codes, category_name, product_name)

    
def save_codes(message, category_name, product_name):
    codes = message.text.split('\n')
    try:
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/products codes.json", 'r') as file:
            product_codes = json.load(file)
            
        for code in codes:
            # Add a new codes to the data dictionary
            product_codes[category_name][product_name].append(code)

        # Write the updated data back to the JSON file
        with open('C:/Users/Shady Emad/Desktop/products bot/Excels/products codes.json', 'w') as file:
            json.dump(product_codes, file, indent=4)
        
        bot.send_message(message.chat.id, "codes is successfully saved")
    
    except Exception as e:
        # Notify the user that an error occurred
        bot.send_message(message.chat.id, f"An error occurred: {e}")   


# # 4. Delete product

# In[12]:


@bot.message_handler(func=lambda message: message.text == "Delete product") 
@admin_only

def select_category(message):
    bot.send_message(message.chat.id, "Which category do you want to delte product from it?", reply_markup=keyboard_category)
    bot.register_next_step_handler(message, select_product_name)
    
def select_product_name(message):
    category_name= message.text
    if category_name == 'بطاقات ببجي':
        bot.send_message(message.chat.id, "Which product do you want to delete?", reply_markup=keyboard_pubg_cards)
    elif category_name == 'رايزر جولد':
        bot.send_message(message.chat.id, "Which product do you want to delete?", reply_markup=keyboard_gold)     
    elif category_name == 'شحن عبر الحساب':
        bot.send_message(message.chat.id, "Which product do you want to delete?", reply_markup=keyboard_charge)     
    elif category_name == 'خدمات ببجي':
        bot.send_message(message.chat.id, "Which product do you want to delete?", reply_markup=keyboard_pubg_services)      
    else:
        pass
    bot.register_next_step_handler(message, delete_data, category_name)
    
    
def delete_data(message,category_name):
    product_name = message.text
    
    # Set the path to the directory containing the image file
    folder_path = f"C:/Users/Shady Emad/Desktop/products bot/products images/{category_name}"

    # Combine the directory path and file name to create the full file path
    file_path = os.path.join(folder_path, product_name+'.jpg')

    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        try: 
            # Load the Excel file into a Pandas dataframe
            df = pd.read_excel(f"C:/Users/Shady Emad/Desktop/products bot/Excels/categories/{category_name}.xlsx")
            # Select the rows that match the condition
            rows_to_drop = df[df['Name'] == product_name].index

            # Drop the selected rows
            df = df.drop(rows_to_drop)

            # Save the updated dataframe back to the Excel file
            df.to_excel('products.xlsx', index=False)
        

            with open("C:/Users/Shady Emad/Desktop/products bot/Excels/products codes.json", 'r') as file:
                product_codes = json.load(file)
                
            del product_codes[category_name][product_name]

            # Write the updated data back to the JSON file
            with open('C:/Users/Shady Emad/Desktop/products bot/Excels/products codes.json', 'w') as file:
                json.dump(product_codes, file, indent=4)
        
            bot.send_message(message.chat.id, f"{product_name} delete successfully.")
    
        except Exception as e:
            # Notify the user that an error occurred
            bot.send_message(message.chat.id, f"An error occurred: {e}")  
        


    else:
        bot.send_message(message.chat.id, f"{product_name} does not exist.")


# # *Customers manager

# # 1. Edit Balance

# In[13]:


@bot.message_handler(func=lambda message: message.text == "Edit Balance") 
@admin_only

def get_customer_id(message):
    bot.reply_to(message, "What's the ID of the customer?") 
    bot.register_next_step_handler(message, get_new_balance)
    
def get_new_balance(message):
    customer_id = str(message.text)
    bot.reply_to(message, "What's the new balance?") 
    bot.register_next_step_handler(message, save_balance, customer_id)
    
def save_balance(message, customer_id):
    new_balance = message.text
    
    try:
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'r') as file:
            customers_data = json.load(file)  
        customers_data[customer_id]['balance'] = new_balance
        # write the updated data to the JSON file
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'w') as file:
            json.dump(customers_data, file, indent=4)
            
        bot.send_message(message.chat.id, "The new balance has been saved successfully")
        
    except Exception as e:
        # Notify the user that an error occurred
        bot.send_message(message.chat.id, f"An error occurred: {e}")


# # 2. Edit loan

# In[14]:


@bot.message_handler(func=lambda message: message.text == "Edit Loans") 
@admin_only

def get_customer_id(message):
    bot.reply_to(message, "What's the ID of the customer?") 
    bot.register_next_step_handler(message, get_new_loan)
    
def get_new_loan(message):
    customer_id = message.text
    bot.reply_to(message, "What's the new Loan?") 
    bot.register_next_step_handler(message, save_loan, customer_id)
    
def save_loan(message, customer_id):
    new_loan = message.text
    
    try:
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'r') as file:
            customers_data = json.load(file)  
        user = customers_data[customer_id]
        user['loan'] = new_loan
        # write the updated data to the JSON file
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'w') as file:
            json.dump(customers_data, file, indent=4)
            
        bot.send_message(message.chat.id, "The new loan has been saved successfully")
        
            
    except Exception as e:
        # Notify the user that an error occurred
        bot.send_message(message.chat.id, f"An error occurred: {e}")


# # 3. ِAdd customer

# In[15]:


@bot.message_handler(func=lambda message: message.text == "ِAdd customer") 
@admin_only

def get_customer_id(message):
    bot.reply_to(message, "What's the ID of the customer?") 
    bot.register_next_step_handler(message, get_customer_balance)

def get_customer_balance(message):
    customer_id = message.text
    bot.reply_to(message, "What's the Balance of the customer?") 
    bot.register_next_step_handler(message, get_customer_loan, customer_id)

def get_customer_loan(message, customer_id):
    customer_balance = message.text
    bot.reply_to(message, "What's the Loan of the customer?") 
    bot.register_next_step_handler(message, save_customer, customer_id, customer_balance)
    
def save_customer(message, customer_id, customer_balance):
    customer_loan = message.text
    try:
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'r') as file:
            customers_data = json.load(file)

        # Add a new user to the data dictionary
        customers_data[customer_id] = {
        'balance': int(customer_balance),
        'loan': int(customer_loan),
        'purchases': []
        }

        # Write the updated data back to the JSON file
        with open('C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json', 'w') as file:
            json.dump(customers_data, file, indent=4)   

            
        bot.send_message(message.chat.id, "Customer data is successfully saved")
        
    except Exception as e:
        # Notify the user that an error occurred
        bot.send_message(message.chat.id, f"An error occurred: {e}")


# # 4. Show customers details

# In[16]:


@bot.message_handler(func=lambda message: message.text == "ِShow customers details") 
@admin_only

def get_customer_id(message):
    bot.reply_to(message, "What's the ID of the customer?") 
    bot.register_next_step_handler(message, show_details)
    

def show_details(message):
    customer_id = message.text
    
    try:
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'r') as file:
            customers_data = json.load(file)
        
        user = customers_data[customer_id]
        bot.send_message(message.chat.id, f"The customer ID: {customer_id}"
                                          f"\n\n Balance: {user['balance']}"
                                          f"\n Loan: {user['loan']}")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {e}")


# # Users:

# # 1. Create buttons

# In[17]:


# Create the first level of buttons
button1 = telebot.types.KeyboardButton("شحن االرصيد")
button2 = telebot.types.KeyboardButton("المنتجات")
button3 = telebot.types.KeyboardButton("رصيدي")
button4 = telebot.types.KeyboardButton("سجل المشتريات")
button5 = telebot.types.KeyboardButton("help")
keyboard_customer = telebot.types.ReplyKeyboardMarkup(row_width=2,selective=True ,one_time_keyboard=True)
keyboard_customer.add(button1, button2, button3, button4, button5)


# products categories
button1 = telebot.types.KeyboardButton("بطاقات ببجي")
button2 = telebot.types.KeyboardButton("رايزر جولد")
button3 = telebot.types.KeyboardButton("شحن عبر الحساب")
button4 = telebot.types.KeyboardButton("خدمات ببجي")
button5 = telebot.types.KeyboardButton("ايتونز")
keyboard_category = telebot.types.ReplyKeyboardMarkup(row_width=2,selective=True ,one_time_keyboard=True)
keyboard_category.add(button1, button2, button3, button4, button5)


# products categories
keyboard_category = telebot.types.ReplyKeyboardMarkup(row_width=2,selective=True ,one_time_keyboard=True)
keyboard_category.add(button1, button2, button3, button4, button5)


# # شحن االرصيد

# In[18]:


@bot.message_handler(func=lambda message: message.text == "شحن االرصيد")
def handel_charge_balance(message):
    bot.send_message(message.chat.id,"لشحن الرصيد تواصل مع هذا الحساب")
    bot.send_message(message.chat.id,"https://t.me/ShaadyEmad")


# In[ ]:





# In[ ]:





# # المنتجات

# In[19]:


@bot.message_handler(func=lambda message: message.text == "المنتجات")
def get_category(message):
    bot.send_message(message.chat.id,"الفئات المتوفرة", reply_markup=keyboard_category)
    bot.register_next_step_handler(message, send_products)

    
def send_products(message):
    category_name = message.text
    global products_df
    if category_name == 'بطاقات ببجي':
        bot.send_message(message.chat.id,"المنتجات المتوفرة", reply_markup=keyboard_pubg_cards)
        products_df = pd.read_excel("C:/Users/Shady Emad/Desktop/products bot/Excels/categories/بطاقات ببجي.xlsx")

    elif category_name == 'رايزر جولد':
        bot.send_message(message.chat.id,"المنتجات المتوفرة", reply_markup=keyboard_gold)
        products_df = pd.read_excel("C:/Users/Shady Emad/Desktop/products bot/Excels/categories/رايزر جولد.xlsx")
        
    elif category_name == 'شحن عبر الحساب':
        bot.send_message(message.chat.id,"المنتجات المتوفرة", reply_markup=keyboard_charge)
        products_df = pd.read_excel("C:/Users/Shady Emad/Desktop/products bot/Excels/categories/شحن عبر الحساب.xlsx")
    
    elif category_name == 'خدمات ببجي':
        bot.send_message(message.chat.id,"المنتجات المتوفرة", reply_markup=keyboard_pubg_services)
        products_df = pd.read_excel("C:/Users/Shady Emad/Desktop/products bot/Excels/categories/خدمات ببجي.xlsx")
     
    elif category_name =='ايتونز':
        bot.send_message(message.chat.id,"المنتجات المتوفرة", reply_markup=keyboard_itunes)
        products_df = pd.read_excel("C:/Users/Shady Emad/Desktop/products bot/Excels/categories/ايتونز.xlsx")
        
    bot.register_next_step_handler(message, show_product_details, category_name)
    
    
def show_product_details(message, category_name):
    global products_df
    product_name = message.text
    product_row = products_df.loc[products_df['Name'] == product_name]
    
    msg = f" المنتج : {product_name} \n"
    msg+= f"الوصف : {product_row.iloc[0]['Description']} \n"
    msg+= f"السعر : {product_row.iloc[0]['Price']}"
    bot.send_message(message.chat.id, msg)
    
    bot.send_message(message.chat.id, "هل تريد شراء هذا المنتج؟", reply_markup=keyboard_confirm_purchase)
    bot.register_next_step_handler(message, confrim_purchase, product_row, category_name, product_name)


# # confirm purchase

# In[20]:


def confrim_purchase(message, product_row, category_name, product_name):
    if message.text == 'نعم ، قم بشراء هذا المنتجt':
        global products_df
        
        # access product codes file
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/products codes.json", 'r') as file:
            product_codes = json.load(file)
            
        # read customers JSON file
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'r') as file:
            customers_data = json.load(file) 
            
        if len(product_codes[category_name][product_name]) != 0 :
            customer_id = str(message.chat.id)
            if customers_data[customer_id]['balance'] >= int(product_row.iloc[0]['Price']): 
                try:
                    customers_data[customer_id]['balance'] -= int(product_row.iloc[0]['Price'])   # remove the product price from customer balance
                    
                    
                    # get the product code
                    code = product_codes[category_name][product_name]    # access product codes list
                    bot.send_message(message.chat.id, code[0])    # send first code in list
                    product_codes[category_name][product_name].pop(0)
                    

                    # Add this purchase to customers JSON file
                    customers_data[customer_id]['purchases'].append([product_name, int(product_row.iloc[0]['Price'])])


                    # write the updated data to the customers JSON file
                    with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'w') as file:
                        json.dump(customers_data, file, indent=4)
                        
                    with open("C:/Users/Shady Emad/Desktop/products bot/Excels/products codes.json", 'w') as file:
                        json.dump(product_codes, file, indent=4)

                except Exception as e:
                    # Notify the user that an error occurred
                    bot.send_message(message.chat.id, f"An error occurred: {e}")
                    
                    
            else:
                bot.send_message(message.chat.id, "آسف ليس لديك رصيد كافي لشراء هذا المنتج")
                
        else:
            bot.send_message(message.chat.id, "عذرا هذا المنتج غير متوفر الآن")
            
    elif message.text =='لا ، إلغاء الشراء':
        bot.send_message(message.chat.id, "مرحبا ايها العميل", reply_markup=keyboard_customer)


# # رصيدي

# In[21]:


@bot.message_handler(func=lambda message: message.text == "رصيدي")
def send_customer_balance(message):
    try:
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'r') as file:
            customers_data = json.load(file)
            
        user_id = str(message.from_user.id)
            
        user = customers_data[user_id]
            
        bot.send_message(message.chat.id, f"رصيدك: {user['balance']}" 
                                          f"\n دينك: {user['loan']}")
        
    except Exception as e:
        # Notify the user that an error occurred
        bot.send_message(message.chat.id, f"An error occurred: {e}")


# # سجل المشتريات

# In[22]:


@bot.message_handler(func=lambda message: message.text == "سجل المشتريات")
def send_last_purchases(message):
    try:
        with open("C:/Users/Shady Emad/Desktop/products bot/Excels/customers.json", 'r') as file:
            customers_data = json.load(file)
            
        user_id = str(message.chat.id)
        for purchase in customers_data[user_id]['purchases']:
            bot.send_message(message.chat.id, f"{purchase[0]} , {purchase[1]}")
        
    except Exception as e:
        # Notify the user that an error occurred
        bot.send_message(message.chat.id, f"An error occurred: {e}")
    


# # help

# In[19]:


@bot.message_handler(func=lambda message: message.text == "help")
def send_help(message):
    bot.send_message(message.chat.id, "إذا كنت بحاجة إلى أي مساعدة ، أرسل رسالة لهذا الحساب")


# In[ ]:


bot.polling()


# In[ ]:




