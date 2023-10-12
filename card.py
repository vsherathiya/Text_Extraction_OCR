# # # import pandas as pd
# # # import streamlit as st
# # # from streamlit_option_menu import option_menu
# # # import easyocr
# # # import sqlite3
# # # from PIL import Image
# # # import cv2
# # # import os
# # # import matplotlib.pyplot as plt
# # # import re

# # # # SETTING PAGE CONFIGURATIONS
# # # icon = Image.open("icon.png")
# # # st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR | By BALAVIGNESH S S",
# # #                    page_icon=icon,
# # #                    layout="wide",
# # #                    initial_sidebar_state="expanded",
# # #                    menu_items={'About': """# This OCR app is created by *BALAVIGNESH S S*!"""})
# # # st.markdown("<h1 style='text-align: center; color: blue;'>BizCardX: Extracting Business Card Data with OCR</h1>",
# # #             unsafe_allow_html=True)


# # # # SETTING-UP BACKGROUND IMAGE
# # # def setting_bg():
# # #     st.markdown(f""" <style>.stApp {{
# # #                         background:url("https://wallpapers.com/images/featured/plain-zoom-background-d3zz0xne0jlqiepg.jpg");
# # #                         background-size: cover}}
# # #                      </style>""", unsafe_allow_html=True)


# # # setting_bg()

# # # # CREATING OPTION MENU
# # # selected = option_menu(None, ["Home", "Upload & Extract", "Modify"],
# # #                        icons=["house", "cloud-upload", "pencil-square"],
# # #                        default_index=0,
# # #                        orientation="horizontal",
# # #                        styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "-2px",
# # #                                             "--hover-color": "#6495ED"},
# # #                                "icon": {"font-size": "35px"},
# # #                                "container": {"max-width": "6000px"},
# # #                                "nav-link-selected": {"background-color": "#6495ED"}})

# # # # INITIALIZING THE EasyOCR READER
# # # reader = easyocr.Reader(['en'])

# # # # CONNECTING WITH SQLite DATABASE
# # # conn = sqlite3.connect("bizcard.db")
# # # cursor = conn.cursor()

# # # # TABLE CREATION
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS card_data
# # #                    (id INTEGER PRIMARY KEY,
# # #                     company_name TEXT,
# # #                     card_holder TEXT,
# # #                     designation TEXT,
# # #                     mobile_number TEXT,
# # #                     email TEXT,
# # #                     website TEXT,
# # #                     area TEXT,
# # #                     city TEXT,
# # #                     state TEXT,
# # #                     pin_code TEXT,
# # #                     image BLOB
# # #                     )''')

# # # # HOME MENU
# # # if selected == "Home":
# # #     col1, col2 = st.columns(2)
# # #     with col1:
# # #         st.image(Image.open("icon.png"), width=500)
# # #         st.markdown("## :green[**Technologies Used :**] Python, Easy OCR, Streamlit, SQLite, Pandas")
# # #     with col2:
# # #         st.write("## :green[**About :**] Bizcard is a Python application designed to extract information from business cards.")
# # #         st.write('## The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')

# # # # UPLOAD AND EXTRACT MENU

# # # if selected == "Upload & Extract":
# # #     if st.button(":blue[Already stored data]"):
# # #         cursor.execute(
# # #             "SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM card_data")
# # #         updated_data = cursor.fetchall()
# # #         updated_df = pd.DataFrame(updated_data,
# # #                                   columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email",
# # #                                            "Website", "Area", "City", "State", "Pin_Code"])
# # #         st.write(updated_df)
# # #     st.subheader(":blue[Upload a Business Card]")
# # #     uploaded_card = st.file_uploader("Upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

# # #     if uploaded_card is not None:
# # #         # Create the "uploaded_cards" directory if it doesn't exist
# # #         uploaded_cards_dir = os.path.join(os.getcwd(), "uploaded_cards")
# # #         if not os.path.exists(uploaded_cards_dir):
# # #             os.makedirs(uploaded_cards_dir)

# # #         def save_card(uploaded_card):
# # #             with open(os.path.join(uploaded_cards_dir, uploaded_card.name), "wb") as f:
# # #                 f.write(uploaded_card.getbuffer())

# # #         save_card(uploaded_card)

# # #         def image_preview(image, res):
# # #             for (bbox, text, prob) in res:
# # #                 # unpack the bounding box
# # #                 (tl, tr, br, bl) = bbox
# # #                 tl = (int(tl[0]), int(tl[1]))
# # #                 tr = (int(tr[0]), int(tr[1]))
# # #                 br = (int(br[0]), int(br[1]))
# # #                 bl = (int(bl[0]), int(bl[1]))
# # #                 cv2.rectangle(image, tl, br, (0, 255, 0), 2)
# # #                 cv2.putText(image, text, (tl[0], tl[1] - 10),
# # #                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
# # #             plt.rcParams['figure.figsize'] = (15, 15)
# # #             plt.axis('off')
# # #             plt.imshow(image)

# # #         # DISPLAYING THE UPLOADED CARD
# # #         col1, col2 = st.columns(2, gap="large")
# # #         with col1:
# # #             st.markdown("#     ")
# # #             st.markdown("#     ")
# # #             st.markdown("### You have uploaded the card")
# # #             st.image(uploaded_card)
# # #         # DISPLAYING THE CARD WITH HIGHLIGHTS
# # #         with col2:
# # #             st.markdown("#     ")
# # #             st.markdown("#     ")
# # #             with st.spinner("Please wait processing image..."):
# # #                 st.set_option('deprecation.showPyplotGlobalUse', False)
# # #                 saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
# # #                 image = cv2.imread(saved_img)
# # #                 res = reader.readtext(saved_img)
# # #                 st.markdown("### Image Processed and Data Extracted")
# # #                 st.pyplot(image_preview(image, res))

