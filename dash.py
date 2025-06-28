import streamlit as st
import re
from collections import defaultdict
import pandas as pd

st.set_page_config(page_title="Duty Log Analyzer", layout="centered")

st.title("🕒 Duty Log Analyzer")
st.markdown("Paste your **Zion City Duty Logs** below to calculate total work time per person.")

log_input = st.text_area("📋 Paste Duty Logs Here", height=400)

if st.button("Analyze Logs"):
    if not log_input.strip():
        st.warning("Please paste some duty log text first.")
    else:
        # Regex pattern to extract name and shift durations
        matches = re.findall(
            r"Name:\s*(.+?)\n.*?Shift duration:\s*(?:(\d+(?:\.\d+)?)\s*hours)?(?:,\s*)?(?:(\d+(?:\.\d+)?)\s*minutes)?|Shift duration:\s*(\d+(?:\.\d+)?)\s*minutes",
            log_input,
            re.DOTALL
        )

        work_log = defaultdict(float)

        for m in matches:
            name = m[0].strip() if m[0] else None
            hours = float(m[1]) if m[1] else 0
            minutes = float(m[2]) if m[2] else 0
            fallback_minutes = float(m[3]) if m[3] else 0

            total_minutes = hours * 60 + minutes + fallback_minutes
            if name:
                work_log[name] += total_minutes

        # Convert to DataFrame
        data = []
        for name, total_min in sorted(work_log.items(), key=lambda x: -x[1]):
            hours = int(total_min // 60)
            minutes = int(total_min % 60)
            data.append({
                "Name": name,
                "Total Hours": hours,
                "Remaining Minutes": minutes,
                "Total Minutes": round(total_min, 2)
            })

        df = pd.DataFrame(data)

        st.success("✅ Analysis Complete!")
        st.dataframe(df[["Name", "Total Hours", "Remaining Minutes"]], use_container_width=True)

        # CSV download
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download CSV", csv, "duty_log_summary.csv", "text/csv")
