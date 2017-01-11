import os
import xlwt
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import pdfkit
from django.conf import settings
from PIL import Image


def convert_to_bitmap(path):
    basewidth = 40
    img = Image.open(path)
    wpercent = (basewidth/float(img.size[0]))
    r, g, b = img.split()
    img = Image.merge("RGB", (r, g, b))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save('converted.bmp')
    return 'converted.bmp'


def render_to_pdf(template_src, context_dict, css=None):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    if css:
        css = settings.BASE_DIR + css
    else:
        pwd = os.path.dirname(__file__)
        css = pwd + '/static/moneycash/bootstrap/css/bootstrap.css'
    pdfkit.from_string(html, 'out.pdf', css=css)
    pdf = open("out.pdf")
    response = HttpResponse(pdf.read(), content_type='application/pdf')
    pdf.close()
    return response


def render_to_excel(filename, data, images=None):
        book = xlwt.Workbook(encoding='utf8')
        sheet = book.add_sheet(filename)
        default_style = xlwt.Style.default_style
        font_size_style = xlwt.easyxf('font: name Calibri, bold on, height 280;')
        font_underline_style = xlwt.easyxf('font: underline on;')
        fill_grey_style = xlwt.easyxf('pattern: back_color gray25;')
        fill_yellow_style = xlwt.easyxf('pattern: back_color yellow;')
        col = 0
        for r, d in enumerate(data):
            col = len(d)
            for c in range(0, col):
                if images:
                    sheet.write(r, c, d[c], style=default_style)
                else:
                    sheet.write(r, c, d[c], style=default_style)
        if images:
            for row, img in enumerate(images):
                if img != '':
                    sheet.insert_bitmap(convert_to_bitmap(img), row+1, col-1)
                    sheet.row(row+1).height_mismatch = True
                    sheet.row(row+1).height = 8*45
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename='+filename+'.xls'
        book.save(response)
        return response