# # #         saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
# # #         result = reader.readtext(saved_img, detail=0, paragraph=False)

# # #         # CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
# # #         def img_to_binary(file):
# # #             # Convert image data to binary format
# # #             with open(file, 'rb') as file:
# # #                 binaryData = file.read()
# # #             return binaryData

# # #         data = {"company_name": [],
# # #                 "card_holder": [],
# # #                 "designation": [],
# # #                 "mobile_number": [],
# # #                 "email": [],
# # #                 "website": [],
# # #                 "area": [],
# # #                 "city": [],
# # #                 "state": [],
# # #                 "pin_code": [],
# # #                 "image": img_to_binary(saved_img)
# # #                 }

# # #         def get_data(res):
# # #             for ind, i in enumerate(res):
# # #                 # Initialize all fields with default values
# # #                 data["company_name"].append("")
# # #                 data["card_holder"].append("")
# # #                 data["designation"].append("")
# # #                 data["mobile_number"].append("")
# # #                 data["email"].append("")
# # #                 data["website"].append("")
# # #                 data["area"].append("")
# # #                 data["city"].append("")
# # #                 data["state"].append("")
# # #                 data["pin_code"].append("")

# # #                 # To get WEBSITE_URL
# # #                 if "www " in i.lower() or "www." in i.lower():
# # #                     data["website"][-1] = i
# # #                 elif "WWW" in i:
# # #                     data["website"][-1] = res[4] + "." + res[5]

# # #                 # To get EMAIL ID
# # #                 elif "@" in i:
# # #                     data["email"][-1] = i

# # #                 # To get MOBILE NUMBER
# # #                 elif "-" in i:
# # #                     data["mobile_number"][-1] = i
# # #                     if len(data["mobile_number"]) == 2:
# # #                         data["mobile_number"][-1] = " & ".join(data["mobile_number"])

# # #                 # To get COMPANY NAME
# # #                 elif ind == len(res) - 1:
# # #                     data["company_name"][-1] = i

# # #                 # To get CARD HOLDER NAME
# # #                 elif ind == 0:
# # #                     data["card_holder"][-1] = i

# # #                 # To get DESIGNATION
# # #                 elif ind == 1:
# # #                     data["designation"][-1] = i

# # #                 # To get AREA
# # #                 if re.findall('^[0-9].+, [a-zA-Z]+', i):
# # #                     data["area"][-1] = i.split(',')[0]
# # #                 elif re.findall('[0-9] [a-zA-Z]+', i):
# # #                     data["area"][-1] = i

# # #                 # To get CITY NAME
# # #                 match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
# # #                 match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
# # #                 match3 = re.findall('^[E].*', i)
# # #                 if match1:
# # #                     data["city"][-1] = match1[0]
# # #                 elif match2:
# # #                     data["city"][-1] = match2[0]
# # #                 elif match3:
# # #                     data["city"][-1] = match3[0]

# # #                 # To get STATE
# # #                 state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
# # #                 if state_match:
# # #                     data["state"][-1] = i[:9]
# # #                 elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
# # #                     data["state"][-1] = i.split()[-1]

# # #                 # To get PINCODE
# # #                 if len(i) >= 6 and i.isdigit():
# # #                     data["pin_code"][-1] = i
# # #                 elif re.findall('[a-zA-Z]{9} +[0-9]', i):
# # #                     data["pin_code"][-1] = i[10:]

# # #         get_data(result)

# # #         # FUNCTION TO CREATE DATAFRAME
# # #         def create_df(data):
# # #             df = pd.DataFrame(data)
# # #             return df

# # #         df = create_df(data)
# # #         st.success("### Data Extracted!")
# # #         st.write(df)

# # #         if st.button("Upload to Database"):
# # #             for i, row in df.iterrows():
# # #                 sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
# # #                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"""
# # #                 cursor.execute(sql, tuple(row))
# # #                 conn.commit()
# # #                 st.success("#### Uploaded to the database successfully!")

# # #         if st.button(":blue[View updated data]"):
# # #             cursor.execute("SELECT company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code FROM card_data")
# # #             data = cursor.fetchall()
# # #             updated_df = pd.DataFrame(data,
# # #                                       columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email",
# # #                                                "Website", "Area", "City", "State", "Pin_Code"])
# # #             st.write(updated_df)

# # # # MODIFY MENU
# # # if selected == "Modify":
# # #     st.subheader(':blue[You can view, alter or delete the extracted data in this app]')
# # #     select = option_menu(None,
# # #                          options=["ALTER", "DELETE"],
# # #                          default_index=0,
# # #                          orientation="horizontal",
# # #                          styles={"container": {"width": "100%"},
# # #                                  "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
# # #                                  "nav-link-selected": {"background-color": "#6495ED"}})

# # #     if select == "ALTER":
# # #         st.markdown(":blue[Alter the data here]")

# # #         try:
# # #             cursor.execute("SELECT card_holder FROM card_data")
# # #             result = cursor.fetchall()
# # #             business_cards = {}
# # #             for row in result:
# # #                 business_cards[row[0]] = row[0]
# # #             options = ["None"] + list(business_cards.keys())
# # #             selected_card = st.selectbox("**Select a card**", options)
# # #             if selected_card == "None":
# # #                 st.write("No card selected.")
# # #             else:
# # #                 st.markdown("#### Update or modify any data below")
# # #                 cursor.execute("SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM card_data WHERE card_holder=?", (selected_card,))
# # #                 result = cursor.fetchone()

# # #                 # DISPLAYING ALL THE INFORMATION
# # #                 company_name = st.text_input("Company_Name", result[0])
# # #                 card_holder = st.text_input("Card_Holder", result[1])
# # #                 designation = st.text_input("Designation", result[2])
# # #                 mobile_number = st.text_input("Mobile_Number", result[3])
# # #                 email = st.text_input("Email", result[4])
# # #                 website = st.text_input("Website", result[5])
# # #                 area = st.text_input("Area", result[6])
# # #                 city = st.text_input("City", result[7])
# # #                 state = st.text_input("State", result[8])
# # #                 pin_code = st.text_input("Pin_Code", result[9])

