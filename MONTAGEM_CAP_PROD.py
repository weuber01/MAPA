from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os
import string
from crop import recortar
from crop import recortar2


def APRESENTACAO():

   


    """ fontes """
    font = ImageFont.truetype("arial", size=16)
    font2 = ImageFont.truetype("arial", size=30)
    font3 = ImageFont.truetype("arial", size=22)
    font4 = ImageFont.truetype("arial", size=24)
    font5=ImageFont.truetype("arial", size=20)

    """ Crop imagens """
    imagem="mapa_temp.png"
    recortar(imagem)

    """ Criar uma imagem """
    im = Image.new('RGBA', (1700,1050),(255,255,255))
    im.save("fundo.png")

    
    """ Carregar imagens """
    im=Image.open("fundo.png")
    mun2=Image.open("mapa_temp_r.png")
    lfig_vertical=Image.open('leg_temp.jpg')
    
    "Desenhar em uma imagem"
    dr = ImageDraw.Draw(im)



    """ Posicionar imagens na base (img) (y,x) """


    im.paste(mun2,(10,10))
    im.paste(lfig_vertical,(674,502))
    """ Escrever os textos na imagem """


    
    """ Salvar a imagem """
    im.save("prov.png")
    recortar2("prov.png")


            
    

