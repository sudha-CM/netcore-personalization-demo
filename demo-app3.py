# app.py — Netcore Personalization Demo (your images preserved)

import streamlit as st
import time
from collections import Counter
import streamlit.components.v1 as components

# -----------------------------
# Page config FIRST (prevents warnings)
# -----------------------------
st.set_page_config(layout="wide", page_title="Netcore Personalization Demo")
st.markdown("""
<style>
/* Keep normal flow, just place sidebar on the right */
div[data-testid="stAppViewContainer"] { display:flex; flex-direction: row; }
section[data-testid="stSidebar"] { order: 2; border-left: 1px solid #eee; border-right: 0; }
div[data-testid="stMain"] { order: 1; }

/* Fix the collapse/expand slide so it moves off the RIGHT side */
section[data-testid="stSidebar"][aria-expanded="true"]  { transform: translateX(0) !important; }
section[data-testid="stSidebar"][aria-expanded="false"] { transform: translateX(100%) !important; }

/* Nice shadow when open on narrow screens */
@media (max-width: 992px) {
  section[data-testid="stSidebar"][aria-expanded="true"] { box-shadow: -2px 0 12px rgba(0,0,0,0.12); }
}

/* Tidy spacing */
section[data-testid="stSidebar"] > div { padding-left: 1rem; padding-right: .5rem; }
</style>
""", unsafe_allow_html=True)



