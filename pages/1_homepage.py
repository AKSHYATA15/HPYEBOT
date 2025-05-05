import streamlit as st
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired
import time
import random
import datetime

# Page configuration
st.set_page_config(page_title="Instagram DM Sender", layout="centered")

st.title("📩 Send Instagram Direct Message")

with st.form("dm_form"):
    sender_username = st.text_input("Your Instagram Username")
    sender_password = st.text_input("Your Instagram Password", type="password")
    receiver_username = st.text_input("Receiver's Instagram Username")
    default_message = f"Hi @{receiver_username}, I came across your profile and wanted to connect!"
    message = st.text_area("Message", value=default_message)

    submit_btn = st.form_submit_button("Send Message")

if submit_btn:
    if not sender_username or not sender_password or not receiver_username or not message:
        st.error("Please fill in all fields.")
    else:
        st.info("⏳ Attempting login and message send...")

        with st.status("Logging in...", expanded=True) as status:
            try:
                login_start = datetime.datetime.now()
                cl = Client()
                cl.delay_range = [2, 5]
                st.write("Initializing Instagram client...")
                cl.login(sender_username, sender_password)
                login_end = datetime.datetime.now()
                status.update(label=f"✅ Logged in ({login_end - login_start})", state="complete")

                # Lookup recipient
                status.update(label="🔍 Finding user ID...")
                user_id = cl.user_id_from_username(receiver_username)
                st.write(f"Found user ID: {user_id}")
                time.sleep(random.uniform(1, 2))

                # Send message
                status.update(label="📨 Sending message...")
                cl.direct_send(message, user_ids=[user_id])
                time.sleep(random.uniform(2, 4))
                status.update(label="✅ Message sent successfully!", state="complete")
                st.success(f"✅ Message sent to @{receiver_username}")
                st.balloons()

            except ChallengeRequired:
                status.update(label="🔐 Challenge Required - login via mobile app first.", state="error")
                st.error("Instagram requires verification. Try logging in via the mobile app first.")
            except Exception as e:
                status.update(label="❌ Error during login or message sending.", state="error")
                st.error(f"Something went wrong: {str(e)}")
