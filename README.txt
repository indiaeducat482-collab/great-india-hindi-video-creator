Great India Cartoon Video Builder
=================================

UPDATED FEATURES
- TXT/MD script upload or paste.
- Script is split into scenes.
- Each scene now shows a drawn cartoon human character (not only an emoji).
- Cartoon environment, movement, speech bubble and scene timeline.
- Hindi narration during Preview using the browser's Hindi SpeechSynthesis voice.
- Voice speed and Hindi voice selection.
- Create Video renders the cartoon scenes to WebM.
- Download Video button is included.

IMPORTANT VOICE NOTE
Browser SpeechSynthesis audio cannot be captured into the canvas MediaRecorder stream by normal web APIs. Therefore the downloaded WebM from this offline version contains the cartoon video but not the browser Hindi voice. The Preview button DOES speak the Hindi script.

For a final MP4 with embedded Hindi narration, the next upgrade should connect a server-side TTS API (for example Google Cloud TTS, Azure Speech, ElevenLabs, or another TTS provider), then mux the returned audio with the rendered video.

HOW TO USE
1. Open index.html in Chrome/Edge.
2. Upload a Hindi .txt file or paste Hindi script.
3. Click "Script से Cartoon Scenes बनाएं".
4. Click "Preview + Hindi Voice" to see the cartoon and hear Hindi narration.
5. Click "Create Video" to render the cartoon WebM.
6. Click "Download Video".
