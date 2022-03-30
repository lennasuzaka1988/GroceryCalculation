from io import BytesIO
import requests
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as PYXLImage
from PIL import Image
from openpyxl.styles import Alignment
from openpyxl.styles import Font


# Now to include the images that fit in the cell!
request = requests.get(
    'https://assets-prd-spr.unataops.com/web/product_small/f85526c802633749da817160b95b94d798fedd43.jpg', stream=True)
img = Image.open(BytesIO(request.content))
max_size = (150, 150)
img.thumbnail(max_size, Image.LANCZOS)
img.save('product.png')
xl_img = PYXLImage('product.png')

workbook = load_workbook(filename='new_list.xlsx')
worksheet = workbook['Sheet1']
xl_img.anchor = 'D1'
worksheet.add_image(xl_img)
worksheet.row_dimensions[1].height = 150
worksheet.column_dimensions['D'].width = 50


# Styling the text
worksheet_columns = worksheet['A1', 'B1', 'C1', 'D1']
worksheet_columns.alignment = Alignment(vertical='center')
worksheet_columns.wrap_text = True
worksheet_columns.font = Font(size=13, vertAlign=True, bold=True)


workbook.save(filename='new_list.xlsx')