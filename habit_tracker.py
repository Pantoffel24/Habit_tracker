import streamlit as st
from datetime import datetime, timedelta
import json
import os

#Data config
DATA_FILE = "habits.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"completed days": []}

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data,f)

#Setting up UI
st.set_page_config(page_title = 'Habit Tracker')
st.title('Habit Tracker')

data = load_data()
today = datetime.now().strftime("%Y-%m-%d")

#Ticking the box mechanic
if today in data['completed days']:
    st.success('Good job!')
    if st.button('Unmark Today'):
        data['completed days'].remove(today)
        save_data(data)
        st.rerun()
else:
    if st.button('Complete Today'):
        data['completed days'].append(today)
        save_data(data)
        st.rerun()
st.divider()


#Visual history
st.write('Progress last 30 days')
cols = st.columns(7)
start_date = datetime.now() - timedelta(days = 29)

for i in range(30):
    date_add = start_date + timedelta(days = i)
    current_date = date_add.strftime("%Y-%m-%d")
    display_date = date_add.strftime("%d")

    with cols[i%7]:
        if current_date in data['completed days']:
            st.markdown(f"### {display_date}")
            st.markdown("🟩")
        else:
            st.markdown(f"### {display_date}")
            st.markdown("⬜")

#Streak calculation
streak = 0
check_date = datetime.now()
while check_date.strftime("%Y-%m-%d") in data['completed days']:
    streak += 1
    check_date -= timedelta(days = 1)

st.write(f"Current Streak: {streak} days")