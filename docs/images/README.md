# Demo Screenshot Assets

The main README references four screenshots in this directory. Add these images
after running the local demo flow in [docs/DEMO_GUIDE.md](../DEMO_GUIDE.md).

## Required Files

### `ui-home.png`

Capture the Streamlit UI after it loads. The screenshot should show:

- `docuverse-rag` title
- short description
- question input
- `top_k` slider
- Ask button

### `answer-example.png`

Capture the Streamlit UI after asking:

```text
What is AWS S3?
```

The screenshot should show the generated answer and visible citations.

### `retrieval-example.png`

Capture the expanded retrieved sources/chunks section in the Streamlit UI. The
screenshot should show source IDs, source file names, similarity scores when
available, and chunk text.

### `api-example.png`

Capture the `/ask` API response from PowerShell, a browser, or an API client.
The screenshot should show the answer, citations, and sources fields.

## Notes

Keep screenshots cropped around the product surface. Avoid screenshots dominated
by terminal chrome, empty whitespace, or unrelated desktop content.
