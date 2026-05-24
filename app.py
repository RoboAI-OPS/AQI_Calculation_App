
# # # import streamlit as st
# # # import pandas as pd
# # # import os
# # # import zipfile
# # # import tempfile
# # # from io import BytesIO

# # # st.set_page_config(page_title="AQI Time Slot Summary Generator", layout="wide")

# # # st.title("🌍 AQI Time Slot Summary Generator")
# # # st.write("Upload a ZIP file or multiple Excel files (.xlsx). The app will process the data and generate Time_Slot_Summary.xlsx.")

# # # time_ranges = {
# # #     '00:00-06:00': (0, 6),
# # #     '06:00-12:00': (6, 12),
# # #     '12:00-18:00': (12, 18),
# # #     '18:00-24:00': (18, 24),
# # # }

# # # direct_ugm3_cols = ['PM 10 (ug/m3)', 'PM 2.5 (ug/m3)', 'PM 1 (ug/m3)', 'Air Quality Index']
# # # env_cols = ['Temp (°C)', 'Humidity %']
# # # ppb_gases = ['NO2', 'SO2', 'CO', 'O3']

# # # address_mapping = {
# # #     "MCT2408041": "Village Panchayat Uguem- Government Office",
# # #     "MCT2408046": "Village Panchayat Pissurlem",
# # #     "MCT2408056": "Village Panchayat Mayam",
# # #     "MCT2408051": "Vasu Hotel, Front Of Tagore School, Hathkhamba- Goa rd, Kotambi",
# # #     "MCT2408022": "Tushar Weighbridge, Near by Vagus Junction",
# # #     "MCT2408043": "Tilamol Junction, Quepem-Curchorem Road",
# # #     "MCT2408044": "Somnath School, Codli",
# # #     "MCT2408023": "Siya Surlekar House, Near by Old Surla Panchayat Office",
# # #     "MCT2408050": "Siddhesh Kotkar, Piligaon, Nearby Vedanta Jetty",
# # #     "MCT2408038": "Ramnath B Naik House, Ambaulim, Gudumol, Quepem, (Near By MDR-46)",
# # #     "MCT2408021": "Ramdas House, Velguem, Sanquelim, Velguem-Surla-sgao rd, (Near State Bank Of India)",
# # #     "MCT2408042": "Quepem Circle (Nearby Govt offices)",
# # #     "MCT2408034": "Mr. Kusta Gaounkar, Nalini Bar & Restaurant, Codli",
# # #     "MCT2408039": "Mr. Ashis Naik House, Rivona Gate, Pandovwado,Sangum, Near by Temple",
# # #     "MCT2408029": "Mr. Aniket Dessai House, Shigaon",
# # #     "MCT2408031": "Mr Dilip House, Near Sai Tample, Ambeudak (Shradha Ispat), Kaley Mineral Rd",
# # #     "MCT2408030": "Kurpem Village (Nearby MDR-47, Ambaulim-Cavorim-Pirla at Anil Fals dessai Home)",
# # #     "MCT2408052": "Jaydev B Natekar House, Wedalade, usgao",
# # #     "MCT2408040": "Govt Primary School Near Fanaswadi Junction, Naveli",
# # #     "MCT2408035": "Govt Polytechnic College, Curchorem, Cacora",
# # #     "MCT2408028": "Govt High School, Zambaulim",
# # #     "MCT2408024": "Govt High School, Colamb",
# # #     "MCT2408026": "Diogo Fernandes House, Uguem Junction",
# # #     "MCT2408037": "Deputy Collector Office, Dharbandora",
# # #     "MCT2408036": "Caverem Pirla Aganwadi",
# # #     "MCT2408045": "Baliram Govind Malik House, mapusa-Bicholim Rd, Sirsai",
# # #     "MCT2408049": "At Mr. Sagun S. Gawas House, Ambegal, pale",
# # #     "MCT2408020": "Ajoba Devesthan Honda, Sanquelim Velguem, Surla, Usgaon Road, Near By Ajoba Nagar",
# # #     "MCT2408032": "IHM Porvorim",
# # #     "MCT2408027": "Mr. Caitano Dcosta, Tollem Bus Stand, Sanvordem, Nearby Capxem Jetty",
# # #     "MCT2408033": "Mr. Aakash Naik Tishem, Borim, Nearby Old Bridge",
# # #     "MCT2408053": "Ravindra Bhagwan, Curchorem Cricel",
# # #     "MCT2408057": "Govt Primary School, Sanvordem",
# # #     "MCT2408055": "Ravindra House, Haldanwadi Mayem, Nearby Vittal Temple (Chokhla Mine)"
# # # }

# # # def smart_round(val):
# # #     try:
# # #         return round(float(val), 2)
# # #     except:
# # #         return None

# # # def process_folder(folder_path):
# # #     results = []

# # #     for file in os.listdir(folder_path):
# # #         if file.endswith(".xlsx"):
# # #             file_path = os.path.join(folder_path, file)
# # #             device_name = os.path.splitext(file)[0]
# # #             location = address_mapping.get(device_name, "Unknown Location")

# # #             try:
# # #                 df = pd.read_excel(file_path, skiprows=6, header=None)

