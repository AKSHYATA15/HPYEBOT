import streamlit as st
import pandas as pd
import time, random
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired

st.set_page_config(page_title="Outreach", layout="wide")
st.title("📨 Automated DM Outreach")

df = pd.read_excel("data/instagram_analysis_Fashion All (1) (1).xlsx", sheet_name=0)
df_success = df[df["status"] == "Success"]
send_list = st.session_state.get("send_list", [])

if not send_list:
    st.warning("No influencers selected for messaging.")
    st.stop()

ig_username = st.text_input("Your Instagram Username")
ig_password = st.text_input("Your Instagram Password", type="password")
default_message = "Hi @{username}, I came across your profile and wanted to connect..."
custom_msg = st.text_area("Message Template", value=default_message, help="Use `{username}` as a placeholder")

if st.button("Send Messages"):
    cl = Client()
    cl.delay_range = [1, 3]

    try:
        with st.spinner("Logging in... If it takes a while, please log in to your Instagram account from your device to verify and authenticate this login activity."):

            cl.login(ig_username, ig_password)
        st.success("✅ Logged in")

        for user in send_list:
            row = df_success[df_success["username"] == user].squeeze()
            msg = custom_msg.replace("{username}", user)

            try:
                user_id = cl.user_id_from_username(user)
                with st.spinner(f"Sending to @{user}..."):
                    cl.direct_send(msg, user_ids=[user_id])
                    st.success(f"✅ Sent to @{user}")
                    time.sleep(random.uniform(2, 4))
            except Exception as e:
                st.error(f"❌ Failed to message @{user}: {str(e)}")

    except ChallengeRequired:
        st.error("Instagram challenge required. Try logging in manually first.")
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
    finally:
        cl.logout()
