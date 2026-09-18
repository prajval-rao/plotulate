# Plotulate

Plotulate is a data visualisation web tool — upload a dataset, explore it in an interactive grid, and ask natural-language questions about it powered by Gemini Flash LLM.

## Features

- **Excel upload & parsing** — Upload `.xlsx` / `.xls` files; the backend cleans and type-converts columns with pandas and returns clean JSON records.
- **Interactive data grid** — Uploaded data renders in an editable, sortable, filterable grid using [ag-Grid Community](https://www.ag-grid.com/).
- **Natural-language querying** — Ask questions about the uploaded dataset in plain English and get concise answers from a Gemini-backed LLM, with per-session conversational context.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript, ag-Grid Community (ESM via CDN) |
| Backend | Python, FastAPI |
| Data handling | pandas |
| LLM | Google Gemini via `langchain-google-genai` |
| Session state | In-memory dict (per `session_id`) |

## Project Structure

```
.
├── main.py            # FastAPI app: handles /submit (Excel upload + cleaning)
├── query.py            # FastAPI app: handles /generate_response (LLM querying)
├── router.py             # Mounts main.py and query.py apps into one root app
├── imports.py           # Shared imports used across backend modules
├── index.js             # Frontend logic: upload handling, ag-Grid rendering, query calls
├── style.css             # Styling
├── assets/               # Static assets
├── uploadfile.html       # Upload UI
├── requirements.txt      # Python dependencies
└── package.json / package-lock.json  # Frontend dependencies

```

## Setup

### Backend

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root with your Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
3. Run the server (from the directory containing `root.py`):
   ```bash
   uvicorn router:root_app --reload --port 8000
   ```

### Frontend

Serve the HTML/JS files with a local dev server (e.g. VS Code Live Server on `http://127.0.0.1:5500`) — this matches the CORS origins currently configured on the backend.

## API Endpoints

All endpoints are served under `http://127.0.0.1:8000`.

| Method | Path | Description |
|---|---|---|
| `POST` | `/submit` | Accepts an uploaded Excel file (`multipart/form-data`), cleans it with pandas, and returns `{ filename, content }` as JSON records. |
| `POST` | `/query/generate_response` | Accepts `{ query, session_id, file_content }`, runs it through the Gemini model with per-session context, and returns `{ output }` as plain text. |

## Notes

- CORS is currently allow-listed for `http://127.0.0.1:5500` and `http://localhost:3000` — update the `origins` list in `main.py`/`query.py`/`router.py` if you serve the frontend elsewhere.
- Session state (`session_storage`) is in-memory and per-process — it resets on server restart and isn't shared across multiple server instances.
- `router.py` mounts sub-apps by prefix; when adding new mounts, register more specific prefixes (e.g. `/query`) **before** the catch-all `/` mount.
