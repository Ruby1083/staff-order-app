import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# Sample product data with images
products = {
    "TSHIRT-BLACK": {
        "name": "Black T-Shirt",
        "image": "https://i.imgur.com/ZKv5i6T.png"
    },
    "HOODIE-GREY": {
        "name": "Grey Hoodie",
        "image": "https://i.imgur.com/GD5kEaA.png"
    },
    "CAP-NAVY": {
        "name": "Navy Cap",
        "image": "https://i.imgur.com/0rLDP2x.png"
    }
}

sizes = ["XS", "S", "M", "L", "XL", "2XL", "3XL"]

st.title("🧾 Staff Apparel Order Form")

staff_name = st.text_input("👤 Staff Name")

st.markdown("### 🛒 Order Items")
num_items = st.number_input("Number of different items to order", min_value=1, max_value=10, value=1)

order_list = []

for i in range(int(num_items)):
    st.markdown(f"#### Item {i + 1}")
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_sku = st.selectbox(f"Product", list(products.keys()), key=f"sku_{i}")
        selected_size = st.selectbox("Size", sizes, key=f"size_{i}")
        quantity = st.number_input("Quantity", min_value=1, step=1, key=f"qty_{i}")
    with col2:
        image_url = products[selected_sku]["image"]
        st.image(image_url, width=200, caption=products[selected_sku]["name"])

    order_list.append({
        "SKU": selected_sku,
        "Product Name": products[selected_sku]["name"],
        "Size": selected_size,
        "Quantity": quantity
    })

submit = st.button("📦 Submit Order")

# Handle order submission
if submit:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_order = []
    for item in order_list:
        full_order.append({
            "Timestamp": timestamp,
            "Staff Name": staff_name,
            **item
        })

    st.suc

