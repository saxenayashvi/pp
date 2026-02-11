import streamlit as st
from pathlib import Path
import base64

# ---------------- PAGE CONFIG (must be first) ----------------
st.set_page_config(
    page_title="BI4BI - EY Landing Page",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------- LOAD CSS (by page) ----------------
def load_css(file_path: Path) -> None:
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

BASE = Path(__file__).parent

# ---------------- SESSION STATE: which page to show ----------------
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Navigate to Choose Tool when "Begin" link is clicked (query param)
# (kept for compatibility with your approach)
try:
    qp = st.query_params
    if qp.get("page") == "choose_tool" and st.session_state.get("page") != "choose_tool":
        st.session_state["page"] = "choose_tool"
        st.query_params.clear()
        st.rerun()
except Exception:
    pass

current_page = st.session_state["page"]

# Handle direct tool clicks via query params early so page rerenders correctly
try:
    qp_early = st.query_params
    tool_val = qp_early.get("tool")
    if tool_val:
        # Streamlit may return str or list depending on version
        clicked = tool_val[0] if isinstance(tool_val, list) else tool_val

        # clear query params
        st.query_params.clear()

        if clicked.lower() == "tableau":
            st.session_state["selected_tool"] = "Tableau"
            st.session_state["page"] = "configure"
            st.rerun()
        else:
            st.session_state["coming_soon_tool"] = clicked
            # stay on choose_tool page
            st.session_state["page"] = "choose_tool"
            st.rerun()
except Exception:
    pass

# Add session state for showing "coming soon" modal/toast
if "coming_soon_tool" not in st.session_state:
    st.session_state["coming_soon_tool"] = None

# Load the unified CSS for all pages
load_css(BASE / "merged-styles.css")

# ---------------- OPTIONAL: Your existing custom image CSS (can keep) ----------------
custom_image_css = """
<style>
.clickable-image {
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    border-radius: 8px;
    overflow: hidden;
    display: inline-block;
    width: 150px;
}

.clickable-image:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.clickable-image img {
    width: 100%;
    height: auto;
    display: block;
}

.image-caption {
    text-align: center;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: #666;
}
</style>
"""
st.markdown(custom_image_css, unsafe_allow_html=True)


# ---------------- RENDER: LANDING PAGE (BI4BI) ----------------
if current_page == "home":
    st.markdown('<div class="center-wrapper">', unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 2.5, 1])

    with col_center:
        st.markdown(
            """
            <div class="landing-card">
                <div class="title">BI4BI</div>
                <div class="desc">
                    BI4BI helps analyze existing BI reports, identify redundancies,
                    and provide recommendations to rationalize and modernize<br>
                    legacy BI environments using metadata-driven insights.
                </div>
                <div class="footer">©️ 2024 EYGM Limited. All Rights Reserved.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Begin →"):
            st.session_state["page"] = "choose_tool"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- RENDER: CHOOSE TOOL PAGE ----------------
elif current_page == "choose_tool":
    st.markdown("# Choose BI Tool")

    # ✅ PAGE-2 ONLY CSS: Make buttons yellow + center image & button
    st.markdown(
        """
        <style>
        /* Center images on this page */
        div[data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
            height: 90px !important;
        }

        /* Center buttons under images */
        div[data-testid="stButton"] {
            display: flex !important;
            justify-content: center !important;
            margin-top: 0.6rem !important;
        }

        /* Yellow button styling */
        div[data-testid="stButton"] > button {
            min-width: 140px !important;   /* close to image width */
            padding: 0.55rem 0.9rem !important;
            border-radius: 10px !important;
            background: #ffd54f !important;
            color: #1a1a1a !important;
            font-weight: 700 !important;
            border: none !important;
            # box-shadow: 0 6px 18px rgba(255,140,0,0.25) !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        }

        div[data-testid="stButton"] > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(255,140,0,0.32) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Tool metadata: name, logo file, adapter_key (None = coming soon)
    tools = [
        {"name": "Tableau", "logo": "tableau.jpg", "adapter_key": "tableau"},
        {"name": "Oracle OBIEE", "logo": "OracleOBIEE.jpg", "adapter_key": None},
        {"name": "Power BI", "logo": "powerbi.jpg", "adapter_key": None},
        {"name": "SAP BusinessObjects", "logo": "SAP-BO.jpg", "adapter_key": None},
        {"name": "Cognos", "logo": "cognos.jpg", "adapter_key": None},
        {"name": "SSRS", "logo": "SSRS.jpg", "adapter_key": None},
    ]

    assets_dir = BASE / "assets"

    # Show "coming soon" notification if a user clicked a future tool
    if st.session_state.get("coming_soon_tool"):
        st.info(
            f"✨ **{st.session_state['coming_soon_tool']}** is on our roadmap. "
            f"We're working hard to bring it to you soon!"
        )
        st.session_state["coming_soon_tool"] = None

    # Create a 3-column grid of logo cards
    cols = st.columns(3)
    for idx, tool in enumerate(tools):
        col = cols[idx % 3]
        with col:
            logo_path = assets_dir / tool["logo"]
            src = None

            if logo_path.exists():
                try:
                    data = logo_path.read_bytes()
                    b64 = base64.b64encode(data).decode("ascii")
                    suffix = logo_path.suffix.lower()
                    mime = "image/png" if suffix == ".png" else "image/jpeg"
                    src = f"data:{mime};base64,{b64}"
                except Exception:
                    src = None

            key_safe = tool["name"].replace(" ", "_")

            # Use a centered container (sub columns optional; CSS already centers)
            if src:
                st.image(src, width=140)
            else:
                st.write(f"Missing logo: {tool['logo']}")

            if tool["adapter_key"]:
                if st.button("Configure", key=f"btn_select_{key_safe}"):
                    st.session_state["selected_tool"] = tool["name"]
                    st.session_state["page"] = "configure"
                    st.rerun()
            else:
                if st.button("Configure", key=f"btn_coming_{key_safe}"):
                    st.session_state["coming_soon_tool"] = tool["name"]
                    st.rerun()

    # Back to home button
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    back_left, back_center, back_right = st.columns(3)
    with back_center:
        if st.button("← Back to Home"):
            st.session_state["page"] = "home"
            if "selected_tool" in st.session_state:
                del st.session_state["selected_tool"]
            st.rerun()


# ---------------- RENDER: CONFIGURE PAGE ----------------
elif current_page == "configure":
    from frontend.tab_configure_app import render_configure_page

    selected_tool = st.session_state.get("selected_tool", "Tableau")
    render_configure_page(selected_tool)


# ---------------- FALLBACK ----------------
else:
    st.session_state["page"] = "home"
    st.rerun()
