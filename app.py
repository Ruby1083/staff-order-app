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
submit = st.button("📦 Submit Order")

if submit:
    if not staff_name.strip():
        st.error("❗ Please enter your name before submitting.")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_order = []
        for item in order_list:
            full_order.append({
                "Timestamp": timestamp,
                "Staff Name": staff_name,
                **item
            })

        st.success("✅ Order submitted!")
        st.subheader("📝 Order Summary")
        order_df = pd.DataFrame(full_order)
        st.dataframe(order_df)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            order_df.to_excel(writer, index=False, sheet_name="Orders")

        safe_name = staff_name.strip().replace(' ', '_') or "unknown_staff"
        file_name = f"order_{safe_name}.xlsx"

        st.download_button(
            label="📁 Download Order Excel File",
            data=output.getvalue(),
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


