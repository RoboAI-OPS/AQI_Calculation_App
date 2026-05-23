
# # import streamlit as st
# # import pandas as pd
# # import os
# # import zipfile
# # import tempfile
# # from io import BytesIO

# # st.set_page_config(page_title="AQI Time Slot Summary Generator", layout="wide")

# # st.title("🌍 AQI Time Slot Summary Generator")
# # st.write("Upload a ZIP file or multiple Excel files (.xlsx). The app will process the data and generate Time_Slot_Summary.xlsx.")

# # time_ranges = {
# #     '00:00-06:00': (0, 6),
# #     '06:00-12:00': (6, 12),
# #     '12:00-18:00': (12, 18),
# #     '18:00-24:00': (18, 24),
# # }

# # direct_ugm3_cols = ['PM 10 (ug/m3)', 'PM 2.5 (ug/m3)', 'PM 1 (ug/m3)', 'Air Quality Index']
# # env_cols = ['Temp (°C)', 'Humidity %']
# # ppb_gases = ['NO2', 'SO2', 'CO', 'O3']

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

# # def smart_round(val):
# #     try:
# #         return round(float(val), 2)
# #     except:
# #         return None

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

# #                         if col_min is not None and col_max is not None and col_min > col_max:
# #                             col_min, col_max = col_max, col_min

# #                         row[f'{col} Min'] = col_min
# #                         row[f'{col} Max'] = col_max

# #                     results.append(row)

# #             except Exception as e:
# #                 st.warning(f"Error processing {file}: {e}")

# #     result_df = pd.DataFrame(results)

# #     for col in result_df.columns:
# #         if 'Min' in col or 'Max' in col:
# #             result_df[col] = pd.to_numeric(result_df[col], errors='coerce')

# #     return result_df


# # upload_type = st.radio("Choose Upload Method", ["ZIP Upload", "Multiple Excel Upload"])

# # if upload_type == "ZIP Upload":
# #     uploaded_zip = st.file_uploader("Upload ZIP file", type=["zip"])

# #     if uploaded_zip and st.button("Process ZIP"):
# #         with tempfile.TemporaryDirectory() as temp_dir:
# #             with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
# #                 zip_ref.extractall(temp_dir)

# #             result_df = process_folder(temp_dir)

# #             if not result_df.empty:
# #                 output = BytesIO()
# #                 with pd.ExcelWriter(output, engine='openpyxl') as writer:
# #                     result_df.to_excel(writer, index=False, sheet_name='Summary')

# #                 st.success("Processing Complete!")
# #                 st.dataframe(result_df.head())

# #                 st.download_button(
# #                     "📥 Download Time_Slot_Summary.xlsx",
# #                     output.getvalue(),
# #                     file_name="Time_Slot_Summary.xlsx",
# #                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #                 )

# # elif upload_type == "Multiple Excel Upload":
# #     uploaded_files = st.file_uploader(
# #         "Upload Excel Files",
# #         type=["xlsx"],
# #         accept_multiple_files=True
# #     )

# #     if uploaded_files and st.button("Process Files"):
# #         with tempfile.TemporaryDirectory() as temp_dir:
# #             for file in uploaded_files:
# #                 with open(os.path.join(temp_dir, file.name), "wb") as f:
# #                     f.write(file.getbuffer())

# #             result_df = process_folder(temp_dir)

# #             if not result_df.empty:
# #                 output = BytesIO()
# #                 with pd.ExcelWriter(output, engine='openpyxl') as writer:
# #                     result_df.to_excel(writer, index=False, sheet_name='Summary')

# #                 st.success("Processing Complete!")
# #                 st.dataframe(result_df.head())

# #                 st.download_button(
# #                     "📥 Download Time_Slot_Summary.xlsx",
# #                     output.getvalue(),
# #                     file_name="Time_Slot_Summary.xlsx",
# #                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #                 )

# ###############################

# import streamlit as st
# import pandas as pd
# import os
# import zipfile
# import tempfile
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
# # PREMIUM UI (CSS STYLE)
# # =========================
# st.markdown("""
#     <style>
#     .main {
#         background-color: #0f172a;
#     }

#     .title {
#         font-size: 38px;
#         font-weight: 700;
#         color: #ffffff;
#         text-align: center;
#         margin-bottom: 10px;
#     }

