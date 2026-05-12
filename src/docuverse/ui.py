from __future__ import annotations

from docuverse.answer import generate_answer


def _format_error(error: Exception) -> str:
    message = str(error)
    lower_message = message.lower()

    if "openai_api_key" in lower_message:
        return "OPENAI_API_KEY is missing. Set it before asking a question."
    if "connection refused" in lower_message or "could not connect" in lower_message:
        return "The database does not appear to be running. Start Postgres with docker compose up -d postgres."
    if "document_chunks" in lower_message:
        return "No stored chunks were found. Run python -m docuverse.store data/corpus_aws first."
    if "no chunks" in lower_message:
        return "No chunks were found. Ingest and store documents before asking questions."

    return f"Something went wrong: {message}"


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="docuverse-rag")

    st.title("docuverse-rag")
    st.write(
        "Ask questions over your local document corpus and get citation-grounded answers."
    )

    question = st.text_area("Question", placeholder="What is AWS S3?")
    top_k = st.slider("Retrieved chunks", min_value=1, max_value=10, value=5)

    if st.button("Ask", type="primary"):
        if not question.strip():
            st.warning("Enter a question before asking.")
            return

        try:
            with st.spinner("Searching documents and generating an answer..."):
                result = generate_answer(question.strip(), top_k=top_k)
        except Exception as error:
            st.error(_format_error(error))
            return

        if not result.get("sources"):
            st.warning(
                "No chunks were found. Ingest and store documents before asking questions."
            )
            return

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Citations")
        citations = result.get("citations", [])
        if citations:
            for citation in citations:
                st.write(f"- {citation}")
        else:
            st.write("No citations returned.")

        with st.expander("Retrieved sources"):
            sources = result.get("sources", [])
            if not sources:
                st.write("No sources returned.")

            for source in sources:
                source_id = source.get("id") or source.get("chunk_id")
                score = source.get("score")
                source_file = source.get("source_file", "unknown source")
                score_text = f" score={score:.2f}" if isinstance(score, float) else ""

                st.markdown(f"**{source_id}** - {source_file}{score_text}")
                st.write(source.get("text", ""))


if __name__ == "__main__":
    main()