# # #                 df.columns = (
# # #                     ['Time']
# # #                     + direct_ugm3_cols[:3]
# # #                     + [f'{gas} (ug/m3)' for gas in ppb_gases]
# # #                     + ['CO2 (ppm)']
# # #                     + env_cols
# # #                     + [direct_ugm3_cols[-1]]
# # #                 )

# # #                 df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
# # #                 df.dropna(subset=['Time'], inplace=True)

# # #                 if df.empty:
# # #                     continue

# # #                 df['Hour'] = df['Time'].dt.hour
# # #                 date_value = df['Time'].dt.date.iloc[0]

# # #                 final_columns = (
# # #                     direct_ugm3_cols[:3]
# # #                     + [f'{gas} (ug/m3)' for gas in ppb_gases]
# # #                     + ['CO2 (ppm)']
# # #                     + env_cols
# # #                     + [direct_ugm3_cols[-1]]
# # #                 )

# # #                 for slot, (start, end) in time_ranges.items():
# # #                     df_slot = df[(df['Hour'] >= start) & (df['Hour'] < end)]
# # #                     if df_slot.empty:
# # #                         continue

# # #                     row = {
# # #                         'Device': device_name,
# # #                         'Location': location,
# # #                         'Date': date_value,
# # #                         'Time Slot': slot,
# # #                     }

# # #                     for col in final_columns:
# # #                         col_min = smart_round(df_slot[col].min())
# # #                         col_max = smart_round(df_slot[col].max())

# # #                         if col_min is not None and col_max is not None and col_min > col_max:
# # #                             col_min, col_max = col_max, col_min

# # #                         row[f'{col} Min'] = col_min
# # #                         row[f'{col} Max'] = col_max

# # #                     results.append(row)

# # #             except Exception as e:
# # #                 st.warning(f"Error processing {file}: {e}")

# # #     result_df = pd.DataFrame(results)

# # #     for col in result_df.columns:
# # #         if 'Min' in col or 'Max' in col:
# # #             result_df[col] = pd.to_numeric(result_df[col], errors='coerce')

# # #     return result_df


# # # upload_type = st.radio("Choose Upload Method", ["ZIP Upload", "Multiple Excel Upload"])

# # # if upload_type == "ZIP Upload":
# # #     uploaded_zip = st.file_uploader("Upload ZIP file", type=["zip"])

# # #     if uploaded_zip and st.button("Process ZIP"):
# # #         with tempfile.TemporaryDirectory() as temp_dir:
# # #             with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
# # #                 zip_ref.extractall(temp_dir)

# # #             result_df = process_folder(temp_dir)

# # #             if not result_df.empty:
# # #                 output = BytesIO()
# # #                 with pd.ExcelWriter(output, engine='openpyxl') as writer:
# # #                     result_df.to_excel(writer, index=False, sheet_name='Summary')

# # #                 st.success("Processing Complete!")
# # #                 st.dataframe(result_df.head())

# # #                 st.download_button(
# # #                     "📥 Download Time_Slot_Summary.xlsx",
# # #                     output.getvalue(),
# # #                     file_name="Time_Slot_Summary.xlsx",
# # #                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# # #                 )

# # # elif upload_type == "Multiple Excel Upload":
# # #     uploaded_files = st.file_uploader(
# # #         "Upload Excel Files",
# # #         type=["xlsx"],
# # #         accept_multiple_files=True
# # #     )

# # #     if uploaded_files and st.button("Process Files"):
# # #         with tempfile.TemporaryDirectory() as temp_dir:
# # #             for file in uploaded_files:
# # #                 with open(os.path.join(temp_dir, file.name), "wb") as f:
# # #                     f.write(file.getbuffer())

# # #             result_df = process_folder(temp_dir)

# # #             if not result_df.empty:
# # #                 output = BytesIO()
# # #                 with pd.ExcelWriter(output, engine='openpyxl') as writer:
# # #                     result_df.to_excel(writer, index=False, sheet_name='Summary')

# # #                 st.success("Processing Complete!")
# # #                 st.dataframe(result_df.head())

# # #                 st.download_button(
# # #                     "📥 Download Time_Slot_Summary.xlsx",
# # #                     output.getvalue(),
# # #                     file_name="Time_Slot_Summary.xlsx",
# # #                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# # #                 )

# # ###############################

# # import streamlit as st
# # import pandas as pd
# # import os
# # import zipfile
# # import tempfile
# # from io import BytesIO

# # # =========================
# # # PAGE CONFIG
# # # =========================
# # st.set_page_config(
# #     page_title="AQI Analytics Dashboard",
# #     layout="wide",
# #     page_icon="🌍"
# # )

# # # =========================
# # # PREMIUM UI (CSS STYLE)
# # # =========================
# # st.markdown("""
# #     <style>
# #     .main {
# #         background-color: #0f172a;
# #     }

# #     .title {
# #         font-size: 38px;
# #         font-weight: 700;
# #         color: #ffffff;
# #         text-align: center;
# #         margin-bottom: 10px;
# #     }

# #     .subtitle {
# #         text-align: center;
# #         color: #94a3b8;
# #         font-size: 16px;
# #         margin-bottom: 30px;
# #     }

# #     .card {
# #         background: #111827;
# #         padding: 20px;
# #         border-radius: 15px;
# #         box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
# #     }

