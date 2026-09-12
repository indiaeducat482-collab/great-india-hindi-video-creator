import json,os,subprocess,sys,textwrap
j=json.load(open(sys.argv[1],encoding='utf-8'));os.makedirs('output',exist_ok=True)
title=j.get('title','Website Tutorial').replace("'",'')
script=j.get('script','').replace("'",'')
lines=textwrap.wrap(script,48)[:18] or ['Hindi website tutorial']
txt='\\n'.join(lines).replace(':','\\:')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
vf=f"drawtext=fontfile={font}:text='{title}':fontsize=42:x=60:y=55:fontcolor=white,drawtext=fontfile={font}:text='{txt}':fontsize=27:x=60:y=140:fontcolor=white:line_spacing=12"
subprocess.run(['ffmpeg','-y','-f','lavfi','-i','color=c=0x111827:s=1280x720:r=30','-t','20','-vf',vf,'-an','-pix_fmt','yuv420p','output/hindi-tutorial.mp4'],check=True)
