#!/usr/bin/env python3
"""v3 — кинематографичный монтаж ≈70 с по тактам музыки (104 BPM, такт 2,31 с).
Три акта: подход (дыхание) → детали (на доли) → внутри (полёт + медленный пол) → вечер (медленно).
Прямые склейки на долях, наплывы только на смене состояния (день→вечер, снаружи→внутрь).
Без субтитров; подпись только у планировки; финальный титр обязателен по ТЗ.
Запуск: bash 05_output/build.sh v3 [--draft]"""
import json, subprocess, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__))+"/..")
FF="_work/ffmpeg"; DRAFT="--draft" in sys.argv
BEAT=60/104; BAR=BEAT*4
MUSIC=("04_audio/music/punch-deck-ethereal.mp3",2.0)   # Ethereal — ровный, без кульминаций
# (id, source, длина в тактах, скорость, наплыв ПЕРЕД кадром в секундах (0 = прямая склейка))
SHOTS=[
 ("S01","03_clips/v2/S01.mp4",2.5,0.85,0),
 ("S02","03_clips/v2/S02.mp4",1.5,1.0,0),
 ("S03","03_clips/v2/S03.mp4",2.0,1.0,0),
 ("S13","03_clips/v2/S13.mp4",1.5,1.0,0),
 ("S04","03_clips/v2/S04.mp4",1.0,1.15,0),
 ("S15","03_clips/v2/S15.mp4",1.0,1.15,0),
 ("S06","03_clips/S06_brick_timber_joint.mp4",1.5,1.0,0),
 ("S05","03_clips/v2/S05.mp4",1.5,1.0,1.5),     # день → ранний вечер: наплыв
 ("S07","03_clips/v2/S07.mp4",1.5,1.0,0.6),
 ("S16","03_clips/S16_floor_plan_7s.mp4",2.5,1.0,1.2),   # план: наплыв внутрь и наружу
 ("S08","03_clips/v3/S08_slow.mp4",2.0,1.0,1.2),
 ("S17","03_clips/v3/S17_slow.mp4",1.5,1.0,0),       # пол — замедлен
 ("S10","03_clips/v2/S10.mp4",1.5,1.0,0),
 ("S09","03_clips/v3/S09_slow.mp4",2.0,1.0,0.6),
 ("S14","03_clips/v3/S14_slow.mp4",2.0,1.0,2.0),     # внутрь → сумерки: наплыв
 ("S11","03_clips/S11_terrace_fire.mp4",2.0,1.0,0.8),
 ("S12","03_clips/v3/S12_ending_10s_v2.mp4",3.5,1.0,2.0),
]
def has_audio(p): return "Audio:" in subprocess.run([FF,"-i",p],capture_output=True,text=True).stderr
n=len(SHOTS); inputs=[]; fc=[]; L=[]
for i,(sid,src,bars,sp,xf) in enumerate(SHOTS):
    inputs+=["-i",src]; ln=bars*BAR+xf
    o=subprocess.run([FF,"-i",src],capture_output=True,text=True).stderr
    d=[l for l in o.splitlines() if "Duration" in l][0].split("Duration:")[1].split(",")[0].strip(); h,mn,sc=d.split(":"); cd=(int(h)*3600+int(mn)*60+float(sc))/sp-0.05
    if ln>cd: print(f"!! {sid}: нужно {ln:.2f} с, клип даёт {cd:.2f} с — укорачиваю"); ln=cd
    L.append(ln)
    slow = "minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:vsbmc=1," if sp<1 else ""
    fc.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS/{sp},{slow}trim=0:{ln:.3f},setpts=PTS-STARTPTS,fps=24,settb=1/24,format=yuv420p,setsar=1[v{i}]")
    if has_audio(src):
        at = f"atempo={sp}," if sp!=1 else ""
        fc.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{at}atrim=0:{ln:.3f},asetpts=PTS-STARTPTS[a{i}]")
    else: fc.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{ln:.3f}[a{i}]")
starts=[0.0]
for i in range(1,n): starts.append(starts[-1]+L[i-1]-SHOTS[i][4])
total=starts[-1]+L[-1]
prev="v0"
for i in range(1,n):
    xf=SHOTS[i][4]
    if xf>0: fc.append(f"[{prev}][v{i}]xfade=transition=fade:duration={xf}:offset={starts[i]:.3f}[vx{i}]")
    else:    fc.append(f"[{prev}][v{i}]concat=n=2:v=1:a=0,settb=1/24,fps=24[vx{i}]")
    prev=f"vx{i}"
V=prev; prev="a0"
for i in range(1,n):
    xf=max(SHOTS[i][4],0.08)   # звук всегда с микро-кроссфейдом, чтобы не щёлкал
    fc.append(f"[{prev}][a{i}]acrossfade=d={xf}:c1=tri:c2=tri[ax{i}]"); prev=f"ax{i}"
AMB=prev
# финальный титр (обязателен по ТЗ) — последние 5 с
inputs+=["-loop","1","-i","_work/cap3_title.png"]; ti=n
st=total-5.0
fc.append(f"[{ti}:v]format=rgba,fade=t=in:st={st:.2f}:d=1.0:alpha=1[t]")
fc.append(f"[{V}][t]overlay=0:0:enable='gte(t,{st:.2f})'[vt]"); V="vt"
fc.append(f"[{V}]fade=t=out:st={total-1.2:.2f}:d=1.2[vf]"); V="vf"
if not DRAFT:
    fc.append(f"[{V}]lut3d=file=05_output/luts/arch_muted.cube:interp=trilinear,vignette=angle=PI/5:mode=forward,noise=alls=5:allf=t+u[vg]"); V="vg"
    inputs+=["-ss",str(MUSIC[1]),"-i",MUSIC[0]]; mi=n+1
    fc.append(f"[{mi}:a]aresample=48000,atrim=0:{total:.2f},afade=t=in:st=0:d=2.0,afade=t=out:st={total-5:.2f}:d=5,volume=-10dB[mus]")
    fc.append(f"[{AMB}]volume=-11dB[ambq]")
    fc.append(f"[ambq][mus]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=8[aout]")
else:
    fc.append(f"[{AMB}]loudnorm=I=-18:TP=-2:LRA=9[aout]")
out="05_output/v3_draft_9x16.mp4" if DRAFT else "05_output/v3_final_9x16.mp4"
cmd=[FF,"-hide_banner","-loglevel","error","-y"]+inputs+["-filter_complex",";".join(fc),"-map",f"[{V}]","-map","[aout]","-t",f"{total:.2f}","-c:v","libx264","-crf","18","-preset","fast","-threads","0","-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","192k","-movflags","+faststart","-progress","_work/progress.txt","-nostats",out]
print("total %.1f s"%total, "cuts:",[round(s,2) for s in starts])
json.dump({"shots":[s[0] for s in SHOTS],"starts":starts,"len":L,"total":total},open("_work/timeline_v3.json","w"),indent=1)
r=subprocess.run(cmd,capture_output=True,text=True); print(r.returncode,r.stderr[-1200:])