# #     .stButton>button {
# #         background: linear-gradient(90deg, #06b6d4, #3b82f6);
# #         color: white;
# #         border-radius: 10px;
# #         padding: 10px 20px;
# #         border: none;
# #         font-weight: bold;
# #     }

# #     .stDownloadButton>button {
# #         background: linear-gradient(90deg, #22c55e, #16a34a);
# #         color: white;
# #         border-radius: 10px;
# #         padding: 10px 20px;
# #         border: none;
# #         font-weight: bold;
# #     }
# #     </style>
# # """, unsafe_allow_html=True)

# # # =========================
# # # HEADER
# # # =========================
# # st.markdown('<div class="title">🌍 AQI Time Slot Analytics Dashboard</div>', unsafe_allow_html=True)
# # st.markdown('<div class="subtitle">Upload Excel or ZIP files → Get Time Slot Summary Report instantly</div>', unsafe_allow_html=True)

# # # =========================
# # # CONFIG
# # # =========================
# # time_ranges = {
# #     '00:00-06:00': (0, 6),
# #     '06:00-12:00': (6, 12),
# #     '12:00-18:00': (12, 18),
# #     '18:00-24:00': (18, 24),
# # }

# # direct_ugm3_cols = ['PM 10 (ug/m3)', 'PM 2.5 (ug/m3)', 'PM 1 (ug/m3)', 'Air Quality Index']
# # env_cols = ['Temp (°C)', 'Humidity %']
# # ppb_gases = ['NO2', 'SO2', 'CO', 'O3']

# # # =========================
# # # DEVICE MAP
# # # =========================
# # address_mapping = {
# #     "MCT2408041": "Village Panchayat Uguem- Government Office",
# #     "MCT2408046": "Village Panchayat Pissurlem",
# #     "MCT2408056": "Village Panchayat Mayam",
# #     "MCT2408051": "Vasu Hotel, Front Of Tagore School, Hathkhamba- Goa rd, Kotambi",
# #     "MCT2408022": "Tushar Weighbridge, Near by Vagus Junction",
# #     "MCT2408043": "Tilamol Junction, Quepem-Curchorem Road",
# #     "MCT2408044": "Somnath School, Codli",
# #     "MCT2408023": "Siya Surlekar House, Near by Old Surla Panchayat Office",
# #     "MCT2408050": "Siddhesh Kotkar, Piligaon, Nearby Vedanta Jetty",
# #     "MCT2408038": "Ramnath B Naik House, Ambaulim, Gudumol, Quepem, (Near By MDR-46)",
# #     "MCT2408021": "Ramdas House, Velguem, Sanquelim, Velguem-Surla-sgao rd, (Near State Bank Of India)",
# #     "MCT2408042": "Quepem Circle (Nearby Govt offices)",
# #     "MCT2408034": "Mr. Kusta Gaounkar, Nalini Bar & Restaurant, Codli",
# #     "MCT2408039": "Mr. Ashis Naik House, Rivona Gate, Pandovwado,Sangum, Near by Temple",
# #     "MCT2408029": "Mr. Aniket Dessai House, Shigaon",
# #     "MCT2408031": "Mr Dilip House, Near Sai Tample, Ambeudak (Shradha Ispat), Kaley Mineral Rd",
# #     "MCT2408030": "Kurpem Village (Nearby MDR-47, Ambaulim-Cavorim-Pirla at Anil Fals dessai Home)",
# #     "MCT2408052": "Jaydev B Natekar House, Wedalade, usgao",
# #     "MCT2408040": "Govt Primary School Near Fanaswadi Junction, Naveli",
# #     "MCT2408035": "Govt Polytechnic College, Curchorem, Cacora",
# #     "MCT2408028": "Govt High School, Zambaulim",
# #     "MCT2408024": "Govt High School, Colamb",
# #     "MCT2408026": "Diogo Fernandes House, Uguem Junction",
# #     "MCT2408037": "Deputy Collector Office, Dharbandora",
# #     "MCT2408036": "Caverem Pirla Aganwadi",
# #     "MCT2408045": "Baliram Govind Malik House, mapusa-Bicholim Rd, Sirsai",
# #     "MCT2408049": "At Mr. Sagun S. Gawas House, Ambegal, pale",
# #     "MCT2408020": "Ajoba Devesthan Honda, Sanquelim Velguem, Surla, Usgaon Road, Near By Ajoba Nagar",
# #     "MCT2408032": "IHM Porvorim",
# #     "MCT2408027": "Mr. Caitano Dcosta, Tollem Bus Stand, Sanvordem, Nearby Capxem Jetty",
# #     "MCT2408033": "Mr. Aakash Naik Tishem, Borim, Nearby Old Bridge",
# #     "MCT2408053": "Ravindra Bhagwan, Curchorem Cricel",
# #     "MCT2408057": "Govt Primary School, Sanvordem",
# #     "MCT2408055": "Ravindra House, Haldanwadi Mayem, Nearby Vittal Temple (Chokhla Mine)"
# # }

# # # =========================
# # # UTIL FUNCTION
# # # =========================
# # def smart_round(val):
# #     try:
# #         return round(float(val), 2)
# #     except:
# #         return None


# # # =========================
# # # CORE PROCESSING
# # # =========================
# # def process_folder(folder_path):
# #     results = []

