import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

inventory = {
    "TSHIRT-BLACK-M": {"name": "Black T-Shirt (M)", "stock": 50},
    "TSHIRT-BLACK-L": {"name": "Black T-Shirt (L)", "stock": 30},
    "HOODIE-GREY-XL": {"name": "Grey Hoodie (XL)", "stock": 20}
}

order_log = []

st.title("🧾 Staff Apparel Order Form")

staff_name = st.text_input("Staff Name")
sku = st.selectbox("Select Product", options=list(inventory.keys()))
qty = st.number_input("Quantity", min_value=1, step=1)
submit = st.button("Submit Order")

if submit:
    if inventory[sku]["stock"] >= qty:
        inventory[sku]["stock"] -= qty
        order = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Staff Name": staff_name,
            "SKU": sku,
            "Product Name": inventory[sku]["name"],
            "Quantity": qty
        }
        order_log.append(order)
        st.success(f"✅ Order placed for {qty}x {inventory[sku]['name']}")
    else:
        st.error("❌ Not enough stock available.")

if order_log:
    st.subheader("📝 Order Summary")
    order_df = pd.DataFrame(order_log)
    st.dataframe(order_df)

st.subheader("📦 Current Inventory")
inv_df = pd.DataFrame([
    {"SKU": sku, "Product Name": item["name"], "Stock": item["stock"]}
    for sku, item in inventory.items()
])
st.dataframe(inv_df)

if order_log:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        order_df.to_excel(writer, sheet_name='Orders', index=False)
        inv_df.to_excel(writer, sheet_name='Inventory', index=False)
    st.download_button(
        label="📁 Download Excel File",
        data=output.getvalue(),
        file_name="staff_orders.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
