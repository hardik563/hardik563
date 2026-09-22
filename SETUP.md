# Hardik Dhamija GitHub Profile — Setup

## Automatic profile refresh

The repository uses one main workflow: **Profile Refresh**.

It automatically regenerates:
- GitHub contribution data and heatmaps
- dark animated contribution Snake GIF
- self-hosted 3D contribution visuals
- skyline/city contribution visuals
- live README sections
- local stats cards

It uses `GITHUB_TOKEN`; no third-party metrics token is required for the core profile.

## Interactive Lucknow 3D

The `city/` folder is deployed to GitHub Pages by `Deploy Interactive 3D Lucknow`.
The scene is a real-time Three.js 3D model inspired by Lucknow landmarks, with:
- Rumi Darwaza-inspired gateway
- Bara Imambara-inspired complex
- Gomti River
- Hazratganj-style roads and lamps
- animated traffic
- animated building lights
- day/night lighting cycle
- orbit, zoom and pan controls

Enable **Settings → Pages → Source: GitHub Actions** once if GitHub Pages has not been enabled for this repository.

The README button then opens:
`https://hardik563.github.io/hardik563/`

## Contribution Snake

`assets/contribution-snake.gif` is generated automatically by `scripts/generate_snake_gif.py`.
The workflow reads Hardik's GitHub contribution calendar through the GitHub GraphQL API and rebuilds the dark animation automatically.

No token value should be pasted into the repository or into chat.

## Optional WakaTime

`WakaTime Weekly Stats` runs only when `WAKATIME_API_KEY` is configured. It is optional and does not affect the core profile.
