from io import BytesIO

import PyPDF2
from django.http import HttpResponse

from PyPDF2.generic import BooleanObject, NameObject, IndirectObject


def pdf(request):
    template = 'templates/template.pdf'

    outfile = "templates/test.pdf"

    input_stream = open(template, "rb")
    pdf_reader = PyPDF2.PdfFileReader(input_stream, strict=False)
    if "/AcroForm" in pdf_reader.trailer["/Root"]:
        pdf_reader.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf_writer = PyPDF2.PdfFileWriter()
    set_need_appearances_writer(pdf_writer)
    if "/AcroForm" in pdf_writer._root_object:
        # Acro form is form field, set needs appearances to fix printing issues
        pdf_writer._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    data_dict = {
        'first_name': 'John\n',
        'last_name': 'Smith\n',
        'email': 'mail@mail.com\n',
        'phone': '889-998-9967\n',
        'company': 'Amazing Inc.\n',
        'job_title': 'Dev\n',
        'street': '123 Main Way\n',
        'city': 'Johannesburg\n',
        'state': 'New Mexico\n',
        'zip': 96705,
        'country': 'USA\n',
        'topic': 'Who cares...\n'

    }

    pdf_writer.addPage(pdf_reader.getPage(0))
    pdf_writer.updatePageFormFieldValues(pdf_writer.getPage(0), data_dict)

    output_stream = BytesIO()
    pdf_writer.write(output_stream)

    # print(fill_in_pdf(template, data_dict).getvalue())

    # fill_in_pdf(template, data_dict).getvalue()
    response = HttpResponse(output_stream.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="completed.pdf"'
    input_stream.close()

    return response
    # return render(request,
    #               'index.html',
    #               {}
    #               )


def set_need_appearances_writer(writer):
    # See 12.7.2 and 7.7.2 for more information:
    # http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    try:
        catalog = writer._root_object
        # get the AcroForm tree and add "/NeedAppearances attribute
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer
