######################
# Import libraries
######################
import streamlit as st
import requests
import pandas as pd
import altair as alt

######################
# Page Title
######################

st.write("""
# Password Strength Checker App

This app checks how strong your password is and whether it has been compromised!

***
""")

######################
# Input Password
######################

st.header('Enter Password')
password = st.text_input("Enter your password:", type="password")

st.write("""
***
""")

######################
# Password Strength Checker
######################

def check_password_strength(password):
    strength = 0
    feedback = []

    # Length check
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Uppercase check
    if any(char.isupper() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    # Lowercase check
    if any(char.islower() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    # Number check
    if any(char.isdigit() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one number.")

    # Special character check
    if any(not char.isalnum() for char in password):
        strength += 1
    else:
        feedback.append("Password should contain at least one special character.")

    # Strength level
    if strength == 5:
        return "Strong", feedback
    elif strength >= 3:
        return "Medium", feedback
    else:
        return "Weak", feedback

if password:
    st.header('Results')
    strength, feedback = check_password_strength(password)

    ### 1. Display Strength Level
    st.subheader('1. Password Strength')
    if strength == "Strong":
        st.success("✅ Your password is **Strong**!")
    elif strength == "Medium":
        st.warning("⚠️ Your password is **Medium**. Consider improving it.")
    else:
        st.error("❌ Your password is **Weak**. Please make it stronger.")

    ### 2. Display Feedback
    st.subheader('2. Feedback')
    if not feedback:
        st.success("👍 Your password meets all the requirements")
    for item in feedback:
        st.write(f"- {item}")

    ### 3. Check if Password is Compromised (API Call)
    st.subheader('3. Password Security Check')
    if st.button("Check if password has been leaked"):

        import hashlib
        sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]

        # Call Have I Been Pwned API
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url)
        if response.status_code == 200:
            hashes = response.text.splitlines()
            for h in hashes:
                if suffix in h:
                    count = int(h.split(":")[1])
                    st.error(f"🚨 This password has been leaked **{count} times**! Do not use it.")
                    break
            else:
                st.success("✅ This password has not been leaked. It's safe to use!")
        else:
            st.error("Failed to check password security. Please try again later.")

    st.subheader('4. Generate a Strong Password')
    if st.button("Generate a strong password"):
        # API Call to Generate Password
        try:
            response = requests.get("https://passwordwolf.com/api/")
            if response.status_code == 200:
                password_data = response.json()
                generated_password = password_data[0]["password"]
                st.code(generated_password)
                st.write("Copy this password and use it securely!")
            else:
                st.error("Failed to generate a password. Please try again later.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
