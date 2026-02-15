import streamlit as st
import base64
from pathlib import Path
from datetime import datetime


# ---------------- PAGE CONFIG (must be first) ----------------
st.set_page_config(
    page_title="BI4BI - EY Landing Page",
    layout="centered",
    initial_sidebar_state="collapsed",
)

BASE = Path(__file__).parent

USE_INTERNAL_BG_AND_LOGO = True  # internal pages background/logo


# ---------------- UTILS ----------------
def get_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def load_css(file_path: Path) -> None:
    if file_path.exists():
        st.markdown(f"<style>{file_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def _get_query_params():
    """Support both new and old Streamlit APIs."""
    try:
        qp = dict(st.query_params)
        return {k: (v[0] if isinstance(v, list) else v) for k, v in qp.items()}
    except Exception:
        qp = st.experimental_get_query_params()
        return {k: (v[0] if isinstance(v, list) else v) for k, v in qp.items()}


def _clear_query_params():
    try:
        st.query_params.clear()
    except Exception:
        st.experimental_set_query_params()


# ---------------- INTERNAL PAGES: BACKGROUND / LOGO ----------------
def inject_background():
    import mimetypes
    candidates = [BASE / "background.png", BASE.parent / "background.png"]
    bg_path = next((p for p in candidates if p.exists()), None)
    if not bg_path:
        return

    mime, _ = mimetypes.guess_type(str(bg_path))
    mime = mime or "image/png"
    b64 = get_base64(bg_path)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:{mime};base64,{b64}") no-repeat fixed center center !important;
            background-size: cover !important;
        }}
        section.main, .main .block-container, .block-container {{
            background: transparent !important;
            box-shadow: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_logo():
    candidates = [BASE / "ey_logo.png", BASE.parent / "ey_logo.png"]
    logo_path = next((p for p in candidates if p.exists()), None)
    if not logo_path:
        return
    b64 = get_base64(logo_path)

    st.markdown(
        f"""
        <style>
        .ey-logo-fixed {{
            position: fixed;
            top: 16px;
            right: 16px;
            width: 140px;
            height: auto;
            z-index: 100000;
            pointer-events: none;
            filter: drop-shadow(0 0 6px rgba(0,0,0,0.08));
        }}
        </style>
        <img class="ey-logo-fixed" src="data:image/png;base64,{b64}" alt="EY Logo" />
        """,
        unsafe_allow_html=True,
    )


# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "coming_soon_tool" not in st.session_state:
    st.session_state["coming_soon_tool"] = None


# ---------------- QUERY PARAM ROUTING (optional) ----------------
qp = _get_query_params()
qp_page = qp.get("page")
if qp_page and st.session_state.get("page") != qp_page:
    st.session_state["page"] = qp_page
    _clear_query_params()
    st.rerun()

current_page = st.session_state["page"]

# ---------------- OPTIONAL: global css ----------------
# load_css(BASE / "merged-styles.css")


# ============================================================
# PAGE 1: HOME (Landing) — BI4BI title + description + Begin
# ============================================================
if current_page == "home":
    # Assets
    bg_candidates = [BASE / "background.png", BASE.parent / "background.png"]
    logo_candidates = [BASE / "ey_logo.png", BASE.parent / "ey_logo.png"]
    bg_path = next((p for p in bg_candidates if p.exists()), None)
    logo_path = next((p for p in logo_candidates if p.exists()), None)

    if not bg_path or not logo_path:
        st.error("Missing background.png or ey_logo.png.")
    else:
        bg_b64 = get_base64(bg_path)
        logo_b64 = get_base64(logo_path)

        # ---------- HEADER + PAGE STYLE ----------
        st.markdown(
            f"""
            <style>
              /* Kill ALL scrollbars and overflow */
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
                padding-top: 1rem !important;
                padding-bottom: 0 !important;
              }}

              /* Hide streamlit chrome */
              header, footer {{ visibility: hidden !important; height: 0 !important; }}
              [data-testid="stToolbar"] {{ display: none !important; }}
              [data-testid="stHeader"] {{ display: none !important; }}
              [data-testid="stDecoration"] {{ display: none !important; }}

              .stApp {{
                background: url("data:image/png;base64,{bg_b64}") no-repeat center center !important;
                background-size: cover !important;
              }}

              section.main, .main .block-container, .block-container {{
                background: transparent !important;
                box-shadow: none !important;
              }}

              /* EY Logo — fixed TOP-right */
              .landing-logo {{
                    position: fixed;
                    top: 28px;
                    right: 40px;
                    z-index: 9999;
              }}
              .landing-logo img {{
                    width: 120px;
                    height: auto;
              }}

              /* Landing content wrapper — vertically centered, no overflow */
              .landing-content {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 68vh;
                    gap : 65px;
                    padding: 0 20px;
              }}

              /* Title */
              .landing-title {{
                    font-size: 48px;
                    font-weight: 800;
                    color: #1a1a1a;
                    font-family: 'EYInterstate', Arial, sans-serif;
                    margin-bottom: 24px;
                    letter-spacing: 1px;
              }}

              /* Description paragraph */
              .landing-desc {{
                    font-size: 20px;
                    color: #333;
                    font-family: 'EYInterstate', Arial, sans-serif;
                    line-height: 1.65;
                    text-align: justify;
                    max-width: 560px;
                    margin-bottom: 24px;
              }}

              /* Footer */
              .landing-footer {{
                    font-size: 11px;
                    color: #888;
                    text-align: center;
                    margin-top: 6px;
                    padding-bottom: 0;
              }}

              /* Begin button */
              .stButton > button {{
                    background-color: #FFD100 !important;
                    color: #000 !important;
                    height: 46px !important;
                    font-size: 20px !important;
                    font-weight: 700 !important;
                    border: none !important;
                    border-radius: 6px !important;
              }}
              .stButton > button:hover {{
                    background-color: #FFC000 !important;
              }}

            </style>

            <!-- FIXED EY LOGO (top-right) -->
            <div class="landing-logo">
                <img src="data:image/png;base64,{logo_b64}" />
            </div>

            """,
            unsafe_allow_html=True,
        )

        # ---------- CONTENT AREA ----------
        left, mid, right = st.columns([0.3, 3.4, 0.3])
        with mid:

            st.markdown(
                """
                <div class="landing-content">
                    <div class="landing-title">BI4BI</div>
                    <div class="landing-desc">
                        The <strong>BI4BI</strong> &ndash; the rationalization tool that is designed to
                        provide EY's clients a suite of BI rationalization solution. The tool can provide
                        end-to-end BI metadata with an organized view and suggest the possible
                        rationalization based on each client's BI environment to reduce manual
                        analysis of the BI environment for the BI modernization .
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Begin Button
            if st.button("Begin", use_container_width=True, key="landing_begin"):
                st.session_state["page"] = "choose_tool"
                st.rerun()

            # Footer
            st.markdown(
                f"""
                <div class="landing-footer">
                    © {datetime.now().year} EYGM Limited. All Rights Reserved.
                </div>
                """,
                unsafe_allow_html=True,
            )

# ============================================================
# PAGE 2: CHOOSE TOOL
# ============================================================
elif current_page == "choose_tool":
    if USE_INTERNAL_BG_AND_LOGO:
        inject_background()
        inject_logo()

    st.markdown(
        """
        <style>
        html, body {
            margin: 0 !important;
            padding: 10px !important;
            height: 100vh !important;
            overflow: hidden !important;
        }

        .block-container {
            padding-top: 0.8rem !important;
            margin-top: 20px !important;
        }

        header, footer { visibility: hidden !important; height: 0 !important; }
        [data-testid="stToolbar"] { display: none !important; }
        [data-testid="stHeader"] { display: none !important; }

        div[data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
            margin-bottom: 10px !important;
        }

        div[data-testid="stButton"] {
            display: flex !important;
            justify-content: center !important;
        }

        div[data-testid="stButton"] > button {
            min-width: 140px !important;
            border-radius: 10px !important;
            background: #ffd54f !important;
            color: #1a1a1a !important;
            font-weight: 700 !important;
            border: none !important;
        }

        .fixed-back-btn {
            position: fixed;
            top: 28px;
            left: 20px;
            z-index: 9999;
        }

        .fixed-back-btn a {
            display: inline-block;
            background: white;
            color: #1a1a1a !important;
            font-weight: 700 !important;
            font-size: 2.0rem !important;
            padding: 0.4rem 1.2rem !important;
            border-radius: 10px !important;
            text-decoration: none !important;
            min-width: 140px !important;
            text-align: center !important;
        }

        /* =========================================================
           >>> ADDED SPACING FOR GRID / BUTTONS <<<
           - Increase gap between columns (both rows)
           - Add space between each logo and its Configure button
           ========================================================= */
        /* Column gap between items */
        [data-testid="stColumns"] {
            gap: 24px !important;              /* tweak: 16–32px */
        }

        /* Space between the logo and the Configure button */
        div[data-testid="stButton"] {
            margin-top: 10px !important;       /* tweak: 6–16px */
        }

        /* Optional: add a little space under each image as well */
        div[data-testid="stImage"] {
            margin-bottom: 14px !important;    /* was 10px */
        }

        /* Spacer element before second row only */
        .row-spacer {
            height: 28px;                      /* tweak: 20–40px */
            width: 100%;
        }
        /* ========================================================= */
        </style>

        <div class="fixed-back-btn">
            <a href="?page=home" target="_self">BI4BI</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align:center; margin-bottom:40px;'>Select a BI Environment</h2>",
        unsafe_allow_html=True
    )

    tools = [
        {"name": "Tableau", "logo": "tableau.png", "adapter_key": "tableau"},
        {"name": "Cognos", "logo": "cognos.png", "adapter_key": None},
        {"name": "Power BI", "logo": "powerbi.png", "adapter_key": None},
        {"name": "SQL Server", "logo": "SSRS.png", "adapter_key": None},
        {"name": "Oracle OBIEE", "logo": "oracleOBIEE.png", "adapter_key": None},
        {"name": "SAP BusinessObjects", "logo": "sap-bo.png", "adapter_key": None},
        {"name": "MicroStrategy", "logo": "strategy.png", "adapter_key": None},
    ]

    assets_dir = BASE / "assets"

    # ---------- FIRST ROW (4 tools) ----------
    row1 = st.columns(4)

    for i in range(4):
        tool = tools[i]
        with row1[i]:
            logo_path = assets_dir / tool["logo"]
            if logo_path.exists():
                st.image(str(logo_path), width=120)

            key_safe = tool["name"].replace(" ", "_")

            if tool["adapter_key"]:
                if st.button("Configure", key=f"btn_{key_safe}"):
                    st.session_state["selected_tool"] = tool["name"]
                    st.session_state["page"] = "configure"
                    st.rerun()
            else:
                if st.button("Configure", key=f"btn_{key_safe}_coming"):
                    st.session_state["coming_soon_tool"] = tool["name"]
                    st.rerun()

    # >>> EXTRA VERTICAL SPACE BETWEEN ROWS <<<
    st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)

    # ---------- SECOND ROW (3 tools centered) ----------
    row2 = st.columns([1, 1, 1, 1, 1])

    for idx, tool in enumerate(tools[4:]):
        with row2[idx + 1]:
            logo_path = assets_dir / tool["logo"]
            if logo_path.exists():
                st.image(str(logo_path), width=120)

            key_safe = tool["name"].replace(" ", "_")

            if tool["adapter_key"]:
                if st.button("Configure", key=f"btn_{key_safe}2"):
                    st.session_state["selected_tool"] = tool["name"]
                    st.session_state["page"] = "configure"
                    st.rerun()
            else:
                if st.button("Configure", key=f"btn_{key_safe}_coming2"):
                    st.session_state["coming_soon_tool"] = tool["name"]
                    st.rerun()
# ============================================================
# ============================================================
# PAGE 3: CONFIGURE
# ============================================================
elif current_page == "configure":
    if USE_INTERNAL_BG_AND_LOGO:
        inject_background()
        inject_logo()

    selected_tool = st.session_state.get("selected_tool", "Tableau")

    st.markdown("""
    <style>
    /* Lock the page and remove scrollbars */
    html, body {
        height: 100vh !important;
        overflow: hidden !important;
        overscroll-behavior: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Remove Streamlit chrome */
    header, footer { visibility: hidden !important; height: 0 !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }

    /* Ensure app containers don't reintroduce scroll */
    [data-testid="stAppViewContainer"],
    section.main,
    .main .block-container,
    .block-container {
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding-top: 4px !important;   /* space for fixed button/heading */
        padding-bottom: 0 !important;
        box-shadow: none !important;
        background: transparent !important;
    }

    /* Hide any visual scrollbar just in case of subpixel overflow */
    ::-webkit-scrollbar { width: 0 !important; height: 0 !important; display: none !important; }
    * { scrollbar-width: none !important; -ms-overflow-style: none !important; }

    /* Keep your existing fixed home button styles */
    .fixed-home-btn {
        position: fixed;
        top: 19px;
        left: 7px;
        z-index: 9999;
    }
    .fixed-home-btn a {
        display: inline-block;
        background: white;
        color: #1a1a1a !important;
        font-weight: 700 !important;
        font-size: 2.0rem !important;
        
        padding: 0.9rem 2.0rem !important;
        border-radius: 9px !important;
        text-decoration: none !important;
        min-width: 200px !important;
        text-align: center !important;
    }

    /* --------------------------------------------------------
       Target the Emotion class you saw in DevTools
       NOTE: this value may change across sessions/builds.
       -------------------------------------------------------- */

    /* >>> YOUR CODE IS HERE <<< */
    .st-emotion-cache-1rfkdi4 {
        /* Example tweaks you showed in the screenshot: */
        font-family: "Source Sans", sans-serif;
        font-size: 1rem;
        margin-bottom: -3rem;   /* pulls the block up to reduce extra space */
        color: inherit;
        max-width: 100%;
        width: 100%;
        overflow-wrap: break-word;
    }

    /* --------------------------------------------------------
       SAFER FALLBACK: catch the same block even if the hash changes,
       by matching any class that starts with "st-emotion-cache-"
       and is inside a Markdown container.
       (Feel free to keep or remove this.)
       -------------------------------------------------------- */
    [data-testid="stMarkdownContainer"] > [class^="st-emotion-cache-"] {
        margin-top: 0 !important;
        /* if you want the same negative bottom margin as above: */
         margin-bottom: -1rem !important; 
        margin-top:1px;
    }

    </style>

    <div class="fixed-home-btn">
        <a href="?page=choose_tool" target="_self">BI4BI</a>
    </div>
    """, unsafe_allow_html=True)

    from frontend.tab_configure_app import render_configure_page
    render_configure_page(selected_tool)

