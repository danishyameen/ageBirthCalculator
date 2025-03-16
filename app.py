import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

# Page configuration
st.set_page_config(page_title="Age & Birthday Calculator", page_icon="🎈")

# Custom CSS styling
st.markdown("""
<style>
    .header {
        font-size: 40px !important;
        color: #0004ff;
        text-align: center;
        padding: 20px;
    }
    .result-box {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .countdown {
        font-size: 24px;
        color: #0004ff;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<p class="header">🎂 Age & Birthday Calculator</p>', unsafe_allow_html=True)

# Date selection columns
col1, col2, col3 = st.columns(3)
with col1:
    birth_year = st.selectbox("Year", reversed(range(1900, datetime.now().year + 1)))
with col2:
    birth_month = st.selectbox("Month", list(calendar.month_name[1:]), format_func=lambda x: x[:3])
with col3:
    month_number = list(calendar.month_name).index(birth_month)
    _, last_day = calendar.monthrange(birth_year, month_number)
    birth_day = st.selectbox("Day", range(1, last_day + 1))

birth_date = datetime(birth_year, month_number, birth_day)
today = datetime.now()

def calculate_age(birth_date):
    delta = relativedelta(today, birth_date)
    
    # Calculate next birthday
    next_birthday = birth_date.replace(year=today.year)
    if today > next_birthday:
        next_birthday = next_birthday.replace(year=today.year + 1)
    
    total_seconds = int((next_birthday - today).total_seconds())
    
    return {
        "years": delta.years,
        "months": delta.months,
        "days": delta.days,
        "total_days": (today - birth_date).days,
        "next_birthday_seconds": total_seconds,
        "next_birthday_date": next_birthday
    }


if st.button("Calculate My Age!", use_container_width=True):
    age_data = calculate_age(birth_date)
    
    # Birthday check
    if birth_date.month == today.month and birth_date.day == today.day:
        st.balloons()
        st.success("🎉 Happy Birthday! 🎉")
        generate_birthday_wish()
    
    # Age results
    with st.expander("AGE BREAKDOWN", expanded=True):
        total_days = age_data['total_days']
        weeks = total_days // 7
        remaining_days = total_days % 7
        
        st.markdown(f"""
        <div class="result-box">
            <p>📅 {age_data['years']} years {age_data['months']} months {age_data['days']} days</p>
            <p>🗓️ {weeks} weeks {remaining_days} days</p>
            <p>⏳ {total_days:,} total days lived</p>
            <p>🕒 {total_days * 24:,} hours</p>
            <p>⏰ {total_days * 1440:,} minutes</p>
            <p>⌛ {total_days * 86400:,} seconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Countdown timer
    st.subheader(f"Time Until Next Birthday ({age_data['next_birthday_date'].strftime('%d %B %Y')}) 🎈")
    
    # Continuous countdown timer using HTML/JavaScript
    countdown_html = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <div id="countdown" class="countdown"></div>
        <script>
            var target = {age_data['next_birthday_seconds']};
            
            function updateTimer() {{
                var days = Math.floor(target / 86400);
                var hours = Math.floor((target % 86400) / 3600);
                var minutes = Math.floor((target % 3600) / 60);
                var seconds = target % 60;
                
                document.getElementById('countdown').innerHTML = 
                    `⏳ ${{days.toString().padStart(2, '0')}}d ` +
                    `${{hours.toString().padStart(2, '0')}}h ` +
                    `${{minutes.toString().padStart(2, '0')}}m ` +
                    `${{seconds.toString().padStart(2, '0')}}s`;
                
                if(target > 0) {{
                    target--;
                    setTimeout(updateTimer, 1000);
                }} else {{
                    document.getElementById('countdown').innerHTML = "🎉 Happy Birthday! 🎉";
                }}
            }}
            updateTimer();
        </script>
    </body>
    </html>
    """
    st.components.v1.html(countdown_html, height=60)

# Sidebar information
st.sidebar.header("About This App")
st.sidebar.info("""
This interactive calculator helps you:
- Determine your exact age in various units
- Calculate time until your next birthday
- Celebrate your special day with animations
- Get birthday wishes in audio format
""")

# Footer
st.markdown("---")
st.markdown("Made with by ❤️ Danish Yameen | Powered by Streamlit")