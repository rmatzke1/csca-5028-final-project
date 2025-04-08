# Web UI

## Development

Create a new file called `.env` in the `applications/web-ui` directory. Fill in with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Install dependencies and run in development mode:
```
Windows
------------------------------------
cd applications\web-ui
npm install
npm run dev

Mac/Linux
------------------------------------
cd applications/web-ui
npm install
npm run dev
```

Note: The rest-api application must be running for the frontend web UI to function correctly.