# # #                 if st.button(":blue[Commit changes to DB]"):
# # #                     cursor.execute("UPDATE card_data SET company_name=?, card_holder=?, designation=?, mobile_number=?, email=?, website=?, area=?, city=?, state=?, pin_code=? WHERE card_holder=?", (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code, selected_card))
# # #                     conn.commit()
# # #                     st.success("Information updated in the database successfully.")

# # #             if st.button(":blue[View updated data]"):
# # #                 cursor.execute("SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM card_data")
# # #                 data = cursor.fetchall()
# # #                 updated_df = pd.DataFrame(data,
# # #                                           columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email",
# # #                                                    "Website", "Area", "City", "State", "Pin_Code"])
# # #                 st.write(updated_df)

# # #         except:
# # #             st.warning("There is no data available in the database")

# # #     if select == "DELETE":
# # #         st.subheader(":blue[Delete the data]")
# # #         try:
# # #             cursor.execute("SELECT card_holder FROM card_data")
# # #             result = cursor.fetchall()
# # #             business_cards = {}
# # #             for row in result:
# # #                 business_cards[row[0]] = row[0]
# # #             options = ["None"] + list(business_cards.keys())
# # #             selected_card = st.selectbox("**Select a card**", options)
# # #             if selected_card == "None":
# # #                 st.write("No card selected.")
# # #             else:
# # #                 st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
# # #                 st.write("#### Proceed to delete this card?")
# # #                 if st.button("Yes, Delete Business Card"):
# # #                     cursor.execute("DELETE FROM card_data WHERE card_holder=?", (selected_card,))
# # #                     conn.commit()
# # #                     st.success("Business card information deleted from the database.")

# # #             if st.button(":blue[View updated data]"):
# # #                 cursor.execute("SELECT company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code FROM card_data")
# # #                 data = cursor.fetchall()
# # #                 updated_df = pd.DataFrame(data,
# # #                                           columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email",
# # #                                                    "Website", "Area", "City", "State", "Pin_Code"])
# # #                 st.write(updated_df)

# # #         except:
# # #             st.warning("There is no data available in the database")

# # # # Close the SQLite connection
# # # conn.close()



# # # =====================================================   /   /   Import library   /   /   ================================================= #

# # # [Scanning library]
# # import easyocr # (Optical Character Recognition)
# # import numpy as np
# # import PIL
# # from PIL import Image, ImageDraw
# # import cv2
# # import os
# # import re

# # # [Data frame libraries]
# # import pandas as pd

# # # [Database library]
# # import sqlite3  # Use SQLite instead of MySQL

# # # [Dashboard library]
# # import streamlit as st

# # # ===================================================   /   /   Dash Board   /   /   ======================================================== # 

# # # Configuring Streamlit GUI 
# # st.set_page_config(layout='wide')

# # # Create or connect to the SQLite database
# # conn = sqlite3.connect("bizcard.db")
# # cursor = conn.cursor()

# # # Create the table to store business card data
# # cursor.execute('''CREATE TABLE IF NOT EXISTS bizcard_data (
# #     id INTEGER PRIMARY KEY,
# #     Company_name TEXT,
# #     Card_holder TEXT,
# #     Designation TEXT,
# #     Mobile_number TEXT,
# #     Email TEXT,
# #     Website TEXT,
# #     Area TEXT,
# #     City TEXT,
# #     State TEXT,
# #     Pin_code TEXT
# # )''')

# # conn.commit()

# # # Title
# # st.title(':blue[Business Card Data Extraction]')

# # # Tabs 
# # tab1, tab2 = st.tabs(["Data Extraction zone", "Data modification zone"])

# # # ==========================================   /   /   Data Extraction and upload zone   /   /   ============================================== #

# # with tab1:
# #     st.subheader(':red[Data Extraction]')

# #     # Image file uploaded
# #     import_image = st.file_uploader('**Select a business card (Image file)**', type=['png', 'jpg', "jpeg"], accept_multiple_files=False)

# #     # Note
# #     st.markdown('''File extension support: **PNG, JPG, TIFF**, File size limit: **2 Mb**, Image dimension limit: **1500 pixel**, Language: **English**.''')

# #     # --------------------------------      /   Extraction process   /     ---------------------------------- #

# #     if import_image is not None:
# #         try:
# #             # Create the reader object with desired languages
# #             reader = easyocr.Reader(['en'], gpu=False)

# #         except:
# #             st.info("Error: easyocr module is not installed. Please install it.")

# #         try:
# #             # Read the image file as a PIL Image object
# #             if isinstance(import_image, str):
# #                 image = Image.open(import_image)
# #             elif isinstance(import_image, Image.Image):
# #                 image = import_image
# #             else:
# #                 image = Image.open(import_image)

# #             image_array = np.array(image)
# #             text_read = reader.readtext(image_array)

# #             result = []
# #             for text in text_read:
# #                 result.append(text[1])

# #         except:
# #             st.info("Error: Failed to process the image. Please try again with a different image.")

# #     # -------------------------      /   Display the processed card with yellow box   /     ---------------------- #

# #         col1, col2 = st.columns(2)

# #         with col1:
# #             # Define a function to draw the box on the image
# #             def draw_boxes(image, text_read, color='yellow', width=2):
# #                 # Create a new image with bounding boxes
# #                 image_with_boxes = image.copy()
# #                 draw = ImageDraw.Draw(image_with_boxes)

# #                 # draw boundaries
# #                 for bound in text_read:
# #                     p0, p1, p2, p3 = bound[0]
# #                     draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
# #                 return image_with_boxes

