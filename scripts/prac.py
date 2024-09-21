import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import requests
#from supabase_py import create_client,Client
from io import StringIO  # Import StringIO directly from the io module
from io import BytesIO
from datetime import datetime
import random
from google.oauth2 import service_account


# Function to get the current timestamp
def get_timestamp():
    return datetime.now()

# Display the PNG image in the top left corner of the Streamlit sidebar with custom dimensions
image_path = 'https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/VS-logo.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svVlMtbG9nby5wbmciLCJpYXQiOjE3MjE5NzA3ODUsImV4cCI6MTc1MzUwNjc4NX0.purLZOGk272W80A4OlvnavqVB9u-yExhzpmI3dZrjdM&t=2024-07-26T05%3A13%3A02.704Z'
st.markdown(
    f'<div style="text-align:center"><img src="{image_path}" width="150"></div>',
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='color: black; font-weight: bold;'>Live Sessions: Attendance & Feedback</h1>", 
    unsafe_allow_html=True
)



# Fetch the service account credentials from the environment variable or any secure location
# Assume the credentials are fetched and stored in service_account_info
# Fetch service account credentials from Supabase storage
supabase_credentials_url = "https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/studied-indexer-431906-h1-e3634918ab42.json?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svc3R1ZGllZC1pbmRleGVyLTQzMTkwNi1oMS1lMzYzNDkxOGFiNDIuanNvbiIsImlhdCI6MTcyNjkwMzEzNywiZXhwIjoxNzU4NDM5MTM3fQ.d-YWFIIV3ue7eUwUIemVHKrxVSgsdy3Dm34bCfkKBPE&t=2024-09-21T07%3A18%3A57.318Z"
response = requests.get(supabase_credentials_url)
    
if response.status_code == 200:
    # Decode the content of the response as a JSON keyfile and create service account credentials
    service_account_info = response.json()
        

# Use the service account info to create credentials
creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(creds)

# Define the sheet key
sheet_key = '175j97xicFqFA1eKPBjzXzQJaKyIfaJYwpwhaL6qGFDg'

# Open the Google Sheet by key and retrieve the specific worksheet
sheet = client.open_by_key(sheet_key).sheet1  # Update with the correct sheet name or index

# Fetch the number from the Google Sheet at row index 1
number_from_sheet = sheet.cell(1, 1).value

# Create a text input box for the user to enter the code
entered_code = st.text_input("Enter the code")

