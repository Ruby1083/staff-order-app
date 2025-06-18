import streamlit as st
import pandas as pd
from io import BytesIO
from email.message import EmailMessage
import smtplib
from datetime import datetime

st.title("Global Merchandise Order Form")

# Inventory with price
inventory = {
        "Apparel": [
    {
        "Item": "Winter Jacket",
        "Image": "https://i.imgur.com/wQLUiUH.jpeg",
        "Sizes": ["XS", "S", "M", "L", "XL", "2XL", "3XL"],
        "Price": 20.06
    },
    {
        "Item": "Men Oxford Shirt",
        "Image": "https://i.imgur.com/nOGc2bd.jpeg",
        "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
        "Price": 16.00
    },
    {
        "Item": "Woman Oxford Shirt",
        "Image": "https://i.imgur.com/Vk1NxDN.jpeg",
        "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
        "Price": 16.00
    },
    {
        "Item": "Men Bamboo Shirt",
        "Image": "https://i.imgur.com/ESNzIId.jpeg",
        "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
        "Price": 16.00
    },
    {
        "Item": "Woman Bamboo Shirt",
        "Image": "https://i.imgur.com/fZ9NcQo.jpeg",
        "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
        "Price": 16.00
    },
    {
        "Item": "Round Neck T-shirt (Long sleeves - Blue)",
        "Image": "https://i.imgur.com/K6PfEQl.jpeg",
        "Sizes": ["S", "M", "L", "2XL"],
        "Price": 7.50
    },
    {
        "Item": "Round Neck T-shirt (Short Sleeves - Blue)",
        "Image": "https://i.imgur.com/2aykJjH.jpeg",
        "Sizes": ["XS", "S", "M", "L", "2XL"],
        "Price": 6.00
    },
    {
        "Item": "Round Neck T-shirt (Long sleeves - Yellow)",
        "Image": "https://i.imgur.com/K2eUZ7M.jpeg",
        "Sizes": ["S", "M", "L", "2XL"],
        "Price": 4.44
    },
    {
        "Item": "Round Neck T-shirt (Long Sleeves - Orange)",
        "Image": "https://i.imgur.com/K2eUZ7M.jpeg",
        "Sizes": ["S", "M", "L", "2XL"],
        "Price": 4.44
    },
    {
        "Item": "Round Neck T-shirt (Short sleeves - Yellow)",
        "Image": "https://i.imgur.com/5R6Dg9r.jpeg",
        "Sizes": ["XS", "S", "M", "L", "2XL"],
        "Price": 4.00
    },
    {
        "Item": "Round Neck T-shirt (Short Sleeves - Orange)",
        "Image": "https://i.imgur.com/5R6Dg9r.jpeg",
        "Sizes": ["XS", "S", "M", "L", "2XL"],
        "Price": 4.00
    },
    {
        "Item": "Men Polo Shirt",
        "Image": "https://i.imgur.com/y7y0UnV.jpeg",
        "Sizes": ["S", "M", "L", "2XL", "3XL", "4XL"],
        "Price": 26.00
    },
    {
        "Item": "Woman Polo Shirt",
        "Image": "https://i.imgur.com/F8z7MNc.jpeg",
        "Sizes": ["XS", "S", "M", "L", "2XL"],
        "Price": 26.00
    },
    {
        "Item": "Beanie",
        "Image": "https://i.imgur.com/qN1zRVc.jpeg",
        "Sizes": ["One Size"],
        "Price": 3.50
    },
    {
        "Item": "Magnetic Pin",
        "Image": "https://i.imgur.com/Qd1Xqtb.jpeg",
        "Sizes": ["One Size"],
        "Price": 1.50
    }
]


# Staff info inputs
st.header("Contact Information")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
location = st.text_input("Location / Office")
address = st.text_area("Delivery Address")

# Order input section
st.header("Order Details")
order = []

for item in inventory:
    with st.expander(item["Item"]):
        st.image(item["Image"], width=150)
        for size in item["Sizes"]:
            qty = st.number_input(
                f"{item['Item']} - Size {size}",
                min_value=0,
                step=1,
                key=f"{item['Item']}_{size}"
            )
            if qty > 0:
                order.append({
                    "Item": item["Item"],
                    "Size": size,
                    "Quantity": qty,
                    "Unit Price (USD)": item["Price"],
                    "Subtotal (USD)": round(qty * item["Price"], 2)
                })

# Show order summary before submission
if order:
    st.subheader("Order Summary")
    summary_df = pd.DataFrame(order)
    st.dataframe(summary_df)

    total_amount = summary_df["Subtotal (USD)"].sum()
    st.markdown(f"### Total Amount: USD ${total_amount:.2f}")
else:
    total_amount = 0.00

# Submit button and processing
if st.button("Submit Order"):
    if not name or not email or not address:
        st.error("Please fill out all required fields.")
    elif len(order) == 0:
        st.warning("No items selected.")
    else:
        df = pd.DataFrame(order)
        df.insert(0, "Name", name)
        df.insert(1, "Email", email)
        df.insert(2, "Phone", phone)
        df.insert(3, "Location", location)
        df.insert(4, "Address", address)
        df["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Order")
        excel_data = output.getvalue()

        # Email sending function
        def send_email():
            msg = EmailMessage()
            msg["Subject"] = f"New Apparel Order from {name}"
            msg["From"] = st.secrets["EMAIL_USER"]
            msg["To"] = st.secrets["ADMIN_EMAIL"]
            msg.set_content(
                f"New order submitted by {name}.\n\n"
                f"Total Amount: USD ${total_amount:.2f}\n\n"
                "See attached Excel file for full order details."
            )

            msg.add_attachment(
                excel_data,
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=f"order_{name.replace(' ', '_')}.xlsx"
            )

            try:
                smtp_server = st.secrets["SMTP_SERVER"]
                smtp_port = int(st.secrets["SMTP_PORT"])
                use_tls = st.secrets.get("SMTP_USE_TLS", "false").lower() == "true"

                if use_tls:
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"])
                        server.send_message(msg)
                else:
                    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                        server.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"])
                        server.send_message(msg)

                return True, "Order submitted and email sent!"
            except Exception as e:
                return False, f"Email failed: {e}"

        success, message = send_email()
        if success:
            st.success(message)
        else:
            st.error(message)