# #             # Function calling
# #             result_image = draw_boxes(image, text_read)

# #             # Result image
# #             st.image(result_image, caption='Captured text')

# #     # ----------------------------    /     Data processing and converted into data frame   /   ------------------ #

# #         with col2:
# #             # Initialize the data dictionary
# #             data = {
# #                 "Company_name": [],
# #                 "Card_holder": [],
# #                 "Designation": [],
# #                 "Mobile_number": [],
# #                 "Email": [],
# #                 "Website": [],
# #                 "Area": [],
# #                 "City": [],
# #                 "State": [],
# #                 "Pin_code": [],
# #             }

# #             # function define
# #             def get_data(res):
# #                 city = ""  # Initialize the city variable
# #                 for ind, i in enumerate(res):
# #                     # To get WEBSITE_URL
# #                     if "www " in i.lower() or "www." in i.lower():
# #                         data["Website"].append(i)
# #                     elif "WWW" in i:
# #                         data["Website"].append(res[ind - 1] + "." + res[ind])

# #                     # To get EMAIL ID
# #                     elif "@" in i:
# #                         data["Email"].append(i)

# #                     # To get MOBILE NUMBER
# #                     elif "-" in i:
# #                         data["Mobile_number"].append(i)
# #                         if len(data["Mobile_number"]) == 2:
# #                             data["Mobile_number"] = " & ".join(data["Mobile_number"])

# #                     # To get COMPANY NAME
# #                     elif ind == len(res) - 1:
# #                         data["Company_name"].append(i)

# #                     # To get CARD HOLDER NAME
# #                     elif ind == 0:
# #                         data["Card_holder"].append(i)

# #                     # To get DESIGNATION
# #                     elif ind == 1:
# #                         data["Designation"].append(i)

# #                     # To get AREA
# #                     if re.findall("^[0-9].+, [a-zA-Z]+", i):
# #                         data["Area"].append(i.split(",")[0])
# #                     elif re.findall("[0-9] [a-zA-Z]+", i):
# #                         data["Area"].append(i)

# #                     # To get CITY NAME
# #                     match1 = re.findall(".+St , ([a-zA-Z]+).+", i)
# #                     match2 = re.findall(".+St,, ([a-zA-Z]+).+", i)
# #                     match3 = re.findall("^[E].*", i)
# #                     if match1:
# #                         city = match1[0]  # Assign the matched city value
# #                     elif match2:
# #                         city = match2[0]  # Assign the matched city value
# #                     elif match3:
# #                         city = match3[0]  # Assign the matched city value

# #                     # To get STATE
# #                     state_match = re.findall("[a-zA-Z]{9} +[0-9]", i)
# #                     if state_match:
# #                         data["State"].append(i[:9])
# #                     elif re.findall("^[0-9].+, ([a-zA-Z]+);", i):
# #                         data["State"].append(i.split()[-1])
# #                     if len(data["State"]) == 2:
# #                         data["State"].pop(0)

# #                     # To get PINCODE
# #                     if len(i) >= 6 and i.isdigit():
# #                         data["Pin_code"].append(i)
# #                     elif re.findall("[a-zA-Z]{9} +[0-9]", i):
# #                         data["Pin_code"].append(i[10:])

# #                 data["City"].append(city)  # Append the city value to the 'city' array

# #             # Call function
# #             get_data(result)

# #             # Create dataframe
# #             data_df = pd.DataFrame(data)

# #             # Show dataframe
# #             st.dataframe(data_df.T)

# #     # --------------------------------------   /   Data Upload to SQLite   /   --------------------------------------- #

# #         # Create a session state object
# #         class SessionState:
# #             def __init__(self, **kwargs):
# #                 self.__dict__.update(kwargs)
# #         session_state = SessionState(data_uploaded=False)

# #         # Upload button
# #         st.write('Click the :red[**Upload to SQLite DB**] button to upload the data')
# #         Upload = st.button('**Upload to SQLite DB**', key='upload_button')

# #         # Check if the button is clicked
# #         if Upload:
# #             session_state.data_uploaded = True

# #         # Execute the program if the button is clicked
# #         if session_state.data_uploaded:
# #             try:
# #                 # Use pandas to insert the DataFrame data into the SQLite Database
# #                 data_df.to_sql('bizcard_data', conn, if_exists='append', index=False)
# #                 conn.commit()

# #                 # Uploaded completed message
# #                 st.info('Data Successfully Uploaded')
# #             except sqlite3.Error as e:
# #                 st.info("Card data already exists")

# #             # Reset the session state after executing the program
# #             session_state.data_uploaded = False

# #     else:
# #         st.info('Click the Browse file button and upload an image')

# # # =================================================   /   /   Modification zone   /   /   ==================================================== #

# # with tab2:

# #     col1, col2 = st.columns(2)

# #     # ------------------------------   /   /   Edit option   /   /   -------------------------------------------- #

# #     with col1:
# #         st.subheader(':red[Edit option]')

# #         try:
# #             # Create a session state object
# #             class SessionState:
# #                 def __init__(self, **kwargs):
# #                     self.__dict__.update(kwargs)
# #             session_state = SessionState(data_update=False)

# #             # Execute the query to retrieve the cardholder data
# #             cursor.execute("SELECT DISTINCT Card_holder FROM bizcard_data")
# #             rows = cursor.fetchall()
# #             names = [row[0] for row in rows]

# #             # Create a selection box to select cardholder name
# #             cardholder_name = st.selectbox("**Select a Cardholder name to Edit the details**", names, key='cardholder_name')

# #             # Fetch the selected cardholder data
# #             cursor.execute("SELECT * FROM bizcard_data WHERE Card_holder = ?", (cardholder_name,))
# #             col_data = cursor.fetchone()

