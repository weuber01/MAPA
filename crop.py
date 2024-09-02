# Improting Image class from PIL module 
from PIL import Image 

def recortar(imagem):
    nome=imagem[0:-4]
    # Opens a image in RGB mode 
    im = Image.open(imagem) 
      
    # Size of the image in pixels (size of orginal image) 
    # (This is not mandatory) 
    width, height = im.size 
      
    # Setting the points for cropped image 
    left =180
    top = 140
    right = 940
    bottom =870
      
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im1 = im.crop((left, top, right, bottom)) 
      
    # Shows the image in image viewer 
    im1.save(nome+"_r.png")
    print("recortado")

def recortar2(imagem):
    nome=imagem[0:-4]
    # Opens a image in RGB mode 
    im = Image.open(imagem) 
      
    # Size of the image in pixels (size of orginal image) 
    # (This is not mandatory) 
    width, height = im.size 
      
    # Setting the points for cropped image 
    left =0
    top = 0
    right = 1100
    bottom =820
      
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im1 = im.crop((left, top, right, bottom)) 
      
    # Shows the image in image viewer 
    im1.save(nome+"_r.png")
    print("recortado")