# #     for file in os.listdir(folder_path):
# #         if file.endswith(".xlsx"):
# #             file_path = os.path.join(folder_path, file)
# #             device_name = os.path.splitext(file)[0]
# #             location = address_mapping.get(device_name, "Unknown Location")

# #             try:
# #                 df = pd.read_excel(file_path, skiprows=6, header=None)

# #                 df.columns = (
# #                     ['Time']
# #                     + direct_ugm3_cols[:3]
# #                     + [f'{gas} (ug/m3)' for gas in ppb_gases]
# #                     + ['CO2 (ppm)']
# #                     + env_cols
# #                     + [direct_ugm3_cols[-1]]
# #                 )

# #                 df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
# #                 df.dropna(subset=['Time'], inplace=True)

# #                 if df.empty:
# #                     continue

# #                 df['Hour'] = df['Time'].dt.hour
# #                 date_value = df['Time'].dt.date.iloc[0]

# #                 final_columns = (
# #                     direct_ugm3_cols[:3]
# #                     + [f'{gas} (ug/m3)' for gas in ppb_gases]
# #                     + ['CO2 (ppm)']
# #                     + env_cols
# #                     + [direct_ugm3_cols[-1]]
# #                 )

# #                 for slot, (start, end) in time_ranges.items():
# #                     df_slot = df[(df['Hour'] >= start) & (df['Hour'] < end)]
# #                     if df_slot.empty:
# #                         continue

# #                     row = {
# #                         'Device': device_name,
# #                         'Location': location,
# #                         'Date': date_value,
# #                         'Time Slot': slot,
# #                     }

# #                     for col in final_columns:
# #                         col_min = smart_round(df_slot[col].min())
# #                         col_max = smart_round(df_slot[col].max())

# #                         row[f'{col} Min'] = col_min
# #                         row[f'{col} Max'] = col_max

# #                     results.append(row)

# #             except Exception as e:
# #                 st.warning(f"Error processing {file}: {e}")

# #     return pd.DataFrame(results)


# # # =========================
# # # SIDEBAR CONTROLS
# # # =========================
# # with st.sidebar:
# #     st.header("⚙️ Controls")

# #     upload_type = st.radio("Upload Method", ["ZIP Upload", "Multiple Excel Upload"])

# #     file_name = st.text_input(
# #         "Output File Name (optional)",
# #         placeholder="Enter file name (e.g. my_report.xlsx)"
# #     )

# #     st.markdown("---")
# #     st.info("If empty → default: timesheet.xlsx")


# # # =========================
# # # MAIN UI CONTAINER
# # # =========================
# # st.markdown('<div class="card">', unsafe_allow_html=True)

# # result_df = None

# # # =========================
# # # ZIP UPLOAD
# # # =========================
# # if upload_type == "ZIP Upload":
# #     uploaded_zip = st.file_uploader("Upload ZIP File", type=["zip"])

# #     if uploaded_zip and st.button("🚀 Process ZIP"):
# #         with st.spinner("Processing ZIP files..."):
# #             with tempfile.TemporaryDirectory() as temp_dir:
# #                 with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
# #                     zip_ref.extractall(temp_dir)

# #                 result_df = process_folder(temp_dir)

# # # =========================
# # # MULTIPLE FILE UPLOAD
# # # =========================
# # elif upload_type == "Multiple Excel Upload":
# #     uploaded_files = st.file_uploader(
# #         "Upload Excel Files",
# #         type=["xlsx"],
# #         accept_multiple_files=True
# #     )

# #     if uploaded_files and st.button("🚀 Process Files"):
# #         with st.spinner("Processing Excel files..."):
# #             with tempfile.TemporaryDirectory() as temp_dir:
# #                 for file in uploaded_files:
# #                     with open(os.path.join(temp_dir, file.name), "wb") as f:
# #                         f.write(file.getbuffer())

# #                 result_df = process_folder(temp_dir)


# # # =========================
# # # OUTPUT SECTION
# # # =========================
# # if result_df is not None and not result_df.empty:
# #     st.success("Processing Completed Successfully ✅")

# #     st.dataframe(result_df.head(), use_container_width=True)

# #     # default file name logic
# #     final_name = file_name.strip() if file_name.strip() else "timesheet.xlsx"

# #     output = BytesIO()
# #     with pd.ExcelWriter(output, engine='openpyxl') as writer:
# #         result_df.to_excel(writer, index=False, sheet_name='Summary')

# #     st.download_button(
# #         "📥 Download Report",
# #         data=output.getvalue(),
# #         file_name=final_name,
# #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #     )

# # elif result_df is not None:
# #     st.warning("No data found after processing ❌")

# # st.markdown('</div>', unsafe_allow_html=True)


# ###################
# # ### Version_3.0.0.7
# import streamlit as st
# import pandas as pd
# import os
# import zipfile
# import tempfile
# import json
# from io import BytesIO

# # =========================
# # PAGE CONFIG
# # =========================
# st.set_page_config(
#     page_title="AQI Analytics Dashboard",
#     layout="wide",
#     page_icon="🌍"
# )

# # =========================
# # LOAD DEVICE MAP (JSON)
# # =========================
# DEVICE_FILE = "device_mapping.json"

# def load_devices():
#     if os.path.exists(DEVICE_FILE):
#         with open(DEVICE_FILE, "r") as f:
#             return json.load(f)
#     return {}