# #             # DISPLAYING ALL THE INFORMATION
# #             Company_name = st.text_input("Company name", col_data[1])
# #             Designation = st.text_input("Designation", col_data[3])
# #             Mobile_number = st.text_input("Mobile number", col_data[4])
# #             Email = st.text_input("Email", col_data[5])
# #             Website = st.text_input("Website", col_data[6])
# #             Area = st.text_input("Area", col_data[7])
# #             City = st.text_input("City", col_data[8])
# #             State = st.text_input("State", col_data[9])
# #             Pin_code = st.text_input("Pincode", col_data[10])

# #             # Update button
# #             st.write('Click the :red[**Update**] button to update the modified data')
# #             update = st.button('**Update**', key='update')

# #             # Check if the button is clicked
# #             if update:
# #                 session_state.data_update = True

# #             # Execute the program if the button is clicked
# #             if session_state.data_update:
# #                 # Update the information for the selected business card in the SQLite database
# #                 cursor.execute(
# #                     "UPDATE bizcard_data SET Company_name = ?, Designation = ?, Mobile_number = ?, Email = ?, "
# #                     "Website = ?, Area = ?, City = ?, State = ?, Pin_code = ? "
# #                     "WHERE Card_holder = ?",
# #                     (Company_name, Designation, Mobile_number, Email, Website, Area, City, State, Pin_code, cardholder_name))
# #                 conn.commit()

# #                 st.success("Successfully Updated.")

# #                 session_state.data_update = False

# #         except sqlite3.Error as e:
# #             st.info('No data stored in the database')

# #     # --------------------------------------   /   /   Delete option   /   /   -------------------------------------- #

# #     with col2:
# #         st.subheader(':red[Delete option]')

# #         try:
# #             # Create a session state object
# #             class SessionState:
# #                 def __init__(self, **kwargs):
# #                     self.__dict__.update(kwargs)
# #             session_state = SessionState(data_delete=False)

# #             # Execute the query to retrieve the cardholder data
# #             cursor.execute("SELECT DISTINCT Card_holder FROM bizcard_data")
# #             rows = cursor.fetchall()
# #             delete_names = [row[0] for row in rows]

# #             # Create a selection box to select cardholder name
# #             delete_name = st.selectbox("**Select a Cardholder name to Delete the details**", delete_names, key='delete_name')

# #             # Delet button
# #             st.write('Click the :red[**Delete**] button to Delete selected Cardholder details')
# #             delete = st.button('**Delete**', key='delete')

# #             # Check if the button is clicked
# #             if delete:
# #                 session_state.data_delete = True

# #             # Execute the program if the button is clicked
# #             if session_state.data_delete:
# #                 # Delete the selected cardholder data from the SQLite database
# #                 cursor.execute("DELETE FROM bizcard_data WHERE Card_holder = ?", (delete_name,))
# #                 conn.commit()

# #                 st.success("Successfully deleted from database.")

# #                 session_state.data_delete = False                                                                                                                                                                                               

# #         except sqlite3.Error as e:
# #             st.info('No data stored in the database')

# # # ======================================================   /   /   Completed   /   /   ====================================================== #

# # [Scanning library]
# import easyocr # (Optical Character Recognition)
# import numpy as np
# import PIL
# from PIL import Image, ImageDraw
# import cv2
# import os
# import re

# # [Data frame libraries]
# import pandas as pd

# # [Database library]
# import sqlite3  # Use SQLite instead of MySQL

# # [Dashboard library]
# import streamlit as st

# # ===================================================   /   /   Dash Board   /   /   ======================================================== # 

# # Configuring Streamlit GUI 
# st.set_page_config(layout='wide')

# # Create or connect to the SQLite database
# conn = sqlite3.connect("bizcard.db")
# cursor = conn.cursor()

# # Create the table to store business card data
# cursor.execute('''CREATE TABLE IF NOT EXISTS bizcard_data (
#     id INTEGER PRIMARY KEY,
#     Company_name TEXT,
#     Card_holder TEXT,
#     Designation TEXT,
#     Mobile_number TEXT,
#     Email TEXT,
#     Website TEXT,
#     Area TEXT,
#     City TEXT,
#     State TEXT,
#     Pin_code TEXT
# )''')

# conn.commit()

# # Title
# st.title(':blue[Business Card Data Extraction]')

# # Tabs 
# tab1, tab2 = st.tabs(["Data Extraction zone", "Data modification zone"])

# # ==========================================   /   /   Data Extraction and upload zone   /   /   ============================================== #

# with tab1:
#     st.subheader(':red[Data Extraction]')

#     # Image file uploaded
#     import_image = st.file_uploader('**Select a business card (Image file)**', type=['png', 'jpg', "jpeg"], accept_multiple_files=False)

#     # Note
#     st.markdown('''File extension support: **PNG, JPG, TIFF**, File size limit: **2 Mb**, Image dimension limit: **1500 pixel**, Language: **English**.''')

#     # --------------------------------      /   Extraction process   /     ---------------------------------- #

#     if import_image is not None:
#         try:
#             # Create the reader object with desired languages
#             reader = easyocr.Reader(['en'], gpu=False)

#         except:
#             st.info("Error: easyocr module is not installed. Please install it.")

#         try:
#             # Read the image file as a PIL Image object
#             if isinstance(import_image, str):
#                 image = Image.open(import_image)
#             elif isinstance(import_image, Image.Image):
#                 image = import_image
#             else:
#                 image = Image.open(import_image)

#             image_array = np.array(image)
#             text_read = reader.readtext(image_array)

#             result = []
#             for text in text_read:
#                 result.append(text[1])

#         except:
#             st.info("Error: Failed to process the image. Please try again with a different image.")

#     # -------------------------      /   Display the processed card with yellow box   /     ---------------------- #

#         col1, col2 = st.columns(2)

