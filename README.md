# Great India Hindi Video Creator

Repository: `great-india-hindi-video-creator`

## Fixed video download flow
1. Open GitHub Pages and enter title, URL and Hindi script.
2. Click **Create Video**. This downloads `video-job.json`.
3. GitHub → Actions → **Build Hindi Video** → Run workflow → paste the JSON.
4. Wait for the workflow to become green.
5. Return to the website and click **Check Video Again**.
6. The latest GitHub Release MP4 is detected automatically and **Download Video** becomes active.

The workflow publishes `output/hindi-tutorial.mp4` as a GitHub Release asset, not as an Actions artifact. The Pages site reads the public latest release and uses its real `browser_download_url`.

## Important
A GitHub Pages static website cannot securely start a GitHub Actions workflow by itself because that would require exposing a GitHub token in the browser. Therefore the safe GitHub-only flow uses the Actions Run workflow screen for the build trigger.
