# Hardik Dhamija GitHub Profile — Setup Guide

This repository is a customized version of the supplied reference profile repository, prepared for `hardik563`.

## 1. Create the profile repository
Create a **public** repository named exactly `hardik563` under the GitHub account `hardik563`.

## 2. Upload this repository
Upload/push all files from this folder into that repository. Keep the `.github` folder and workflow files.

## 3. Important workflow permissions
In the repository go to **Settings → Actions → General** and make sure workflows are allowed to run and that **Workflow permissions** allow read and write access where available.

## 4. Run the workflows
After the first push, open **Actions** and run these manually once:
- `Profile Refresh` — generates the live stats, contribution heatmaps, skyline/city visuals, and 3D profile from GitHub GraphQL.
- `Generate Snake and Dragon` — publishes the snake and dragon animations to the `output` branch.
- `Update README` — refreshes activity and other lightweight README sections.

The old `Metrics`, `3D Profile Contributions`, and `PortfolioCraft` workflows were removed because they depended on external services/actions that were causing the broken API/error cards shown in the reference profile. The new profile assets are self-hosted in this repository.

## 5. Optional WakaTime
WakaTime is optional. The WakaTime workflow is configured to skip itself unless `WAKATIME_API_KEY` exists. If you want WakaTime statistics, add that repository secret later.

## 6. Personal links already configured
- GitHub: https://github.com/hardik563
- LinkedIn: https://www.linkedin.com/in/hardik-dhamija-35932228b/
- LeetCode: https://leetcode.com/u/hardikdhamija_/
- Codolio: https://codolio.com/profile/hardikdhamija

## 7. Do not add secrets to README or source files
Use GitHub repository **Secrets and variables → Actions** for API keys/tokens. Never paste a personal access token into a YAML file.
