from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime

from .forms import DoctorForm
from .models import *
from django.contrib.auth import authenticate, login, logout
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from django.http import HttpResponse
import pickle
import os
# Create your views here.

def Home(request):
    return render(request,'carousel.html')

def Admin_Home(request):
    dis = Search_Data.objects.all()
    pat = Patient.objects.all()
    doc = Doctor.objects.all()
    feed = Feedback.objects.all()

    d = {'dis':dis.count(),'pat':pat.count(),'doc':doc.count(),'feed':feed.count()}
    return render(request,'admin_home.html',d)

@login_required(login_url="login")
def assign_status(request,pid):
    doctor = Doctor.objects.get(id=pid)
    if doctor.status == 1:
        doctor.status = 2
        messages.success(request, 'Selected doctor are successfully withdraw his approval.')
    else:
        doctor.status = 1
        messages.success(request, 'Selected doctor are successfully approved.')
    doctor.save()
    return redirect('view_doctor')

@login_required(login_url="login")
def User_Home(request):
    return render(request,'patient_home.html')

@login_required(login_url="login")
def Doctor_Home(request):
    return render(request,'doctor_home.html')

def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')


def Gallery(request):
    return render(request,'gallery.html')


def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Patient.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat1"
            else:
                pure=False
                try:
                    pure = Doctor.objects.get(status=1,user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "pat2"
                else:
                    login(request, user)
                    error="notmember"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'login.html', d)

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            error="pat"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        d = request.POST['dob']
        con = request.POST['contact']
        add = request.POST['add']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        if type == "Patient":
            Patient.objects.create(user=user,contact=con,address=add,image=im,dob=d)
        else:
            Doctor.objects.create(dob=d,image=im,user=user,contact=con,address=add,status=2)
        error = "create"
    d = {'error':error}
    return render(request,'register.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url="login")
def Change_Password(request):
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    if not request.user.is_staff:
        try:
            sign = Patient.objects.get(user=user)
            if sign:
                error = "pat"
        except:
            sign = Doctor.objects.get(user=user)
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror,'data':sign}
    return render(request,'change_password.html',d)


def preprocess_inputs(df, scaler):
    df = df.copy()
    # Split df into X and y
    y = df['target'].copy()
    X = df.drop('target', axis=1).copy()
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    return X, y


def prdict_heart_disease(list_data):
    """
    Predict heart disease using pre-trained models.
    Loads saved models from trained_models/ directory.
    If models don't exist, falls back to training on-the-fly.
    """
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'trained_models')
    model_info_path = os.path.join(models_dir, 'model_info.pkl')
    
    # Check if pre-trained models exist
    if os.path.exists(model_info_path):
        print("Loading pre-trained models...")
        
        # Load model info
        with open(model_info_path, 'rb') as f:
            model_info = pickle.load(f)
        
        # Load all models and make predictions
        predictions = {}
        accuracies = {}
        
        model_names = {
            'logistic_regression': 'Logistic Regression',
            'random_forest': 'Random Forest',
            'decision_tree': 'Decision Tree',
            'knn': 'KNN',
            'naive_bayes': 'Naive Bayes'
        }
        
        for model_key, display_name in model_names.items():
            model_path = os.path.join(models_dir, f'{model_key}.pkl')
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                
                pred = model.predict([list_data])
                accuracy = model_info[model_key]['test_accuracy']
                predictions[display_name] = pred[0]
                accuracies[display_name] = accuracy
                print(f"{display_name} Accuracy: {accuracy:.2f}%")
        
        # Use the model with highest accuracy
        best_model_name = max(accuracies, key=accuracies.get)
        best_accuracy = accuracies[best_model_name]
        final_prediction = predictions[best_model_name]
        
        print(f"\nBest Model: {best_model_name}")
        print(f"Best Accuracy: {best_accuracy:.2f}%")
        print(f"Predicted Value: {final_prediction}")
        
        return best_accuracy, np.array([final_prediction])
    
    else:
        # Fallback: Train models on-the-fly if pre-trained models don't exist
        print("Pre-trained models not found. Training on-the-fly...")
        print("Run 'python train_and_save_models.py' to create pre-trained models for faster predictions.")
        
        csv_file = Admin_Helath_CSV.objects.get(id=1)
        df = pd.read_csv(csv_file.csv_file)

        X = df[['age','sex','cp',  'trestbps',  'chol',  'fbs',  'restecg',  'thalach',  'exang',  'oldpeak',  'slope',  'ca',  'thal']]
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=123, stratify=y)
        
        # Initialize multiple models
        models = {
            'Logistic Regression': LogisticRegression(max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=123),
            'Decision Tree': DecisionTreeClassifier(criterion='entropy', random_state=123),
            'KNN': KNeighborsClassifier(n_neighbors=7),
            'Naive Bayes': GaussianNB()
        }
        
        # Train all models and get predictions
        predictions = {}
        accuracies = {}
        
        for name, model in models.items():
            model.fit(X_train, y_train)
            pred = model.predict([list_data])
            accuracy = model.score(X_test, y_test) * 100
            predictions[name] = pred[0]
            accuracies[name] = accuracy
            print(f"{name} Accuracy: {accuracy:.2f}%")
        
        # Use the model with highest accuracy
        best_model_name = max(accuracies, key=accuracies.get)
        best_accuracy = accuracies[best_model_name]
        final_prediction = predictions[best_model_name]
        
        print(f"\nBest Model: {best_model_name}")
        print(f"Best Accuracy: {best_accuracy:.2f}%")
        print(f"Predicted Value: {final_prediction}")
        
        return best_accuracy, np.array([final_prediction])