# Check if the entered code matches the number from the Google Sheet
if entered_code == number_from_sheet:
    st.write("Code matched! Further functionalities can now run.")

        
    file_url = 'https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/General%20Information%20source.csv?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svR2VuZXJhbCBJbmZvcm1hdGlvbiBzb3VyY2UuY3N2IiwiaWF0IjoxNzI2ODMzNzExLCJleHAiOjE3NTgzNjk3MTF9.uSfuVCQQnXyDJibKm5rz7uZXzhZd--1SvWpQixEqFhE&t=2024-09-20T12%3A01%3A49.688Z'
    # Make a GET request to the URL to retrieve the CSV file
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Read the content of the response as a pandas DataFrame, specifying the appropriate encoding
        data = pd.read_csv(BytesIO(response.content), encoding='latin1')  # You can try 'latin1' encoding as an alternative
        # Proceed with processing the data in the dataframe 'df'
    except requests.exceptions.RequestException as e:
        print("An error occurred while accessing the CSV file:", e)

            
    #data = pd.read_excel(r"C:\Users\User\Downloads\General Information Source.xlsx")


    #if update_code == access_code:
    email_phone = st.text_input("Enter the email ID that you use to login to the VigyanShaala app/platform *:")
    if not email_phone in data['Email'].values:
        st.error("Please fill in all the compulsory fields marked with * before proceeding.")
        st.stop()


    # Split the input into email and phone number
    email = ""
    phone = ""
    if "@" in email_phone:  # Check if the input contains '@', assuming it's an email
        email = email_phone
    else:  # If '@' is not found, assume it's a phone number
        phone = email_phone

    if email in data['Email'].values:
        # Get the associated information (college name, class) for the entered email or phone
        user_info = data[(data['Email'] == email_phone)]
    
        # Display the entered email and phone number
        st.write("Entered Email ID:", email)
    
    
        # Check if the email or phone exists in the data
        if not user_info.empty:
            for index, row in user_info.iterrows():
                college_name = row['Name of College']
                student_class = row['Name']
            
            
        else:
            st.error("Entered Email ID or Phone number does not match any records in the data. Please fill in all the compulsory fields marked with * before proceeding.")
            st.stop()

    st.write("College Name:", college_name)
    st.write("Name:", student_class)
    # Create a dot button with options arranged horizontally
    selected_option = st.radio("Select the type of live session you attended today. (Refer Program Calendar*:", ("Special AMA Session", "Live Speak Up Kalpana session", "Live Masterclass Session","Live Mentee mixer event","Live Workshop","Live Kalpana- She for STEM Inauguration","Live Orientation Session"))

    # Use the selected_option
    st.write("You have selected:", selected_option)

    if selected_option == "Live Speak Up Kalpana session":

        # Create a dot button with options arranged horizontally
        option1 = st.radio("Prior to today's talk, have you had an opportunity to hear and interact with women role models from these STEM fields?:", ("Yes","No"))

        option = st.radio("Did today's talk introduce you to:", 
                ("Exposure to New field of STEM careers",
                   "Thinking broadly for careers and opportunities in STEM",
                   "Skills and qualities required to excel in these STEM careers (cross disciplinarity and interdisciplinary thinking, computational skills, social surveys, teaching children about ecology)",
                   "Importance of Networking - both peer networking and networking with seniors (especially from various other disciplines)",
                   "None of the above", 
                "Other"))

        if option == "Other":
            other_response = st.text_input("Other:")


        options = st.radio("How Inspiring did you find the session?",("Not Inspiring at all-Boring", 
                "Not Inspiring",
                   "Neutral",
                   "Inspiring",
                   "Very Inspiring"
                ))


        optionn = st.radio("How relatable did you find our previous Mentees? Can you apply anything to yourself? Did you think, if they can do these big things, So can I?",
                ("Not relatable at all, very confusing", 
                   "Not relatable-Do not know what to take",
                   "Neutral - Neither relatable nor not-relatable",
                   "Relatable-somewhere i feel, if she can do it, so can I",
                   "Very Relatable-strong feeling that even i can do it, if they can do it."
                ))




    Major_takeaway = st.text_area("What are the major takeaways from today's live session*:", height=60)

    # Display the instruction
    st.write("How would you rate today's live session?:")
    # Create a placeholder for selected rating
    selected_rating = None
    selected_value = st.select_slider("Ratings", options=[1, 2, 3, 4, 5])

    input=st.text_area("Do you have any suggestions to make our Live sessions better?" ,height=30)  

    timestamp = get_timestamp()
    timestamp_str = str(timestamp)
    #st.write(f'The current timestamp is: {timestamp_str}')


    # Define the function to create the feedback DataFrame
    def create_feedback_dataframe(email_phone, student_class, college_name, selected_option, option1, option, options, optionn, Major_takeaway, selected_value, input,timestamp_str):
        if selected_option == "Live Speak Up Kalpana session":
        # Use the detailed function
            data = {
                'Email': [email_phone],
                'Name': [student_class],
                'Name of College': [college_name],
                'Type of live session attended today': [selected_option],
                "Prior to today's talk, have you had an opportunity to hear and interact with women role models from these STEM fields?": [option1],
                "Did today's talk introduce you to": [option],
                "How Inspiring did you find the session?": [options],
                "How relatable did you find our previous Mentees? Can you apply anything to yourself? Did you think, if they can do these big things, So can I?": [optionn],
                "Major takeaways from todays live session": [Major_takeaway],
                "Rate today's live session": [selected_value],
                "Do you have any suggestions to make our Live sessions better?": [input],
                "Timestamp":[timestamp_str]
            }
        else:
        #  Use the simpler function
            data = {
            'Email': [email_phone],
            'Name': [student_class],
            'Name of College': [college_name],
            'Type of live session attended today': [selected_option],
            "Prior to today's talk, have you had an opportunity to hear and interact with women role models from these STEM fields?": [''],
            "Did today's talk introduce you to": [''],
            "How Inspiring did you find the session?": [''],
            "How relatable did you find our previous Mentees? Can you apply anything to yourself? Did you think, if they can do these big things, So can I?": [''],
            "Major takeaways from todays live session": [Major_takeaway],
            "Rate today's live session": [selected_value],
            "Do you have any suggestions to make our Live sessions better?": [input],
            "Timestamp":[timestamp_str]
            }

        feedback_df = pd.DataFrame(data)
        return feedback_df


    if selected_option == "Live Speak Up Kalpana session":
        combined_df = create_feedback_dataframe(email_phone,student_class, college_name, selected_option, option1, option, options, optionn, Major_takeaway, selected_value, input,timestamp_str)
                             
    else:
        combined_df = create_feedback_dataframe(email_phone,student_class, college_name, selected_option, '', '', '', '', Major_takeaway, selected_value, input,timestamp_str)


    supabase_credentials_url = 'https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/studied-indexer-431906-h1-e3634918ab42.json?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svc3R1ZGllZC1pbmRleGVyLTQzMTkwNi1oMS1lMzYzNDkxOGFiNDIuanNvbiIsImlhdCI6MTcyNjgzNzM3NywiZXhwIjoxNzU4MzczMzc3fQ.Pl6qNuXIuRDXMnFm0VJx2GamlvfNx8_otpZ8PdFnwVw&t=2024-09-20T13%3A02%3A56.284Z'

    # Fetch service account credentials from Supabase storage
    response = requests.get(supabase_credentials_url)

    if response.status_code == 200:
    # Decode the content of the response as a JSON keyfile and create service account credentials
        service_account_info = response.json()
    
    # Use the service account info to create credentials
        creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=['https://www.googleapis.com/auth/spreadsheets'])
        client = gspread.authorize(creds)
    # Obtain an access token for the specified scope
        access_token = creds.token

        # The access_token variable now contains the access token that can be used to authenticate requests to the Google API
    else:
        print("Failed to fetch the service account credentials. Status code:", response.status_code)

        # Set up credentials using the service account file
        #creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\User\Downloads\studied-indexer-431906-h1-b8e07c75772f.json", scope)

    # Create a button in Streamlit
    combined_button_text = "Print"
    if st.button(combined_button_text):
        # Insert the feedback dataframe into the Google Sheet
        sheet_key = '1B-Rq9OzxCLNN4JKHM5EEhYR1n9efioq9xARnqG0MuWM'
        sheet_name ='Attendance GUI'
        sheet = client.open_by_key(sheet_key).get_worksheet(0)  # Update with the correct sheet name or index
        # Get existing data and determine the next row
        existing_data = sheet.get_all_values()
        next_row_index = len(existing_data) + 1
        
        # Append the new data below the already stored data
        data_to_insert = combined_df.values.tolist()
        sheet.update(f'A{next_row_index}', data_to_insert)
        st.write("Feedback data inserted successfully")
        st.balloons()
    
else:
    st.write("Code did not match. Further functionalities will not run.")
