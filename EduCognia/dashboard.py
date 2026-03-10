# app/dashboard.py
import sys
from pathlib import Path
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

# make project root importable (so src.* imports work)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.utils.paths import processed_dir, models_dir
from src.realtime.run_live_session import (
    LiveInteractionLogger,
    compute_session_features,
    align_and_predict,
    compute_window_durations,
)

# ---------------------------------------------------------------------
# Cached loaders
# ---------------------------------------------------------------------
@st.cache_resource
def load_model_and_mapping():
    model_path = models_dir("xgb_multimodal_label.pkl")
    mapping_path = models_dir("xgb_multimodal_label_mapping.pkl")
    try:
        model = joblib.load(model_path)
        mapping = joblib.load(mapping_path)
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        raise
    return model, mapping


@st.cache_data
def load_multimodal_dataset():
    p = processed_dir("multimodal_dataset.parquet")
    if not p.exists():
        return pd.DataFrame()
    return pd.read_parquet(p)


# ---------------------------------------------------------------------
# Helpers: safe feature extraction (avoid KeyErrors if feature missing)
# ---------------------------------------------------------------------
def _safe_val(df, col, default=0.0, cast=float):
    if (df is None) or df.empty:
        return default
    if col in df.columns:
        try:
            v = df[col].iloc[0]
            if pd.isna(v):
                return default
            return cast(v)
        except Exception:
            return default
    return default


def fmt_px(x):
    try:
        return f"{x:.0f}px"
    except Exception:
        return "0px"


def fmt_pct(x):
    try:
        return f"{x*100:.1f}%"
    except Exception:
        return "0.0%"


