import streamlit as st
from PIL import Image
import os
import pandas as pd
import numpy as np


st.set_page_config(page_title = "Jira tasks reports",
                  page_icon = ":sun_with_face:",
                  layout = "wide")



try:
    uploaded_files = st.file_uploader("Choose CSV file",type = ["csv"])



    df = pd.read_csv(uploaded_files)
except:

    st.subheader("Please select file to continue")
    st.stop()





st.title('Daily status  - Jira Tasks')








status = df.pivot_table(index = 'Assignee',columns = 'Status',values = 'Issue key',aggfunc = 'count',margins = True,fill_value=0).reset_index()
status['Pending'] = status['All']-status['CSI Verified']
status["Completion%"] = round((status['CSI Verified']/status['All'])*100).astype(str)+ '%'


st.dataframe(status)

def convert_df(file1):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return file1.to_csv().encode('utf-8')

csv = convert_df(status)



st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='status.csv',
    mime='text/csv',
)

def automail():

    import email, smtplib, ssl
    import time

    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText



    sender_email = 'cyspanautomail@gmail.com'
    password = 'vgitaridhtqsxahi'
    #receiver_email = "jishnuva10@gmail.com"
    receiver_email = 'pbabu@integretz.com'
    subject = "Jira Status"


    from pretty_html_table import build_table
    output = build_table(status, 'blue_light')




    body = "Hi,\n\nPlease find attached status for your reference.\n\n"

    body2 = "\n\nThanks and Regards\n\nJishnu V A\n+91 9995355951\n\n"


    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(status.to_html())

    part1 = MIMEText(html, 'html')



    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = "jishnuva10@gmail.com"
    message["Subject"] = subject
    message["Cc"] = "cyspanautomail@gmail.com"



    # Add body to email
    message.attach(MIMEText(body, "plain"))
    message.attach(part1)
    message.attach(MIMEText(body2, "plain"))



    # Add attachment to message and convert message to string
    #message.attach(part1)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    print("mail send")


st.button('Email status',automail())



