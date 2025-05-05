import streamlit as st
import time
import random
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired

st.set_page_config(page_title="Outreach", layout="wide")

st.title("📨 Automated Outreach")

if "outreach_list" not in st.session_state or not st.session_state["outreach_list"]:
    st.warning("No influencers selected for outreach.")
    st.stop()

ig_username = st.text_input("Your Instagram Username")
ig_password = st.text_input("Your Instagram Password", type="password")

message_template = st.text_area("Message Template", "Hi @{username}, I came across your profile and wanted to connect...")

if st.button("Send Messages"):
    try:
        cl = Client()
        cl.delay_range = [1, 3]

        with st.spinner("Logging in... If this takes a while, please log into your Instagram app to authenticate this login activity."):
            cl.login(ig_username, ig_password)
        st.success("Logged in successfully")

        for influencer in st.session_state["outreach_list"]:
            username = influencer['username']
            user_id = cl.user_id_from_username(username)
            message = message_template.replace("@{username}", f"@{username}")
            with st.spinner(f"Sending message to @{username}..."):
                cl.direct_send(message, user_ids=[user_id])
                time.sleep(random.uniform(2, 4))
            st.success(f"Message sent to @{username}")

        cl.logout()

    except ChallengeRequired:
        st.error("Instagram requires verification. Please authenticate this login from your device.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
