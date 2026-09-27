# n8n Track (Weeks 14-16)

This folder contains starter workflows for AI + automation integration.

## Why n8n
- High demand in startups and product teams
- Fast prototyping of trigger-action flows
- Easy integration with Python services via HTTP nodes
- Self-hostable and open source

## Local setup (Docker)
1. Install Docker Desktop.
2. Start n8n:
   - `docker run -it --rm --name n8n -p 5678:5678 -v $HOME/.n8n:/home/node/.n8n n8nio/n8n`
3. Open `http://localhost:5678`.

## Import starter flow
1. Open n8n editor.
2. Import JSON from `automation/n8n/workflows/hello_webhook_to_python.json`.
3. Activate workflow.
4. Call webhook endpoint and inspect output.

## Learning goals for this track
- Build robust webhook-driven automation
- Add retries and idempotency checks
- Integrate n8n with Python agent APIs
- Route failed tasks to review queues
