import os
import streamlit as st
import requests
import pandas as pd
from core.config import BACKEND_URL, CREDENTIALS_PATH

# NOTE: this module exposes a callable function `render_configure_page(selected_tool)`
# so the configuration UI can be embedded in other pages without creating a new Streamlit page.


def _load_saved_credentials():
    cred_path = os.path.abspath(CREDENTIALS_PATH)
    server_saved = None
    api_version_saved = '3.17'
    token_name_saved = None
    token_secret_saved = None
    site_name_saved = ''
    if os.path.exists(cred_path):
        try:
            df = pd.read_csv(cred_path)
            row = df.iloc[0]
            server_saved = row.get('server_saved')
            api_version_saved = row.get('api_version_saved') or api_version_saved
            token_name_saved = row.get('token_name_saved')
            token_secret_saved = row.get('token_secret_saved')
            site_name_saved = row.get('site_name_saved') or site_name_saved
        except Exception:
            pass
    return cred_path, server_saved, api_version_saved, token_name_saved, token_secret_saved, site_name_saved


def render_configure_page(selected_tool: str = 'Tableau'):
    """Render the configure UI for the given tool inside the current Streamlit page."""

    cred_path, server_saved, api_version_saved, token_name_saved, token_secret_saved, site_name_saved = _load_saved_credentials()

    # ---------- Page styling ----------
    st.markdown("""<style>
        html, body, .stApp {
            margin: 0 !important;
            padding: 0 !important;
        }
        /* Center the header */
        h2 {
            text-align: center !important;
        }
        
        /* Style all buttons */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s ease !important;
        }
        
        /* Yellow buttons (Test Connection, Upload, Save) */
        button[kind="primary"],
        .stButton > button[kind="primary"] {
            background-color: #FFD100 !important;
            color: #000 !important;
            border: none !important;
        }
        
        button[kind="primary"]:hover,
        .stButton > button[kind="primary"]:hover {
            background-color: #FFC000 !important;
            box-shadow: 0 2px 8px rgba(255, 209, 0, 0.3) !important;
        }
        
        /* Fixed back button — top left corner */
        .fixed-back-btn {
            position: fixed;
            top: 18px;
            left: 24px;
            z-index: 99999;
        }
        .fixed-back-btn a {
            display: inline-block;
            background:  #ffd54f;
            color: #222;
            font-weight: 600;
            font-size: 0.85rem;
            font-family: Arial, sans-serif;
            padding: 0.35rem 1rem;
            border: 1px solid #ccc;
            border-radius: 8px;
            text-decoration: none;
            transition: background 0.15s ease;
        }
        .fixed-back-btn a:hover {
           transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(255,140,0,0.32) !important;
        }
    </style>

    """, unsafe_allow_html=True)

    # ---------- Header ----------
    st.markdown(f"<h2 style='text-align:center; margin-bottom:0;'>Configure {selected_tool}</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:#555; margin-top:0.2rem; margin-bottom:1rem;'>"
        "Provide Tableau connection details (personal access token).</p>",
        unsafe_allow_html=True,
    )

    # ---------- Input Fields ----------
    server = st.text_input('Server', value=server_saved if server_saved else '')
    api_version = st.text_input('API version', value=api_version_saved)
    token_name = st.text_input('Token name', value=token_name_saved if token_name_saved else '')
    token_secret = st.text_input('Token secret', value=token_secret_saved if token_secret_saved else '', type='password')
    site_name = st.text_input('Site name', value=site_name_saved)

    # ---------- Test Connection button (centered) ----------
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        test_conn = st.button('Test Connection', use_container_width=True, type='primary', key='test_connection_btn')

    # ---------- Handle Test Connection ----------
    if test_conn:
        if server and token_name and token_secret:
            with st.spinner('Testing connection...'):
                try:
                    config = {
                        'tableau_prod': {
                            'server': server,
                            'api_version': api_version,
                            'personal_access_token_name': token_name,
                            'personal_access_token_secret': token_secret,
                            'site_name': site_name,
                        }
                    }
                    adapter_key = selected_tool.lower() if selected_tool else 'tableau'
                    r = requests.post(
                        f'{BACKEND_URL}/reports/test-connection',
                        json={'adapter': adapter_key, 'config': config},
                        timeout=30,
                    )
                    r.raise_for_status()
                    st.success('Connection successful!')
                except Exception as e:
                    st.error(f'Connection failed: {e}')
        else:
            st.warning('Please fill in Server, Token name, and Token secret to test the connection.')

    # ---------- Upload metadata file ----------
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='margin-bottom:8px; font-weight:600; color:#1a1a1a;'>Upload metadata file:</div>",
        unsafe_allow_html=True
    )

    # File uploader with Upload button
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload metadata file",
            type=["csv"],
            key="metadata_csv",
            label_visibility="collapsed"
        )
    with col2:
        upload_btn = st.button('Upload', use_container_width=True, type='primary', key='upload_file_btn')

    # Handle file upload
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"Uploaded {uploaded_file.name} — {len(df_upload)} rows")
            st.dataframe(df_upload.head())
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")

    # ---------- Save and Cancel buttons at bottom ----------
    st.markdown("<div style='margin-top:3rem;'></div>", unsafe_allow_html=True)
    
    # Create 3 columns with Save and Cancel buttons
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1.5])
    
    with col2:
        save_btn = st.button('Save', use_container_width=True, type='primary', key='save_config_btn')
    
    with col3:
        cancel_btn = st.button('Cancel', use_container_width=True, key='cancel_config_btn')

    # Handle Save button
    if save_btn:
        try:
            dfw = pd.DataFrame({
                'server_saved': [server],
                'api_version_saved': [api_version],
                'token_name_saved': [token_name],
                'token_secret_saved': [token_secret],
                'site_name_saved': [site_name],
                'site_url_saved': ['']
            })
            os.makedirs(os.path.dirname(cred_path), exist_ok=True)
            dfw.to_csv(cred_path, index=False)
            st.success('Credentials saved successfully!')
        except Exception as e:
            st.error(f'Failed saving credentials: {e}')

    # Handle Cancel button
    if cancel_btn:
        st.info('Configuration cancelled')

    # Add some bottom spacing
    st.markdown("<div style='margin-bottom:2rem;'></div>", unsafe_allow_html=True)


if __name__ == '__main__':
    # Allow running this file directly for quick debugging
    st.set_page_config(page_title='bi4bi - Configure (debug)', layout='centered')
    render_configure_page('Tableau')
