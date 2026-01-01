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
    def prev(key, default=50):
        return int(tlx_prev.get(key, default))

    with st.form("tlx_form"):

        st.markdown("**How mentally demanding was the task?**")
        st.caption("1 = Very Low  7 = Very High")
        mental = st.slider(
            label="",
            min_value=1,
            max_value=7,
            value=prev("mental", 4),
            step=1,
            key="mental"
        )

        st.markdown("**How physically demanding was the task?**")
        st.caption("1 = Very Low  7 = Very High")
        physical = st.slider(
            label="",
            min_value=1,
            max_value=7,
            value=prev("physical", 4),
            step=1,
            key="physical"
        )

        st.markdown("**How hurried or rushed was the pace of the task?**")
        st.caption("1 = Very Low  7 = Very High")
        temporal = st.slider(
            label="",
            min_value=1,
            max_value=7,
            value=prev("temporal", 4),
            step=1,
            key="temporal"
        )

        st.markdown("**How successful were you in accomplishing what you were asked to do?**")
        st.caption("1 = Perfect  7 = Failure")
        performance = st.slider(
            label="",
            min_value=1,
            max_value=7,
            value=prev("performance", 4),
            step=1,
            key="performance"
        )

        st.markdown("**How hard did you have to work to accomplish your level of performance?**")
        st.caption("1 = Very Low  7 = Very High")
        effort = st.slider(
            label="",
            min_value=1,
            max_value=7,
            value=prev("effort", 4),
            step=1,
            key="effort"
        )

        st.markdown("**How insecure, discouraged, irritated, stressed, and annoyed were you?**")
        st.caption("1 = Very Low  7 = Very High")
        frustration = st.slider(
            label="",
            min_value=1,
            max_value=7,
            value=prev("frustration", 4),
            step=1,
            key="frustration"
        )

        left, right = st.columns([1, 1])
        with left:
            back_clicked = st.form_submit_button("⬅️ Back")
        with right:
            next_clicked = st.form_submit_button("Next ➡️")


        if back_clicked:
            st.session_state.step = 1
            st.rerun()

        if next_clicked:
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
    st.json(st.session_state.basic)

    st.subheader("NASA-TLX")
    st.json(st.session_state.tlx)

    mean_tlx = sum(st.session_state.tlx.values()) / 6.0
    st.metric("NASA-TLX", f"{mean_tlx:.2f}")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("⬅️ Back to Previous Page"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        st.button("Submit")