@login_required(login_url="login")
def add_doctor(request,pid=None):
    doctor = None
    if pid:
        doctor = Doctor.objects.get(id=pid)
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance = doctor)
        if form.is_valid():
            new_doc = form.save()
            new_doc.status = 1
            if not pid:
                user = User.objects.create_user(password=request.POST['password'], username=request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                new_doc.user = user
            new_doc.save()
            return redirect('view_doctor')
    d = {"doctor": doctor}
    return render(request, 'add_doctor.html', d)

@login_required(login_url="login")
def add_heartdetail(request):
    if request.method == "POST":
        # list_data = [57, 0, 1, 130, 236, 0, 0, 174, 0, 0.0, 1, 1, 2]
        list_data = []
        value_dict = eval(str(request.POST)[12:-1])
        count = 0
        for key,value in value_dict.items():
            if count == 0:
                count =1
                continue
            if key == "sex" and value[0] == "Male" or value[0] == 'male' or value[0]=='m' or value[0] == 'M':
                list_data.append(0)
                continue
            elif key == "sex":
                list_data.append(1)
                continue
            # Convert string values to numeric (int or float)
            try:
                # Try to convert to float first (handles both int and float values)
                numeric_value = float(value[0])
                # If it's a whole number, convert to int
                if numeric_value.is_integer():
                    list_data.append(int(numeric_value))
                else:
                    list_data.append(numeric_value)
            except (ValueError, TypeError):
                # If conversion fails, append as is (shouldn't happen with valid input)
                list_data.append(value[0])

        # list_data = [57, 0, 1, 130, 236, 0, 0, 174, 0, 0.0, 1, 1, 2]
        accuracy,pred = prdict_heart_disease(list_data)
        patient = Patient.objects.get(user=request.user)
        Search_Data.objects.create(patient=patient, prediction_accuracy=accuracy, result=pred[0], values_list=list_data)
        rem = int(pred[0])
        print("Result = ",rem)
        if pred[0] == 0:
            pred = "<span style='color:green'>You are healthy</span>"
        else:
            pred = "<span style='color:red'>You are Unhealthy, Need to Checkup.</span>"
        return redirect('predict_desease', str(rem), str(accuracy))
    return render(request, 'add_heartdetail.html')

@login_required(login_url="login")
def predict_desease(request, pred, accuracy):
    doctor = Doctor.objects.filter(address__icontains=Patient.objects.get(user=request.user).address)
    d = {'pred': pred, 'accuracy':accuracy, 'doctor':doctor}
    return render(request, 'predict_disease.html', d)

@login_required(login_url="login")
def view_search_pat(request):
    doc = None
    try:
        doc = Doctor.objects.get(user=request.user)
        data = Search_Data.objects.filter(patient__address__icontains=doc.address).order_by('-id')
    except:
        try:
            doc = Patient.objects.get(user=request.user)
            data = Search_Data.objects.filter(patient=doc).order_by('-id')
        except:
            data = Search_Data.objects.all().order_by('-id')
    return render(request,'view_search_pat.html',{'data':data})

@login_required(login_url="login")
def delete_doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    doc.delete()
    return redirect('view_doctor')

@login_required(login_url="login")
def delete_feedback(request,pid):
    doc = Feedback.objects.get(id=pid)
    doc.delete()
    return redirect('view_feedback')

@login_required(login_url="login")
def delete_patient(request,pid):
    doc = Patient.objects.get(id=pid)
    doc.delete()
    return redirect('view_patient')

@login_required(login_url="login")
def delete_searched(request,pid):
    doc = Search_Data.objects.get(id=pid)
    doc.delete()
    return redirect('view_search_pat')

@login_required(login_url="login")
def View_Doctor(request):
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html',d)

@login_required(login_url="login")
def View_Patient(request):
    patient = Patient.objects.all()
    d = {'patient':patient}
    return render(request,'view_patient.html',d)

@login_required(login_url="login")
def View_Feedback(request):
    dis = Feedback.objects.all()
    d = {'dis':dis}
    return render(request,'view_feedback.html',d)

@login_required(login_url="login")
def View_My_Detail(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error': error,'pro':sign}
    return render(request,'profile_doctor.html',d)

@login_required(login_url="login")
def Edit_Doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    error = ""
    # type = Type.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        cat = request.POST['type']
        try:
            im = request.FILES['image']
            doc.image=im
            doc.save()
        except:
            pass
        dat = datetime.date.today()
        doc.user.first_name = f
        doc.user.last_name = l
        doc.user.email = e
        doc.contact = con
        doc.category = cat
        doc.address = add
        doc.user.save()
        doc.save()
        error = "create"
    d = {'error':error,'doc':doc,'type':type}
    return render(request,'edit_doctor.html',d)

@login_required(login_url="login")
def Edit_My_deatail(request):
    terror = ""
    print("Hii welvome")
    user = User.objects.get(id=request.user.id)
    error = ""
    # type = Type.objects.all()
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        try:
            im = request.FILES['image']
            sign.image = im
            sign.save()
        except:
            pass
        to1 = datetime.date.today()
        sign.user.first_name = f
        sign.user.last_name = l
        sign.user.email = e
        sign.contact = con
        if error != "pat":
            cat = request.POST['type']
            sign.category = cat
            sign.save()
        sign.address = add
        sign.user.save()
        sign.save()
        terror = "create"
    d = {'error':error,'terror':terror,'doc':sign}
    return render(request,'edit_profile.html',d)

@login_required(login_url='login')
def sent_feedback(request):
    terror = None
    if request.method == "POST":
        username = request.POST['uname']
        message = request.POST['msg']
        username = User.objects.get(username=username)
        Feedback.objects.create(user=username, messages=message)
        terror = "create"
    return render(request, 'sent_feedback.html',{'terror':terror})


@login_required(login_url='login')
def upload_ecg(request):
    """Upload ECG image for analysis"""
    error = ""
    if request.method == "POST" and request.FILES.get('ecg_image'):
        try:
            from .ecg_predictor import ECGPredictor
            
            # Get uploaded file
            ecg_file = request.FILES['ecg_image']
            
            # Save temporarily
            patient = Patient.objects.get(user=request.user)
            ecg_record = ECG_Prediction.objects.create(
                patient=patient,
                ecg_image=ecg_file
            )
            
            # Get file path
            ecg_image_path = ecg_record.ecg_image.path
            
            # Process ECG
            predictor = ECGPredictor()
            result = predictor.predict_from_ecg_image(ecg_image_path)
            
            if result['success']:
                # Update record with prediction
                ecg_record.prediction_code = result['prediction_code']
                ecg_record.prediction_label = result['prediction_label']
                ecg_record.prediction_message = result['prediction_message']
                ecg_record.confidence = result.get('confidence')
                ecg_record.save()
                
                # Redirect to result page
                return redirect('ecg_result', ecg_record.id)
            else:
                error = result.get('error', 'Failed to process ECG image')
                ecg_record.delete()
        
        except Exception as e:
            error = str(e)
    
    d = {'error': error}
    return render(request, 'upload_ecg.html', d)

@login_required(login_url='login')
def ecg_result(request, ecg_id):
    """Display ECG prediction result"""
    try:
        ecg_record = ECG_Prediction.objects.get(id=ecg_id, patient__user=request.user)
        
        # Get nearby doctors
        patient = Patient.objects.get(user=request.user)
        doctors = Doctor.objects.filter(address__icontains=patient.address, status=1)
        
        d = {
            'ecg_record': ecg_record,
            'doctors': doctors
        }
        return render(request, 'ecg_result.html', d)
    
    except ECG_Prediction.DoesNotExist:
        return redirect('upload_ecg')

@login_required(login_url='login')
def ecg_history(request):
    """View ECG prediction history"""
    try:
        patient = Patient.objects.get(user=request.user)
        ecg_records = ECG_Prediction.objects.filter(patient=patient).order_by('-created')
        d = {'ecg_records': ecg_records}
        return render(request, 'ecg_history.html', d)
    except:
        return redirect('user_home')


@login_required(login_url='login')
def find_doctors(request):
    """Find nearby cardiac doctors with map"""
    import json
    
    try:
        patient = Patient.objects.get(user=request.user)
        
        # Get all approved cardiologists
        doctors = Doctor.objects.filter(status=1).order_by('hospital_name')
        
        # Prepare doctor data for map
        doctors_data = []
        for doctor in doctors:
            doctors_data.append({
                'id': doctor.id,
                'name': f"Dr. {doctor.user.first_name} {doctor.user.last_name}",
                'hospital': doctor.hospital_name or 'Private Practice',
                'address': doctor.address,
                'contact': doctor.contact,
                'specialization': doctor.specialization or 'Cardiologist',
                'latitude': doctor.latitude or 0,
                'longitude': doctor.longitude or 0,
            })
        
        context = {
            'doctors': doctors,
            'doctors_json': json.dumps(doctors_data),
            'patient_address': patient.address
        }
        
        return render(request, 'find_doctors.html', context)
    
    except Patient.DoesNotExist:
        return redirect('patient_home')

@login_required(login_url='login')
def book_appointment(request, doctor_id):
    """Book appointment with a doctor"""
    try:
        patient = Patient.objects.get(user=request.user)
        doctor = Doctor.objects.get(id=doctor_id, status=1)
        
        error = ""
        success = ""
        
        if request.method == "POST":
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
            reason = request.POST.get('reason', '')
            
            # Get related prediction/ECG if provided
            prediction_id = request.POST.get('prediction_id')
            ecg_id = request.POST.get('ecg_id')
            
            related_prediction = None
            related_ecg = None
            
            if prediction_id:
                try:
                    related_prediction = Search_Data.objects.get(id=prediction_id, patient=patient)
                except:
                    pass
            
            if ecg_id:
                try:
                    related_ecg = ECG_Prediction.objects.get(id=ecg_id, patient=patient)
                except:
                    pass
            
            # Create appointment
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                related_prediction=related_prediction,
                related_ecg=related_ecg,
                status='pending'
            )
            
            success = "Appointment booked successfully! The doctor will confirm shortly."
            
        context = {
            'doctor': doctor,
            'error': error,
            'success': success
        }
        
        return render(request, 'book_appointment.html', context)
    
    except (Patient.DoesNotExist, Doctor.DoesNotExist):
        return redirect('find_doctors')

@login_required(login_url='login')
def my_appointments(request):
    """View patient's appointments"""
    try:
        patient = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')
        
        context = {'appointments': appointments}
        return render(request, 'my_appointments.html', context)
    
    except Patient.DoesNotExist:
        return redirect('patient_home')

@login_required(login_url='login')
def cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    try:
        patient = Patient.objects.get(user=request.user)
        appointment = Appointment.objects.get(id=appointment_id, patient=patient)
        
        if appointment.status == 'pending' or appointment.status == 'confirmed':
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, 'Appointment cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel this appointment.')
        
        return redirect('my_appointments')
    
    except (Patient.DoesNotExist, Appointment.DoesNotExist):
        return redirect('my_appointments')


