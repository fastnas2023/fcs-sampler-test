from PIL import Image, ImageDraw, ImageFont

def create_app_icon():
    # 创建一个512x512的图像
    size = 512
    image = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], fill='#2196F3')
    
    # 添加文字
    try:
        font = ImageFont.truetype('Arial.ttf', 160)
    except:
        font = ImageFont.load_default()
    
    text = "FCS"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill='white', font=font)
    
    # 保存为不同格式
    image.save('app_icon.png')
    
    # 为Mac创建icns
    image.save('app_icon.icns')
    
    # 为Windows创建ico
    image.save('app_icon.ico')

if __name__ == "__main__":
    create_app_icon() 