#         with col1:
#             # Define a function to draw the box on the image
#             def draw_boxes(image, text_read, color='yellow', width=2):
#                 # Create a new image with bounding boxes
#                 image_with_boxes = image.copy()
#                 draw = ImageDraw.Draw(image_with_boxes)

#                 # draw boundaries
#                 for bound in text_read:
#                     p0, p1, p2, p3 = bound[0]
#                     draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
#                 return image_with_boxes

#             # Function calling
#             result_image = draw_boxes(image, text_read)

#             # Result image
#             st.image(result_image, caption='Captured text')

#     # ----------------------------    /     Data processing and converted into data frame   /   ------------------ #

#         with col2:
#             # Initialize the data dictionary
#             data = {
#                 "Company_name": [],
#                 "Card_holder": [],
#                 "Designation": [],
#                 "Mobile_number": [],
#                 "Email": [],
#                 "Website": [],
#                 "Area": [],
#                 "City": [],
#                 "State": [],
#                 "Pin_code": [],
#             }

#             # function define
#             # function define
#         def get_data(res):
#             city = ""  # Initialize the city variable
#             mobile_numbers = [i for i in res if re.match(r'\d{10,}', i)]

#             for ind, i in enumerate(res):
#                 # To get WEBSITE_URL
#                 if "www " in i.lower() or "www." in i.lower():
#                     data["Website"].append(i)
#                 elif "WWW" in i:
#                     data["Website"].append(res[ind - 1] + "." + res[ind])

#                 # To get EMAIL ID
#                 elif "@" in i:
#                     data["Email"].append(i)

#                 # To get COMPANY NAME
#                 elif ind == len(res) - 1:
#                     data["Company_name"].append(i)

#                 # To get CARD HOLDER NAME
#                 elif ind == 0:
#                     data["Card_holder"].append(i)

#                 # To get DESIGNATION
#                 elif ind == 1:
#                     data["Designation"].append(i)

#                 # To get AREA
#                 if re.findall("^[0-9].+, [a-zA-Z]+", i):
#                     data["Area"].append(i.split(",")[0])
#                 elif re.findall("[0-9] [a-zA-Z]+", i):
#                     data["Area"].append(i)

#                 # To get CITY NAME
#                 match1 = re.findall(".+St , ([a-zA-Z]+).+", i)
#                 match2 = re.findall(".+St,, ([a-zA-Z]+).+", i)
#                 match3 = re.findall("^[E].*", i)
#                 if match1:
#                     city = match1[0]  # Assign the matched city value
#                 elif match2:
#                     city = match2[0]  # Assign the matched city value
#                 elif match3:
#                     city = match3[0]  # Assign the matched city value

#                 # To get STATE
#                 state_match = re.findall("[a-zA-Z]{9} +[0-9]", i)
#                 if state_match:
#                     data["State"].append(i[:9])
#                 elif re.findall("^[0-9].+, ([a-zA-Z]+);", i):
#                     data["State"].append(i.split()[-1])
#                 if len(data["State"]) == 2:
#                     data["State"].pop(0)

#                 # To get PINCODE
#                 if len(i) >= 6 and i.isdigit():
#                     data["Pin_code"].append(i)
#                 elif re.findall("[a-zA-Z]{9} +[0-9]", i):
#                     data["Pin_code"].append(i[10:])

#             data["City"].append(city)  # Append the city value to the 'city' array

#             # To get MOBILE NUMBER
#             mobile_numbers = [i for i in res if re.match(r'\d{10,}', i)]
#             if mobile_numbers:
#                 data["Mobile_number"].extend(mobile_numbers)  # Append the city value to the 'city' array

#             # Call function
#             get_data(result)

#             # Create dataframe
#             data_df = pd.DataFrame(data)

#             # Show dataframe
#             st.dataframe(data_df.T)

#     # --------------------------------------   /   Data Upload to SQLite   /   --------------------------------------- #

#         # Create a session state object
#         class SessionState:
#             def __init__(self, **kwargs):
#                 self.__dict__.update(kwargs)
                
#         session_state = SessionState(data_uploaded=False)

#         # Upload button
#         st.write('Click the :red[**Upload to SQLite DB**] button to upload the data')
#         Upload = st.button('**Upload to SQLite DB**', key='upload_button')

#         # Check if the button is clicked
#         if Upload:
#             session_state.data_uploaded = True

#         # Execute the program if the button is clicked
#         if session_state.data_uploaded:
#             try:
#                 # Use pandas to insert the DataFrame data into the SQLite Database
#                 data_df.to_sql('bizcard_data', conn, if_exists='append', index=False)
#                 conn.commit()

#                 # Uploaded completed message
#                 st.info('Data Successfully Uploaded')
#             except sqlite3.Error as e:
#                 st.info("Card data already exists")

#             # Reset the session state after executing the program
#             session_state.data_uploaded = False

#     else:
#         st.info('Click the Browse file button and upload an image')

# # =================================================   /   /   Modification zone   /   /   ==================================================== #

# with tab2:

#     col1, col2 = st.columns(2)

#     # ------------------------------   /   /   Edit option   /   /   -------------------------------------------- #

#     with col1:
#         st.subheader(':red[Edit option]')

#         try:
#             # Create a session state object
#             class SessionState:
#                 def __init__(self, **kwargs):
#                     self.__dict__.update(kwargs)
#             session_state = SessionState(data_update=False)

#             # Execute the query to retrieve the cardholder data
#             cursor.execute("SELECT DISTINCT Card_holder FROM bizcard_data")
#             rows = cursor.fetchall()
#             names = [row[0] for row in rows]

#             if names:
#                 # Create a selection box to select cardholder name
#                 cardholder_name = st.selectbox("**Select a Cardholder name to Edit the details**", names, key='cardholder_name')

#                 # Fetch the selected cardholder data
#                 cursor.execute("SELECT * FROM bizcard_data WHERE Card_holder = ?", (cardholder_name,))
#                 col_data = cursor.fetchone()

