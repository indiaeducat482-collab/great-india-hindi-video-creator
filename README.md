# Great India Hindi AI Video Creator

Repository: `great-india-hindi-video-creator`

## What this version does
1. Website URL + Hindi instructions are entered in `index.html`.
2. Create Video downloads `video-job.json`.
3. GitHub Actions opens the website with Playwright and captures screenshots.
4. Gemini analyzes the screenshots + your instructions and creates natural Hindi narration/scenes.
5. Google Cloud Text-to-Speech creates Hindi audio.
6. FFmpeg combines screenshots + Hindi narration into an MP4.
7. GitHub Actions publishes the MP4 as a GitHub Release asset.
8. `Check Video Again` finds the MP4 and activates the direct Download Video button.

## Required GitHub Secrets
Repository → Settings → Secrets and variables → Actions → New repository secret:

- `GEMINI_API_KEY`
- `GOOGLE_TTS_API_KEY`

Never put either key in `index.html`.

## Run
1. Push all files to the `main` branch.
2. Open Actions → **Build Hindi AI Video** → Run workflow.
3. Paste the complete `video-job.json` content into `job_json`.
4. Run the workflow and wait for it to finish.
5. Open the Pages site and click **Check Video Again**.
6. Click **Download Video**.

## Important
The website page cannot safely contain a GitHub token, so this GitHub-only version uses a manual Actions run. The final MP4 is public through the GitHub Release asset when the repository/release is public.
