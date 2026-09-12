# Great India Hindi Video Creator

Repository name: `great-india-hindi-video-creator`

## GitHub Pages
Settings → Pages → Deploy from branch → `main` → `/(root)`.

## Video flow
1. Enter title, website URL and Hindi script.
2. Upload website screenshot/photo.
3. Click Create Video and download `video-job.json`.
4. GitHub → Actions → Build Hindi Video → Run workflow → paste the JSON.
5. Workflow creates MP4 and publishes it automatically as a GitHub Release asset.

The Release asset gives a real MP4 URL that can be used by a Download Video button.

Important: this V1 renderer is a working MP4 pipeline foundation. Natural AI Hindi narration and automatic website understanding require Gemini/TTS APIs and should be connected server-side using GitHub Secrets, never in `index.html`.