# ---------------------------------------------------------------------
# UI styling (dark theme)
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="EduCognia Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      html, body { background-color: #020617; }
      .stApp { background-color: #020617; color: #e5e7eb; }
      section[data-testid="stSidebar"] { background-color: #071029; border-right: 1px solid #0b1220; }
      .big-metric { font-size: 2.3rem; font-weight:700; color:#f9fafb; }
      .metric-label { font-size:0.75rem; color:#9ca3af; text-transform:uppercase; letter-spacing:0.08em; }
      .state-pill { padding: .45rem 1rem; border-radius:999px; background: linear-gradient(90deg,#22c55e,#16a34a); color:#052e16; font-weight:700; }
      .focus-pill { padding: .3rem .75rem; border-radius:999px; background:#0f1724; color:#e5e7eb; font-weight:600; }
      .card { background: transparent; border-radius: .8rem; padding: .8rem; border: 1px solid #0f1724; }
      .prob-bar { height: .55rem; border-radius:999px; background:#0b1220; overflow:hidden; margin-bottom:.45rem; }
      .prob-bar-inner { height:100%; background:linear-gradient(90deg,#2563eb,#4f46e5); }
      h1,h2,h3,h4 { color:#f9fafb !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 EduCognia – Multimodal Cognitive State Analytics (Live Monitor)")

# load model + dataset
model, label_map = load_model_and_mapping()
df_all = load_multimodal_dataset()

# tabs: live first, then history
tab_live, tab_history = st.tabs(
    ["🟢 Live Monitor", "📈 Session History"]
)

# session history path
SESSION_LOG_PATH = processed_dir("session_history.parquet")


def append_session_log(record: dict):
    path = SESSION_LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            df_old = pd.read_parquet(path)
            df_new = pd.concat([df_old, pd.DataFrame([record])], ignore_index=True)
        except Exception:
            # If file exists but unreadable, overwrite with new
            df_new = pd.DataFrame([record])
    else:
        df_new = pd.DataFrame([record])
    # ensure unique column names and safe types
    df_new.to_parquet(path, index=False)


def load_session_history():
    if not SESSION_LOG_PATH.exists():
        return pd.DataFrame()
    return pd.read_parquet(SESSION_LOG_PATH)


# -------------------------
# LIVE MONITOR TAB
# -------------------------
with tab_live:
    st.subheader("Live Cognitive Monitor")

    st.write(
        "Run a short session where EduCognia observes mouse, keyboard and active window usage "
        "and estimates your cognitive state. Keep the browser window open in the background."
    )

    col_left, col_right = st.columns([1, 1])

    with col_left:
        duration_sec = st.slider(
            "Capture duration (seconds)",
            min_value=15,
            max_value=120,
            value=30,
            step=5,
        )
        st.info(
            "Start a session, move the mouse, scroll, type and switch windows as usual. "
            "Keep the learning platform tab (Pegasus/Udemy) open if you want on-task checks."
        )
        start_btn = st.button("▶️ Start Live Capture", type="primary")

    status_ph = st.empty()
    feat_ph = st.empty()
    state_ph = st.empty()
    probs_ph = st.empty()

    if start_btn:
        status_ph.info("Recording interactions... move, type, scroll, switch apps. 👀")
        logger = LiveInteractionLogger(duration_sec=duration_sec)
        events_df = logger.run()

        status_ph.success(f"Captured {len(events_df)} events over {duration_sec} seconds.")

        # compute features and raw prediction
        feat_df = compute_session_features(events_df)  # one-row df
        raw_label, prob_map = align_and_predict(feat_df)

        # compute window durations and total tracked time
        app_durations, total_tracked = compute_window_durations(events_df)

        # compute safe numeric features for UI
        n_events = int(_safe_val(feat_df, "n_events", default=0, cast=float))
        duration = float(_safe_val(feat_df, "duration", default=0.0, cast=float))
        total_path = float(_safe_val(feat_df, "total_path", default=0.0, cast=float))
        idle_fraction = float(_safe_val(feat_df, "idle_fraction", default=0.0, cast=float))
        keys_per_second = float(_safe_val(feat_df, "keys_per_second", default=0.0, cast=float))
        window_switch_count = int(_safe_val(feat_df, "window_switch_count", default=0, cast=float))
        window_switch_rate = float(_safe_val(feat_df, "window_switch_rate", default=0.0, cast=float))
        top_app_share = float(_safe_val(feat_df, "top_app_share", default=0.0, cast=float))
        top_app_time = float(_safe_val(feat_df, "top_app_time", default=0.0, cast=float))
        last_active_app = feat_df["last_active_app"].iloc[0] if "last_active_app" in feat_df.columns else None

        # apply policy: mark on-task if top app looks like learning platform
        EDU_KEYWORDS = ["pegasus", "imarticus", "udemy", "moodle", "canvas", "khan academy"]
        if app_durations:
            top_app, top_seconds = max(app_durations.items(), key=lambda x: x[1])
            top_share = top_seconds / (sum(app_durations.values()) or 1.0)
            top_app_lower = top_app.lower()
            is_edu = any(k in top_app_lower for k in EDU_KEYWORDS)
        else:
            top_app = None
            top_share = 0.0
            is_edu = False

        # local focus score (same heuristic used previously)
        def compute_focus_score_local(feat_df_local):
            top_share_local = _safe_val(feat_df_local, "top_app_share", default=0.0, cast=float)
            idle_fraction_local = _safe_val(feat_df_local, "idle_fraction", default=0.0, cast=float)
            switch_rate_local = _safe_val(feat_df_local, "window_switch_rate", default=0.0, cast=float)
            switch_penalty = min(switch_rate_local * 3.0, 1.0)
            base = top_share_local
            score = base * (1.0 - 0.5 * idle_fraction_local) * (1.0 - 0.5 * switch_penalty)
            score = max(0.0, min(1.0, score))
            return score * 100.0

        focus_score = compute_focus_score_local(feat_df)

        # policy adjustment: if model says Engaged/Focused but top app not educational -> downgrade to Distracted
        final_label = raw_label
        explanation = ""
        if raw_label in ["Engaged", "Focused"]:
            reasons = []
            if not is_edu:
                reasons.append("active window is not a recognised learning platform (Pegasus/Udemy/etc.)")
            if top_share < 0.6:
                reasons.append(f"only {top_share*100:.1f}% of time on the main window")
            if focus_score < 40.0:
                reasons.append(f"low focus score ({focus_score:.1f})")
            if reasons:
                final_label = "Distracted"
                explanation = (
                    f"Model predicted **{raw_label}**, but we downgraded to **Distracted** because: "
                    + "; ".join(reasons)
                    + f". Top app: **{top_app}** ({top_share*100:.1f}%)."
                )
            else:
                explanation = (
                    f"Model predicted **{raw_label}** and the label was retained. Top app: **{top_app}** ({top_share*100:.1f}%)."
                )
        else:
            explanation = f"Model predicted **{raw_label}** based on behaviour; policy did not change it. Top app: **{top_app}**."

        # ----------------- Render top metrics -----------------
        st.markdown("---")
        top_cols = st.columns([1.2, 1.0, 1.0])

        with top_cols[0]:
            st.markdown('<p class="metric-label">Predicted cognitive state</p>', unsafe_allow_html=True)
            st.markdown(f'<span class="state-pill">{final_label}</span>', unsafe_allow_html=True)

            st.markdown("<br/>", unsafe_allow_html=True)
            st.markdown('<p class="metric-label">Focus score</p>', unsafe_allow_html=True)
            st.markdown(f'<span class="focus-pill">{focus_score:.1f} / 100</span>', unsafe_allow_html=True)

            if top_app:
                status = "On-task (learning platform)" if is_edu else "Off-task app / non-learning window"
                st.caption(f"Top app: **{top_app}** — {top_share*100:.1f}% of window time • {status}")

        with top_cols[1]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<p class="metric-label">Events & activity</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-metric">{n_events:,}</p>', unsafe_allow_html=True)
            st.caption(f"Mouse distance: {fmt_px(total_path)} • Idle fraction: {idle_fraction:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        with top_cols[2]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<p class="metric-label">Typing</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-metric">{keys_per_second:.2f}</p>', unsafe_allow_html=True)
            st.caption("Keys per second during active typing window.")
            st.markdown("</div>", unsafe_allow_html=True)

        # ----------------- Explanation + probability bars -----------------
        st.markdown("### Summary for this session")
        st.markdown(explanation, unsafe_allow_html=True)

        st.markdown("### Model confidence")
        prob_df = pd.DataFrame({"state": list(prob_map.keys()), "probability": list(prob_map.values())}).sort_values("probability", ascending=False)
        for _, row in prob_df.iterrows():
            st.markdown(f"**{row['state']}** &nbsp;&nbsp; {row['probability']:.3f}")
            st.markdown(f"""
                <div class="prob-bar">
                  <div class="prob-bar-inner" style="width: {row['probability']*100:.1f}%;"></div>
                </div>
                """, unsafe_allow_html=True)

        # ----------------- App usage breakdown (NO 'share' column) -----------------
        st.markdown("### 🧿 App usage during this session")
        if app_durations:
            app_df = pd.DataFrame([{"app": k, "seconds_active": v} for k, v in app_durations.items()])
            app_df = app_df.sort_values("seconds_active", ascending=False).reset_index(drop=True)
            # doughnut/pie
            fig = px.pie(app_df, names="app", values="seconds_active", hole=0.5)
            fig.update_layout(paper_bgcolor="#020617", plot_bgcolor="#020617", font_color="#e5e7eb")
            st.plotly_chart(fig, use_container_width=True)
            # show the table without the 'share' column
            st.dataframe(app_df, use_container_width=True)
        else:
            st.info("No window-switching activity detected in this session.")

        # ----------------- Activity & window timeline -----------------
        st.markdown("### 🧭 Activity timeline")
        if not events_df.empty:
            t0 = events_df["timestamp"].min()
            events_df = events_df.copy()
            events_df["t_rel"] = events_df["timestamp"] - t0
            bin_size = 5.0
            events_df["t_bin"] = (events_df["t_rel"] // bin_size) * bin_size
            activity_df = events_df.groupby("t_bin").size().reset_index(name="n_events").sort_values("t_bin")
            activity_df["t_label"] = activity_df["t_bin"].astype(int)
            chart = alt.Chart(activity_df).mark_bar(color="#38bdf8").encode(
                x=alt.X("t_label:Q", title="Seconds since start (binned)"),
                y=alt.Y("n_events:Q", title="Number of events"),
            ).properties(height=200)
            st.altair_chart(chart, use_container_width=True)

            df_win = events_df[events_df["event_type"] == "window_change"].copy()
            if not df_win.empty:
                df_win["t_rel"] = df_win["timestamp"] - t0
                df_win["app"] = df_win["key"].astype(str)
                switch_chart = alt.Chart(df_win).mark_point(size=60, filled=True, color="#f97316").encode(
                    x=alt.X("t_rel:Q", title="Seconds since start"),
                    y=alt.value(0),
                    tooltip=["app", "t_rel"],
                ).properties(height=80)
                st.markdown("### 🔁 Window switches")
                st.altair_chart(switch_chart, use_container_width=True)
            else:
                st.info("No window changes logged in this session.")
        else:
            st.info("No events captured.")

        # ----------------- Persist session record -----------------
        session_record = {
            "timestamp": datetime.now(),
            "duration_sec": duration_sec,
            "raw_label": raw_label,
            "final_label": final_label,
            "focus_score": float(focus_score),
            "top_app": top_app,
            "top_share": float(top_share) if top_app else np.nan,
            "is_edu_app": bool(is_edu),
            "n_events": n_events,
            "idle_fraction": idle_fraction,
            "keys_per_second": keys_per_second,
            "window_switch_count": window_switch_count,
        }
        append_session_log(session_record)

        st.caption("Each live session is logged in the Session History tab.")


# -------------------------
# SESSION HISTORY TAB
# -------------------------
with tab_history:
    st.subheader("Session History")
    df_hist = load_session_history()
    if df_hist is None or df_hist.empty:
        st.info("No live sessions logged yet. Run at least one session in Live Monitor.")
    else:
        df_hist["timestamp"] = pd.to_datetime(df_hist["timestamp"])
        df_hist = df_hist.sort_values("timestamp")

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<p class="metric-label">Total sessions</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-metric">{len(df_hist):,}</p>', unsafe_allow_html=True)
        with c2:
            st.markdown('<p class="metric-label">Average focus score</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-metric">{df_hist["focus_score"].mean():.1f}</p>', unsafe_allow_html=True)
        with c3:
            if "is_edu_app" in df_hist.columns:
                on_task_mask = df_hist["is_edu_app"] & df_hist["final_label"].isin(["Engaged", "Focused"])
                on_task_ratio = on_task_mask.mean()
                st.markdown('<p class="metric-label">On-task engaged sessions</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="big-metric">{on_task_ratio*100:.1f}%</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="metric-label">On-task engaged sessions</p>', unsafe_allow_html=True)
                st.markdown('<p class="big-metric">–</p>', unsafe_allow_html=True)

        st.markdown("### Focus over time")
        focus_chart = alt.Chart(df_hist).mark_line(point=True, color="#38bdf8").encode(
            x=alt.X("timestamp:T", title="Timestamp"),
            y=alt.Y("focus_score:Q", title="Focus score"),
            tooltip=["timestamp:T", "focus_score:Q", "final_label:N", "top_app:N"],
        ).properties(height=260)
        st.altair_chart(focus_chart, use_container_width=True)

        st.markdown("### Final cognitive states across sessions")

# Build label_counts robustly (ensure correct column names for plotting)
label_counts = (
    df_hist.groupby("final_label")
    .size()
    .reset_index(name="n_sessions"))          # -> columns: final


st.markdown("### Recent sessions")
st.dataframe(df_hist.sort_values("timestamp", ascending=False).head(25), use_container_width=True)