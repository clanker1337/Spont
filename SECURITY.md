# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| `main`  | Yes       |

## Reporting a vulnerability

Do not open a public issue for security reports. Email the maintainer or use GitHub's
private vulnerability reporting. Include reproduction steps, impact, and a suggested fix if
available.

## Secrets and API keys

- Provider API keys are server-side only. They are read via SvelteKit `$env/dynamic/private`
  and used inside `/api/*` server endpoints.
- Client code must never receive an unrestricted provider key.
- No key is ever committed. `.env` is gitignored. `.env.example` contains only placeholders.
- CI runs in demo mode and does not require real keys.
- Treat every provider response as untrusted input and validate it at the adapter boundary
  with Zod.

## Location privacy

- Browser geolocation is requested only after an explicit user action, with an explanation.
- Manual location entry (city/neighborhood/address) is always supported without permission.
- Precise coordinates are not mandatory and are not persisted in the MVP.
- Avoid logging precise coordinates, provider credentials, or sensitive request data.

## Dependencies

- Lockfile is committed and CI installs from it (`npm ci`).
- Dependency review runs on pull requests where supported.
- A secret-scan step runs in CI.
