import streamlit as st


st.set_page_config(page_title="Questionnaire", layout="centered")


if "step" not in st.session_state:
    st.session_state.step = 1
if "basic" not in st.session_state:
    st.session_state.basic = {}
if "tlx" not in st.session_state:
    st.session_state.tlx = {}


st.title("Questionnaire")


# page 1 -----------------------------------------------------------------------------
if st.session_state.step == 1:
    st.header("1. Basic Information")

    with st.form("basic_form"):
        id = st.text_input("ID", placeholder="e.g. 12")
        age = st.number_input("Age", min_value=0, max_value=120, value=0, step=1)
        gender = st.selectbox(
            "Gender",
            ["", "Female", "Male", "Non-binary", "Prefer not to say", "Other"]
        )

    
        next_clicked = st.form_submit_button("Next")

    if next_clicked:
        required_fields = {
            "ID": id,
            "Age": age,
            "Gender": gender,
        }

        missing = [
            name for name, value in required_fields.items()
            if value == "" or value == 0
        ]

        if missing:
            st.warning(
                "Please fill in all required fields:\n- " + "\n- ".join(missing)
            )
        else:
            st.session_state.basic = {
                "id": id.strip(),
                "age": int(age),
                "gender": gender,
            }
            st.session_state.step = 2
            st.rerun()


# page 2 -----------------------------------------------------------------------------

elif st.session_state.step == 2:
    st.header("2) NASA-TLX")

    tlx_prev = st.session_state.tlx or {}
    def prev(key, default=4):
        return int(tlx_prev.get(key, default))

    def tlx_item(key, question, left_anchor, right_anchor):
        st.markdown(f"**{question}**")
        lcol, scol, rcol = st.columns([2, 7, 2], vertical_alignment="center")

        with lcol:
            st.markdown(
                f"<div style='text-align:left; font-size:0.9rem;'><b>{left_anchor}</b></div>",
                unsafe_allow_html=True
            )

        with scol:
            v = st.slider(
                label=key,
                min_value=1,
                max_value=7,
                value=prev(key, 4),
                step=1,
                key=f"tlx_{key}",
                label_visibility="collapsed",
            )
    

        with rcol:
            st.markdown(
                f"<div style='text-align:right; font-size:0.9rem;'><b>{right_anchor}</b></div>",
                unsafe_allow_html=True
            )

        st.markdown("<div class='tlx_item_gap'></div>", unsafe_allow_html=True)
        return v

    mental = tlx_item("mental", "How mentally demanding was the task?", "Very Low", "Very High")
    physical = tlx_item("physical", "How physically demanding was the task?", "Very Low", "Very High")
    temporal = tlx_item("temporal", "How hurried or rushed was the pace of the task?", "Very Low", "Very High")
    performance = tlx_item("performance", "How successful were you in accomplishing what you were asked to do?", "Perfect", "Failure")
    effort = tlx_item("effort", "How hard did you have to work to accomplish your level of performance?", "Very Low", "Very High")
    frustration = tlx_item("frustration", "How insecure, discouraged, irritated, stressed, and annoyed were you?", "Very Low", "Very High")

    st.divider()

    padL, left, right, padR = st.columns([1, 3, 3, 1])
    with left:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with right:
        if st.button("Next ➡️", type="primary", use_container_width=True):
            st.session_state.tlx = {
                "mental": int(mental),
                "physical": int(physical),
                "temporal": int(temporal),
                "performance": int(performance),
                "effort": int(effort),
                "frustration": int(frustration),
            }
            st.session_state.step = 3
            st.rerun()



# step 3 ---------------------------------------------
else:
    st.header("3) Preview")

    st.subheader("Basic Information")
    b = st.session_state.basic
    st.write(f"**ID:** {b.get('id','')}")
    st.write(f"**Age:** {b.get('age','')}")
    st.write(f"**Gender:** {b.get('gender','')}")

    st.subheader("NASA-TLX")
    t = st.session_state.tlx

    rows = [
        ("Mental Demand", t.get("mental", "")),
        ("Physical Demand", t.get("physical", "")),
        ("Temporal Demand", t.get("temporal", "")),
        ("Performance", t.get("performance", "")),
        ("Effort", t.get("effort", "")),
        ("Frustration", t.get("frustration", "")),
    ]

    for label, val in rows:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.write(label)
        with c2:
            st.write(f"**{val}**")

    mean_tlx = sum(int(v) for _, v in rows if str(v) != "") / 6.0
    st.metric("NASA-TLX (Mean)", f"{mean_tlx:.2f}")

    padL, left, right, padR = st.columns([1, 3, 3, 1])
    with left:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with right:
        if st.button("Submit", type="primary", use_container_width=True):
            st.success("Submitted !")