#     .subtitle {
#         text-align: center;
#         color: #94a3b8;
#         font-size: 16px;
#         margin-bottom: 30px;
#     }

#     .card {
#         background: #111827;
#         padding: 20px;
#         border-radius: 15px;
#         box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
#     }

#     .stButton>button {
#         background: linear-gradient(90deg, #06b6d4, #3b82f6);
#         color: white;
#         border-radius: 10px;
#         padding: 10px 20px;
#         border: none;
#         font-weight: bold;
#     }

#     .stDownloadButton>button {
#         background: linear-gradient(90deg, #22c55e, #16a34a);
#         color: white;
#         border-radius: 10px;
#         padding: 10px 20px;
#         border: none;
#         font-weight: bold;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # =========================
# # HEADER
# # =========================
# st.markdown('<div class="title">🌍 AQI Time Slot Analytics Dashboard</div>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">Upload Excel or ZIP files → Get Time Slot Summary Report instantly</div>', unsafe_allow_html=True)

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
# # DEVICE MAP
# # =========================
# address_mapping = {
#     "MCT2408041": "Village Panchayat Uguem- Government Office",
#     "MCT2408046": "Village Panchayat Pissurlem",
#     "MCT2408056": "Village Panchayat Mayam",
#     "MCT2408051": "Vasu Hotel, Front Of Tagore School, Hathkhamba- Goa rd, Kotambi",
#     "MCT2408022": "Tushar Weighbridge, Near by Vagus Junction",
#     "MCT2408043": "Tilamol Junction, Quepem-Curchorem Road",
#     "MCT2408044": "Somnath School, Codli",
#     "MCT2408023": "Siya Surlekar House, Near by Old Surla Panchayat Office",
#     "MCT2408050": "Siddhesh Kotkar, Piligaon, Nearby Vedanta Jetty",
#     "MCT2408038": "Ramnath B Naik House, Ambaulim, Gudumol, Quepem, (Near By MDR-46)",
#     "MCT2408021": "Ramdas House, Velguem, Sanquelim, Velguem-Surla-sgao rd, (Near State Bank Of India)",
#     "MCT2408042": "Quepem Circle (Nearby Govt offices)",
#     "MCT2408034": "Mr. Kusta Gaounkar, Nalini Bar & Restaurant, Codli",
#     "MCT2408039": "Mr. Ashis Naik House, Rivona Gate, Pandovwado,Sangum, Near by Temple",
#     "MCT2408029": "Mr. Aniket Dessai House, Shigaon",
#     "MCT2408031": "Mr Dilip House, Near Sai Tample, Ambeudak (Shradha Ispat), Kaley Mineral Rd",
#     "MCT2408030": "Kurpem Village (Nearby MDR-47, Ambaulim-Cavorim-Pirla at Anil Fals dessai Home)",
#     "MCT2408052": "Jaydev B Natekar House, Wedalade, usgao",
#     "MCT2408040": "Govt Primary School Near Fanaswadi Junction, Naveli",
#     "MCT2408035": "Govt Polytechnic College, Curchorem, Cacora",
#     "MCT2408028": "Govt High School, Zambaulim",
#     "MCT2408024": "Govt High School, Colamb",
#     "MCT2408026": "Diogo Fernandes House, Uguem Junction",
#     "MCT2408037": "Deputy Collector Office, Dharbandora",
#     "MCT2408036": "Caverem Pirla Aganwadi",
#     "MCT2408045": "Baliram Govind Malik House, mapusa-Bicholim Rd, Sirsai",
#     "MCT2408049": "At Mr. Sagun S. Gawas House, Ambegal, pale",
#     "MCT2408020": "Ajoba Devesthan Honda, Sanquelim Velguem, Surla, Usgaon Road, Near By Ajoba Nagar",
#     "MCT2408032": "IHM Porvorim",
#     "MCT2408027": "Mr. Caitano Dcosta, Tollem Bus Stand, Sanvordem, Nearby Capxem Jetty",
#     "MCT2408033": "Mr. Aakash Naik Tishem, Borim, Nearby Old Bridge",
#     "MCT2408053": "Ravindra Bhagwan, Curchorem Cricel",
#     "MCT2408057": "Govt Primary School, Sanvordem",
#     "MCT2408055": "Ravindra House, Haldanwadi Mayem, Nearby Vittal Temple (Chokhla Mine)"
# }