#                 if col_data:
#                     # DISPLAYING ALL THE INFORMATION
#                     Company_name = st.text_input("Company name", col_data[1])
#                     Designation = st.text_input("Designation", col_data[3])
#                     Mobile_number = st.text_input("Mobile number", col_data[4])
#                     Email = st.text_input("Email", col_data[5])
#                     Website = st.text_input("Website", col_data[6])
#                     Area = st.text_input("Area", col_data[7])
#                     City = st.text_input("City", col_data[8])
#                     State = st.text_input("State", col_data[9])
#                     Pin_code = st.text_input("Pincode", col_data[10])

#                     # Update button
#                     st.write('Click the :red[**Update**] button to update the modified data')
#                     update = st.button('**Update**', key='update')

#                     # Check if the button is clicked
#                     if update:
#                         session_state.data_update = True

#                     # Execute the program if the button is clicked
#                     if session_state.data_update:
#                         # Update the information for the selected business card in the SQLite database
#                         cursor.execute(
#                             "UPDATE bizcard_data SET Company_name = ?, Designation = ?, Mobile_number = ?, Email = ?, "
#                             "Website = ?, Area = ?, City = ?, State = ?, Pin_code = ? "
#                             "WHERE Card_holder = ?",
#                             (Company_name, Designation, Mobile_number, Email, Website, Area, City, State, Pin_code, cardholder_name))
#                         conn.commit()

#                         st.success("Successfully Updated.")

#                         session_state.data_update = False
#                 else:
#                     st.info("No data found for the selected cardholder.")
#             else:
#                 st.info("No cardholders found in the database.")

#         except sqlite3.Error as e:
#             st.error(f"An error occurred: {str(e)}")

# # ======================================================   /   /   Completed   /   /   ====================================================== #


import easyocr  # Optical Character Recognition
import numpy as np
from PIL import Image, ImageDraw
import re

# Data frame libraries
import pandas as pd

# Database library
import sqlite3  # Use SQLite instead of MySQL

# Dashboard library
import streamlit as st

# Configuring Streamlit GUI
st.set_page_config(layout='wide')

# Create or connect to the SQLite database
conn = sqlite3.connect("bizcard.db")
cursor = conn.cursor()

# Create the table to store business card data
cursor.execute('''CREATE TABLE IF NOT EXISTS bizcard_data (
    id INTEGER PRIMARY KEY,
    Company_name TEXT,
    Card_holder TEXT,
    Designation TEXT,
    Mobile_number TEXT,
    Email TEXT,
    Website TEXT,
    Area TEXT,
    City TEXT,
    State TEXT,
    Pin_code TEXT
)''')

conn.commit()

# Title
st.title(':blue[Business Card Data Extraction]')

# Tabs
tab1, tab2 = st.columns(2)

# ==========================================   /   /   Data Extraction and upload zone   /   /   ============================================== #

