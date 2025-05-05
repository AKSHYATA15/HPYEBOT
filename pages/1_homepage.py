import streamlit as st
import time
import random
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired

# Page configuration
st.set_page_config(page_title="Send Instagram DM", layout="centered")

st.title("📩 Send Instagram DM")
st.info("Enter your Instagram credentials to send a Direct Message.")

# Message form
with st.form("dm_form"):
    sender_username = st.text_input("Your Instagram Username")
    sender_password = st.text_input("Your Instagram Password", type="password")
    recipient_username = st.text_input("Recipient Instagram Username")
    message = st.text_area("Message", value="Hi! I wanted to connect with you.")

    send_button = st.form_submit_button("Send Message")

if send_button:
    try:
        cl = Client()
        cl.delay_range = [1, 3]

        with st.spinner("🔐 Logging in..."):
            cl.login(sender_username, sender_password)
        st.success("✅ Login successful")

        with st.spinner("🔍 Finding recipient..."):
            user_id = cl.user_id_from_username(recipient_username)
            time.sleep(random.uniform(1, 2))

        with st.spinner("✉️ Sending message..."):
            cl.direct_send(message, user_ids=[user_id])
            time.sleep(random.uniform(2, 4))

        st.success(f"✅ Message sent to @{recipient_username}")
        st.balloons()

    except ChallengeRequired:
        st.error("🔐 Login challenge required. Try logging in via the mobile app first.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    finally:
        try:
            cl.logout()
        except:
            pass