# def save_devices(data):
#     with open(DEVICE_FILE, "w") as f:
#         json.dump(data, f, indent=4)

# if "device_mapping" not in st.session_state:
#     st.session_state.device_mapping = load_devices()

# # =========================
# # SESSION STATE INIT
# # =========================
# if "result_df" not in st.session_state:
#     st.session_state.result_df = None

# if "show_devices" not in st.session_state:
#     st.session_state.show_devices = False

# # =========================
# # PREMIUM UI (CSS)
# # =========================
# st.markdown("""
#     <style>
#     .main { background-color: #0f172a; }

#     .title {
#         font-size: 38px;
#         font-weight: 700;
#         color: #ffffff;
#         text-align: center;
#     }

#     .subtitle {
#         text-align: center;
#         color: #94a3b8;
#     }

#     .card {
#         background: #111827;
#         padding: 20px;
#         border-radius: 15px;
#     }

#     .stButton>button {
#         background: linear-gradient(90deg, #06b6d4, #3b82f6);
#         color: white;
#         border-radius: 10px;
#     }

#     .stDownloadButton>button {
#         background: linear-gradient(90deg, #22c55e, #16a34a);
#         color: white;
#         border-radius: 10px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # =========================
# # HEADER
# # =========================
# st.markdown('<div class="title">🌍 AQI Time Slot Analytics Dashboard</div>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">Upload Excel or ZIP → Get Time Slot Summary Report</div>', unsafe_allow_html=True)

# # =========================
# # CONFIG
# # =========================
# time_ranges = {
#     '00:00-06:00': (0, 6),
#     '06:00-12:00': (6, 12),
#     '12:00-18:00': (12, 18),
#     '18:00-24:00': (18, 24),
# }

# direct_ugm3_cols = ['PM 10 (ug/m3)', 'PM 2.5 (ug/m3)', 'PM 1 (ug/m3)', 'Air Quality Index']
# env_cols = ['Temp (°C)', 'Humidity %']
# ppb_gases = ['NO2', 'SO2', 'CO', 'O3']

# # =========================
# # UTILS
# # =========================
# def smart_round(val):
#     try:
#         return round(float(val), 2)
#     except:
#         return None


# def process_folder(folder_path, device_map):
#     results = []

#     for file in os.listdir(folder_path):
#         if file.endswith(".xlsx"):
#             file_path = os.path.join(folder_path, file)
#             device_name = os.path.splitext(file)[0]
#             location = device_map.get(device_name, "Unknown Location")

#             try:
#                 df = pd.read_excel(file_path, skiprows=6, header=None)

#                 df.columns = (
#                     ['Time']
#                     + direct_ugm3_cols[:3]
#                     + [f'{gas} (ug/m3)' for gas in ppb_gases]
#                     + ['CO2 (ppm)']
#                     + env_cols
#                     + [direct_ugm3_cols[-1]]
#                 )

#                 df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
#                 df.dropna(subset=['Time'], inplace=True)

#                 if df.empty:
#                     continue

#                 df['Hour'] = df['Time'].dt.hour
#                 date_value = df['Time'].dt.date.iloc[0]

#                 final_columns = (
#                     direct_ugm3_cols[:3]
#                     + [f'{gas} (ug/m3)' for gas in ppb_gases]
#                     + ['CO2 (ppm)']
#                     + env_cols
#                     + [direct_ugm3_cols[-1]]
#                 )

#                 for slot, (start, end) in time_ranges.items():
#                     df_slot = df[(df['Hour'] >= start) & (df['Hour'] < end)]
#                     if df_slot.empty:
#                         continue

#                     row = {
#                         'Device': device_name,
#                         'Location': location,
#                         'Date': date_value,
#                         'Time Slot': slot,
#                     }

#                     for col in final_columns:
#                         row[f'{col} Min'] = smart_round(df_slot[col].min())
#                         row[f'{col} Max'] = smart_round(df_slot[col].max())

#                     results.append(row)

#             except Exception as e:
#                 st.warning(f"Error processing {file}: {e}")

#     return pd.DataFrame(results)

# # =========================
# # SIDEBAR
# # =========================
# with st.sidebar:
#     st.header("⚙️ Controls")

#     upload_type = st.radio("Upload Method", ["ZIP Upload", "Multiple Excel Upload"])

#     # ================= DEVICE ADD =================
#     st.markdown("### ➕ Add Device")
#     new_id = st.text_input("Device ID")
#     new_location = st.text_input("Device Location")

#     if st.button("Add Device"):
#         if new_id and new_location:
#             st.session_state.device_mapping[new_id] = new_location
#             save_devices(st.session_state.device_mapping)
#             st.success("Device Added Successfully ✅")
#         else:
#             st.warning("Please enter both fields")

#     if st.button("📋 Show Devices"):
#         st.session_state.show_devices = True

#     st.markdown("---")

#     # ================= FILE NAME =================
#     file_name = st.text_input("Output File Name (no extension)")

#     st.markdown("---")

#     # ================= CLEAR BUTTON =================
#     if st.button("🧹 Clear / Reset App"):
#         st.session_state.result_df = None
#         st.session_state.show_devices = False
#         st.rerun()

# # =========================
# # MAIN CONTAINER
# # =========================
# st.markdown('<div class="card">', unsafe_allow_html=True)

# # ================= SHOW DEVICES =================
# if st.session_state.show_devices:
#     st.subheader("📋 Registered Devices")
#     st.dataframe(pd.DataFrame(
#         list(st.session_state.device_mapping.items()),
#         columns=["Device ID", "Location"]
#     ), use_container_width=True)

# # ================= ZIP UPLOAD =================
# if upload_type == "ZIP Upload":
#     uploaded_zip = st.file_uploader("Upload ZIP File", type=["zip"])

#     if uploaded_zip and st.button("🚀 Process ZIP"):
#         with st.spinner("Processing..."):
#             with tempfile.TemporaryDirectory() as temp_dir:
#                 with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
#                     zip_ref.extractall(temp_dir)

#                 st.session_state.result_df = process_folder(
#                     temp_dir,
#                     st.session_state.device_mapping
#                 )

# # ================= MULTIPLE UPLOAD =================
# elif upload_type == "Multiple Excel Upload":
#     uploaded_files = st.file_uploader(
#         "Upload Excel Files",
#         type=["xlsx"],
#         accept_multiple_files=True
#     )

#     if uploaded_files and st.button("🚀 Process Files"):
#         with st.spinner("Processing..."):
#             with tempfile.TemporaryDirectory() as temp_dir:
#                 for file in uploaded_files:
#                     with open(os.path.join(temp_dir, file.name), "wb") as f:
#                         f.write(file.getbuffer())

#                 st.session_state.result_df = process_folder(
#                     temp_dir,
#                     st.session_state.device_mapping
#                 )

# # ================= OUTPUT =================
# df = st.session_state.result_df

# if df is not None and not df.empty:
#     st.success("Processing Completed ✅")
#     st.dataframe(df.head(), use_container_width=True)

#     # filename handling (force .xlsx)
#     final_name = file_name.strip() if file_name.strip() else "timesheet"
#     if not final_name.endswith(".xlsx"):
#         final_name += ".xlsx"

#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False, sheet_name='Summary')

#     st.download_button(
#         "📥 Download Report",
#         data=output.getvalue(),
#         file_name=final_name,
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

# elif df is not None:
#     st.warning("No data found ❌")

# st.markdown('</div>', unsafe_allow_html=True)


#######################
## Date: 24/5/2026
### Version: 3.0.1.1
import streamlit as st
import pandas as pd
import os
import zipfile
import tempfile
import json
import time
from io import BytesIO

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AQI Analytics Dashboard",
    page_icon="🌍",
    layout="wide"
)

# =========================================================
# FILES
# =========================================================
DEVICE_FILE = "device_mapping.json"

