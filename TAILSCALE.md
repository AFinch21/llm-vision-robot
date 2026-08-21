# Private robot access with Tailscale

The production setup runs FastAPI on the Jetson and lets FastAPI serve the
built Vue app. Tailscale Serve provides the private HTTPS URL and proxies both
normal HTTP traffic and the WebSocket connection to FastAPI.

## 1. Join the Jetson to the tailnet

Run on the Jetson:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Open the authentication URL printed by `tailscale up`, sign in with the same
account used for the Tailscale admin console, and confirm that the Jetson appears
on the Machines page.

Give it a stable, memorable name:

```bash
sudo tailscale set --hostname=tomoro-bot
tailscale status
```

Install Tailscale on the Mac and sign in to the same account. Confirm the
private connection from the Mac:

```bash
ping tomoro-bot
ssh YOUR_JETSON_USER@tomoro-bot
```

This uses the existing SSH server; enabling the separate Tailscale SSH feature
is not required.

## 2. Build and run the app on the Jetson

From the repository checkout on the Jetson:

```bash
cd frontend/tomoro-bot
npm ci
npm run build

cd ../../backend
uv run uvicorn main:app --host 127.0.0.1 --port 8000
```

FastAPI detects `frontend/tomoro-bot/dist` at startup and serves the Vue app.
Verify it locally in a second Jetson terminal:

```bash
curl http://127.0.0.1:8000/api/health
```

The expected response is `{"status":"ok"}`.

## 3. Publish it privately within Tailscale

Run on the Jetson:

```bash
tailscale serve --bg 8000
tailscale serve status
```

The first command may print a browser URL asking for permission to enable HTTPS
for the tailnet. Approve it. It then prints the private HTTPS URL, similar to:

```text
https://tomoro-bot.your-tailnet.ts.net
```

Open that URL on the Mac while Tailscale is connected. The browser loads Vue
over HTTPS and Vue automatically connects to `wss://<same-host>/ws`.

`--bg` makes the Tailscale proxy survive logout and reboot. FastAPI still needs
to be configured as a system service separately before the whole application
will start automatically after reboot.

## Local frontend development

`npm run dev` defaults to a backend on port 8000 of the same machine. To run
Vite on the Mac while FastAPI runs on the Jetson, override the WebSocket URL:

```bash
VITE_WEBSOCKET_URL=ws://tomoro-bot:8000/ws npm run dev
```

For this development-only route, start Uvicorn with `--host 0.0.0.0` so it can
accept connections directly over Tailscale. The production Serve setup should
keep Uvicorn bound to `127.0.0.1`.
