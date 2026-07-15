# Security Policy

## Supported versions

ViralMint is a desktop / local-first application. Only the latest release on `main` receives security fixes.

## Reporting a vulnerability

If you believe you've found a security vulnerability in ViralMint, please **do not** open a public GitHub issue. Instead, report it privately by opening a [GitHub Security Advisory](https://github.com/openclaw-easy/ViralMint/security/advisories/new) — that surfaces the report only to the maintainers and lets us coordinate a fix before public disclosure.

Please include:

- A description of the vulnerability
- Steps to reproduce
- The version / commit you tested against
- Any proof-of-concept code or screenshots

We will acknowledge receipt within 7 days and provide a status update within 14 days. We aim to release a fix within 30 days for critical issues.

## Scope

In scope:

- The ViralMint backend (FastAPI, agents, services)
- The ViralMint frontend (React app served by FastAPI)
- The launcher (`run.py`, `launcher.py`)
- Encrypted storage logic (`backend/core/crypto.py`)

Out of scope (please report to the upstream project):

- Issues in third-party dependencies (yt-dlp, FFmpeg, faster-whisper, etc.)
- Issues in external API providers (Anthropic, OpenAI, Pexels, etc.)
- Issues that require physical access to the user's machine

## What we treat as a security issue

- Credential leakage (storing keys in plaintext, logging keys, etc.)
- Path traversal in storage / file-serving endpoints
- Server-side request forgery (SSRF) via user-supplied URLs
- Authentication bypass on OAuth callback flows
- Cross-site scripting (XSS) in the frontend
- Cross-site request forgery (CSRF) on state-changing endpoints
- Remote code execution (RCE) via malformed input

## What we do **not** consider a security issue

- Self-XSS that requires the user to paste attacker-supplied JavaScript
- Issues that require the attacker to already control the user's machine
- Missing security headers on `localhost` (the default deployment target)

Thanks for helping keep ViralMint safe.
