import streamlit as st
from datetime import datetime, timedelta
import json
import os
from supabase import Client, create_client
#Data config
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]

print("URL AND KEY INITIALISED")
supabase: Client = create_client(URL, KEY)

def load_data():
    response = supabase.table('diet_data').select('date_string').execute()
    #Pull part
    completed_days = [row['date_string'] for row in response.data]
    return {"completed_days": completed_days}


def save_data(date_str, action = 'add'):
    if action == 'add':
        supabase.table('diet_data').insert({'date_string': date_str}).execute()
    elif action == 'remove':
        supabase.table('diet_data').delete().eq('date_string', date_str).execute()




#Setting up UI
st.set_page_config(page_title = 'Habit Tracker')
st.title('Diet tracker')
st.subheader('For tracking each day you ate a good amount.')
st.subheader('You got this!')

data = load_data()
#Today will is actually now going to be yesterday. I'll change the notation later
yesterday = (datetime.now()-timedelta(days = 1)).strftime("%Y-%m-%d")

#Display bar weekly
last_7_days = []
for i in range(7):
    temp_day = (datetime.now() - timedelta(days = 1)) - timedelta(days = i)
    #Convert to string
    date_string = temp_day.strftime("%Y-%m-%d")
    last_7_days.append(date_string)

weekly_count = 0
for day in last_7_days:
    if day in data['completed_days']:
        weekly_count += 1
if weekly_count == 7:
    st.balloons()
    st.subheader("Congratulations! You nailed 1 week!")

#Ticking the box mechanic
if yesterday in data['completed_days']:
    st.success('Good job!')
    if st.button('Unmark Yesterday'):
        save_data(yesterday, action = 'remove')
        st.rerun()
else:
    if st.button('Complete Yesterday'):
        save_data(yesterday, action = 'add')
        st.rerun()
st.divider()


#Visual history
st.write('Progress last 30 days')
cols = st.columns(7)
start_date = (datetime.now()) - timedelta(days = 29)
today = (datetime.now()).strftime("%Y-%m-%d")

for i in range(30):
    date_add = start_date + timedelta(days = i)
    current_date = date_add.strftime("%Y-%m-%d")
    display_date = date_add.strftime("%d")

    with cols[i%7]:
        if current_date == today:
            st.markdown(f"### {display_date}")
            st.markdown("⬜")
        elif current_date in data['completed_days']:
            st.markdown(f"### {display_date}")
            st.markdown("🟩")
        else:
            st.markdown(f"### {display_date}")
            st.markdown("🟥")


#Streak calculation
streak = 0
check_date = datetime.now() - timedelta(days = 1)
while check_date.strftime("%Y-%m-%d") in data['completed_days']:
    streak += 1
    check_date -= timedelta(days = 1)

st.write(f"Current Streak: {streak} days")

#Goal logic
#This is for progressing things like 7 days and a month and what not
total_completed = len(data['completed_days'])
weekly_goal = 7
monthly_goal = 31
progress_monthly = min(total_completed/monthly_goal,1.0)


#Display bar monthly
st.write(f'## Monthly Goal: {total_completed}/{monthly_goal} days')
st.progress(progress_monthly)


st.write(f'## Weekly Challenge: {weekly_count}/{weekly_goal} days')
progress_weekly = min(weekly_count/weekly_goal,1.0)
st.progress(progress_weekly)
