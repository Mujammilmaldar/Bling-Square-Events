from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.utils.http import quote
from datetime import datetime, timedelta
import pandas as pd
from django.contrib.auth.hashers import make_password
# from .authentication_views import check_user
from ..authentication.permission_views import *
from ..models import *

@login_required(login_url="/login")
# @check_user
def exp_to_excel_Users(request):
    objs = CUser.objects.all()
    data = []
    for obj in objs:
        data.append({
            'gender': obj.gender,
            'dob': obj.dob,
            'joiningdate': obj.joiningdate,
            'designation': obj.designation,
            'mobileno': obj.mobileno,
            'address': obj.address,
            'age': calculate_age(obj.dob)
        })

    df = pd.DataFrame(data)

    if not df.empty:
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'output_{current_datetime}.xlsx'
        df.to_excel(filename, index=False)

        with open(filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
            return response
    else:
        return HttpResponse('No data available to export.')

@login_required(login_url="/login")
# @check_user
def imp_to_excel_Users(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('excel')
        if excel_file:
            try:
                df = pd.read_excel(excel_file)
                df['dob'] = df['dob'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
                df['joiningdate'] = df['joiningdate'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
                user_data = df.to_dict(orient='records')
                for data in user_data:
                    password = make_password(data['password'])
                    CustomUser.objects.create(
                        gender=data['gender'],
                        dob=data['dob'],
                        joiningdate=data['joiningdate'],
                        designation=data['designation'],
                        email=data['email'],
                        mobileno=data['mobileno'],
                        password=password,
                        address=data['address']
                    )
                return redirect('/success/')
            except Exception as e:
                return HttpResponse(f'Error importing data: {e}')
        else:
            return HttpResponse('No file uploaded.')
    else:
        return render(request, 'importexcel.html')

# Helper functions

def calculate_age(dob):
    current_date = datetime.now().date()
    age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    return age

@login_required(login_url="/login")
# @check_user

def exp_to_excel_sales(request):

    objs = sales.objects.all()
    data = []
    for obj in objs:
        data.append({
            'clientname': obj.clientname,
            'typeofevent': obj.typeofevent,
            'clientnumber': obj.clientnumber,
            'clientemail': obj.clientemail,
            'Venueofevent': obj.Venueofevent,
            'Dateofevent': obj.Dateofevent.strftime('%Y-%m-%d'),  # Convert date to string format
            'dayofevent': obj.dayofevent,
            'duration': obj.duration,
            'Eventstatus': obj.Eventstatus,
            'marketcost': obj.marketcost,
            'discount': obj.discount,
            'finalamount': obj.finalamount,
            'paymenttype': obj.paymenttype,
            'paymentstatus': obj.paymentstatus,
            'amountreceived': obj.amountreceived,
            'amountreceivedon': obj.amountreceivedon,
            'clientrating': obj.clientrating,
            'thirdparty': obj.thirdparty,
            'thirdpartypayment': obj.thirdpartypayment
        })

    df = pd.DataFrame(data)

    if not df.empty:
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'output_sales_{current_datetime}.xlsx'
        df.to_excel(filename, index=False)

        with open(filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
            return response
    else:
        return HttpResponse('No data available to export.')
import traceback
from ..models import EventExcel , Client , Venue

def import_data(request):
    if request.method == 'POST' and request.FILES.get('excel'):
        excel_file = request.FILES['excel']
        if excel_file.name.endswith('.xlsx'):
            try:
                # Save the uploaded Excel file to the desired location
                event_excel = EventExcel.objects.create(excel=excel_file)

                with transaction.atomic():
                    df = pd.read_excel(excel_file)
                    for index, row in df.iterrows():
                        # Extract data from each row
                        client_name = row.get('Client Name', None)
                        client_number = row.get('Client Number', None)
                        client_email = row.get('Client Email', None)
                        venue_name = row.get('Venue', None)
                        venue_address = row.get('Venue Address', None)
                        venue_capacity = row.get('Venue Capacity', None)
                        start_date = row.get('Start Date', None)
                        end_date = row.get('End Date', None)
                        type_of_event = row.get('Type of Event', None)
                        status = row.get('Status', None)
                        mode_of_payment = row.get('Mode of Payment', None)

                        # Create or get the client
                        client = None
                        if client_name:
                            client, _ = Client.objects.get_or_create(
                                name=client_name,
                                defaults={'number': client_number, 'email': client_email}
                            )

                        # Create or get the venue
                        venue = None
                        if venue_name:
                            venue, _ = Venue.objects.get_or_create(
                                name=venue_name,
                                defaults={'address': venue_address, 'capacity': venue_capacity}
                            )

                        # Your existing code to create the event goes here, 
                        # ensuring that client and venue are assigned accordingly

                return render(request, 'all_events.html', {'message': 'Data imported successfully.'})
            except Exception as e:
                return render(request, 'all_events.html', {'error_message': f'An error occurred: {e}'})
        else:
            return render(request, 'all_events.html', {'error_message': 'Only Excel files (.xlsx) are supported.'})
    return redirect('/All_Events')
