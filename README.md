# Great India Hindi Video Creator — Tested Voice Recording Fix

Added **Start Recording with Tested Voice**.

- Uses the Hindi Voice Test text.
- Starts screen/tab recording after permission.
- Does not request microphone for this mode.
- For no outside sound, select **This Tab** and enable **Share tab audio**.
- Output is WebM in the browser.

Note: browser speechSynthesis audio capture depends on the browser. If the tested speech is not captured in tab audio, use the normal recorded/uploaded voice option or a fixed TTS audio provider.


## New recording resume feature
- Pause Recording: temporarily pauses the same MediaRecorder session.
- Continue Recording: resumes from the paused point.
- In Tested Voice mode, browser speech synthesis is paused/resumed together with the recording.
- Stop & Finish finalizes one WebM recording.
- Tested voice speed is set to 0.75x.
- This is a browser-only implementation; exact speechSynthesis audio capture still depends on the browser and tab-audio permission.