# # =========================
# # UTIL FUNCTION
# # =========================
# def smart_round(val):
#     try:
#         return round(float(val), 2)
#     except:
#         return None


# # =========================
# # CORE PROCESSING
# # =========================
# def process_folder(folder_path):
#     results = []

#     for file in os.listdir(folder_path):
#         if file.endswith(".xlsx"):
#             file_path = os.path.join(folder_path, file)
#             device_name = os.path.splitext(file)[0]
#             location = address_mapping.get(device_name, "Unknown Location")

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
#                         col_min = smart_round(df_slot[col].min())
#                         col_max = smart_round(df_slot[col].max())

#                         row[f'{col} Min'] = col_min
#                         row[f'{col} Max'] = col_max

#                     results.append(row)

#             except Exception as e:
#                 st.warning(f"Error processing {file}: {e}")

#     return pd.DataFrame(results)


# # =========================
# # SIDEBAR CONTROLS
# # =========================
# with st.sidebar:
#     st.header("⚙️ Controls")

#     upload_type = st.radio("Upload Method", ["ZIP Upload", "Multiple Excel Upload"])

#     file_name = st.text_input(
#         "Output File Name (optional)",
#         placeholder="Enter file name (e.g. my_report.xlsx)"
#     )

#     st.markdown("---")
#     st.info("If empty → default: timesheet.xlsx")


# # =========================
# # MAIN UI CONTAINER
# # =========================
# st.markdown('<div class="card">', unsafe_allow_html=True)

# result_df = None

# # =========================
# # ZIP UPLOAD
# # =========================
# if upload_type == "ZIP Upload":
#     uploaded_zip = st.file_uploader("Upload ZIP File", type=["zip"])

#     if uploaded_zip and st.button("🚀 Process ZIP"):
#         with st.spinner("Processing ZIP files..."):
#             with tempfile.TemporaryDirectory() as temp_dir:
#                 with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
#                     zip_ref.extractall(temp_dir)

#                 result_df = process_folder(temp_dir)

# # =========================
# # MULTIPLE FILE UPLOAD
# # =========================
# elif upload_type == "Multiple Excel Upload":
#     uploaded_files = st.file_uploader(
#         "Upload Excel Files",
#         type=["xlsx"],
#         accept_multiple_files=True
#     )

#     if uploaded_files and st.button("🚀 Process Files"):
#         with st.spinner("Processing Excel files..."):
#             with tempfile.TemporaryDirectory() as temp_dir:
#                 for file in uploaded_files:
#                     with open(os.path.join(temp_dir, file.name), "wb") as f:
#                         f.write(file.getbuffer())

#                 result_df = process_folder(temp_dir)


# # =========================
# # OUTPUT SECTION
# # =========================
# if result_df is not None and not result_df.empty:
#     st.success("Processing Completed Successfully ✅")

#     st.dataframe(result_df.head(), use_container_width=True)

#     # default file name logic
#     final_name = file_name.strip() if file_name.strip() else "timesheet.xlsx"

#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         result_df.to_excel(writer, index=False, sheet_name='Summary')

#     st.download_button(
#         "📥 Download Report",
#         data=output.getvalue(),
#         file_name=final_name,
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

# elif result_df is not None:
#     st.warning("No data found after processing ❌")

# st.markdown('</div>', unsafe_allow_html=True)


###################
### Version_3.0.0.4
import streamlit as st
import pandas as pd
import os
import zipfile
import tempfile
import json
from io import BytesIO

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AQI Analytics Dashboard",
    layout="wide",
    page_icon="🌍"
)

