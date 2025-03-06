import json
import streamlit as st
from database_manager import DatabaseManager
from config import Config
import pandas as pd

st.header("Configure Rebate Program")

from datetime import datetime
from chat_manager import ChatManager 
import re
import torch

class RebateForm:
    def __init__(self):         
        self.chat_manager = ChatManager()
        self.db_manager = DatabaseManager(Config.DATABASE_CONNECTION_STRING)

    # Function to convert camelCase/PascalCase to space-separated words
    def format_field_name(self, name):
        return re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
    
    def create_field(self,field_name, field_data, key_suffix=""):
        """Dynamically create form field based on type"""
        field_type = field_data.get("type", "text") 
        field_value = field_data.get("value")
        label = self.format_field_name(field_name)
        # print(field_name, " Field Type : -", field_type, " value ", field_value)
        
        if field_type == "text":
            return st.text_input(label, value=str(field_value), key=f"{field_name}_{key_suffix}")
        
        elif field_type == "date":
            try:
                date_value = datetime.strptime(field_value, "%m/%d/%Y").date()
                return st.date_input(label, value=date_value,format="MM/DD/YYYY", key=f"{field_name}_{key_suffix}")
                # return st.date_input(label, value=date_value,format="MM/DD/YYYY", key=f"{field_name}_{key_suffix}")
            except:
                return st.date_input(label, key=f"{field_name}_{key_suffix}")
        
        elif field_type == "number":
            # Special handling for currency fields
            if field_name == "MinimumSalesOrder":
                return st.number_input(label + " ($)", value=float(field_value), step=1000.0, format="%.2f", key=f"{field_name}_{key_suffix}")
            
            # Handling for percentage fields
            elif "rebate" in field_name.lower() or "rate" in field_name.lower():
                col1, col2 = st.columns([4, 1])
                with col1:
                    value = st.number_input(label, value=float(field_value), step=0.5, format="%.1f", key=f"{field_name}_{key_suffix}")
                with col2:
                    st.markdown("""
                        <div style='padding-top: 32px;'>
                            <span style='font-size: 16px;'>%</span>
                        </div>
                    """, unsafe_allow_html=True)
                return value
            else:
                return st.number_input(label, value=float(field_value), key=f"{field_name}_{key_suffix}")

    def retrieve_program_details(self):
        retrieve_program_details_in_json = """
            provide the following details for the incentive program-
            0) Rebate Program name.
            1) Start Date
            2) End Date
            3) Minimum sales order
            4) list all the categories and products with rebate value eligible for the incentive program, It should be an array of categories and its respective products with rebate percentage (only numeric value)

            Note - provide the exact details without explanation in the json format (All the date type should be in the MM/DD/YYYY format) -
            below is the example -

            {"ProgramName":{"type":"text","value":"Rebate Program"},"StartDate":{"type":"date","value":"10/10/2024"},"ProductList":[{"Category":{"type":"text","value":"Insecticides"},"products":[{"produtName":"ABC","value":8,"type":"number"},{"produtName":"XYZ","value":10,"type":"number"}]}]}
        """ 
        
        with st.spinner("Loading Program details..", show_time=True):
            json_data = self.chat_manager.get_response(retrieve_program_details_in_json) 
            return json_data

    def load_form(self):        
        with st.spinner("Loading Program details..", show_time=True):
            retrieve_program_details_in_json_format="""
            provide the following details for the incentive program-
            1) Rebate Program name.
            2) Start Date
            3) End Date
            4) Minimum sales order
            5) list all the categories and products with rebate value eligible for the incentive program, It should be an array of categories and its respective products with rebate percentage (only numeric value)

            Note - provide the exact details without explanation in the json format (All the date type should be in the MM/DD/YYYY format) -
            below is the example -

            {"ProgramName":{"type":"text","value":"Rebate Program"},"StartDate":{"type":"date","value":"10/10/2024"},"ProductList":[{"Category":{"type":"text","value":"Insecticides"},"products":[{"productName":"ABC","value":8,"type":"number"},{"productName":"XYZ","value":10,"type":"number"}]}]}
        """
            
            response = self.chat_manager.get_response(retrieve_program_details_in_json_format)
            response_data = response.content.replace('```','')
            print(response_data)
            data = json.loads(response_data)
            data1 ={
                    "ProgramName": {
                        "type": "text",
                        "value": "2025 AgriTechRetailer Rebate Program"
                    },
                    "StartDate": {
                        "type": "date",
                        "value": "10/01/2024"
                    },
                    "EndDate": {
                        "type": "date",
                        "value": "09/30/2025"
                    },
                    "MinimumSalesOrder": {
                        "type": "number",
                        "value": 75000
                    },
                    "ProductList": [
                        {
                            "Category": {
                                "type": "text",
                                "value": "Insecticides"
                            },
                            "products": [
                                {
                                    "productName": "NovaShieldTech® Ultra",
                                    "value": 8,
                                    "type": "number"
                                },
                                {
                                    "productName": "PestBusterTech® Max",
                                    "value": 10,
                                    "type": "number"
                                },
                                {
                                    "productName": "CropGuardian® Elite",
                                    "value": 6,
                                    "type": "number"
                                }
                            ]
                        },
                        {
                            "Category": {
                                "type": "text",
                                "value": "Fungicides"
                            },
                            "products": [
                                {
                                    "productName": "FungiSafeTech® Pro",
                                    "value": 9,
                                    "type": "number"
                                },
                                {
                                    "productName": "SporeBlock® XT",
                                    "value": 12,
                                    "type": "number"
                                }
                            ]
                        },
                        {
                            "Category": {
                                "type": "text",
                                "value": "Herbicides"
                            },
                            "products": [
                                {
                                    "productName": "WeedTerminatorTech® Plus",
                                    "value": 11,
                                    "type": "number"
                                },
                                {
                                    "productName": "SeedField® Control",
                                    "value": 7,
                                    "type": "number"
                                }
                            ]
                        },
                        {
                            "Category": {
                                "type": "text",
                                "value": "Seed Treatments"
                            },
                            "products": [
                                {
                                    "productName": "SeedArmor® 500",
                                    "value": 10,
                                    "type": "number"
                                }
                            ]
                        }
                    ]
                }
            
            data2 = {
  "ProgramName": {"type": "text", "value": "2025 AgriTechRetailer Rebate Program"},
  "StartDate": {"type": "date", "value": "10/01/2024"},
  "EndDate": {"type": "date", "value": "09/30/2025"},
  "MinimumSalesOrder": {"type": "number", "value": 75000},
  "ProductList": [
    {
      "Category": {"type": "text", "value": "Insecticides"},
      "products": [
        {"productName": "NovaShieldTech® Ultra", "value": 8, "type": "number"},
        {"productName": "PestBusterTech® Max", "value": 10, "type": "number"},
        {"productName": "CropGuardian® Elite", "value": 6, "type": "number"}
      ]
    },
    {
      "Category": {"type": "text", "value": "Fungicides"},
      "products": [
        {"productName": "FungiSafeTech® Pro", "value": 9, "type": "number"},
        {"productName": "SporeBlock® XT", "value": 12, "type": "number"}
      ]
    },
    {
      "Category": {"type": "text", "value": "Herbicides"},
      "products": [
        {"productName": "WeedTerminatorTech® Plus", "value": 11, "type": "number"},
        {"productName": "SeedField® Control", "value": 7, "type": "number"}
      ]
    },
    {
      "Category": {"type": "text", "value": "Seed Treatments"},
      "products": [
        {"productName": "SeedArmor® 500", "value": 10, "type": "number"}
      ]
    }
  ]
}
            st.write(data)

            
            with st.form("rebate_program_form"):
                # Program Details
                col1, col2 = st.columns(2)
                
                form_data = {}
                # Create main program fields dynamically
                with col1:
                    form_data["ProgramName"] = self.create_field("ProgramName", data["ProgramName"])
                    form_data["StartDate"] = self.create_field("StartDate", data["StartDate"])

                with col2:
                    form_data["MinimumSalesOrder"] = self.create_field("MinimumSalesOrder", data["MinimumSalesOrder"])
                    form_data["EndDate"] = self.create_field("EndDate", data["EndDate"])

                # Product List Section
                st.header("Product Categories")
                product_data = []
                
                for category in data["ProductList"]:
                    category_name = category["Category"]["value"]
                    
                    st.subheader(category["Category"]["value"])
                    
                    for product in category["products"]:
                        with st.container():
                            col1, col2 = st.columns([3, 3])
                            
                            with col1:
                                product_name = self.create_field(
                                    "ProductName",
                                    {"type": "text", "value": product["productName"]},
                                    key_suffix=f"{category_name}_{product['productName']}"
                                )
                            
                            with col2:
                                rebate_rate = self.create_field(
                                    "RebateRate",
                                    {"type": "number", "value": product["value"]},
                                    key_suffix=f"{category_name}_{product['productName']}"
                                )
                            
                            product_data.append({
                                "category": category_name,
                                "product_name": product_name,
                                "rebate_rate": rebate_rate
                            })
                            
                            st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)
                
                # Ensure the submit button is inside the form
                submitted = st.form_submit_button("Submit")
                
                if submitted:
                    st.write("Form Submitted!")
                    st.write("Form Data:")
                    st.write(form_data)  # This will print out the Program details form data
                    st.write(product_data)  # This will print out product and rebate details
                    start_date = form_data["StartDate"]
                    formatted_date = start_date.strftime('%m-%d-%Y')
                    print(formatted_date)
                    st.write(formatted_date)

                    # Save Form Data
                    rebate_program_data = {
                        'program_name': form_data["ProgramName"],
                        'start_date': form_data["StartDate"].strftime('%m-%d-%Y'),
                        'end_date': form_data["EndDate"].strftime('%m-%d-%Y'),
                        'minimum_sales_value': form_data["MinimumSalesOrder"]
                    }
                    
                    # schema = self.db_manager.get_schema_info()
                    # print(schema)
                    self.db_manager.save_row_data("dbo.Rebate_Program",rebate_program_data)

                    # saved_data = self.db_manager.execute_query("SELECT * FROM information_schema.tables WHERE table_name = 'Rebate_Program'")
                    # print(saved_data)
                    st.success("Rebase program saved successfully!!")









            # if data is not None:
            #     with st.form("rebate_program_form"):
            #         # Program Details
            #         col1, col2 = st.columns(2)
                    
            #         form_data = {}
            #         # Create main program fields dynamically
            #         with col1:
            #             form_data["ProgramName"] = self.create_field("ProgramName", data["ProgramName"])
            #             form_data["StartDate"] = self.create_field("StartDate", data["StartDate"])
                        
                    
            #         with col2:
            #             form_data["MinimumSalesOrder"] = self.create_field("MinimumSalesOrder", data["MinimumSalesOrder"])
            #             form_data["EndDate"] = self.create_field("EndDate", data["EndDate"])
                        
                    
            #         # Product List Section
            #         st.header("Product Categories")
            #         product_data = []
                    
            #         for category in data["ProductList"]:
            #             category_name = category["Category"]["value"]
                        
            #             st.subheader(category["Category"]["value"])
                        
            #             for product in category["products"]:
            #                 with st.container():
            #                     col1, col2 = st.columns([3, 3])
                                
            #                     with col1:
            #                         product_name = self.create_field(
            #                             "ProductName",
            #                             {"type": "text", "value": product["productName"]},
            #                             key_suffix=f"{category_name}_{product['productName']}"
            #                         )
                                
            #                     with col2:
            #                         rebate_rate = self.create_field(
            #                             "RebateRate",
            #                             {"type": "number", "value": product["value"]},
            #                             key_suffix=f"{category_name}_{product['productName']}"
            #                         )
                                
            #                     product_data.append({
            #                         "category": category_name,
            #                         "product_name": product_name,
            #                         "rebate_rate": rebate_rate
            #                     })
                                
            #                     st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)
                    
            #         submitted = st.form_submit_button("Submit")
                    
            #         if submitted:
            #             print("submitted")
            #             st.write("Form Submitted!")
            #             st.write("Form Data:")
            #             st.write(form_data)  # This will print out the Program details form data
            #             st.write(product_data)  # This will print out product and rebate details


# When this page is loaded through navigation, run the assistant
if __name__ == "__main__":
    torch.classes.__path__ = [] 

# Always instantiate and run the assistant when this file is loaded through navigation
rebate_assistant = RebateForm()
rebate_assistant.load_form()