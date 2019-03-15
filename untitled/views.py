from io import BytesIO

from django.http import HttpResponse
import pdfrw
from django.shortcuts import render


def pdf(request):
    template = 'templates/template.pdf'
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

    print(fill_in_pdf(template, data_dict).getvalue())
    #
    response = HttpResponse(fill_in_pdf(template, data_dict).getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="completed.pdf"'
    return response
    # return render(request,
    #               'index.html',
    #               {}
    #               )


def fill_in_pdf(input_pdf_path, data_dict):
    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'

    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        # print(annotation)
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                # print(key)
                if key in data_dict.keys():
                    # annotation['/V'] = annotation[ANNOT_FIELD_KEY]
                    # annotation[SUBTYPE_KEY] = '/T'
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key], ))
                    )


    # does not work or it would show in view.
    memory_pdf = BytesIO()
    pdfrw.PdfWriter().write(memory_pdf, template_pdf)

    # pdfrw.PdfWriter().write('templates/output.pdf', template_pdf)

    print(str(memory_pdf.getvalue()).replace('/Widget', ''))

    return memory_pdf
