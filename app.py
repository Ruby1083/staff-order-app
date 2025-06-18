import streamlit as st
import pandas as pd
from io import BytesIO
from email.message import EmailMessage
import smtplib
from datetime import datetime

st.title("Global Merchandise Item Order Form")

# Inventory grouped by categories, with image URLs added for all items
inventory = {
    "Apparel": [
        {"Item": "Winter Jacket", "Image": "https://i.imgur.com/wQLUiUH.jpeg", "Sizes": ["XS", "S", "M", "L", "XL", "2XL", "3XL"], "Price": 20.06},
        {"Item": "Men Oxford Shirt", "Image": "https://i.imgur.com/2IjT20W.jpeg", "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"], "Price": 16.00},
        {"Item": "Woman Oxford Shirt", "Image": "https://i.imgur.com/y0yxA6Q.jpeg", "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"], "Price": 16.00},
        {"Item": "Men Bamboo Shirt", "Image": "https://i.imgur.com/gLY4cHy.jpeg", "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"], "Price": 16.00},
        {"Item": "Woman Bamboo Shirt", "Image": "https://i.imgur.com/nqgN1Oz.jpeg", "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"], "Price": 16.00},
        {"Item": "Round Neck T-shirt (Long sleeves - Blue)", "Image": "https://i.imgur.com/TZ2h7eF.jpeg", "Sizes": ["S", "M", "L", "2XL"], "Price": 7.50},
        {"Item": "Round Neck T-shirt (Short Sleeves - Blue)", "Image": "https://i.imgur.com/QMUPvRH.jpeg", "Sizes": ["XS", "S", "M", "L", "2XL"], "Price": 6.00},
        {"Item": "Round Neck T-shirt (Long sleeves - Yellow)", "Image": "https://i.imgur.com/AWZx7Gm.jpeg", "Sizes": ["S", "M", "L", "2XL"], "Price": 4.44},
        {"Item": "Round Neck T-shirt (Long Sleeves - Orange)", "Image": "https://i.imgur.com/xR8aYwc.jpeg", "Sizes": ["S", "M", "L", "2XL"], "Price": 4.44},
        {"Item": "Round Neck T-shirt (Short sleeves - Yellow)", "Image": "https://i.imgur.com/1HfHPut.jpeg", "Sizes": ["XS", "S", "M", "L", "2XL"], "Price": 4.00},
        {"Item": "Round Neck T-shirt (Short Sleeves - Orange)", "Image": "https://i.imgur.com/jh7w6Ut.jpeg", "Sizes": ["XS", "S", "M", "L", "2XL"], "Price": 4.00},
        {"Item": "Men Polo Shirt", "Image": "https://i.imgur.com/RF4eJrm.jpeg", "Sizes": ["S", "M", "L", "2XL", "3XL", "4XL"], "Price": 26.00},
        {"Item": "Woman Polo Shirt", "Image": "https://i.imgur.com/1xhlGp9.jpeg", "Sizes": ["XS", "S", "M", "L", "2XL"], "Price": 26.00},
        {"Item": "Beanie", "Image": "https://i.imgur.com/M7DAlGB.jpeg", "Sizes": ["One Size"], "Price": 3.50},
        {"Item": "Magnetic Pin", "Image": "https://i.imgur.com/3grZmcd.jpeg", "Sizes": ["One Size"], "Price": 1.50},
    ],
    "Work Protection Gear": [
        {
            "Item": "Safety Helmet",
            "Image": "https://i.imgur.com/helmet_example.jpg",  # Replace with your helmet image URL
            "Colors": ["Blue", "Red", "White"],
            "Price": 3.67
        },
        {
            "Item": "Safety Vest",
            "Image": "https://i.imgur.com/safetyvest_example.jpg",  # Replace with your safety vest image URL
            "Sizes": ["L", "XL", "2XL", "3XL"],
            "Price": 3.73
        },
    ]
}

# Contact info inputs
st.header("Contact Information")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
location = st.text_input("Location / Office")
address = st.text_area("Delivery Address")

# Order input section
st.header("Order Details")

order = []
total_amount = 0.0

for category, items in inventory.items():
    with st.expander(category):
        for item in items:
            st.subheader(f"{item['Item']} (USD {item['Price']:.2f})")
            if item.get("Image"):
                st.image(item["Image"], width=150)

            # Handle items with colors (for Safety Helmet)
            if "Colors" in item:
                for color in item["Colors"]:
                    qty = st.number_input(f"{color}", min_value=0, step=1, key=f"{item['Item']}_{color}")
                    if qty > 0:
                        subtotal = qty * item["Price"]
                        order.append({
                            "Category": category,
                            "Name": name,
                            "Email": email,
                            "Phone": phone,
                            "Location": location,
                            "Address": address,
                            "Item": item["Item"],
                            "Size/Color": color,
                            "Quantity": qty,
                            "Unit Price (USD)": item["Price"],
                            "Subtotal (USD)": round(subtotal, 2)
                        })
                        total_amount += subtotal

            # Handle items with sizes
            elif "Sizes" in item:
                if item["Sizes"] == ["One Size"]:
                    qty = st.number_input(f"{item['Item']}", min_value=0, step=1, key=f"{item['Item']}_one_size")
                    if qty > 0:
                        subtotal = qty * item["Price"]
                        order.append({
                            "Category": category,
                            "Name": name,
                            "Email": email,
                            "Phone": phone,
                            "Location": location,
                            "Address": address,
                            "Item": item["Item"],
                            "Size/Color": "",
                            "Quantity": qty,
                            "Unit Price (USD)": item["Price"],
                            "Subtotal (USD)": round(subtotal, 2)
                        })
                        total_amount += subtotal
                else:
                    for size in item["Sizes"]:
                        qty = st.number_input(f"{size}", min_value=0, step=1, key=f"{item['Item']}_{size}")
                        if qty > 0:
                            subtotal = qty * item["Price"]
                            order.append({
                                "Category": category,
                                "Name": name,
                                "Email": email,
                                "Phone": phone,
                                "Location": location,
                                "Address": address,
                                "Item": item["Item"],
                                "Size/Color": size,
                                "Quantity": qty,
                                "Unit Price (USD)": item["Price"],
                                "Subtotal (USD)": round(subtotal, 2)
                            })
                            total_amount += subtotal
            st.markdown("---")

st.write(f"### Total Amount: USD {total_amount:.2f}")

# Submit button and processing
if st.button("Submit Order"):
    if not name or not email or not address:
        st.error("Please fill out all required fields.")
    elif len(order) == 0:
        st.warning("No items selected.")
    else:
        df = pd.DataFrame(order)
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
