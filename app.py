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
            "Item": "Men Oxford Shirt",
            "Image": "https://i.imgur.com/URHj9BN.png",
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Price": 16.00
        },
        {
            "Item": "Woman Oxford Shirt",
            "Image": "https://i.imgur.com/6kzygzj.png",
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Price": 16.00
        },
        {
            "Item": "Men Bamboo Shirt",
            "Image": "https://i.imgur.com/D1JeIe4.png",
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Price": 16.00
        },
        {
            "Item": "Woman Bamboo Shirt",
            "Image": "https://i.imgur.com/VbJ7vwJ.png",
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Price": 16.00
        },
        {
            "Item": "Round Neck T-shirt (Long sleeves - Blue)",
            "Image": "https://i.imgur.com/Jq0DzyE.png",
            "Sizes": ["S", "M", "L", "2XL"],
            "Price": 7.50
        },
        {
            "Item": "Round Neck T-shirt (Short Sleeves - Blue)",
            "Image": "https://i.imgur.com/Hy8SOhI.png",
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Price": 6.00
        },
        {
            "Item": "Round Neck T-shirt (Long sleeves - Yellow)",
            "Image": "https://i.imgur.com/GxIKeZv.png",
            "Sizes": ["S", "M", "L", "2XL"],
            "Price": 4.44
        },
        {
            "Item": "Round Neck T-shirt (Long Sleeves - Orange)",
            "Image": "https://i.imgur.com/LvL2FZM.png",
            "Sizes": ["S", "M", "L", "2XL"],
            "Price": 4.44
        },
        {
            "Item": "Round Neck T-shirt (Short sleeves - Yellow)",
            "Image": "https://i.imgur.com/SMYMwFo.png",
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Price": 4.00
        },
        {
            "Item": "Round Neck T-shirt (Short Sleeves - Orange)",
            "Image": "https://i.imgur.com/Y7XaNXa.png",
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Price": 4.00
        },
        {
            "Item": "Men Polo Shirt",
            "Image": "",  # Add image if you have
            "Sizes": ["S", "M", "L", "2XL", "3XL", "4XL"],
            "Price": 26.00
        },
        {
            "Item": "Woman Polo Shirt",
            "Image": "",  # Add image if you have
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Price": 26.00
        },
        {
            "Item": "Beanie",
            "Image": "",  # Add image if you have
            "Sizes": [],
            "Price": 3.50
        },
        {
            "Item": "Magnetic Pin",
            "Image": "",  # Add image if you have
            "Sizes": [],
            "Price": 1.50
        },
        {
            "Item": "Winter Jacket",
            "Image": "https://drive.google.com/uc?export=view&id=1IIQIoRobm5ofyWGK7wdkxgFqL41Vm0t2",
            "Sizes": ["XS", "S", "M", "L", "XL", "2XL", "3XL"],
            "Price": 20.06
        },
    ],
    # Add other categories here if needed
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

for category, items in inventory.items():
    with st.expander(category):
        for item in items:
            item_name = item["Item"]
            item_price = item["Price"]
            sizes = item["Sizes"]
            image_url = item["Image"]

            # Display image if available
            if image_url:
                st.image(image_url, width=150)

            # Create sub-expander for each item with price shown
            with st.expander(f"{item_name} (USD {item_price:.2f})"):

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
                                "Item": item_name,
                                "Size": size,
                                "Quantity": qty,
                                "Price": item_price,
                                "Amount": qty * item_price
                            })
                else:
                    # For no-size items (Beanie, Magnetic Pin)
                    qty = st.number_input(
                        "",
                        min_value=0,
                        step=1,
                        key=f"{item_name}_no_size"
                    )
                    if qty > 0:
                        order.append({
                            "Item": item_name,
                            "Size": "",
                            "Quantity": qty,
                            "Price": item_price,
                            "Amount": qty * item_price
                        })

# Calculate total
total_amount = sum(item["Amount"] for item in order)

st.write(f"### Total Amount: USD {total_amount:.2f}")

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
            msg["Subject"] = f"New Merchandise Order from {name}"
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
