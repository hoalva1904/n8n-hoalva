# -*- coding: utf-8 -*-
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as RC
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PI, ImageDraw as ID
import textwrap,json,sys,base64,os,random,math,subprocess
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
FN,FNB='DV','DVB'
NAVY=HexColor('#0D1B2A');GOLD=HexColor('#C8A96E');GOLD2=HexColor('#E8D090')
GRAY=HexColor('#7A7875');DIM=HexColor('#B8B6B2');WHITE=HexColor('#FFFFFF')
STEEL=HexColor('#1A3050');DARK=HexColor('#071520');MID=HexColor('#091D35');ACC=HexColor('#1A3A55')
d=json.loads(base64.b64decode(sys.argv[1]).decode())
TITLE=d['title'];EXCERPT=d['excerpt'];SLUG=d['slug']
ORIG_URL=d['orig_url'];PUB_DATE=d.get('pub_date','')
STATS3=d['stats'];CHART_D=d['chart'];INFO=d['info_data'];CHART_SRC=d.get('chart_source','')
TAGLINE=d['tagline'];TITLE_LINE=d['title_line'];S4H=d['s4h'];S5H=d['s5h'];S3H=d['s3h']
CTA=d['cta'];PDF_PATH=d['pdf_path'];PNG_PATH=d['png_path']
SOURCE=d['source'];KEY_FACT=d['key_fact'];DTXT=PUB_DATE[:10] if PUB_DATE else str(INFO.get('date',''))
ACTIONS_RAW=d['actions'];INSIGHT=str(INFO.get('insight',EXCERPT))
W=220*mm;PAD=8*mm;INNER=W-2*PAD;GAP=7*mm;DIVH=8*mm
PORT_H=58*mm;STATS_H=26*mm;SEC_HDR=13*mm
def smart_lines(text,fs,max_w_mm,max_lines=None):
    cpl=max(10,int(max_w_mm/(fs*0.515)));lines=textwrap.wrap(str(text),width=cpl)
    if max_lines and len(lines)>max_lines:
        sentences=[s.strip() for s in str(text).replace('—','.').split('.') if len(s.strip())>8]
        bullets=[]
        for s in sentences[:max_lines]:
            for ln in textwrap.wrap('- '+s,width=cpl):bullets.append(ln)
        return bullets[:max_lines+2]
    return lines
FS_IN=10.5;LH_IN=7.8*mm
in_lines=smart_lines(INSIGHT,FS_IN,(INNER-10)/mm,max_lines=12)
BOX_IN_H=max(len(in_lines)*LH_IN+26*mm,40*mm)
ICON_W=28*mm;TX=PAD+3.5*mm+ICON_W+5*mm;TW=W-TX-PAD;FS_ACT=10;LH_ACT=6.8*mm
act_data=[]
for a in ACTIONS_RAW:
    n2=str(a.get('num','01'));t2=str(a.get('title',''));desc2=str(a.get('desc',a.get('action','')))
    ls=smart_lines(desc2,FS_ACT,TW/mm,max_lines=5);h2=max(len(ls)*LH_ACT+26*mm,32*mm);act_data.append((n2,t2,ls,h2))
ACT_TOTAL=sum(h2 for _,_,_,h2 in act_data)+len(act_data)*3*mm
CHART_H=50*mm;FOOTER_H=30*mm
H=(PORT_H+GAP+STATS_H+GAP+DIVH+SEC_HDR+BOX_IN_H+GAP+DIVH+SEC_HDR+ACT_TOTAL+GAP+DIVH+8*mm+CHART_H+16*mm+GAP+FOOTER_H)
c=RC.Canvas(PDF_PATH,pagesize=(W,H))
def bg_grad():
    for i in range(int(H/mm)+2):
        ratio=i/(H/mm);r=int(13+ratio*2);g2=int(27+ratio*4);b=int(42+ratio*6)
        c.setFillColor(Color(r/255,g2/255,b/255));c.rect(0,i*mm,W,1.3*mm,fill=1,stroke=0)
