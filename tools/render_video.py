import json, os, subprocess, sys, textwrap, re
j=json.load(open(sys.argv[1],encoding='utf-8')); os.makedirs('output',exist_ok=True)
title=j.get('title','Website Tutorial')
script=j.get('script','') or 'Hindi website tutorial'
# Escape FFmpeg drawtext characters.
def esc(s):
    return s.replace('\\','\\\\').replace(':','\\:').replace("'","\\'").replace('%','\\%')
lines=textwrap.wrap(script, 46)[:18]
text='\\n'.join(lines)
font='/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf'
if not os.path.exists(font): font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
vf=f"drawtext=fontfile={font}:text='{esc(title)}':fontsize=42:x=60:y=55:fontcolor=white,drawtext=fontfile={font}:text='{esc(text)}':fontsize=27:x=60:y=140:fontcolor=white:line_spacing=12"
subprocess.run(['ffmpeg','-y','-f','lavfi','-i','color=c=0x111827:s=1280x720:r=30','-t','20','-vf',vf,'-an','-pix_fmt','yuv420p','-movflags','+faststart','output/hindi-tutorial.mp4'],check=True)
