Backend package structure for greenwash-auditor

Structure:

backend/
  app/
    agents/     # agent implementations
    tools/      # integration utilities
    services/   # business logic
    models/     # data models and schemas
    memory/     # memory / persistence helpers
  api/          # HTTP API modules or routers
  core/         # config, settings, utilities
  tests/        # unit/integration tests
  main.py       # entrypoint FastAPI app

How to run (dev):

1. Create a virtualenv and install dependencies (if requirements provided):

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Start the server:

   uvicorn backend.main:app --reload --port 8000

Notes:
- Add modules under `app` as your implementation grows.
- `tests/test_smoke.py` checks importability of `backend.main`.
