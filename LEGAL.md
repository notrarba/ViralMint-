# Legal & Terms of Use

ViralMint is a personal tool you run on your own machine. It does not host
your content, route your traffic through a ViralMint server, or make API
calls on your behalf. **You are the operator of every action it performs**,
which means you are responsible for ensuring those actions comply with the
laws and terms of service that apply to you.

This document is **not legal advice**. It is a plain-language explanation of
the obligations that come with using ViralMint, and the framing the
maintainers expect users to operate under.

## What ViralMint is for

ViralMint is intended for **creators managing their own content and content
they have rights to use**. Typical legitimate uses:

- Mirroring videos you uploaded yourself for backup or repurposing.
- Generating new videos from your own scripts, voices, and licensed footage.
- Researching public trends and your own channel performance via official
  APIs (YouTube Data API, TikHub, etc.).
- Posting to your own social accounts via the platforms' official OAuth
  upload flows.

## What ViralMint is *not* for

Do not use ViralMint to:

- Download copyrighted content you do not have the rights to redistribute,
  modify, or republish.
- Bypass DRM, geo-blocks, paywalls, or other access controls.
- Operate fake accounts, scraped scout data, or automation in ways that
  violate any platform's Terms of Service.
- Impersonate other channels, brands, or people.
- Generate or distribute content that is illegal where you live or where
  your audience is.

Violating any of the above is **your responsibility**, not the maintainers'.

## Platform-specific notes

ViralMint integrates with several third-party platforms. Each has its own
Terms of Service that you remain bound by. Read them before enabling the
related features.

### YouTube

- **Scouting / channel analytics:** uses the official YouTube Data API v3
  with your own API key. Stays within YouTube's Terms when you stay within
  your daily quota and don't redistribute the data.
  Terms: https://www.youtube.com/static?template=terms
  Developer Policies: https://developers.google.com/youtube/terms/developer-policies
- **Uploading:** uses YouTube's official OAuth + upload API. Sanctioned use.
  You must comply with YouTube's Community Guidelines for the content you
  upload.

### TikTok

- **Uploading via OAuth (recommended):** uses TikTok's official Content
  Posting API. Sanctioned use.
- **Uploading via session cookie (advanced / discouraged):** the
  `tiktok-uploader` library acts as your browser. **This is against TikTok's
  Terms of Service.** It exists as a fallback for users who can't get
  Content Posting API approval. Use at your own risk; TikTok may suspend
  the account associated with the cookie.
- **Scouting via session cookie:** same as above — your TikTok account is
  the actor and TikTok's Terms apply. **Prefer the TikHub API path**, which
  is built on TikTok's own data-licensing partners.
  Terms: https://www.tiktok.com/legal/terms-of-service

### Douyin

- **Scouting via session cookie** is in the same category as TikTok cookie
  scouting and carries the same risk. There is currently no official
  Douyin developer API for non-mainland-China developers. Use only if you
  have a legitimate Douyin account and accept that account's risk profile.

### Pexels

- Uses the official Pexels API with your own key. Free for both personal
  and commercial use under the Pexels License.
  License: https://www.pexels.com/license/

### yt-dlp (Universal Downloader)

ViralMint uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download videos
from 1000+ sites. yt-dlp is an open-source library; ViralMint is not
affiliated with it. **Downloading a video does not give you rights to
redistribute or remix it.** Use the downloader on:

- Content you uploaded yourself.
- Content licensed under Creative Commons, public domain, or similar
  permissive terms.
- Content for which you have a written license from the rights holder.
- Content you are downloading for fair-use research / commentary / parody
  *as defined by your local law*. Fair use is jurisdiction-specific; talk
  to a lawyer if unsure.

ViralMint will not block you from downloading copyrighted material — it has
no way to know the license of an arbitrary URL. That doesn't make it legal
for you to do so.

## Trademarks

"YouTube", "TikTok", "Douyin", "Pexels", "Instagram", "Telegram",
"WhatsApp", "Discord", "Slack", and any related logos are trademarks of
their respective owners. ViralMint is not affiliated with, endorsed by, or
sponsored by any of these companies. Where their names appear in the
ViralMint UI or docs, it is solely to describe interoperability.

## DMCA / takedown

ViralMint is a tool, not a service. The maintainers do not host any of your
content, scraped data, downloaded videos, or uploaded videos. If you
believe a ViralMint user has infringed your copyright, you must contact
that user or the platform where the infringing content is hosted.

If you believe the **ViralMint source code itself** infringes your
copyright, file a DMCA notice with GitHub:
https://docs.github.com/en/site-policy/content-removal-policies/dmca-takedown-policy

## No warranty

ViralMint is licensed under AGPL-3.0 and provided **AS IS**, without
warranty of any kind. See [LICENSE](LICENSE) sections 15–17. The
maintainers are not liable for any account suspensions, content takedowns,
data loss, billing charges from third-party APIs, or other consequences of
your use of the software.

## Reporting concerns

- **Security vulnerabilities:** see [SECURITY.md](SECURITY.md).
- **License or trademark concerns about ViralMint itself:** open a GitHub
  issue or contact the maintainers via the address listed at
  [viralmint.net](https://viralmint.net).
- **Content posted to a third-party platform by a ViralMint user:** contact
  that platform directly. The maintainers cannot remove content the
  software did not host.
