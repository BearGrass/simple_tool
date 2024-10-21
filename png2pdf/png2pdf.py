import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def png_to_pdf(input_folder, output_pdf):
    # 获取所有PNG文件并按文件名排序
    png_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith('.png')], key=lambda x: int(''.join(filter(str.isdigit, os.path.splitext(x)[0]))))
    
    if not png_files:
        print("未找到PNG文件")
        return
    
    # 创建PDF文档
    c = canvas.Canvas(output_pdf)
    
    for png_file in png_files:
        img_path = os.path.join(input_folder, png_file)
        img = Image.open(img_path)
        width, height = img.size
        
        # 设置PDF页面大小为图片大小
        c.setPageSize((width, height))
        
        # 在PDF中绘制图片
        c.drawImage(img_path, 0, 0, width, height)
        
        # 添加新页面
        c.showPage()
    
    # 保存PDF
    c.save()
    print(f"PDF文件已保存为: {output_pdf}")

# 使用示例
input_folder = "png_files"  # 包含PNG文件的文件夹
output_pdf = "output.pdf"   # 输出的PDF文件名

png_to_pdf(input_folder, output_pdf)
