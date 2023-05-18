from PIL import Image, ImageDraw, ImageFont

def createImage(id, name, population, food, outlook, defences, campaing):
    image1 = Image.open('data/SettlementKart0.png')

    # Wczytanie drugiego obrazu
    image2 = Image.open(f'data/radiobutton/high_image_{id}.png')

    # Wymiary pierwszego obrazu
    width1, height1 = image1.size

    # Wymiary drugiego obrazu
    width2, height2 = image2.size

    # Współrzędne, na których chcesz nałożyć drugi obraz
    x = 110-60+140*id
    y = 400-60

    # Stworzenie nowego obrazu o rozmiarze pierwszego obrazu
    merged_image = Image.new('RGBA', (width1, height1), (0, 0, 0, 0))

    # Nałożenie pierwszego obrazu
    merged_image.paste(image1, (0, 0))

    # Nałożenie drugiego obrazu na pierwszy obraz w określonych współrzędnych
    merged_image.paste(image2, (x, y, x + width2, y + height2), mask=image2)
    
    
    draw = ImageDraw.Draw(merged_image)

    # Ścieżka do pliku czcionki
    font_path = 'data/Overseer-pLVd.ttf'

    # Rozmiar czcionki
    font_size = 90

    # Wczytanie czcionki
    font = ImageFont.truetype(font_path, font_size)
    draw.text((80, 60), name , font=font, fill=(0, 0, 0))
    draw.text((405, 205), str(food) , font=font, fill=(0, 0, 0))
    draw.text((625, 205), str(outlook) , font=font, fill=(0, 0, 0))
    draw.text((865, 205), str(defences) , font=font, fill=(0, 0, 0))
    
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)
    draw.text((75, 235), population , font=font, fill=(0, 0, 0))
    
    
    
    

    # Zapisanie wynikowego obrazu
    merged_image.save(f'data/temp/{campaing}_{name}.png')
    
