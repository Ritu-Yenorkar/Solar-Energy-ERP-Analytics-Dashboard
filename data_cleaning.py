import pandas as pd

file_path = "data/Solar_Energy_ERP_Dataset.xlsx"

suppliers = pd.read_excel(file_path, sheet_name="Sheet11")
projects = pd.read_excel(file_path, sheet_name="Sheet10")
products = pd.read_excel(file_path, sheet_name="Sheet9")
procurement = pd.read_excel(file_path, sheet_name="Sheet8")
maintenance = pd.read_excel(file_path, sheet_name="Sheet7")
inventory = pd.read_excel(file_path, sheet_name="Sheet6")
installation = pd.read_excel(file_path, sheet_name="Sheet5")
employees = pd.read_excel(file_path, sheet_name="Sheet4")
billing = pd.read_excel(file_path, sheet_name="Sheet3")
customers = pd.read_excel(file_path, sheet_name="Sheet2")

print("All 10 ERP tables loaded successfully!")

print("Customers:", customers.shape)
print("Suppliers:", suppliers.shape)
print("Products:", products.shape)
print("Employees:", employees.shape)
print("Projects:", projects.shape)
print("Procurement:", procurement.shape)
print("Installation:", installation.shape)
print("Billing:", billing.shape)
print("Maintenance:", maintenance.shape)
print("Inventory:", inventory.shape)

# Checking missing and null values
print("\n--- Data Quality Check ---")

tables = {
    "Customers": customers,
    "Suppliers": suppliers,
    "Products": products,
    "Employees": employees,
    "Projects": projects,
    "Procurement": procurement,
    "Installation": installation,
    "Billing": billing,
    "Maintenance": maintenance,
    "Inventory": inventory
}

for name, df in tables.items():
    print(f"\n{name}")
    print("Missing values:")
    print(df.isnull().sum())
    print("Duplicate rows:", df.duplicated().sum())



    print("\n--- Date Column Data Types ---")

print("\nProjects:")
print(projects[[
    "Project_Date",
    "Expected_Completion",
    "Actual_Completion"
]].dtypes)

print("\nProcurement:")
print(procurement[[
    "PO_Date",
    "Expected_Delivery",
    "Actual_Delivery"
]].dtypes)

print("\nBilling:")
print(billing[[
    "Invoice_Date",
    "Due_Date"
]].dtypes)

print("\nInstallation:")
print(installation["Installation_Date"].dtype)

print("\nMaintenance:")
print(maintenance["Maintenance_Date"].dtype)

print("\nInventory:")
print(inventory["Transaction_Date"].dtype)





print("\n--- Sample Date Values ---")

print("\nProjects:")
print(projects[[
    "Project_Date",
    "Expected_Completion",
    "Actual_Completion"
]].head())

print("\nProcurement:")
print(procurement[[
    "PO_Date",
    "Expected_Delivery",
    "Actual_Delivery"
]].head())

# Convert date column
# Convert Excel serial numbers to proper dates

project_date_columns = [
    "Project_Date",
    "Expected_Completion",
    "Actual_Completion"
]

for col in project_date_columns:
    projects[col] = pd.to_datetime(
        projects[col],
        unit="D",
        origin="1899-12-30",
        errors="coerce"
    )


procurement_date_columns = [
    "PO_Date",
    "Expected_Delivery",
    "Actual_Delivery"
]

for col in procurement_date_columns:
    procurement[col] = pd.to_datetime(
        procurement[col],
        unit="D",
        origin="1899-12-30",
        errors="coerce"
    )


billing_date_columns = [
    "Invoice_Date",
    "Due_Date"
]

for col in billing_date_columns:
    billing[col] = pd.to_datetime(
        billing[col],
        unit="D",
        origin="1899-12-30",
        errors="coerce"
    )


installation["Installation_Date"] = pd.to_datetime(
    installation["Installation_Date"],
    unit="D",
    origin="1899-12-30",
    errors="coerce"
)

maintenance["Maintenance_Date"] = pd.to_datetime(
    maintenance["Maintenance_Date"],
    unit="D",
    origin="1899-12-30",
    errors="coerce"
)

inventory["Transaction_Date"] = pd.to_datetime(
    inventory["Transaction_Date"],
    unit="D",
    origin="1899-12-30",
    errors="coerce"
)


print("\n--- Converted Date Values ---")

print(projects[
    ["Project_Date", "Expected_Completion", "Actual_Completion"]
].head())

print("\nDate conversion completed successfully!")

# Checking duplicate ids
print("\n--- Duplicate ID Check ---")

id_columns = {
    "Customers": (customers, "Customer_ID"),
    "Suppliers": (suppliers, "Supplier_ID"),
    "Products": (products, "Product_ID"),
    "Employees": (employees, "Employee_ID"),
    "Projects": (projects, "Project_ID"),
    "Procurement": (procurement, "PO_ID"),
    "Installation": (installation, "Installation_ID"),
    "Billing": (billing, "Invoice_ID"),
    "Maintenance": (maintenance, "Maintenance_ID"),
    "Inventory": (inventory, "Inventory_ID")
}

for name, (df, id_col) in id_columns.items():
    duplicate_ids = df[id_col].duplicated().sum()
    print(f"{name} - Duplicate {id_col}: {duplicate_ids}")