with tab1:
    st.subheader(':red[Data Extraction]')

    # Image file uploaded
    import_image = st.file_uploader('**Select a business card (Image file)**', type=['png', 'jpg', "jpeg"], accept_multiple_files=False)

    # Note
    st.markdown(
        '''File extension support: **PNG, JPG, TIFF**, File size limit: **2 Mb**, Image dimension limit: **1500 pixel**, Language: **English**.''')

    # --------------------------------      /   Extraction process   /     ---------------------------------- #

    if import_image is not None:
        try:
            # Create the reader object with desired languages
            reader = easyocr.Reader(['en'], gpu=False)

        except:
            st.info("Error: easyocr module is not installed. Please install it.")

        try:
            # Read the image file as a PIL Image object
            if isinstance(import_image, str):
                image = Image.open(import_image)
            elif isinstance(import_image, Image.Image):
                image = import_image
            else:
                image = Image.open(import_image)

            image_array = np.array(image)
            text_read = reader.readtext(image_array)

            result = []
            for text in text_read:
                result.append(text[1])

        except:
            st.info("Error: Failed to process the image. Please try again with a different image.")

        # -------------------------      /   Display the processed card with yellow box   /     ---------------------- #

        col1, col2 = st.columns(2)

        with col1:
            # Define a function to draw the box on the image
            def draw_boxes(image, text_read, color='yellow', width=2):
                # Create a new image with bounding boxes
                image_with_boxes = image.copy()
                draw = ImageDraw.Draw(image_with_boxes)

                # draw boundaries
                for bound in text_read:
                    p0, p1, p2, p3 = bound[0]
                    draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
                return image_with_boxes

            # Function calling
            result_image = draw_boxes(image, text_read)

            # Result image
            st.image(result_image, caption='Captured text')

        # ----------------------------    /     Data processing and converted into data frame   /   ------------------ #

        with col2:
            # Initialize the data dictionary
            # Initialize the data dictionary
            data = {
                "Company_name": [],
                "Card_holder": [],
                "Designation": [],
                "Mobile_number": [],
                "Email": [],
                "Website": [],
                "Area": [],
                "City": [],
                "State": [],
                "Pin_code": [],
            }

            # Function to get data
            def get_data(res):
                city = ""  # Initialize the city variable
                mobile_numbers = [i for i in res if re.match(r'\d{10,}', i)]

                card_holder_name = ""
                designation = ""
                area = ""
                city = ""
                state = ""
                pin_code = ""

                for ind, i in enumerate(res):
                    # To get WEBSITE_URL
                    if "www " in i.lower() or "www." in i.lower():
                        data["Website"].append(i)
                    elif "WWW" in i:
                        data["Website"].append(res[ind - 1] + "." + res[ind])

                    # To get EMAIL ID
                    elif "@" in i:
                        data["Email"].append(i)

                    # To get COMPANY NAME
                    elif ind == len(res) - 1:
                        data["Company_name"].append(i)

                    # To get CARD HOLDER NAME
                    elif ind == 0:
                        card_holder_name = i

                    # To get DESIGNATION
                    elif ind == 1:
                        designation = i

                    # To get AREA
                    if re.findall("^[0-9].+, [a-zA-Z]+", i):
                        area = i.split(",")[0]
                    elif re.findall("[0-9] [a-zA-Z]+", i):
                        area = i

                    # To get CITY NAME
                    match1 = re.findall(".+St , ([a-zA-Z]+).+", i)
                    match2 = re.findall(".+St,, ([a-zA-Z]+).+", i)
                    match3 = re.findall("^[E].*", i)
                    if match1:
                        city = match1[0]  # Assign the matched city value
                    elif match2:
                        city = match2[0]  # Assign the matched city value
                    elif match3:
                        city = match3[0]  # Assign the matched city value

                    # To get STATE
                    state_match = re.findall("[a-zA-Z]{9} +[0-9]", i)
                    if state_match:
                        state = i[:9]
                    elif re.findall("^[0-9].+, ([a-zA-Z]+);", i):
                        state = i.split()[-1]
                    if len(data["State"]) == 2:
                        state = data["State"].pop(0)

                    # To get PINCODE
                    if len(i) >= 6 and i.isdigit():
                        pin_code = i
                    elif re.findall("[a-zA-Z]{9} +[0-9]", i):
                        pin_code = i[10:]

                data["Card_holder"].append(card_holder_name)
                data["Designation"].append(designation)
                data["Area"].append(area)
                data["City"].append(city)
                data["State"].append(state)
                data["Pin_code"].append(pin_code)

                # To get MOBILE NUMBER
                data["Mobile_number"].extend(mobile_numbers)  # Append the city value to the 'city' array

            # Call function
            get_data(result)

            # Ensure all lists have the same length
            max_length = max(
                len(data["Company_name"]), len(data["Card_holder"]),
                len(data["Designation"]), len(data["Mobile_number"]),
                len(data["Email"]), len(data["Website"]),
                len(data["Area"]), len(data["City"]),
                len(data["State"]), len(data["Pin_code"])
            )

            # Fill in any missing values
            for key in data:
                while len(data[key]) < max_length:
                    data[key].append("")

            # Create dataframe
            data_df = pd.DataFrame(data)

            # Show dataframe
            st.dataframe(data_df.T)

        # --------------------------------------   /   Data Upload to SQLite   /   --------------------------------------- #

        # Create a session state object
        class SessionState:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
        session_state = SessionState(data_uploaded=False)

        # Upload button
        st.write('Click the :red[**Upload to SQLite DB**] button to upload the data')
        Upload = st.button('**Upload to SQLite DB**', key='upload_button')

        # Check if the button is clicked
        if Upload:
            session_state.data_uploaded = True

        # Execute the program if the button is clicked
        if session_state.data_uploaded:
            try:
                # Use pandas to insert the DataFrame data into the SQLite Database
                data_df.to_sql('bizcard_data', conn, if_exists='append', index=False)
                conn.commit()

                # Uploaded completed message
                st.info('Data Successfully Uploaded')
            except sqlite3.Error as e:
                st.info("Card data already exists")

            # Reset the session state after executing the program
            session_state.data_uploaded = False

    else:
        st.info('Click the Browse file button and upload an image')

# =================================================   /   /   Modification zone   /   /   ==================================================== #

with tab2:

    col1, col2 = st.columns(2)

    # ------------------------------   /   /   Edit option   /   /   -------------------------------------------- #

    with col1:
        st.subheader(':red[Edit option]')

        try:
            # Create a session state object
            class SessionState:
                def __init__(self, **kwargs):
                    self.__dict__.update(kwargs)
            session_state = SessionState(data_update=False)

            # Execute the query to retrieve the cardholder data
            cursor.execute("SELECT DISTINCT Card_holder FROM bizcard_data")
            rows = cursor.fetchall()
            names = [row[0] for row in rows]

            if names:
                # Create a selection box to select cardholder name
                cardholder_name = st.selectbox("**Select a Cardholder name to Edit the details**", names, key='cardholder_name')

                # Fetch the selected cardholder data
                cursor.execute("SELECT * FROM bizcard_data WHERE Card_holder = ?", (cardholder_name,))
                col_data = cursor.fetchone()

                if col_data:
                    # DISPLAYING ALL THE INFORMATION
                    Company_name = st.text_input("Company name", col_data[1])
                    Designation = st.text_input("Designation", col_data[3])
                    Mobile_number = st.text_input("Mobile number", col_data[4])
                    Email = st.text_input("Email", col_data[5])
                    Website = st.text_input("Website", col_data[6])
                    Area = st.text_input("Area", col_data[7])
                    City = st.text_input("City", col_data[8])
                    State = st.text_input("State", col_data[9])
                    Pin_code = st.text_input("Pincode", col_data[10])

                    # Update button
                    st.write('Click the :red[**Update**] button to update the modified data')
                    update = st.button('**Update**', key='update')

                    # Check if the button is clicked
                    if update:
                        session_state.data_update = True

                    # Execute the program if the button is clicked
                    if session_state.data_update:
                        # Update the information for the selected business card in the SQLite database
                        cursor.execute(
                            "UPDATE bizcard_data SET Company_name = ?, Designation = ?, Mobile_number = ?, Email = ?, "
                            "Website = ?, Area = ?, City = ?, State = ?, Pin_code = ? "
                            "WHERE Card_holder = ?",
                            (Company_name, Designation, Mobile_number, Email, Website, Area, City, State, Pin_code, cardholder_name))
                        conn.commit()

                        st.success("Successfully Updated.")

                        session_state.data_update = False
                else:
                    st.info("No data found for the selected cardholder.")
            else:
                st.info("No cardholders found in the database.")

        except sqlite3.Error as e:
            st.error(f"An error occurred: {str(e)}")