# =========================================================
# SESSION STATE
# =========================================================
DEFAULT_SESSION = {
    "result_df": None,
    "show_devices": False,
    "search_term": "",
    "processing_done": False
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# CUSTOM CSS
# =========================================================
def apply_custom_css():
    st.markdown("""
    <style>

    /* ================= MAIN APP ================= */
    .stApp {
        background: linear-gradient(135deg, #020617, #0f172a, #111827);
        color: white;
    }

    .main {
        background: transparent;
    }

    /* ================= HEADER ================= */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        color: white;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* ================= SIDEBAR ================= */
    section[data-testid="stSidebar"] {
        background: #07111f;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* ================= CARD ================= */
    .custom-card {
        background: rgba(17, 24, 39, 0.75);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    }

    /* ================= BUTTONS ================= */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.7rem;
        font-weight: 700;
        color: white;
        background: linear-gradient(90deg, #06b6d4, #3b82f6);
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(59,130,246,0.4);
    }

    /* ================= DOWNLOAD BUTTON ================= */
    .stDownloadButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.8rem;
        font-weight: 700;
        color: white;
        background: linear-gradient(90deg, #22c55e, #16a34a);
    }

    /* ================= INPUT ================= */
    .stTextInput > div > div > input {
        background-color: #111827;
        color: white;
        border-radius: 10px;
        border: 1px solid #334155;
    }

    .stTextArea textarea {
        background-color: #111827;
        color: white;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #111827;
    }

    /* ================= DATAFRAME ================= */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ================= METRIC CARD ================= */
    .metric-box {
        background: linear-gradient(135deg, #0f172a, #111827);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .metric-title {
        font-size: 14px;
        color: #94a3b8;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: white;
    }

    /* ================= FOOTER ================= */
    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 40px;
        margin-bottom: 20px;
    }

    </style>
    """, unsafe_allow_html=True)

# =========================================================
# LOAD DEVICES
# =========================================================
def load_devices():
    if os.path.exists(DEVICE_FILE):
        with open(DEVICE_FILE, "r") as f:
            return json.load(f)
    return {}

# =========================================================
# SAVE DEVICES
# =========================================================
def save_devices(device_map):
    with open(DEVICE_FILE, "w") as f:
        json.dump(device_map, f, indent=4)

# =========================================================
# INITIALIZE DEVICE MAP
# =========================================================
if "device_mapping" not in st.session_state:
    st.session_state.device_mapping = load_devices()

# =========================================================
# HEADER
# =========================================================
def show_header():
    st.markdown(
        '<div class="main-title">🌍 AQI Time Slot Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Professional AQI Processing • Device Management • Smart Analytics</div>',
        unsafe_allow_html=True
    )

# =========================================================
# CONFIG
# =========================================================
time_ranges = {
    '00:00-06:00': (0, 6),
    '06:00-12:00': (6, 12),
    '12:00-18:00': (12, 18),
    '18:00-24:00': (18, 24),
}

direct_ugm3_cols = [
    'PM 10 (ug/m3)',
    'PM 2.5 (ug/m3)',
    'PM 1 (ug/m3)',
    'Air Quality Index'
]

env_cols = ['Temp (°C)', 'Humidity %']

ppb_gases = ['NO2', 'SO2', 'CO', 'O3']

# =========================================================
# ROUND FUNCTION
# =========================================================
def smart_round(val):
    try:
        return round(float(val), 2)
    except:
        return None

# =========================================================
# PROCESS EXCEL FILE
# =========================================================
def process_excel_file(file_path, device_map):

    results = []

    device_name = os.path.splitext(os.path.basename(file_path))[0]

    location = device_map.get(device_name, "Unknown Location")

    try:
        df = pd.read_excel(file_path, skiprows=6, header=None)

        df.columns = (
            ['Time']
            + direct_ugm3_cols[:3]
            + [f'{gas} (ug/m3)' for gas in ppb_gases]
            + ['CO2 (ppm)']
            + env_cols
            + [direct_ugm3_cols[-1]]
        )

        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

        df.dropna(subset=['Time'], inplace=True)

        if df.empty:
            return []

        df['Hour'] = df['Time'].dt.hour

        date_value = df['Time'].dt.date.iloc[0]

        final_columns = (
            direct_ugm3_cols[:3]
            + [f'{gas} (ug/m3)' for gas in ppb_gases]
            + ['CO2 (ppm)']
            + env_cols
            + [direct_ugm3_cols[-1]]
        )

        for slot, (start, end) in time_ranges.items():

            df_slot = df[(df['Hour'] >= start) & (df['Hour'] < end)]

            if df_slot.empty:
                continue

            row = {
                'Device': device_name,
                'Location': location,
                'Date': date_value,
                'Time Slot': slot,
            }

            for col in final_columns:
                row[f'{col} Min'] = smart_round(df_slot[col].min())
                row[f'{col} Max'] = smart_round(df_slot[col].max())

            results.append(row)

    except Exception as e:
        st.warning(f"Error processing {device_name}: {e}")

    return results

# =========================================================
# PROCESS FOLDER
# =========================================================
def process_folder(folder_path, device_map):

    all_results = []

    files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]

    progress_bar = st.progress(0)

    status = st.empty()

    total_files = len(files)

    for idx, file in enumerate(files):

        status.markdown(f"""
        <div class="custom-card">
        <h4>⚡ Processing File</h4>
        <p>📄 {file}</p>
        <p>⏳ Reading AQI Data...</p>
        </div>
        """, unsafe_allow_html=True)

        file_path = os.path.join(folder_path, file)

        result = process_excel_file(file_path, device_map)

        all_results.extend(result)

        progress = int(((idx + 1) / total_files) * 100)

        progress_bar.progress(progress)

        time.sleep(0.3)

    status.markdown("""
    <div class="custom-card">
    <h3>✅ Processing Completed Successfully</h3>
    <p>Report generated successfully.</p>
    </div>
    """, unsafe_allow_html=True)

    return pd.DataFrame(all_results)

# =========================================================
# DEVICE MANAGER
# =========================================================
def add_device_ui():

    st.sidebar.markdown("## ➕ Add Device")

    new_device_id = st.sidebar.text_input(
        "Device ID",
        key="new_device_id"
    )

    new_location = st.sidebar.text_area(
        "Device Location",
        key="new_device_location"
    )

    if st.sidebar.button("Add Device"):

        if new_device_id and new_location:

            st.session_state.device_mapping[new_device_id] = new_location

            save_devices(st.session_state.device_mapping)

            st.sidebar.success("Device Added Successfully ✅")

        else:
            st.sidebar.warning("Please fill all fields")

# =========================================================
# SEARCH DEVICE
# =========================================================
def search_device_ui():

    st.sidebar.markdown("## 🔍 Search Device")

    search = st.sidebar.text_input(
        "Search by Device ID or Location",
        key="device_search"
    )

    st.session_state.search_term = search

