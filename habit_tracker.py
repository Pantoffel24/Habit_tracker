import streamlit as st
from datetime import datetime, timedelta
from supabase import Client, create_client

# --- Setting up UI Config (MUST be at the very top) ---
st.set_page_config(page_title='Habit Tracker')
st.title('Diet tracker')

# Data config
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(URL, KEY)

def load_data():
    response = supabase.table('diet_data').select('date_string').execute()
    completed_days = [row['date_string'] for row in response.data]
    return {"completed_days": completed_days}

def save_data(table_name,date_str, action='add'):
    if action == 'add':
        supabase.table(table_name).insert({'date_string': date_str}).execute()
    elif action == 'remove':
        supabase.table(table_name).delete().eq('date_string', date_str).execute()

# Global Data Fetch
data = load_data()
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# --- Functions for page dynamics ---
def Diet_tracker(data, yesterday):
    st.subheader('For tracking each day you ate a good amount.')
    st.subheader('You got this!')
    
    # Display bar weekly
    last_7_days = []
    for i in range(7):
        temp_day = (datetime.now() - timedelta(days=1)) - timedelta(days=i)
        date_string = temp_day.strftime("%Y-%m-%d")
        last_7_days.append(date_string)

    weekly_count = 0
    for day in last_7_days:
        if day in data['completed_days']:
            weekly_count += 1
            
    if weekly_count == 7:
        st.balloons()
        st.subheader("Congratulations! You nailed 1 week!")

    # FIXED: Restructured the button logic scope
    if yesterday in data['completed_days']:
        st.success('Good job!')
        if st.button('Unmark Yesterday'):
            save_data('diet_data',yesterday, action='remove')
            st.rerun()
    else:
        if st.button('Complete Yesterday', use_container_width=True):
            save_data('diet_data', yesterday, action='add')
            st.rerun()
            
    st.divider()

    # Visual history
    st.write('Progress last 30 days')

    start_date = datetime.now() - timedelta(days=29)
    today = datetime.now().strftime("%Y-%m-%d")

    #Initialize grid html
    grid_html = '<div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 10px; text-align: center;">'

    for i in range(30):
        date_add = start_date + timedelta(days=i)
        current_date = date_add.strftime("%Y-%m-%d")
        display_date = date_add.strftime("%d")
        if current_date == today:
            emoji = "⬜"
        elif current_date in data['completed_days']:
            emoji = "✅"
        else: 
            emoji = "🟥"
    
        #Grid html set up instead of the columns strat with streamlit
        grid_html += f'''<div style="border: 1px solid #333; padding: 5px; border-radius: 5px; background-color: #111;"><span style="font-size: 12px; font-weight: bold; color: #aaa;">{display_date}</span><br><span style="font-size: 18px;">{emoji}</span></div>'''

    grid_html += '</div>'

    #Render the grid
    st.markdown(grid_html, unsafe_allow_html = True)
    st.write("")#Spacer


    # Streak calculation
    streak = 0
    check_date = datetime.now() - timedelta(days=1)
    while check_date.strftime("%Y-%m-%d") in data['completed_days']:
        streak += 1
        check_date -= timedelta(days=1)

    st.write(f"Current Streak: {streak} days")

    # Goal logic
    total_completed = len(data['completed_days'])
    weekly_goal = 7
    monthly_goal = 31
    progress_monthly = min(total_completed/monthly_goal, 1.0)

    # Display bars
    st.write(f'## Monthly Goal: {total_completed}/{monthly_goal} days')
    st.progress(progress_monthly)

    st.write(f'## Weekly Challenge: {weekly_count}/{weekly_goal} days')
    progress_weekly = min(weekly_count/weekly_goal, 1.0)
    st.progress(progress_weekly)









def Other_Page():
    st.subheader('Other')
    st.write("TBD")

# --- Sidebar Navigation Menu ---
with st.sidebar:
    st.title('Navigation')
    page = st.radio('Go to', ['Diet Tracker', 'Other'])

# --- Routing Engine ---
if page == 'Diet Tracker':
    Diet_tracker(data, yesterday)
elif page == 'Other':
    Other_Page()