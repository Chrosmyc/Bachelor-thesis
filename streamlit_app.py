import os
from pathlib import Path

import streamlit as st

from parser.load_all import load_all
from llm.question import ask_question
from llm.show_models import get_models


st.set_page_config(
    page_title="Legacy Modernization Risk Analysis",
    page_icon="🔎",
    layout="wide",
)


CONTEXTS = {
    "1 – Full structured context": "full",
    "2 – Structured context without relationships": "without_relationships",
    "3 – No additional context": "none",
    "4 – Unstructured context": "raw",
}


def configure_secrets() -> None:
    """Expose Streamlit secrets to the existing modules as environment variables."""
    try:
        api_key = st.secrets.get("KICONNECT_API_KEY")
    except FileNotFoundError:
        api_key = None

    if api_key:
        os.environ["KICONNECT_API_KEY"] = str(api_key)


def require_password() -> bool:
    """Optional simple access protection using APP_PASSWORD in Streamlit secrets."""
    try:
        expected_password = st.secrets.get("APP_PASSWORD")
    except FileNotFoundError:
        expected_password = None

    if not expected_password:
        return True

    if st.session_state.get("authenticated"):
        return True

    st.title("Legacy Modernization Risk Analysis")
    password = st.text_input("Evaluation password", type="password")

    if st.button("Open application", type="primary"):
        if password == str(expected_password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    return False


@st.cache_resource(show_spinner=False)
def load_structured_context():
    return load_all()


@st.cache_resource(show_spinner=False)
def load_raw_context():
    raw_folder = Path(__file__).resolve().parent / "data" / "raw"

    risks_file = raw_folder / "Risks.txt"
    mitigations_file = raw_folder / "Mitigations.txt"
    relationship_files = sorted(raw_folder.glob("Relationships_High_*.txt"))

    missing = [
        str(path)
        for path in (risks_file, mitigations_file)
        if not path.exists()
    ]
    if missing:
        raise FileNotFoundError("Missing file(s): " + ", ".join(missing))

    if not relationship_files:
        raise FileNotFoundError(
            f"No Relationships_High_*.txt files found in {raw_folder}"
        )

    risks = risks_file.read_text(encoding="utf-8", errors="replace")
    mitigations = mitigations_file.read_text(encoding="utf-8", errors="replace")
    relationships = "\n\n".join(
        f"--- {path.name} ---\n"
        f"{path.read_text(encoding='utf-8', errors='replace')}"
        for path in relationship_files
    )
    return risks, mitigations, relationships


def get_context(context_key: str):
    if context_key == "full":
        return load_structured_context()

    if context_key == "without_relationships":
        risks, mitigations, _ = load_structured_context()
        return risks, mitigations, []

    if context_key == "none":
        return [], [], []

    if context_key == "raw":
        return load_raw_context()

    raise ValueError(f"Unknown context: {context_key}")


@st.cache_data(ttl=300, show_spinner=False)
def load_models():
    return get_models()


def reset_history() -> None:
    st.session_state.answers = []


configure_secrets()

if not require_password():
    st.stop()

st.title("Legacy Modernization Risk Analysis")
st.caption(
    "Select a context condition and model, enter an evaluation task, "
    "and review the generated answer."
)

with st.sidebar:
    st.header("Configuration")

    selected_context = st.selectbox(
        "Context condition",
        options=list(CONTEXTS.keys()),
    )
    context_key = CONTEXTS[selected_context]

    try:
        models = load_models()
    except Exception as exc:
        st.error(f"Models could not be loaded: {exc}")
        st.stop()

    if not models:
        st.error("No compatible chat models were returned by the API.")
        st.stop()

    selected_model = st.selectbox("Model", options=models)

    st.divider()
    st.write("**Current selection**")
    st.write(selected_context)
    st.write(selected_model)

    if st.button("Clear answer history", use_container_width=True):
        reset_history()
        st.rerun()

if "answers" not in st.session_state:
    st.session_state.answers = []

st.info(
    "Use the same selected tasks for all four context conditions. "
    "Copy one task from the cheat sheet, submit it, and evaluate the answer "
    "in the questionnaire."
)

question = st.text_area(
    "Task / question",
    height=180,
    placeholder="Paste one evaluation task here...",
)

submit = st.button(
    "Generate answer",
    type="primary",
    disabled=not question.strip(),
)

if submit:
    try:
        risks, mitigations, relationships = get_context(context_key)

        with st.spinner("Generating answer..."):
            answer = ask_question(
                question.strip(),
                risks,
                mitigations,
                relationships,
                selected_model,
            )

        st.session_state.answers.insert(
            0,
            {
                "context": selected_context,
                "model": selected_model,
                "question": question.strip(),
                "answer": answer,
            },
        )
    except Exception as exc:
        st.error(f"The request failed: {exc}")

if st.session_state.answers:
    st.subheader("Generated answers")

    for index, item in enumerate(st.session_state.answers, start=1):
        with st.container(border=True):
            st.caption(f"{item['context']} · {item['model']}")
            st.markdown("**Task / question**")
            st.write(item["question"])
            st.markdown("**Answer**")
            st.markdown(item["answer"])