# =========================
# UI STYLE
# =========================
st.markdown("""
<style>
.title {
    font-size: 36px;
    font-weight: 800;
    text-align: center;
    color: white;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 15px;
}

.card {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌍 AQI Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload → Process → Download Report</div>', unsafe_allow_html=True)

# =========================
# LOAD DEVICE MAP
# =========================
MAPPING_FILE = "device_mapping.json"

def load_mapping():
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r") as f:
            return json.load(f)
    return {}

def save_mapping(mapping):
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=4)

address_mapping = load_mapping()

# =========================
# CONSTANTS
# =========================
time_ranges = {
    '00-06': (0, 6),
    '06-12': (6, 12),
    '12-18': (12, 18),
    '18-24': (18, 24),
}

direct_cols = ['PM 10 (ug/m3)', 'PM 2.5 (ug/m3)', 'PM 1 (ug/m3)', 'Air Quality Index']
env_cols = ['Temp (°C)', 'Humidity %']
gas_cols = ['NO2', 'SO2', 'CO', 'O3']

# =========================
# UTIL
# =========================
def smart(val):
    try:
        return round(float(val), 2)
    except:
        return None

# =========================
# PROCESS FUNCTION
# =========================
def process_folder(path):
    results = []

    for file in os.listdir(path):
        if file.endswith(".xlsx"):
            file_path = os.path.join(path, file)
            device = os.path.splitext(file)[0]
            location = address_mapping.get(device, "Unknown Location")

            try:
                df = pd.read_excel(file_path, skiprows=6, header=None)

                df.columns = (
                    ['Time']
                    + direct_cols[:3]
                    + [f"{g} (ug/m3)" for g in gas_cols]
                    + ['CO2 (ppm)']
                    + env_cols
                    + [direct_cols[-1]]
                )

                df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
                df = df.dropna(subset=['Time'])

                df['Hour'] = df['Time'].dt.hour

                final_cols = (
                    direct_cols[:3]
                    + [f"{g} (ug/m3)" for g in gas_cols]
                    + ['CO2 (ppm)']
                    + env_cols
                    + [direct_cols[-1]]
                )

                for slot, (s, e) in time_ranges.items():
                    df_s = df[(df['Hour'] >= s) & (df['Hour'] < e)]

                    if df_s.empty:
                        continue

                    row = {
                        "Device": device,
                        "Location": location,
                        "Time Slot": slot
                    }

                    for col in final_cols:
                        row[f"{col} Avg"] = smart(df_s[col].mean())

                    results.append(row)

            except:
                continue

    return pd.DataFrame(results)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("⚙️ Controls")

    new_id = st.text_input("Device ID")
    new_name = st.text_input("Device Name")

    if st.button("➕ Add Device"):
        if new_id and new_name:
            address_mapping[new_id] = new_name
            save_mapping(address_mapping)
            st.success("Device Added!")

    st.markdown("---")

    upload_type = st.radio("Upload Type", ["ZIP", "Excel Files"])

    file_name = st.text_input("Output file name (optional)")

# =========================
# MAIN UI
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

result_df = None
download_ready = False
output_buffer = None

# =========================
# PROCESS BUTTON LOGIC
# =========================
if upload_type == "ZIP":
    zip_file = st.file_uploader("Upload ZIP File", type=["zip"])

    if zip_file:
        if st.button("🚀 Process"):
            with tempfile.TemporaryDirectory() as tmp:
                with zipfile.ZipFile(zip_file, 'r') as z:
                    z.extractall(tmp)

                result_df = process_folder(tmp)

                if not result_df.empty:
                    download_ready = True

else:
    files = st.file_uploader("Upload Excel Files", type=["xlsx"], accept_multiple_files=True)

    if files:
        if st.button("🚀 Process"):
            with tempfile.TemporaryDirectory() as tmp:
                for f in files:
                    with open(os.path.join(tmp, f.name), "wb") as w:
                        w.write(f.getbuffer())

                result_df = process_folder(tmp)

                if not result_df.empty:
                    download_ready = True

# =========================
# OUTPUT + DOWNLOAD (ONLY AFTER PROCESS)
# =========================
if download_ready and result_df is not None:

    st.success("Processing Completed ✅")

    st.dataframe(result_df, use_container_width=True)

    final_name = file_name.strip()

    if not final_name:
        final_name = "timesheet.xlsx"
    elif not final_name.endswith(".xlsx"):
        final_name += ".xlsx"

    output_buffer = BytesIO()
    with pd.ExcelWriter(output_buffer, engine="openpyxl") as writer:
        result_df.to_excel(writer, index=False)

    st.download_button(
        "📥 Download Report",
        output_buffer.getvalue(),
        file_name=final_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown('</div>', unsafe_allow_html=True)