# ---- GLOBAL CSS FIXES ----
st.markdown("""
<style>
/* tighten buttons */
button[kind="secondary"] { padding: 0.35rem 0.75rem !important; }
/* reduce extra spacing between elements */
.block-container { padding-top: 3.25rem; }
/* image corners */
img { border-radius: 12px; }
/* ensure uniform card layout */
.css-1v0mbdj, .stImage, .element-container { margin-bottom: 0.25rem !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 0) INIT
# -----------------------------
if "clicks" not in st.session_state:
    st.session_state.clicks = []
if "pred" not in st.session_state:
    st.session_state.pred = {"Category": "-", "Discount Affinity": "-", "Style": "-"}
# ---- Modal control (for Quick View popup) ----
if "modal_product" not in st.session_state:
    st.session_state.modal_product = None


# -----------------------------
# 2) MOCK CATALOG (your images preserved)
# -----------------------------
def items(cat, base_price, styles, discounted_idx, imgs):
    out = []
    n = 8  # fixed number of products per category
    for i in range(n):
        style = styles[i % len(styles)]
        img = imgs[i] if i < len(imgs) else f"https://placehold.co/260x320?text={cat}%0A{style}%20#{i+1}"
        out.append({
            "name": f"{style} {cat[:-1]} #{i+1}",
            "category": cat,
            "price": round(base_price + (i % 5) * 7.0, 2),
            "discount": i in discounted_idx,
            "style": style,
            "img": img
        })
    return out


# ----- YOUR IMAGE LISTS (unchanged) -----
DRESSES_IMGS = [
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2045417%E2%80%AFPM-20542.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2045429%E2%80%AFPM-20559.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2050454%E2%80%AFPM-21158.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2045450%E2%80%AFPM-20578.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2045456%E2%80%AFPM-20985.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2050512%E2%80%AFPM-21169.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2045435%E2%80%AFPM-20568.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2050648%E2%80%AFPM-21258.png",
]
TOPS_IMGS = [
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051210%E2%80%AFPM-21578.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051349%E2%80%AFPM-21699.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051615%E2%80%AFPM-21872.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051009%E2%80%AFPM-21461.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051341%E2%80%AFPM-21699.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051633%E2%80%AFPM-21872.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2050951%E2%80%AFPM-21461.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051402%E2%80%AFPM-21699.png",
]
BOTTOMS_IMGS = [
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051910%E2%80%AFPM-22103.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051938%E2%80%AFPM-22103.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2052029%E2%80%AFPM-22103.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051856%E2%80%AFPM-22103.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051958%E2%80%AFPM-22103.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2052022%E2%80%AFPM-22103.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051904%E2%80%AFPM-22103.png",
    "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-18%20at%2051946%E2%80%AFPM-22103.png",
]

DRESSES = items("Dress", 49.0, ["Solid","Printed","Lace"], {0,2,5,7,9}, DRESSES_IMGS)
TOPS    = items("Tops",    29.0, ["Solid","Printed","Striped"], {1,3,6,8,10}, TOPS_IMGS)
BOTTOMS = items("Bottoms", 39.0, ["Denim","Solid","Printed"], {0,4,7,11}, BOTTOMS_IMGS)
CATALOG = [("👗 Dresses", DRESSES), ("👚 Tops", TOPS), ("👖 Bottoms", BOTTOMS)]

# -----------------------------
# 3) RIGHT SIDEBAR — PREDICTIONS
# -----------------------------
with st.sidebar:
    st.header("📊 Session & Predictions")

    # --- Store analytics (mocked for now) ---
    st.write("**Dwell Time:**", f"{int(time.time() % 300)}s")
    st.write("**Scroll %:**", "65%")
    st.write("**Location:**", "New York, US")
    st.write("**Weather:**", "20.2°C")

    st.markdown("---")
    st.subheader("🔮 Realtime Profile")

    # compute predictions from clicks
    if st.session_state.clicks:
        cat_counter   = Counter([p["category"] for p in st.session_state.clicks])
        style_counter = Counter([p["style"] for p in st.session_state.clicks])
        type_counter  = Counter([p.get("type","") for p in st.session_state.clicks])
        top_cat, _    = cat_counter.most_common(1)[0]
        top_style, _  = style_counter.most_common(1)[0]
        top_type, _   = type_counter.most_common(1)[0]
        disc_rate     = sum(1 for p in st.session_state.clicks if p["discount"]) / len(st.session_state.clicks)
        disc_aff      = "High" if disc_rate >= 0.5 else "Low"
        st.session_state.pred = {
            "Category": top_cat,
            "Style": top_style,
            "Type": top_type or "-",
            "Discount Affinity": disc_aff
        }

    for k in ["Category","Style","Type","Discount Affinity"]:
        st.write(f"**{k}:** {st.session_state.pred.get(k,'-')}")

    st.markdown("---")
    st.subheader("📝 Recent events")
    # scrollable recent events list
    with st.container(height=220, border=True):
        if st.session_state.clicks:
            for p in st.session_state.clicks[-30:][::-1]:
                sale = " • SALE" if p["discount"] else ""
                st.write(f"- {p['category']} / {p.get('type','-')} / {p['style']} • ${p['price']}{sale}")
        else:
            st.caption("No interactions yet")


# -----------------------------
# Helper: Version-agnostic Quick View
# -----------------------------
def show_quick_view(p):
    # Use st.modal if present (newer Streamlit)
    if hasattr(st, "modal"):
        with st.modal("Quick View"):
            c1, c2 = st.columns([1,1])
            with c1: st.image(p["img"], use_container_width=True)
            with c2:
                st.write(f"**{p['name']}**")
                st.write(f"**Category:** {p['category']}")
                st.write(f"**Style:** {p['style']}")
                st.write(f"**Price:** ${p['price']}{'  (SALE)' if p['discount'] else ''}")
                st.write("Soft-touch fabric. Ships in 2–3 days.")
            if st.button("Close"): st.session_state.modal_product = None
        return
    # Older builds: st.dialog if available
    if hasattr(st, "dialog"):
        @st.dialog("Quick View", width="large")
        def _dlg():
            c1, c2 = st.columns([1,1])
            with c1: st.image(p["img"], use_container_width=True)
            with c2:
                st.write(f"**{p['name']}**")
                st.write(f"**Category:** {p['category']}")
                st.write(f"**Style:** {p['style']}")
                st.write(f"**Price:** ${p['price']}{'  (SALE)' if p['discount'] else ''}")
                st.write("Soft-touch fabric. Ships in 2–3 days.")
            if st.button("Close"): st.session_state.modal_product = None
        _dlg()
        return
    # Fallback: inline panel at bottom (still avoids grid jump)
    st.markdown("### Quick View")
    c1, c2 = st.columns([1,1])
    with c1: st.image(p["img"], use_container_width=True)
    with c2:
        st.write(f"**{p['name']}**")
        st.write(f"**Category:** {p['category']}")
        st.write(f"**Style:** {p['style']}")
        st.write(f"**Price:** ${p['price']}{'  (SALE)' if p['discount'] else ''}")
        st.write("Soft-touch fabric. Ships in 2–3 days.")
    if st.button("Close"): st.session_state.modal_product = None

# -----------------------------
# 4) GRID + QUICK VIEW (no layout jump)
# -----------------------------
CARD_IMG_H = 320  # reserved for future fixed heights
st.title("Netcore Fashion Store (Demo)")

for section_title, items_list in CATALOG:
    st.subheader(section_title)
    cols = st.columns(4)
    for i, p in enumerate(items_list):
        with cols[i % 4]:
            st.image(p["img"], use_container_width=True)  # widest compatibility
            st.markdown(f"<div style='height: 24px'><strong>{p['name']}</strong></div>", unsafe_allow_html=True)
            price = f"${p['price']}"
            if p["discount"]:
                st.markdown(f"<span style='color:#10b981'>SALE</span> · {price}", unsafe_allow_html=True)
            else:
                st.write(price)
            if st.button(f"Quick View — {p['name']}", key=f"qv-{section_title}-{i}"):
                st.session_state.clicks.append(p)
                st.session_state.modal_product = p

# Render Quick View once, outside the grid
if st.session_state.get("modal_product"):
    show_quick_view(st.session_state.modal_product)

st.markdown("---")

# -----------------------------
# 5) EMAIL PREVIEW (rich HTML) + download
# -----------------------------
BRAND_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Netcore_Cloud_logo.svg/512px-Netcore_Cloud_logo.svg.png"

def render_email_html(logo_url, hero_url, footer_url, pred, recs):
    cards = "".join([
        f"""
        <td style="padding:10px; text-align:center;">
          <img src="{p['img']}" width="160" style="border-radius:8px; display:block; margin:0 auto 8px;" />
          <div style="font:600 14px/1.2 Arial;color:#111">{p['name']}</div>
          <div style="font:12px Arial;color:#666">{p.get('type','-')} • {p['style']}</div>
          <div style="font:14px Arial;color:#444">${p['price']}{' <span style="color:#10b981;">(SALE)</span>' if p['discount'] else ''}</div>
        </td>
        """ for p in recs
    ])
    hero_block = f"""
      <tr><td style="padding:8px 24px 0; text-align:center;">
        <img src="{hero_url}" width="592" style="width:100%; max-width:592px; border-radius:12px;" alt="Hero"/>
      </td></tr>
    """ if hero_url else ""

    footer_block = f"""
      <tr><td style="padding:0 24px 24px; text-align:center;">
        <img src="{footer_url}" width="592" style="width:100%; max-width:592px; border-radius:12px;" alt="Footer"/>
      </td></tr>
    """ if footer_url else ""

    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#f7f7f7; padding:24px;">
      <tr><td align="center">
        <table width="640" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden;">
          <tr><td style="padding:24px 24px 0; text-align:center;">
            <img src="{logo_url}" height="36" alt="Brand" />
          </td></tr>
          {hero_block}
          <tr><td style="padding:16px 24px 0; font:700 22px Arial; color:#111; text-align:center;">
            Picks we made just for you — more {pred['Style'].lower()} {pred['Category'].lower()}
          </td></tr>
          <tr><td style="padding:8px 24px 0; font:16px Arial; color:#333; text-align:center;">
            We noticed you liked {pred['Style'].lower()} {pred['Type'].lower() if pred.get('Type') and pred['Type']!='-' else 'styles'} in {pred['Category'].lower()} ({'on sale' if pred['Discount Affinity']=='High' else 'regular priced'}).
          </td></tr>
          <tr><td style="padding:16px 8px 24px;">
            <table align="center" cellpadding="0" cellspacing="0"><tr>
              {cards}
            </tr></table>
          </td></tr>
          {footer_block}
        </table>
      </td></tr>
    </table>
    """


BRAND_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Netcore_Cloud_logo.svg/512px-Netcore_Cloud_logo.svg.png"
HERO_PH        = "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-27%20at%2081843%E2%80%AFPM-15335.png"
FOOTER_PH      = "https://imageaws.netcoresmartech.com/images/netcoredemoboxx/Screenshot%202025-10-27%20at%2081950%E2%80%AFPM-15353.png"

st.subheader("✉️ Personalized Email")
logo_url  = st.text_input("Brand logo URL", value=BRAND_LOGO_URL)
hero_url  = st.text_input("Hero image URL (optional)", value=HERO_PH)
footer_url= st.text_input("Footer image URL (optional)", value=FOOTER_PH)

# Close modal BEFORE render to avoid Quick View popping
def close_modal(): st.session_state.modal_product = None
email_btn = st.button("Show Personalized Email Preview", on_click=close_modal)

if email_btn:
    pred = st.session_state.pred
    if pred["Category"] == "-":
        st.info("Browse a few items first to personalize the email.")
    else:
        pool   = [p for _, lst in CATALOG for p in lst if p["category"] == pred["Category"]]
        styled = [p for p in pool if pred['Style'] in p['style']]
        typed  = [p for p in (styled or pool) if p.get("type","") == pred.get("Type","")]
        recs   = (typed or styled or pool)[:3]

        html = render_email_html(logo_url or BRAND_LOGO_URL, hero_url, footer_url, pred, recs)
        components.html(html, height=680, scrolling=True)