@login_required(login_url='login')
def ai_book_appointment(request):
    """Initiate AI call to book appointment"""
    from .ai_calling_agent import create_simple_booking_call
    import re
    
    if request.method == "POST":
        hospital_name = request.POST.get('hospital_name')
        hospital_phone = request.POST.get('hospital_phone')
        hospital_address = request.POST.get('hospital_address')
        
        print(f"DEBUG: Received booking request for {hospital_name}")
        print(f"DEBUG: Phone number received: {hospital_phone}")
        
        try:
            patient = Patient.objects.get(user=request.user)
            patient_name = f"{request.user.first_name} {request.user.last_name}"
            patient_contact = patient.contact
            
            # Format phone number to E.164 format if needed
            if hospital_phone and not hospital_phone.startswith('+'):
                # Remove all non-digit characters
                clean_phone = re.sub(r'\D', '', hospital_phone)
                
                # Add country code if not present
                if len(clean_phone) == 10:  # Indian number without country code
                    hospital_phone = f"+91{clean_phone}"
                elif len(clean_phone) == 11 and clean_phone.startswith('0'):
                    hospital_phone = f"+91{clean_phone[1:]}"
                elif not clean_phone.startswith('91'):
                    hospital_phone = f"+{clean_phone}"
                else:
                    hospital_phone = f"+{clean_phone}"
                
                print(f"DEBUG: Formatted phone to: {hospital_phone}")
            
            # Get reason from recent ECG or prediction
            reason = "Cardiac consultation - Recent ECG analysis showed concerning results"
            
            # Initiate AI call
            print(f"DEBUG: Calling create_simple_booking_call with phone: {hospital_phone}")
            result = create_simple_booking_call(
                hospital_phone,
                patient_name,
                patient_contact,
                reason
            )
            
            print(f"DEBUG: Call result: {result}")
            
            if result['success']:
                messages.success(
                    request,
                    f"✅ AI Agent is calling {hospital_name} to book your appointment. "
                    f"Call SID: {result.get('call_sid', 'N/A')}. "
                    f"You'll receive an SMS confirmation shortly."
                )
            else:
                error_msg = result.get('error', result.get('message', 'Unknown error'))
                messages.error(request, f"❌ Failed to initiate call: {error_msg}")
                print(f"DEBUG: Call failed with error: {error_msg}")
        
        except Exception as e:
            error_msg = str(e)
            messages.error(request, f"❌ Error: {error_msg}")
            print(f"DEBUG: Exception occurred: {error_msg}")
            import traceback
            traceback.print_exc()
        
        return redirect('find_doctors')
    
    return redirect('find_doctors')

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def ai_call_handler(request):
    """Handle AI call conversation flow with Gemini AI"""
    from .ai_calling_agent import AICallingAgent
    from twilio.twiml.voice_response import VoiceResponse
    
    print(f"\n{'='*60}")
    print(f"🎯 AI CALL HANDLER TRIGGERED")
    print(f"{'='*60}")
    print(f"Method: {request.method}")
    print(f"Path: {request.path}")
    print(f"GET params: {dict(request.GET)}")
    print(f"POST params: {dict(request.POST)}")
    
    agent = AICallingAgent()
    stage = request.GET.get('stage', 'greeting')
    call_sid = request.GET.get('call_sid', request.POST.get('CallSid', ''))
    
    print(f"DEBUG: AI Call Handler - Stage: {stage}, CallSid: {call_sid}")
    
    # Get speech result if available
    speech_result = request.POST.get('SpeechResult', '')
    print(f"DEBUG: Speech Result: {speech_result}")
    
    # Get patient data from URL params
    patient_name = request.GET.get('patient_name', '')
    patient_contact = request.GET.get('patient_contact', '')
    reason = request.GET.get('reason', 'Cardiac consultation')
    
    patient_data = {
        'name': patient_name,
        'contact': patient_contact,
        'reason': reason
    }
    
    # Handle different conversation stages
    if stage == 'greeting':
        # Initial greeting with patient data
        data = {'patient_data': patient_data}
        twiml = agent.create_twiml_response('greeting', data=data, call_sid=call_sid)
    
    elif stage == 'conversation':
        # AI-powered conversation
        patient_name = request.GET.get('patient_name', '')
        patient_contact = request.GET.get('patient_contact', '')
        reason = request.GET.get('reason', 'Cardiac consultation')
        
        patient_data = {
            'name': patient_name,
            'contact': patient_contact,
            'reason': reason
        }
        
        data = {
            'SpeechResult': speech_result,
            'patient_data': patient_data
        }
        
        twiml = agent.create_twiml_response('conversation', data=data, call_sid=call_sid)
    
    elif stage == 'confirm_appointment':
        # Final confirmation
        twiml = agent.create_twiml_response('confirm_appointment')
    
    else:
        # Default fallback
        twiml = agent.create_twiml_response('greeting', call_sid=call_sid)
    
    print(f"DEBUG: Generated TwiML: {twiml[:200]}...")
    return HttpResponse(twiml, content_type='text/xml')

@csrf_exempt
def call_status(request):
    """Handle call status callbacks"""
    call_sid = request.POST.get('CallSid')
    call_status = request.POST.get('CallStatus')
    
    # Log call status (in production, save to database)
    print(f"Call {call_sid} status: {call_status}")
    
    return HttpResponse('OK')
