from django.shortcuts import render

from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse

from convert_csv.forms import DocumentForm
from datetime import datetime

VENMO_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
YNAB_DATE_FORMAT = '%m/%d/%Y'
OUTPUT_ORDER = ['Date', 'Payee', 'Memo', 'Outflow', 'Inflow']

import csv

# TODO(jacob): Move convert to another file
def convert_row(row):
    print(row)
    memo = row['Note']
    tmpdate = row['Datetime'].split(' ')
    tmpdate = ' '.join(tmpdate[:4] + tmpdate[5:])
    if not tmpdate.strip(): 
        return [False, {}]

    date = datetime.strptime(tmpdate, VENMO_DATE_FORMAT).strftime(YNAB_DATE_FORMAT)
    amount = float(row['Amount (total)'].replace(' $', '').replace(',', ''))
    if amount < 0:
        inflow = None
        outflow = abs(amount)
        payee = row['To']
    else:
        inflow = amount
        outflow = None
        payee = row['From']

    return [True, {
        'Inflow': inflow,
        'Outflow': outflow,
        'Date': date,
        'Payee': payee,
        'Memo': memo,
    }]

def convert_file(input_file, output_file): 
    decoded_file = input_file.read().decode('utf-8').splitlines()
    input_reader = csv.DictReader(decoded_file)

    #writer = csv.writer(output_file)
    #writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    #writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    output_writer = csv.DictWriter(output_file, OUTPUT_ORDER)

    output_writer.writeheader()
    for row in input_reader:
        [valid, converted] = convert_row(row)
        if valid:
            print(converted)
            output_writer.writerow(converted)

def convert(request):
    # Handle file upload
    if request.method == 'POST':
        print("Cponvert Request"); 
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = request.FILES['docfile']

            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = "attachment; filename=\"{doc_name}_ynab4.csv\"".format(doc_name=str(doc).replace(".csv", ""))

            convert_file(doc, response)

            print("Response"); 
            return response
        else:
            print("invalid"); 
            return
    else:
        form = DocumentForm() # A empty, unbound form

    # Render list page with the form
    # 
    return render(request, 'index.html', { 'form': form })
