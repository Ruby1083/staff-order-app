import streamlit as st
import pandas as pd
from io import BytesIO
from email.message import EmailMessage
import smtplib
from datetime import datetime

st.title("Global Merchandise Item Order Form")

# Inventory with categories, items, prices, sizes, and images
inventory = {
    "Apparel": [
        {
            "Item": "Winter Jacket",
            "Price": 20.06,
            "Sizes": ["XS", "S", "M", "L", "XL", "2XL", "3XL"],
            "Image": "https://i.imgur.com/jKq8875.png",
        },
        {
            "Item": "Men Oxford Shirt",
            "Price": 16.00,
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Image": "https://i.imgur.com/URHj9BN.png",
        },
        {
            "Item": "Woman Oxford Shirt",
            "Price": 16.00,
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Image": "https://i.imgur.com/6kzygzj.png",
        },
        {
            "Item": "Men Bamboo Shirt",
            "Price": 16.00,
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Image": "https://i.imgur.com/D1JeIe4.png",
        },
        {
            "Item": "Woman Bamboo Shirt",
            "Price": 16.00,
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Image": "https://i.imgur.com/VbJ7vwJ.png",
        },
        {
            "Item": "Round Neck T-shirt (Long sleeves - Blue)",
            "Price": 7.50,
            "Sizes": ["S", "M", "L", "2XL"],
            "Image": "https://i.imgur.com/Jq0DzyE.png",
        },
        {
            "Item": "Round Neck T-shirt (Short Sleeves - Blue)",
            "Price": 6.00,
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Image": "https://i.imgur.com/Hy8SOhI.png",
        },
        {
            "Item": "Round Neck T-shirt (Long sleeves - Yellow)",
            "Price": 4.44,
            "Sizes": ["S", "M", "L", "2XL"],
            "Image": "https://i.imgur.com/GxIKeZv.png",
        },
        {
            "Item": "Round Neck T-shirt (Long Sleeves - Orange)",
            "Price": 4.44,
            "Sizes": ["S", "M", "L", "2XL"],
            "Image": "https://i.imgur.com/LvL2FZM.png",
        },
        {
            "Item": "Round Neck T-shirt (Short sleeves - Yellow)",
            "Price": 4.00,
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Image": "https://i.imgur.com/SMYMwFo.png",
        },
        {
            "Item": "Round Neck T-shirt (Short Sleeves - Orange)",
            "Price": 4.00,
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Image": "https://i.imgur.com/Y7XaNXa.png",
        },
        {
            "Item": "Men Polo Shirt",
            "Price": 26.00,
            "Sizes": ["S", "M", "L", "2XL", "3XL", "4XL"],
            "Image": "",
        },
        {
            "Item": "Woman Polo Shirt",
            "Price": 26.00,
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Image": "",
        },
        {
            "Item": "Beanie",
            "Price": 3.50,
            "Sizes": [],
            "Image": "",
        },
        {
            "Item": "Magnetic Pin",
            "Price": 1.50,
            "Sizes": [],
            "Image": "",
        },
    ],
    "Work Protection Gear": [
        {
            "Item": "Safety Helmet - Blue",
            "Price": 3.67,
            "Sizes": [],
            "Image": "",
        },
        {
            "Item": "Safety Helmet - Red",
            "Price": 3.67,
            "Sizes": [],
            "Image": "",
        },
        {
            "Item": "Safety Helmet - White",
            "Price": 3.67,
            "Sizes": [],
            "Image": "",
        },
        {
            "Item": "Safety Vest",
            "Price": 3.73,
            "Sizes": ["L", "XL", "2XL", "3XL"],
            "Image": "",
        },
    ],
}

st.header("Contact Information")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
location = st.text_input("Location / Office")
address = st.text_area("Delivery Address")

st.header("Order Details")

order = []

for category_name, items in inventory.items():
    with st.expander(category_name):
        for item in items:
            item_name = item["Item"]
            item_price = item["Price"]
            sizes = item["Sizes"]
            image_url = item.get("Image", "")

            st.subheader(f"{item_name} (USD {item_price:.2f})")
            if image_url:
                st.image(image_url, width=150)

            if sizes:
                for size in sizes:
                    qty = st.number_input(
                        f"{size}",
                        min_value=0,
                        step=1,
                        key=f"{item_name}_{size}"
                    )
                    if qty > 0:
                        order.append({
                            "Category": category_name,
                            "Item": item_name,
                            "Size": size,
                            "Quantity": qty,
                            "Price": item_price,
                        })
            else:
                # No size, no label after input
                qty = st.number_input(
                    key=f"{item_name}_qty",
                    label="",
                    min_value=0,
                    step=1,
                )
                if qty > 0:
                    order.append({
                        "Category": category_name,
                        "Item": item_name,
                        "Size": "",
                        "Quantity": qty,
                        "Price": item_price,
                    })

total_amount = sum(o["Quantity"] * o["Price"] for o in order)
st.markdown(f"### Total Amount: USD {total_amount:.2f}")

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

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Order")
        excel_data = output.getvalue()

        def send_email():
            msg = EmailMessage()
            msg["Subject"] = f"New Apparel Order from {name}"
            msg["From"] = st.secrets["EMAIL_USER"]
            msg["To"] = st.secrets["ADMIN_EMAIL"]
            msg.set_content(f"New order submitted by {name}.\n\nSee attached Excel file.")

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
