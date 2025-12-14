import streamlit as st
import pandas as pd 
from PIL import Image
import io
import random
import smtplib
from email.message import EmailMessage
import sqlite3

for key in ["name", "cls", "roll", "mobile", "otp_generated"]:
    if key not in st.session_state:
        st.session_state[key] = None

st.set_page_config(page_title="REGISTER FORM")
st.sidebar.title("navigation")
page = st.sidebar.radio("go to", ["register/payment", "databaseview"])

conn=sqlite3.connect("pongal_registration.db",check_same_thread=False)
cursor=conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS registration(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    class TEXT,
    rollno INTEGER,
    mobile TEXT,
    payment_image BLOB
)
""")
conn.commit()


def savedb(name,cls,roll,mobile,image_data):
    cursor.execute("""
                   INSERT INTO registration (name, class, rollno, mobile, payment_image)
                   VALUES (?, ?, ?, ?, ?)
    """,(name, cls, roll, mobile, image_data))
    conn.commit()
    
def databasedb():
    st.subheader("📘 Registration Database")

    cursor.execute("SELECT * FROM registration")
    data = cursor.fetchall()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Name", "Class", "Roll No", "Mobile", "Payment Image"])
        st.dataframe(df)
    else:
        st.warning("No registrations found.")

    # 🔍 View specific row
    st.subheader("🔍 View Specific Row")
    view_id = st.number_input("Enter ID to view", step=1)
    if st.button("View Row"):
        cursor.execute("SELECT * FROM registration WHERE id=?", (view_id,))
        row = cursor.fetchone()
        if row:
            st.write(dict(zip(["ID", "Name", "Class", "Roll No", "Mobile", "Payment Image"], row)))
        else:
            st.error("No row found with that ID.")

    # 🖼️ View uploaded payment image  ← ADD THIS BLOCK HERE
    st.subheader("🖼️ View Payment Image")
    img_id = st.number_input("Enter ID to view image", step=1, key="view_image")

    if st.button("View Image"):
        cursor.execute("SELECT payment_image FROM registration WHERE id=?", (img_id,))
        img_data = cursor.fetchone()

        if img_data and img_data[0] not in (None, b"cash"):
            st.image(img_data[0], caption=f"Payment Screenshot for ID {img_id}")
        elif img_data and img_data[0] == b"cash":
            st.warning("This user registered using CASH. No image available.")
        else:
            st.error("No image found for this ID.")

    # 🗑️ Delete row
    st.subheader("🗑️ Delete Row")
    delete_id = st.number_input("Enter ID to delete", step=1, key="delete")
    if st.button("Delete Row"):
        cursor.execute("DELETE FROM registration WHERE id=?", (delete_id,))
        conn.commit()
        st.success(f"Row with ID {delete_id} deleted.")

    # ✏️ Update row
    st.subheader("✏️ Update Row")
    update_id = st.number_input("Enter ID to update", step=1, key="update")
    new_name = st.text_input("New Name")
    new_class = st.text_input("New Class")
    new_roll = st.number_input("New Roll No", step=1)
    new_mobile = st.text_input("New Mobile", max_chars=10)

    if st.button("Update Row"):
        cursor.execute("""
            UPDATE registration
            SET name=?, class=?, rollno=?, mobile=?
            WHERE id=?
        """, (new_name, new_class, new_roll, new_mobile, update_id))
        conn.commit()
        st.success(f"Row with ID {update_id} updated.")






server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
from_mail ="chandruveeramani65@gmail.com"
server.login(from_mail,"aoic ouvx hpeq sxoh")
to_mail="chandruchandru272007@gmail.com"



def generator_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0,9))
    return otp




if page == "register/payment":    
    if "page" not in st.session_state:
        st.session_state.page = 'register'

    if st.session_state.page == 'register':
        st.title("PONGAL REGISTRATION FORM")

        col1,col2=st.columns(2)

        with col1:
            st.header("NAME:")
            st.header("CLASS:")
            st.header("ROLLNO:")
            st.header("MOBILE:")
        
        
        with col2:
            name=st.text_input("enter your name")
            cls=st.text_input("enter your class")
            roll=st.number_input("enter your rollno",step=1)
            mobile=st.text_input("enter your mobile number", max_chars=10)

        colleft,colcenter,colright=st.columns([1,1,1])
        with colcenter:
            sub=st.button("NEXT")
            if sub:
                if not name or not cls or not roll or not mobile:
                    st.error("please fill in all the fields.")
                elif mobile and (len(mobile) != 10 or not mobile.isdigit()):
                    st.error("mobile number must be exactly 10 digits and contains only numbers.")
                else:
                    st.session_state.name = name
                    st.session_state.cls = cls
                    st.session_state.roll = int(roll)
                    st.session_state.mobile = mobile
                    st.session_state.page = 'next'
                    st.balloons()

    elif st.session_state.page == 'next':
        if st.session_state.name is None:
            st.error("Please complete the registration form first.")
            st.stop()

        st.title("PAYMENT PAGE")
        st.header("Welcome to the payment page!")
        st.write("""please proceed your payment for the pongal event registration.
                 by using the qrcode below👇🏻👇🏻👇🏻""")    
        img=Image.open(r"C:\Users\Welcome\Downloads\prathisgpay.jpeg")
        st.image(img)
        # Download button for the image
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()
        st.download_button('Download QR Code', img_bytes, 'prathisgpay.jpeg')
        st.success("""after the payment take screenshot of the payment and attach  the photo to the upload button
                     if you did not upload the file your registration was incomplete make sure it is in jpeg or jfif format
                     upload here👇🏻👇🏻👇🏻""")
        uploaded_file = st.file_uploader("upload the payment screenshot", type=['jpeg', 'jfif'])
    
        if uploaded_file is not None:
            st.success("You have uploaded a payment screenshot. click the Registration button")
        else:
            st.warning("""if you did not have the account and have only cash payment
                       please fill your name in the below box we will send a 6 digit otp to the PRATHISH OR CHANDRU
                       give the money to them and they will say the otp to you. you need to enter the otp int OTP BOX and confirm your registration,
                    you need to upload a file or enter the otp either one is enoungh to register your form
                    """)
            email = st.text_input("enter your name")
            but = st.button("SEND OTP")
            if but:
                generated_otp = generator_otp()
                st.session_state.otp_generated =generated_otp
                # sending email to the two different user one is prathish and another one is chandru
                msg = EmailMessage()
                msg["Subject"] = "OTP for pongal registration"
                msg["From"] = from_mail
                msg["To"] = to_mail
                msg.set_content(f"Your OTP for Pongal registration is {generated_otp}. Please do not share it with anybody, Mr/Mrs. {st.session_state.name}.")
                server.send_message(msg)
                st.success("OTP sent successfully to PRATHISH AND CHANDRU")
        otp_entered = st.text_input("enter the otp here")
        colleft,colcenter,colright=st.columns([1,1,1])
        with colleft:
            b1 = st.button("REGISTER NOW")        
            if b1:
                if uploaded_file is not None:
                    image_bytes = uploaded_file.read()
                    savedb(
                        st.session_state.name,
                        st.session_state.cls,
                        st.session_state.roll,                        st.session_state.mobile,
                        image_bytes
                    )
                    st.success("Registration completed with payment screenshot!")
                elif otp_entered == st.session_state.get('otp_generated', ''):
                    savedb(
                    st.session_state.name,
                    st.session_state.cls,
                    st.session_state.roll,
                    st.session_state.mobile,
                    b"cash"
                 )
                    st.success("Registration completed with cash payment!")
                else:
                    st.error("Invalid OTP or no file uploaded. Please try again.")
                
        with colright:
            back=st.button("BACK👈🏻")
            if back:
                st.session_state.page="register"
    


elif page == "databaseview":
    st.title("🔐 Admin Access")

    password_input = st.text_input("Enter admin password", type="password")
    correct_password = "##**"

    if password_input != correct_password:
        st.warning("Enter correct password to access database tools.")
        st.stop()

    databasedb()