# Check negative value
print("\n--- Numeric Data Check ---")

numeric_checks = {
    "Projects - Capacity_kW": projects["Capacity_kW"],
    "Projects - Estimated_Cost": projects["Estimated_Cost"],
    "Projects - Actual_Cost": projects["Actual_Cost"],
    "Projects - Contract_Value": projects["Contract_Value"],
    "Procurement - Quantity": procurement["Quantity"],
    "Procurement - Unit_Price": procurement["Unit_Price"],
    "Procurement - Total_Amount": procurement["Total_Amount"],
    "Installation - Team_Size": installation["Team_Size"],
    "Installation - Hours_Worked": installation["Hours_Worked"],
    "Installation - Quality_Score": installation["Quality_Score"],
    "Billing - Invoice_Amount": billing["Invoice_Amount"],
    "Billing - Paid_Amount": billing["Paid_Amount"],
    "Maintenance - Maintenance_Cost": maintenance["Maintenance_Cost"],
    "Inventory - Quantity": inventory["Quantity"]
}

for name, column in numeric_checks.items():
    print(f"{name} - Negative values: {(column < 0).sum()}")


# Status / category check
print("\n--- Categorical Values Check ---")

categorical_columns = {
    "Customer Type": customers["Customer_Type"],
    "Supplier Category": suppliers["Supplier_Category"],
    "Project Type": projects["Project_Type"],
    "Project Status": projects["Project_Status"],
    "Delivery Status": procurement["Delivery_Status"],
    "Installation Status": installation["Installation_Status"],
    "Payment Status": billing["Payment_Status"],
    "Issue Type": maintenance["Issue_Type"],
    "Priority": maintenance["Priority"],
    "Resolution Status": maintenance["Resolution_Status"],
    "Transaction Type": inventory["Transaction_Type"]
}

for name, column in categorical_columns.items():
    print(f"\n{name}:")
    print(column.unique())


# Business validation check
print("\n--- Business Validation Check ---")

# Procurement: Total Amount check
procurement_expected = procurement["Quantity"] * procurement["Unit_Price"]

procurement_difference = (
    procurement["Total_Amount"] - procurement_expected
).abs()

print(
    "Procurement Total Amount mismatches:",
    (procurement_difference > 0.01).sum()
)

# Billing: Paid Amount should not exceed Invoice Amount
print(
    "Billing Paid Amount > Invoice Amount:",
    (billing["Paid_Amount"] > billing["Invoice_Amount"]).sum()
)

# Projects: Actual Cost should not be negative
print(
    "Projects Actual Cost > Contract Value:",
    (projects["Actual_Cost"] > projects["Contract_Value"]).sum()
)


# Handle missing dates according to business logic
print("\n--- Missing Date Business Check ---")

# Completed projects with missing actual completion date
completed_missing = projects[
    (projects["Project_Status"] == "Completed") &
    (projects["Actual_Completion"].isna())
]

print(
    "Completed projects with missing Actual_Completion:",
    len(completed_missing)
)

# Delivered procurement with missing actual delivery date
delivered_missing = procurement[
    (procurement["Delivery_Status"] == "Delivered") &
    (procurement["Actual_Delivery"].isna())
]

print(
    "Delivered POs with missing Actual_Delivery:",
    len(delivered_missing)
)

# Cost Overrun Calculation
projects["Cost_Overrun"] = (
    projects["Actual_Cost"] - projects["Estimated_Cost"]
)

print("\n--- Cost Overrun ---")

print(
    projects[
        [
            "Project_ID",
            "Estimated_Cost",
            "Actual_Cost",
            "Cost_Overrun"
        ]
    ].head()
)

# Cost Overrun Percentage
projects["Cost_Overrun_Pct"] = (
    projects["Cost_Overrun"] / projects["Estimated_Cost"]
) * 100

print("\n--- Cost Overrun Percentage ---")

print(
    projects[
        [
            "Project_ID",
            "Estimated_Cost",
            "Actual_Cost",
            "Cost_Overrun",
            "Cost_Overrun_Pct"
        ]
    ].head()
)

# Project Delay Days
projects["Delay_Days"] = (
    projects["Actual_Completion"] -
    projects["Expected_Completion"]
).dt.days

print("\n--- Project Delay ---")

print(
    projects[
        [
            "Project_ID",
            "Project_Status",
            "Expected_Completion",
            "Actual_Completion",
            "Delay_Days"
        ]
    ].head(10)
)


# Save cleaned data as CSV files

customers.to_csv("data/cleaned_customers.csv", index=False)
suppliers.to_csv("data/cleaned_suppliers.csv", index=False)
products.to_csv("data/cleaned_products.csv", index=False)
employees.to_csv("data/cleaned_employees.csv", index=False)
projects.to_csv("data/cleaned_projects.csv", index=False)
procurement.to_csv("data/cleaned_procurement.csv", index=False)
installation.to_csv("data/cleaned_installation.csv", index=False)
billing.to_csv("data/cleaned_billing.csv", index=False)
maintenance.to_csv("data/cleaned_maintenance.csv", index=False)
inventory.to_csv("data/cleaned_inventory.csv", index=False)

print("\nAll cleaned CSV files saved successfully!")