def hline(y,col=None,lw=0.6):c.setStrokeColor(col or STEEL);c.setLineWidth(lw);c.line(PAD,y,W-PAD,y)
def dots(y,r=1.6):c.setFillColor(GOLD);c.circle(PAD,y,r*mm,fill=1,stroke=0);c.circle(W-PAD,y,r*mm,fill=1,stroke=0)
def badge(txt,x,y,fs=9.5,bg=None,fg=None):
    bg=bg or GOLD;fg=fg or NAVY;c.setFont(FNB,fs);tw=c.stringWidth(txt,FNB,fs)
    c.setFillColor(bg);c.roundRect(x-4*mm,y-3*mm,tw+8*mm,8.5*mm,2.5*mm,fill=1,stroke=0);c.setFillColor(fg);c.drawString(x,y,txt)
def corners():
    c.setStrokeColor(GOLD);c.setLineWidth(2.5)
    c.line(PAD,H-PAD,PAD+20*mm,H-PAD);c.line(PAD,H-PAD,PAD,H-PAD-20*mm)
    c.setLineWidth(1.2);c.line(W-PAD-12*mm,PAD,W-PAD,PAD);c.line(W-PAD,PAD,W-PAD,PAD+12*mm)
def icon_lens(cx,cy,r=5):
    rm=r*mm;c.setFillColor(ACC);c.circle(cx,cy+rm*0.25,rm*0.75,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(2.2);c.circle(cx,cy+rm*0.25,rm*0.75,fill=0,stroke=1)
    c.setLineWidth(2.5);c.line(cx+rm*0.5,cy-rm*0.2,cx+rm*1.5,cy-rm*1.1)
    c.setStrokeColor(GOLD2);c.setLineWidth(1.0);c.line(cx-rm*0.3,cy+rm*0.65,cx+rm*0.1,cy+rm*0.9)
def icon_bulb(cx,cy,r=5):
    rm=r*mm;c.setFillColor(ACC);c.circle(cx,cy+rm*0.35,rm*0.82,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(2.2);c.circle(cx,cy+rm*0.35,rm*0.82,fill=0,stroke=1)
    c.setStrokeColor(GOLD);c.setLineWidth(2.0)
    c.line(cx-rm*0.4,cy-rm*0.38,cx+rm*0.4,cy-rm*0.38);c.line(cx-rm*0.28,cy-rm*0.72,cx+rm*0.28,cy-rm*0.72)
    c.setStrokeColor(GOLD2);c.setLineWidth(1.2)
    c.line(cx,cy+rm*1.25,cx,cy+rm*1.65);c.line(cx+rm*0.6,cy+rm*1.05,cx+rm*0.9,cy+rm*1.32);c.line(cx-rm*0.6,cy+rm*1.05,cx-rm*0.9,cy+rm*1.32)
def icon_globe(cx,cy,r=12):
    rm=r*mm;c.setFillColor(ACC);c.circle(cx,cy,rm,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(1.0);c.circle(cx,cy,rm,fill=0,stroke=1)
    for lat in[-0.45,-0.15,0.15,0.45]:
        ry=cy+lat*rm*2;rw=math.sqrt(max(0,rm**2-(cy-ry)**2))*0.88
        if rw>1:c.setStrokeColor(HexColor('#2A4A6A'));c.setLineWidth(0.4);c.line(cx-rw,ry,cx+rw,ry)
    for lng in[-0.55,-0.15,0.15,0.55]:
        c.setStrokeColor(HexColor('#2A4A6A'));c.setLineWidth(0.4)
        c.bezier(cx+lng*rm,cy-rm*0.92,cx+lng*rm*1.25,cy-rm*0.25,cx+lng*rm*1.25,cy+rm*0.25,cx+lng*rm,cy+rm*0.92)
    c.setStrokeColor(GOLD);c.setLineWidth(0.8);c.circle(cx,cy,rm,fill=0,stroke=1)
def icon_chart_box(cx,cy,r=12):
    rm=r*mm;c.setFillColor(ACC);c.roundRect(cx-rm,cy-rm,rm*2,rm*2,rm*0.12,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(1.0);c.roundRect(cx-rm,cy-rm,rm*2,rm*2,rm*0.12,fill=0,stroke=1)
    for i2,(bx_r,bh_r) in enumerate([(0.18,0.52),(0.42,0.33),(0.66,0.72),(0.90,0.90)]):
        bw_i=rm*0.30;bx_i=cx-rm+bx_r*rm*2-bw_i/2;bh_i=bh_r*(rm*1.35)
        c.setFillColor(GOLD if i2==3 else HexColor('#2A4A6A'));c.roundRect(bx_i,cy-rm*0.55,bw_i,bh_i,1,fill=1,stroke=0)
    c.setStrokeColor(GOLD2);c.setLineWidth(1.2)
    c.line(cx-rm*0.8,cy+rm*0.2,cx+rm*0.8,cy-rm*0.8);c.line(cx+rm*0.8,cy-rm*0.8,cx+rm*0.55,cy-rm*0.55);c.line(cx+rm*0.8,cy-rm*0.8,cx+rm*0.8,cy-rm*0.45)
def icon_doc(cx,cy,r=12):
    rm=r*mm;c.setFillColor(ACC);c.roundRect(cx-rm*0.68,cy-rm,rm*1.36,rm*2,rm*0.08,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(1.0);c.roundRect(cx-rm*0.68,cy-rm,rm*1.36,rm*2,rm*0.08,fill=0,stroke=1)
    c.setFillColor(HexColor('#0A2035'));c.rect(cx+rm*0.28,cy+rm*0.6,rm*0.4,rm*0.4,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(0.8)
    c.line(cx+rm*0.28,cy+rm*1.0,cx+rm*0.68,cy+rm*0.6);c.line(cx+rm*0.28,cy+rm*0.6,cx+rm*0.68,cy+rm*0.6)
    for i2,lw in enumerate([0.85,0.65,0.85,0.50,0.70]):
        ly=cy+rm*(0.45-i2*0.32);c.setStrokeColor(GOLD if i2==0 else HexColor('#3A5A7A'));c.setLineWidth(0.9 if i2==0 else 0.5);c.line(cx-rm*0.42,ly,cx-rm*0.42+rm*lw*0.75,ly)
    c.setFillColor(GOLD);c.circle(cx+rm*0.25,cy-rm*0.72,rm*0.24,fill=1,stroke=0)
    c.setStrokeColor(NAVY);c.setLineWidth(1.4);c.line(cx+rm*0.10,cy-rm*0.72,cx+rm*0.22,cy-rm*0.85);c.line(cx+rm*0.22,cy-rm*0.85,cx+rm*0.44,cy-rm*0.55)
ICONS=[icon_globe,icon_chart_box,icon_doc]
def make_port(w=880,h=320):
    img=PI.new('RGB',(w,h),(8,20,38));d2=ID.Draw(img)
    for y in range(h*2//5):
        r2=int(8+y*0.4);g2=int(20+y*0.7);b2=int(38+y*0.9);d2.line([(0,y),(w,y)],fill=(min(r2,55),min(g2,75),min(b2,85)))
    for y in range(h*2//5,h):
        ratio=(y-h*2//5)/(h*3//5);d2.line([(0,y),(w,y)],fill=(int(6+ratio*4),int(18+ratio*6),int(35+ratio*8)))
    for cx3 in[90,220,360,500,640,760]:
        ch=random.randint(70,110);hy=h*2//5
        d2.rectangle([cx3-3,hy-ch,cx3+3,hy],fill=(165,145,105));d2.rectangle([cx3-26,hy-ch,cx3+26,hy-ch+5],fill=(180,155,115))
        d2.line([(cx3,hy-ch),(cx3+28,hy-ch-10)],fill=(178,155,115),width=3);d2.line([(cx3+28,hy-ch-10),(cx3+28,hy-ch+26)],fill=(162,142,105),width=2)
    cols=[(172,42,42),(42,94,155),(185,158,42),(42,125,70),(145,80,42),(84,42,138),(42,145,140)]
    for row in range(3):
        x=12
        for ci in range(16):
            col3=cols[ci%len(cols)];cy2=h*2//5-(row+1)*17;d2.rectangle([x,cy2,x+47,cy2+15],fill=col3);d2.rectangle([x,cy2,x+47,cy2+15],outline=(0,0,0),width=1);d2.line([(x+23,cy2),(x+23,cy2+15)],fill=(0,0,0),width=1);x+=50
    d2.polygon([(40,h*2//5+4),(w-40,h*2//5+4),(w-15,h*2//5+22),(15,h*2//5+22)],fill=(35,50,70));d2.rectangle([80,h*2//5-28,w-80,h*2//5+4],fill=(45,60,82))
    for _ in range(12):rx=random.randint(0,w);ry=h*2//5+random.randint(8,40);d2.line([(rx,ry),(rx+random.randint(20,65),ry)],fill=(200,169,110),width=1)
    ov=PI.new('RGBA',(w,h),(0,0,0,0));od=ID.Draw(ov);od.rectangle([0,h*3//5,w,h],fill=(0,0,0,195));od.rectangle([0,0,w,h//5],fill=(0,0,0,100))
    img2=img.convert('RGBA');img2.alpha_composite(ov);return img2.convert('RGB')
PORT_PATH='/tmp/port_media.jpg'
if not os.path.exists(PORT_PATH):make_port().save(PORT_PATH,'JPEG',quality=93)
bg_grad();corners();cur=H
c.drawImage(PORT_PATH,0,H-PORT_H,width=W,height=PORT_H,mask=None,preserveAspectRatio=False)
for i in range(int(PORT_H/mm)+1):
    a=(i/(PORT_H/mm))**1.4*0.88;c.setFillColor(Color(0.05,0.1,0.16,alpha=a));c.rect(0,H-PORT_H+i*mm,W,1.3*mm,fill=1,stroke=0)
badge(TITLE_LINE,PAD,H-16*mm,fs=9.5)
if DTXT:
    c.setFont(FNB,8.5);tw_d=c.stringWidth(DTXT,FNB,8.5)
    c.setFillColor(HexColor('#0D2540'));c.roundRect(W-tw_d-12*mm,H-17*mm,tw_d+8*mm,8.5*mm,2*mm,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(0.8);c.roundRect(W-tw_d-12*mm,H-17*mm,tw_d+8*mm,8.5*mm,2*mm,fill=0,stroke=1)
    c.setFillColor(GOLD);c.setFont(FNB,8.5);c.drawString(W-tw_d-8*mm,H-16*mm,DTXT)
title_lines=smart_lines(TITLE,18,(INNER-60)/mm,max_lines=2)
ty=H-34*mm
for ln in title_lines:c.setFillColor(WHITE);c.setFont(FNB,18);c.drawString(PAD,ty,ln);ty-=12*mm
if KEY_FACT:c.setFillColor(GOLD);c.setFont(FNB,13);c.drawString(PAD,H-47*mm,KEY_FACT[:55])
cur=H-PORT_H-GAP
bw=(INNER-3*mm)/3
for i,sh in enumerate(STATS3):
    bx=PAD+i*(bw+1.5*mm);by=cur-STATS_H
    c.setFillColor(MID);c.roundRect(bx,by,bw,STATS_H,2.5*mm,fill=1,stroke=0)
    c.setStrokeColor(GOLD if i==0 else ACC);c.setLineWidth(1.5 if i==0 else 0.6);c.roundRect(bx,by,bw,STATS_H,2.5*mm,fill=0,stroke=1)
    c.setFillColor(GOLD if i==0 else WHITE);c.setFont(FNB,12);c.drawCentredString(bx+bw/2,by+STATS_H-11*mm,str(sh.get('val','--'))[:18])
    c.setFillColor(DIM);c.setFont(FN,8);c.drawCentredString(bx+bw/2,by+4.5*mm,str(sh.get('lbl','--'))[:24])
cur-=STATS_H+4*mm
c.setFillColor(GRAY);c.setFont(FN,7.5);c.drawRightString(W-PAD,cur+1.5*mm,SOURCE[:65]);cur-=GAP
hline(cur,col=GOLD,lw=0.8);dots(cur);cur-=DIVH
icon_lens(PAD+6*mm,cur-5.5*mm);c.setFillColor(GOLD);c.setFont(FNB,10.5);c.drawString(PAD+14*mm,cur-4*mm,S4H);cur-=SEC_HDR
c.setFillColor(DARK);c.roundRect(PAD,cur-BOX_IN_H,INNER,BOX_IN_H,2.5*mm,fill=1,stroke=0)
c.setStrokeColor(ACC);c.setLineWidth(0.5);c.roundRect(PAD,cur-BOX_IN_H,INNER,BOX_IN_H,2.5*mm,fill=0,stroke=1)
c.setFillColor(GOLD);c.roundRect(PAD,cur-BOX_IN_H,3.5*mm,BOX_IN_H,1*mm,fill=1,stroke=0)
c.setFont(FNB,52);c.setFillColor(HexColor('#152535'));c.drawString(PAD+5*mm,cur-7.5*mm,'\u201c');c.drawString(W-PAD-20*mm,cur-BOX_IN_H+12*mm,'\u201d')
ty=cur-14*mm
for ln in in_lines:c.setFillColor(WHITE);c.setFont(FN,FS_IN);c.drawString(PAD+5*mm,ty,ln);ty-=LH_IN
sig='-- Ho Alva  -  CMO Big E Co.  -  hoalva.bigeco.vn';sig_y=cur-BOX_IN_H+5.5*mm
c.setFillColor(HexColor('#0A2035'));tw_s=c.stringWidth(sig,FNB,9)+6*mm;c.roundRect(PAD+3*mm,sig_y-2.5*mm,tw_s,7*mm,1.5*mm,fill=1,stroke=0)
c.setFillColor(GOLD);c.setFont(FNB,9);c.drawString(PAD+5*mm,sig_y,sig);cur-=BOX_IN_H+GAP
hline(cur,col=GOLD,lw=0.8);dots(cur);cur-=DIVH
icon_bulb(PAD+6*mm,cur-5.5*mm);c.setFillColor(GOLD);c.setFont(FNB,10.5);c.drawString(PAD+14*mm,cur-4*mm,S5H);cur-=SEC_HDR
for idx2,(n2,t2,ls2,bh) in enumerate(act_data):
    by=cur-bh;c.setFillColor(MID);c.roundRect(PAD,by,INNER,bh,2.5*mm,fill=1,stroke=0)
    c.setStrokeColor(ACC);c.setLineWidth(0.5);c.roundRect(PAD,by,INNER,bh,2.5*mm,fill=0,stroke=1)
    c.setFillColor(GOLD);c.roundRect(PAD,by,3.5*mm,bh,1*mm,fill=1,stroke=0)
    c.setFillColor(DARK);c.roundRect(PAD+4*mm,by+2*mm,ICON_W,bh-4*mm,2*mm,fill=1,stroke=0);ICONS[idx2%3](PAD+4*mm+ICON_W/2,by+bh/2,r=12)
    c.setFillColor(GOLD);c.roundRect(PAD+4*mm+ICON_W/2-5*mm,by+4*mm,10*mm,7*mm,1.5*mm,fill=1,stroke=0)
    c.setFillColor(NAVY);c.setFont(FNB,10);c.drawCentredString(PAD+4*mm+ICON_W/2,by+7.5*mm,n2)
    c.setStrokeColor(ACC);c.setLineWidth(0.5);c.line(TX-3*mm,by+3*mm,TX-3*mm,by+bh-3*mm)
    c.setFillColor(GOLD);c.setFont(FNB,11);c.drawString(TX,by+bh-9*mm,t2[:42])
    c.setStrokeColor(HexColor('#1A3A55'));c.setLineWidth(0.4);c.line(TX,by+bh-13*mm,W-PAD-2*mm,by+bh-13*mm)
    ty2=by+bh-20*mm
    for ln in ls2:c.setFillColor(WHITE);c.setFont(FN,FS_ACT);c.drawString(TX,ty2,ln);ty2-=LH_ACT
    cur=by-3*mm
cur-=GAP
hline(cur,col=GOLD,lw=0.8);dots(cur);cur-=DIVH
c.setFillColor(GRAY);c.setFont(FNB,8.5);c.drawString(PAD,cur-3*mm,S3H);cur-=8*mm
if CHART_D and len(CHART_D)>=2:
    vals=[float(x.get('val',x.get('value',0))) for x in CHART_D];maxv=max(vals);minv=min(vals)
    base2=cur-CHART_H;cw2=INNER;nb=len(vals);bwe=cw2/nb*0.58;gpe=cw2/nb*0.42
    for gi in range(5):
        gy=base2+(gi/4)*CHART_H;c.setStrokeColor(HexColor('#1A3040'));c.setLineWidth(0.4);c.line(PAD,gy,W-PAD,gy)
        gv=minv*0.88+(maxv-minv*0.88)*gi/4;c.setFillColor(GRAY);c.setFont(FN,7);c.drawRightString(PAD-1.5*mm,gy-2*mm,f'{gv:.0f}')
    for i,xd in enumerate(CHART_D):
        val=float(xd.get('val',xd.get('value',0)));lbl2=str(xd.get('lbl',xd.get('label',''))).replace('\\n','\n')
        bx=PAD+i*(bwe+gpe);bh2=(val-minv*0.88)/(maxv-minv*0.88)*CHART_H if maxv>minv else CHART_H*0.5;hi2=(i==len(CHART_D)-1)
        c.setFillColor(GOLD if hi2 else HexColor('#2A4A6A'));c.roundRect(bx,base2,bwe,bh2,1*mm,fill=1,stroke=0)
        if hi2:
            c.setStrokeColor(GOLD2);c.setLineWidth(1.5);c.roundRect(bx,base2,bwe,bh2,1*mm,fill=0,stroke=1)
            c.setFillColor(GOLD);c.setFont(FNB,7.5);c.drawCentredString(bx+bwe/2,base2+bh2+7*mm,'* Moi nhat')
        c.setFillColor(WHITE if hi2 else DIM);c.setFont(FNB,8);c.drawCentredString(bx+bwe/2,base2+bh2+2*mm,f'{val:.1f}')
        parts=lbl2.split('\n');c.setFont(FNB if hi2 else FN,8);c.setFillColor(GOLD if hi2 else DIM);c.drawCentredString(bx+bwe/2,base2-5.5*mm,parts[0][:10])
        if len(parts)>1:c.setFont(FN,7);c.setFillColor(GOLD if hi2 else HexColor('#3A5A7A'));c.drawCentredString(bx+bwe/2,base2-10.5*mm,parts[1][:8])
    c.setFillColor(GRAY);c.setFont(FN,7.5);c.drawRightString(W-PAD,base2-14*mm,(CHART_SRC or 'Nguon: Tong cuc Hai quan')[:55]);cur=base2-16*mm
else:
    c.setFillColor(MID);c.roundRect(PAD,cur-18*mm,INNER,16*mm,2*mm,fill=1,stroke=0)
    c.setFillColor(GRAY);c.setFont(FN,10);c.drawCentredString(W/2,cur-11*mm,'Chua co du lieu bieu do');cur-=20*mm
cur-=GAP
hline(cur,col=GOLD,lw=0.8);dots(cur);cur-=8*mm
c.setFillColor(MID);c.roundRect(PAD,cur-12*mm,66*mm,13*mm,2*mm,fill=1,stroke=0)
c.setFont(FNB,11);c.setFillColor(GOLD);c.drawString(PAD+4*mm,cur-6.5*mm,'hoalva.bigeco.vn')
c.setFont(FN,8);c.setFillColor(DIM);c.drawString(PAD+4*mm,cur-12*mm,'CMO - Big E Co.')
c.setFillColor(HexColor('#0D2845'));c.roundRect(W/2-52*mm,cur-13*mm,104*mm,13*mm,3*mm,fill=1,stroke=0)
c.setStrokeColor(GOLD);c.setLineWidth(1.2);c.roundRect(W/2-52*mm,cur-13*mm,104*mm,13*mm,3*mm,fill=0,stroke=1)
c.setFont(FNB,9.5);c.setFillColor(GOLD);c.drawCentredString(W/2,cur-7.5*mm,CTA)
c.setFont(FN,8);c.setFillColor(GRAY)
tg_parts=TAGLINE.replace(' - ','-').split('-');c.drawRightString(W-PAD,cur-5*mm,('-'.join(tg_parts[:2])).strip())
if len(tg_parts)>2:c.drawRightString(W-PAD,cur-11*mm,tg_parts[2].strip())
c.showPage();c.save()
try:
    subprocess.run(['pdftoppm','-r','200','-png','-singlefile',PDF_PATH,PNG_PATH.replace('.png','')],check=True,timeout=60,capture_output=True)
    tmp=PNG_PATH.replace('.png','')+'.png'
    if os.path.exists(tmp) and tmp!=PNG_PATH:os.rename(tmp,PNG_PATH)
except:
    try:PI.open(PDF_PATH).save(PNG_PATH,'PNG')
    except:pass
try:os.unlink(PDF_PATH)
except:pass
print(PNG_PATH)