# =========================================================
# SHOW DEVICES
# =========================================================
def show_devices_table():

    device_map = st.session_state.device_mapping

    df = pd.DataFrame(
        list(device_map.items()),
        columns=["Device ID", "Location"]
    )

    search = st.session_state.search_term.strip().lower()

    if search:
        df = df[
            df["Device ID"].str.lower().str.contains(search)
            |
            df["Location"].str.lower().str.contains(search)
        ]

    st.markdown("""
    <div class="custom-card">
    <h3>📋 Registered Devices</h3>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True)

# =========================================================
# EDIT DEVICE
# =========================================================
def edit_device_ui():

    st.sidebar.markdown("## ✏️ Edit Device")

    device_keys = list(st.session_state.device_mapping.keys())

    if device_keys:

        selected_device = st.sidebar.selectbox(
            "Select Device",
            device_keys,
            key="edit_device_select"
        )

        current_location = st.session_state.device_mapping[selected_device]

        edited_id = st.sidebar.text_input(
            "Edit Device ID",
            value=selected_device,
            key="edited_device_id"
        )

        edited_location = st.sidebar.text_area(
            "Edit Location",
            value=current_location,
            key="edited_location"
        )

        if st.sidebar.button("Update Device"):

            if edited_id and edited_location:

                del st.session_state.device_mapping[selected_device]

                st.session_state.device_mapping[edited_id] = edited_location

                save_devices(st.session_state.device_mapping)

                st.sidebar.success("Device Updated ✅")

                st.rerun()

# =========================================================
# DELETE DEVICE
# =========================================================
def delete_device_ui():

    st.sidebar.markdown("## 🗑 Delete Device")

    device_keys = list(st.session_state.device_mapping.keys())

    if device_keys:

        delete_device = st.sidebar.selectbox(
            "Select Device To Delete",
            device_keys,
            key="delete_device"
        )

        confirm = st.sidebar.checkbox(
            "Confirm Delete",
            key="confirm_delete"
        )

        if st.sidebar.button("Delete Device"):

            if confirm:

                del st.session_state.device_mapping[delete_device]

                save_devices(st.session_state.device_mapping)

                st.sidebar.success("Device Deleted Successfully")

                st.rerun()

            else:
                st.sidebar.warning("Please confirm deletion")

# =========================================================
# SIDEBAR CONTROLS
# =========================================================
def sidebar_controls():

    st.sidebar.markdown("# ⚙️ Control Panel")

    upload_type = st.sidebar.radio(
        "Upload Method",
        ["ZIP Upload", "Multiple Excel Upload"]
    )

    st.sidebar.markdown("---")

    add_device_ui()

    st.sidebar.markdown("---")

    search_device_ui()

    st.sidebar.markdown("---")

    edit_device_ui()

    st.sidebar.markdown("---")

    delete_device_ui()

    st.sidebar.markdown("---")

    output_name = st.sidebar.text_input(
        "Output File Name",
        placeholder="Enter filename only"
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("📋 Show Devices"):
        st.session_state.show_devices = True

    if st.sidebar.button("🧹 Clear / Reset App"):

        st.session_state.result_df = None
        st.session_state.show_devices = False
        st.session_state.processing_done = False

        st.rerun()

    return upload_type, output_name

# =========================================================
# DASHBOARD METRICS
# =========================================================
def show_metrics():

    total_devices = len(st.session_state.device_mapping)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Registered Devices</div>
            <div class="metric-value">{total_devices}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        total_reports = 0

        if st.session_state.result_df is not None:
            total_reports = len(st.session_state.result_df)

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">Processed Records</div>
            <div class="metric-value">{total_reports}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        status = "Ready"

        if st.session_state.processing_done:
            status = "Completed"

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-title">System Status</div>
            <div class="metric-value">{status}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# UPLOAD SECTION
# =========================================================
def upload_section(upload_type):

    st.markdown("""
    <div class="custom-card">
    <h3>📤 Upload AQI Files</h3>
    </div>
    """, unsafe_allow_html=True)

    if upload_type == "ZIP Upload":

        uploaded_zip = st.file_uploader(
            "Upload ZIP File",
            type=["zip"]
        )

        if uploaded_zip and st.button("🚀 Process ZIP Files"):

            with tempfile.TemporaryDirectory() as temp_dir:

                with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                result_df = process_folder(
                    temp_dir,
                    st.session_state.device_mapping
                )

                st.session_state.result_df = result_df
                st.session_state.processing_done = True

    else:

        uploaded_files = st.file_uploader(
            "Upload Multiple Excel Files",
            type=["xlsx"],
            accept_multiple_files=True
        )

        if uploaded_files and st.button("🚀 Process Excel Files"):

            with tempfile.TemporaryDirectory() as temp_dir:

                for file in uploaded_files:

                    save_path = os.path.join(temp_dir, file.name)

                    with open(save_path, "wb") as f:
                        f.write(file.getbuffer())

                result_df = process_folder(
                    temp_dir,
                    st.session_state.device_mapping
                )

                st.session_state.result_df = result_df
                st.session_state.processing_done = True

# =========================================================
# RESULT SECTION
# =========================================================
def show_result_section(output_name):

    df = st.session_state.result_df

    if df is not None and not df.empty:

        st.markdown("""
        <div class="custom-card">
        <h3>✅ AQI Summary Report</h3>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)

        final_name = output_name.strip() if output_name.strip() else "timesheet"

        if not final_name.endswith(".xlsx"):
            final_name += ".xlsx"

        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Summary')

        st.download_button(
            label="📥 Download Report",
            data=output.getvalue(),
            file_name=final_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    elif df is not None:
        st.warning("No valid data found after processing.")

# =========================================================
# FOOTER
# =========================================================
def show_footer():

    st.markdown("""
    <div class="footer">
    AQI Analytics Dashboard • Professional Environmental Data Processing System
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MAIN APP
# =========================================================
def main():

    apply_custom_css()

    show_header()

    show_metrics()

    upload_type, output_name = sidebar_controls()

    if st.session_state.show_devices:
        show_devices_table()

    upload_section(upload_type)

    show_result_section(output_name)

    show_footer()

# =========================================================
# RUN APP
# =========================================================
if __name__ == "__main__":
    main()
