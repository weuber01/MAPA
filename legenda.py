from PIL import Image, ImageDraw,ImageFont
import os


def legenda_prod_vertical(lcores,faixa,rot):
    lado=40
    im = Image.new('RGB', (420,300), (255,255,255))
    draw = ImageDraw.Draw(im)
    l_cor=lcores
    maxi=max(faixa)
    lraz=[]
    lenmax=0
    dirpath=os.getcwd()
    for ff in faixa:
        s_raz="{:,}".format(ff).replace(",", " ")
        lraz.append(s_raz)
    l_raz=[]
    for lr in lraz:
        temp=lr.replace(".0","")
        l_raz.append(temp)

    font = ImageFont.truetype("arial", size=16)
    font2 = ImageFont.truetype("arial", size=18)
    for y in range(0,len(l_cor)):
        print(y)
        draw.rectangle((20, 50+y*lado, 20+lado,50+lado+y*lado), fill=l_cor[y], outline=(250,250,250),width=1)
        comp=len(l_raz[y])
        draw.text((63,60+y*lado),l_raz[y],font=font, fill="black")
        draw.text((63+9*comp+40,60+y*lado),l_raz[y+1],font=font, fill="black")
        draw.line((63+9*comp+10,70+y*lado,63+9*comp+30,70+y*lado),fill="black",width=3)
        if y>0:
            draw.line((63+9*comp+8,70+y*lado-5,63+9*comp+8,70+y*lado+5),fill="black",width=3)
        if y==(len(l_cor)-1):
            draw.line((63+9*comp+32,70+y*lado-5,63+9*comp+32,70+y*lado+5),fill="black",width=3)
    texto=rot
    

    draw.text((30,5),texto,font=font2, fill="black")
    im.save(dirpath+'\\leg_temp.jpg', quality=95)   
