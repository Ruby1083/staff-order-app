import streamlit as st
import pandas as pd
from io import BytesIO
from email.message import EmailMessage
import smtplib
from datetime import datetime

st.title("Global Merchandise Item Order Form")

# Inventory grouped by category, each item with image URL, sizes, price
inventory = {
    "Apparel": [
        {
            "Item": "Winter Jacket",
            "Image": "https://i.imgur.com/VZGnatT.jpeg",
            "Sizes": ["XS", "S", "M", "L", "XL", "2XL", "3XL"],
            "Price": 20.06,
        },
        {
            "Item": "Men Oxford Shirt",
            "Image": "https://i.imgur.com/URHj9BN.png",
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Price": 16.00,
        },
        {
            "Item": "Woman Oxford Shirt",
            "Image": "https://i.imgur.com/6kzygzj.png",
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Price": 16.00,
        },
        {
            "Item": "Men Bamboo Shirt",
            "Image": "https://i.imgur.com/D1JeIe4.png",
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Price": 16.00,
        },
        {
            "Item": "Woman Bamboo Shirt",
            "Image": "https://i.imgur.com/VbJ7vwJ.png",
            "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"],
            "Price": 16.00,
        },
        {
            "Item": "Round Neck T-shirt (Long sleeves - Blue)",
            "Image": "https://i.imgur.com/Jq0DzyE.png",
            "Sizes": ["S", "M", "L", "2XL"],
            "Price": 7.50,
        },
        {
            "Item": "Round Neck T-shirt (Short Sleeves - Blue)",
            "Image": "https://i.imgur.com/Hy8SOhI.png",
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Price": 6.00,
        },
        {
            "Item": "Round Neck T-shirt (Long sleeves - Yellow)",
            "Image": "https://i.imgur.com/GxIKeZv.png",
            "Sizes": ["S", "M", "L", "2XL"],
            "Price": 4.44,
        },
        {
            "Item": "Round Neck T-shirt (Long Sleeves - Orange)",
            "Image": "https://i.imgur.com/LvL2FZM.png",
            "Sizes": ["S", "M", "L", "2XL"],
            "Price": 4.44,
        },
        {
            "Item": "Round Neck T-shirt (Short sleeves - Yellow)",
            "Image": "https://i.imgur.com/SMYMwFo.png",
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Price": 4.00,
        },
        {
            "Item": "Round Neck T-shirt (Short Sleeves - Orange)",
            "Image": "https://i.imgur.com/Y7XaNXa.png",
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Price": 4.00,
        },
        {
            "Item": "Men Polo Shirt",
            "Image": "",  # add image URL if available
            "Sizes": ["S", "M", "L", "2XL", "3XL", "4XL"],
            "Price": 26.00,
        },
        {
            "Item": "Woman Polo Shirt",
            "Image": "",  # add image URL if available
            "Sizes": ["XS", "S", "M", "L", "2XL"],
            "Price": 26.00,
        },
        {
            "Item": "Beanie",
            "Image": "",  # add image URL if available
            "Sizes": [],  # no size options
            "Price": 3.50,
        },
        {
            "Item": "Magnetic Pin",
            "Image": "",  # add image URL if available
            "Sizes": [],  # no size options
            "Price": 1.50,
        },
    ],
    "Work Protection Gear": [
        {
            "Item": "Safety Helmet - Blue",
            "Image": "",  # add image URL if available
            "Sizes": [],  # no size
            "Price": 3.67,
        },
        {
            "Item": "Safety Helmet - Red",
            "Image": "",  # add image URL if available
            "Sizes": [],
            "Price": 3.67,
        },
        {
            "Item": "Safety Helmet - White",
            "Image": "",  # add image URL if available
            "Sizes": [],
            "Price": 3.67,
        },
        {
            "Item": "Safety Vest",
            "Image": "",  # add image URL if available
            "Sizes": ["L", "XL", "2XL", "3XL"],
            "Price": 3.73,
        },
    ],
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

            # Input quantities for each size if sizes exist
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
                # No size options — just one quantity input without label after item name
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

# Calculate total amount
total_amount = sum(o["Quantity"] * o["Price"] for o in order)
st.markdown(f"### Total Amount: USD {total_amount:.2f}")

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
            msg.set_content(f"New order submitted by {name}.\n\nSee attached Excel file.")

            msg.add_attachment(
                excel_data,
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=f"order_{name.replace(' ', '_')}.xlsx"
            )

            try:
