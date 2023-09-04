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