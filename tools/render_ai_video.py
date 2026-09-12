import base64, json, os, re, subprocess, sys, textwrap, time
from pathlib import Path
import requests
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
job=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
url=job.get('url','').strip(); user_script=job.get('script','').strip(); title=job.get('title','Website Tutorial').strip(); kind=job.get('type','short')
if not url.startswith(('http://','https://')): raise SystemExit('Invalid URL')

def capture():
    shots=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1280,'height':720}, device_scale_factor=1)
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=45000)
            page.wait_for_timeout(5000)
            page.screenshot(path=str(OUT/'site-1.png'), full_page=False)
            shots.append(OUT/'site-1.png')
            page.evaluate('window.scrollTo(0, Math.max(0, document.body.scrollHeight/2))')
            page.wait_for_timeout(1200)
            page.screenshot(path=str(OUT/'site-2.png'), full_page=False)
            shots.append(OUT/'site-2.png')
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(1200)
            page.screenshot(path=str(OUT/'site-3.png'), full_page=False)
            shots.append(OUT/'site-3.png')
        except Exception as e:
            print('Browser capture warning:',e)
        finally: browser.close()
    if not shots: raise SystemExit('Could not capture website')
    return shots
shots=capture()

def gemini():
    parts=[{'text':f'''You are a professional Hindi website tutorial video narrator. Create a concise, accurate Hindi narration for this website.
Website URL: {url}
User instructions/script: {user_script}
Video type: {kind}
Use only information visibly supported by the screenshots plus the user's instructions. Do not invent buttons, prices, features, login details, or facts. Explain the likely user flow step-by-step. If the screenshots do not prove a detail, phrase it as an instruction from the user's script rather than a factual claim.
Return ONLY valid JSON with keys: narration, scenes. narration is natural spoken Hindi, 90-180 words for short and 180-350 for full. scenes is an array of 3-6 objects with title and text. Keep Hindi simple and suitable for TTS.'''}]
    for s in shots:
        data=base64.b64encode(s.read_bytes()).decode()
        parts.append({'inline_data':{'mime_type':'image/png','data':data}})
    key=os.environ['GEMINI_API_KEY']
    endpoint='https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key='+key
    r=requests.post(endpoint,json={'contents':[{'parts':parts}],'generationConfig':{'temperature':0.2,'responseMimeType':'application/json'}},timeout=90)
    r.raise_for_status(); txt=r.json()['candidates'][0]['content']['parts'][0]['text']
    txt=re.sub(r'^```json\s*|\s*```$','',txt.strip(),flags=re.I)
    return json.loads(txt)
try: ai=gemini()
except Exception as e:
    print('Gemini warning:',e)
    ai={'narration':user_script,'scenes':[{'title':'Website Tutorial','text':user_script}]}

narration=ai.get('narration') or user_script
(OUT/'narration.txt').write_text(narration,encoding='utf-8')
(OUT/'scenes.json').write_text(json.dumps(ai.get('scenes',[]),ensure_ascii=False,indent=2),encoding='utf-8')

# Google Cloud Text-to-Speech REST API. API key is kept only in GitHub Secrets.
tts_key=os.environ['GOOGLE_TTS_API_KEY']
tts_url='https://texttospeech.googleapis.com/v1/text:synthesize?key='+tts_key
payload={'input':{'text':narration},'voice':{'languageCode':'hi-IN','name':'hi-IN-Wavenet-A'},'audioConfig':{'audioEncoding':'MP3','speakingRate':0.95}}
r=requests.post(tts_url,json=payload,timeout=90)
r.raise_for_status(); audio=base64.b64decode(r.json()['audioContent']); (OUT/'narration.mp3').write_bytes(audio)

# Make a simple tutorial video: website screenshots + Hindi narration + readable scene text.
# Duration follows narration; screenshots are looped/concatenated.
scene_text='\\n'.join([f"{i+1}. {x.get('title','')} - {x.get('text','')}" for i,x in enumerate(ai.get('scenes',[]))])
scene_text=re.sub(r"[\\\"']",'',scene_text)
scene_text=scene_text[:1800]
# Normalize screenshots to 1280x720 and make a 3-image concat sequence, then loop as needed.
for i,s in enumerate(shots,1):
    subprocess.run(['ffmpeg','-y','-i',str(s),'-vf',"scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1",'-frames:v','1',str(OUT/f'frame{i}.png')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
# 6-second clips, concat, then trim to audio duration.
concat=OUT/'concat.txt'; concat.write_text('\n'.join([f"file '{OUT/f'frame{i}.png'}'\nduration 6" for i in range(1,len(shots)+1)])+f"\nfile '{OUT/f'frame{len(shots)}.png'}'\n",encoding='utf-8')
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-vf',"format=yuv420p,drawbox=x=0:y=0:w=iw:h=120:color=black@0.65:t=fill,drawtext=fontfile=/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf:text='"+title.replace("'",'')+"':fontsize=38:x=45:y=35:fontcolor=white",'-r','30','-pix_fmt','yuv420p',str(OUT/'silent.mp4')],check=True)
# Get audio duration and trim video to it.
dur=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(OUT/'narration.mp3')],text=True).strip()
subprocess.run(['ffmpeg','-y','-stream_loop','-1','-i',str(OUT/'silent.mp4'),'-i',str(OUT/'narration.mp3'),'-t',dur,'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast','-c:a','aac','-b:a','128k','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'hindi-ai-tutorial.mp4')],check=True)
print('Created',OUT/'hindi-ai-tutorial.mp4')
