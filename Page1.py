# PAGE 2: CHOOSE TOOL
# ============================================================
elif current_page == "choose_tool":
    if USE_INTERNAL_BG_AND_LOGO:
        inject_background()
        inject_logo()

    st.markdown(
        f"""
        <style>
        /* Kill scroll — fixed background */
        html, body {{
                margin: 0 !important;
                padding: 0 !important;
                height: 100vh !important;
                max-height: 100vh !important;
                overflow: hidden !important;
        }}
        .stApp,
        [data-testid="stAppViewContainer"],
        section.main,
        .main .block-container,
        .block-container {{
                overflow: hidden !important;
                max-height: 100vh !important;
        }}
        .block-container {{
                padding-top: 0.3rem !important;
                padding-bottom: 0 !important;
                margin-top : 63px;
        }}

        div[data-testid="stImage"] {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            height: 110px !important;
        }}

        /* Hide streamlit chrome */
        header, footer {{ visibility: hidden !important; height: 0 !important; }}
        [data-testid="stToolbar"] {{ display: none !important; }}
        [data-testid="stHeader"] {{ display: none !important; }}
        [data-testid="stDecoration"] {{ display: none !important; }}

        /* Center configure buttons */
        div[data-testid="stButton"] {{
            display: flex !important;
            justify-content: center !important;
        }}
        div[data-testid="stButton"] > button {{
            min-width: 140px !important;
            border-radius: 10px !important;
            background: #ffd54f !important;
            color: #1a1a1a !important;
            font-weight: 700 !important;
            border: none !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }}
        div[data-testid="stButton"] > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(255,140,0,0.32) !important;
        }}

        /* Center the tool grid columns content */
        [data-testid="stVerticalBlock"] {{
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # (Back button fully removed here)

    tools = [
        {"name": "MicroStrategy", "logo": "strategy.png", "adapter_key": None},
        {"name": "Oracle OBIEE", "logo": "oracleOBIEE.png", "adapter_key": None},
        {"name": "Cognos", "logo": "cognos.png", "adapter_key": None},
        {"name": "Power BI", "logo": "powerbi.png", "adapter_key": None},
        {"name": "SAP BusinessObjects", "logo": "sap-bo.png", "adapter_key": None},
        {"name": "SSRS", "logo": "SSRS.png", "adapter_key": None},
        {"name": "Tableau", "logo": "tableau.png", "adapter_key": "tableau"},
    ]

    assets_dir = BASE / "assets"

    if st.session_state.get("coming_soon_tool"):
        st.info(
            f"✨ **{st.session_state['coming_soon_tool']}** is on our roadmap. "
            f"We're working hard to bring it to you soon!"
        )
        st.session_state["coming_soon_tool"] = None

    st.markdown(
        "<h1 style='margin-top: -0.5rem; padding-top: 0; text-align: center; font-size: 1.8rem;'>Select a BI Environment</h1>",
        unsafe_allow_html=True
    )

    cols = st.columns(3)

    for idx, tool in enumerate(tools):
        col = cols[idx % 3]
        if "tableau" in tool["name"].lower():
            col = cols[1]  # Center Tableau

        with col:
            logo_path = assets_dir / tool["logo"]
            if logo_path.exists():
                st.image(str(logo_path), width=140)
            else:
                st.write(f"Missing logo: {tool['logo']}")

            key_safe = tool["name"].replace(" ", "_").replace("/", "_")

            if tool["adapter_key"]:
                if st.button("Configure", key=f"btn_select_{key_safe}"):
                    st.session_state["selected_tool"] = tool["name"]
                    st.session_state["page"] = "configure"
                    st.rerun()
            else:
                if st.button("Configure", key=f"btn_coming_{key_safe}"):
                    st.session_state["coming_soon_tool"] = tool["name"]
                    st.rerun()
