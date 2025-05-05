# pages/shortlist_outreach.py
import streamlit as st
import random, time
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired

st.set_page_config(page_title="Shortlist Outreach", layout="wide")

st.title("📤 Shortlist Outreach")

shortlisted = st.session_state.get("shortlisted_users", [])

if not shortlisted:
    st.warning("No users shortlisted yet.")
    st.stop()

# Login Form
with st.form("ig_login_form"):
    ig_username = st.text_input("Your Instagram Username")
    ig_password = st.text_input("Your Instagram Password", type="password")
    message = st.text_area("Message to send", "Hi, I came across your profile and would love to connect...")

    if st.form_submit_button("Send Message to All"):
        try:
            cl = Client()
            cl.delay_range = [2, 5]
            with st.spinner("Logging in..."):
                cl.login(ig_username, ig_password)
            st.success("✅ Logged in successfully")

            for user in shortlisted:
                try:
                    username = user["username"]
                    with st.spinner(f"Sending to @{username}..."):
                        user_id = cl.user_id_from_username(username)
                        cl.direct_send(message, [user_id])
                        st.success(f"✅ Sent to @{username}")
                        time.sleep(random.randint(15, 30))
                except Exception as e:
                    st.error(f"❌ Failed for @{username}: {str(e)}")

            cl.logout()
            st.success("🎉 All messages processed!")
            st.balloons()
        except ChallengeRequired:
            st.error("🔐 Challenge required. Try logging in via Instagram app first.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
