import streamlit as st
import pandas as pd
from io import BytesIO
from email.message import EmailMessage
import smtplib
from datetime import datetime

st.title("Global Merchandise Item Order Form")

# Inventory with categories, images, and pricing
inventory = {
    "Apparel": [
        {"Item": "Winter Jacket", "Image": "https://i.imgur.com/jKq8875.png", "Price": 20.06, "Sizes": ["XS", "S", "M", "L", "XL", "2XL", "3XL"]},
        {"Item": "Men Oxford Shirt", "Image": "https://i.imgur.com/URHj9BN.png", "Price": 16, "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"]},
        {"Item": "Woman Oxford Shirt", "Image": "https://i.imgur.com/6kzygzj.png", "Price": 16, "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"]},
        {"Item": "Men Bamboo Shirt", "Image": "https://i.imgur.com/D1JeIe4.png", "Price": 16, "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"]},
        {"Item": "Woman Bamboo Shirt", "Image": "https://i.imgur.com/VbJ7vwJ.png", "Price": 16, "Sizes": ["XS", "S", "M", "L", "2XL", "3XL"]},
        {"Item": "Round Neck T-shirt (Long sleeves - Blue)", "Image": "https://i.imgur.com/Jq0DzyE.png", "Price": 7.5, "Sizes": ["S", "M", "L", "2XL"]},
        {"Item": "Round Neck T-shirt (Short Sleeves - Blue)", "Image": "https://i.imgur.com/ZeF7FTF.jpeg", "Price": 6, "Sizes": ["XS", "S", "M", "L", "2XL"]},
        {"Item": "Round Neck T-shirt (Long sleeves - Yellow)", "Image": "https://i.imgur.com/GxIKeZv.png", "Price": 4.44, "Sizes": ["S", "M", "L", "2XL"]},
        {"Item": "Round Neck T-shirt (Long Sleeves - Orange)", "Image": "https://i.imgur.com/LvL2FZM.png", "Price": 4.44, "Sizes": ["S", "M", "L", "2XL"]},
        {"Item": "Round Neck T-shirt (Short sleeves - Yellow)", "Image": "https://i.imgur.com/SMYMwFo.png", "Price": 4, "Sizes": ["XS", "S", "M", "L", "2XL"]},
        {"Item": "Round Neck T-shirt (Short Sleeves - Orange)", "Image": "https://i.imgur.com/Y7XaNXa.png", "Price": 4, "Sizes": ["XS", "S", "M", "L", "2XL"]},
        {"Item": "Men Polo Shirt", "Image": "https://i.imgur.com/dNljgKo.jpeg", "Price": 26, "Sizes": ["S", "M", "L", "2XL", "3XL", "4XL"]},
        {"Item": "Woman Polo Shirt", "Image": "https://i.imgur.com/zlffC6N.jpeg", "Price": 26, "Sizes": ["XS", "S", "M", "L", "2XL"]},
        {"Item": "Beanie", "Image": "https://i.imgur.com/fB6vQdE.jpeg", "Price": 3.5, "Sizes": []},
        {"Item": "Magnetic Pin", "Image": "https://i.imgur.com/yjteqqu.jpeg", "Price": 1.5, "Sizes": []}
    ],
    "Work Protection Gear": [
        {"Item": "Safety Helmet - Blue", "Image": "https://i.imgur.com/4egynk5.png", "Price": 3.67, "Sizes": []},
        {"Item": "Safety Helmet - Red", "Image": "https://i.imgur.com/c14k5Ji.png", "Price": 3.67, "Sizes": []},
        {"Item": "Safety Helmet - White", "Image": "https://i.imgur.com/aGWu8WE.png", "Price": 3.67, "Sizes": []},
        {"Item": "Safety Vest", "Image": "", "Price": 3.73, "Sizes": ["L", "XL", "2XL", "3XL"]}
    ],
  "Job Fair Sourvenirs": [
        {"Item": "Ball Pen - Blue Ink (box)", "Image": "https://i.imgur.com/EdOevMh.jpeg", "Price": 21, "Sizes": []},
        {"Item": "Ball Pen - Black Ink (box)", "Image": "https://i.imgur.com/CDheZrD.jpeg", "Price": 18, "Sizes": []},
    ]
}
# Contact Info
st.header("Contact Information")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
location = st.text_input("Location / Office")
address = st.text_area("Delivery Address")

# Order Collection
st.header("Order Details")
order = []

for category, items in inventory.items():
    with st.expander(category):
        for item in items:
            item_name = item["Item"]
            item_price = item["Price"]
            img_url = item.get("Image", "")

            st.markdown(f"**{item_name}** - USD {item_price:.2f}")
            if img_url:
                st.image(img_url, width=150)

            if item["Sizes"]:
                for size in item["Sizes"]:
                    qty = st.number_input(
                        f"{item_name} - Size {size}",
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
                            "Total": qty * item_price
                        })
            else:
                qty = st.number_input(
                    f"{item_name}",
                    min_value=0,
                    step=1,
                    key=f"{item_name}_qty"
                )
                if qty > 0:
                    order.append({
                        "Item": item_name,
                        "Size": "",
                        "Quantity": qty,
                        "Price": item_price,
                        "Total": qty * item_price
                    })

# Show summary before submission
if order:
    st.subheader("Order Summary")
    summary_df = pd.DataFrame(order)[["Item", "Size", "Quantity", "Price", "Total"]]
    st.dataframe(summary_df, use_container_width=True)
    total_amount = summary_df["Total"].sum()
    st.markdown(f"### **Total Amount: USD {total_amount:.2f}**")

# Submit
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
