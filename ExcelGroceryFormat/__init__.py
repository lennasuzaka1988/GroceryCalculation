from io import BytesIO
import requests
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as PYXLImage
from PIL import Image
from openpyxl.styles import Alignment
from openpyxl.styles import Font


# Include the product images for reference
def image_data():
    request = requests.get(
        'https://assets-prd-spr.unataops.com/web/product_small/f85526c802633749da817160b95b94d798fedd43.jpg',
        stream=True)
    img = Image.open(BytesIO(request.content))
    max_size = (150, 150)
    img.thumbnail(max_size, Image.LANCZOS)
    img.save('product.png')
    xl_img = PYXLImage('product.png')
    return xl_img


# Inserting the image and resizing the cell to fit the images
workbook = load_workbook(filename='new_list.xlsx')
worksheet = workbook['Sheet1']
image_data().anchor = 'D1'
worksheet.add_image(image_data())
worksheet.row_dimensions[1].height = 150
worksheet.column_dimensions['D'].width = 50


# Styling the text
def sheet_style():
    worksheet_columns = worksheet['A1']
    worksheet_columns.alignment = Alignment(vertical='center')
    worksheet_columns.font = Font(size=13, bold=True)


image_data()
sheet_style()
workbook.save(filename='new_list.xlsx')
