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
📁 my-fastapi-app/
├── 📁 routers/              # Modular routing components
│   ├── 📄 __init__.py       # Initializes APIRouter() object "router"
│   ├── 📄 data.py           # Handles /submit (Excel upload & cleaning)
│   └── 📄 query.py          # Handles /generate_response (LLM querying)
│
├── 📁 assets/               # Static images and icons
├── 📄 main.py               # FastAPI application entry point
├── 📄 imports.py            # Shared imports used across backend modules
│
├── 📄 uploadfile.html       # Frontend UI template
├── 📄 index.js              # Frontend logic (upload handling, ag-Grid, API calls)
├── 📄 style.css             # Application styling and layout
│
├── 📄 requirements.txt      # Python dependencies
└── 📄 package.json          # Node.js dependencies & scripts

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
3. Run the server (from the directory containing `router.py`):
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

- Session state (`session_storage`) is in-memory and per-process — it resets on server restart and isn't shared across multiple server instances.

## Planned future features:

- Actual chart generation
- Chart export
- Persistent storage and user profile storage
- Multi-file support
- Real-time changes on editing grid
