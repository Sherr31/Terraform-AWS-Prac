#!/usr/bin/env python3
"""Simple Flask demo app for Terraform + AWS EC2 practice."""

import os
import platform
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Terraform AWS Demo</title>
  <style>
    :root {
      --bg: #0b1220;
      --panel: #121a2b;
      --text: #e8eefc;
      --muted: #9aa8c7;
      --accent: #3dd6c6;
      --accent-2: #5b8cff;
      --line: rgba(255, 255, 255, 0.08);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      min-height: 100vh;
      font-family: "Segoe UI", system-ui, sans-serif;
      color: var(--text);
      background:
        radial-gradient(900px 500px at 10% -10%, rgba(61, 214, 198, 0.18), transparent 55%),
        radial-gradient(700px 400px at 100% 0%, rgba(91, 140, 255, 0.16), transparent 50%),
        var(--bg);
      display: grid;
      place-items: center;
      padding: 2rem 1rem;
    }

    .shell {
      width: min(720px, 100%);
      background: color-mix(in srgb, var(--panel) 92%, white 8%);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 2rem;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      font-size: 0.8rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 1rem;
    }

    .badge::before {
      content: "";
      width: 0.55rem;
      height: 0.55rem;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 0 4px rgba(61, 214, 198, 0.2);
    }

    h1 {
      font-size: clamp(1.7rem, 4vw, 2.3rem);
      line-height: 1.15;
      margin-bottom: 0.75rem;
    }

    p.lead {
      color: var(--muted);
      line-height: 1.6;
      margin-bottom: 1.5rem;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 0.85rem;
      margin-bottom: 1.5rem;
    }

    .card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 0.9rem 1rem;
    }

    .card span {
      display: block;
      color: var(--muted);
      font-size: 0.78rem;
      margin-bottom: 0.35rem;
    }

    .card strong {
      font-size: 0.98rem;
      word-break: break-all;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
    }

    a.btn {
      text-decoration: none;
      color: #041018;
      background: linear-gradient(135deg, var(--accent), #7be7db);
      padding: 0.7rem 1.1rem;
      border-radius: 999px;
      font-weight: 600;
      font-size: 0.92rem;
    }

    a.btn.secondary {
      color: var(--text);
      background: transparent;
      border: 1px solid var(--line);
    }

    footer {
      margin-top: 1.5rem;
      color: var(--muted);
      font-size: 0.82rem;
    }
  </style>
</head>
<body>
  <main class="shell">
    <div class="badge">Live on AWS EC2</div>
    <h1>Terraform + Flask demo is up</h1>
    <p class="lead">
      This app was provisioned by Terraform onto an Ubuntu EC2 instance.
      Use it to verify VPC, security group, and remote-exec wiring.
    </p>

    <section class="grid">
      <div class="card">
        <span>Hostname</span>
        <strong>{{ hostname }}</strong>
      </div>
      <div class="card">
        <span>Private IP</span>
        <strong>{{ private_ip }}</strong>
      </div>
      <div class="card">
        <span>Python</span>
        <strong>{{ python_version }}</strong>
      </div>
      <div class="card">
        <span>UTC time</span>
        <strong>{{ utc_now }}</strong>
      </div>
    </section>

    <div class="actions">
      <a class="btn" href="/health">Health check</a>
      <a class="btn secondary" href="/api/info">JSON info</a>
    </div>

    <footer>Region target: us-east-1 · Port 80 · Provisioners practice lab</footer>
  </main>
</body>
</html>
"""


def _private_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "unavailable"


@app.get("/")
def home():
    return render_template_string(
        PAGE,
        hostname=socket.gethostname(),
        private_ip=_private_ip(),
        python_version=platform.python_version(),
        utc_now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.get("/health")
def health():
    return jsonify(status="ok", service="terraform-aws-demo"), 200


@app.get("/api/info")
def info():
    return jsonify(
        {
            "app": "terraform-aws-demo",
            "hostname": socket.gethostname(),
            "private_ip": _private_ip(),
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "pid": os.getpid(),
            "utc_now": datetime.now(timezone.utc).isoformat(),
        }
    )


if __name__ == "__main__":
    # Port 80 matches the security group in main.tf; sudo is used by remote-exec.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "80")))
