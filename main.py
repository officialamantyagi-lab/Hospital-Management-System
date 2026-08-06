from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse
from database import connection as conn
from starlette.responses import Response
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from typing import Optional
import pymysql
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
app = FastAPI(title="Hospital Management System")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

cursor = conn.cursor(pymysql.cursors.DictCursor)

@app.get("/login")
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": ""
        }
    )
    
@app.post("/login")
async def login(

    request: Request,

    username: str = Form(...),
    password: str = Form(...)

):

    if username == "admin" and password == "admin123":

        response = RedirectResponse(
            url="/",
            status_code=303
        )

        response.set_cookie(
            key="user",
            value="admin"
        )

        return response

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error":"Invalid Username or Password"
        }
    )

@app.get("/")
async def dashboard(request: Request):
    cookie = request.cookies.get("user")

    if cookie != "admin":

     return RedirectResponse(
        url="/login",
        status_code=303
    )

    # Total Patients
    cursor.execute("SELECT COUNT(*) AS total FROM Patient order by id ASC")
    patients = cursor.fetchone()["total"]

    # Total Doctors
    cursor.execute("SELECT COUNT(*) AS total FROM Doctor")
    doctors = cursor.fetchone()["total"]

    # Total Appointments
    cursor.execute("SELECT COUNT(*) AS total FROM Appointment")
    appointments = cursor.fetchone()["total"]

    # Total Revenue
    cursor.execute("SELECT IFNULL(SUM(amount),0) AS revenue FROM Billing")
    revenue = cursor.fetchone()["revenue"]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "patients": patients,
            "doctors": doctors,
            "appointments": appointments,
            "revenue": revenue
        }
    )
    
@app.get("/patient")
async def patient_page(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="patient.html",
    context={}
)


@app.post("/add_patient")
async def add_patient(

patient_name:str=Form(...),
gender:str=Form(...),
age:int=Form(...),
phone:str=Form(...),
address:str=Form(...),
blood_group:str=Form(...)

):

    sql="""

    INSERT INTO Patient

    (patient_name,gender,age,phone,address,blood_group)

    VALUES(%s,%s,%s,%s,%s,%s)

    """

    values=(

    patient_name,

    gender,

    age,

    phone,

    address,

    blood_group

    )

    cursor.execute(sql,values)

    conn.commit()

    return RedirectResponse(
        "/patient",
        status_code=303
    )
    
@app.get("/patients")
async def patients(
    request: Request,
    search: Optional[str] = None
):

    if search:

        cursor.execute(
            "SELECT * FROM Patient WHERE patient_name LIKE %s ORDER BY patient_id DESC",
            (f"%{search}%",)
        )

    else:

        cursor.execute(
            "SELECT * FROM Patient ORDER BY patient_id DESC"
        )

    patients = cursor.fetchall()

    return templates.TemplateResponse(
        request=request,
        name="patients.html",
        context={
            "patients": patients
        }
    )
    
    # ================= DELETE PATIENT =================

@app.get("/delete_patient/{patient_id}")
async def delete_patient(patient_id: int):

    cursor.execute(
        "DELETE FROM Patient WHERE patient_id=%s",
        (patient_id,)
    )

    conn.commit()

    return RedirectResponse(
        url="/patients",
        status_code=303
    )


# ================= EDIT PATIENT PAGE =================

@app.get("/edit_patient/{patient_id}")
async def edit_patient(request: Request, patient_id: int):

    cursor.execute(
        "SELECT * FROM Patient WHERE patient_id=%s",
        (patient_id,)
    )

    patient = cursor.fetchone()

    return templates.TemplateResponse(
        request=request,
        name="patient.html",
        context={
            "patient": patient
        }
    )


# ================= UPDATE PATIENT =================

@app.post("/update_patient/{patient_id}")
async def update_patient(

    patient_id:int,

    patient_name:str=Form(...),
    gender:str=Form(...),
    age:int=Form(...),
    phone:str=Form(...),
    address:str=Form(...),
    blood_group:str=Form(...)

):

    cursor.execute("""

    UPDATE Patient

    SET

    patient_name=%s,
    gender=%s,
    age=%s,
    phone=%s,
    address=%s,
    blood_group=%s

    WHERE patient_id=%s

    """,

    (

    patient_name,
    gender,
    age,
    phone,
    address,
    blood_group,
    patient_id

    )

    )

    conn.commit()

    return RedirectResponse(
        url="/patients",
        status_code=303
    )
    
    # ================= DOCTOR PAGE =================

@app.get("/doctor")
async def doctor_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="doctor.html",
        context={}
    )


# ================= ADD DOCTOR =================

@app.post("/add_doctor")
async def add_doctor(

    doctor_name: str = Form(...),
    gender: str = Form(...),
    phone: str = Form(...),
    specialization: str = Form(...),
    experience: int = Form(...),
    department_id: int = Form(...)

):

    cursor.execute("""

    INSERT INTO Doctor

    (doctor_name,gender,phone,specialization,experience,department_id)

    VALUES(%s,%s,%s,%s,%s,%s)

    """,

    (

    doctor_name,
    gender,
    phone,
    specialization,
    experience,
    department_id

    )

    )

    conn.commit()

    return RedirectResponse(
        url="/doctor",
        status_code=303
    )


# ================= VIEW DOCTORS =================

@app.get("/doctors")
async def doctors(request: Request):

    cursor.execute(
        "SELECT * FROM Doctor ORDER BY doctor_id DESC"
    )

    doctors = cursor.fetchall()

    return templates.TemplateResponse(
        request=request,
        name="doctors.html",
        context={
            "doctors": doctors
        }
    )


# ================= DELETE DOCTOR =================

@app.get("/delete_doctor/{doctor_id}")
async def delete_doctor(doctor_id: int):

    cursor.execute(
        "DELETE FROM Doctor WHERE doctor_id=%s",
        (doctor_id,)
    )

    conn.commit()

    return RedirectResponse(
        url="/doctors",
        status_code=303
    )
    
# ================= APPOINTMENT PAGE =================

@app.get("/appointment")
async def appointment_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="appointment.html",
        context={}
    )


# ================= ADD APPOINTMENT =================

@app.post("/add_appointment")
async def add_appointment(

    patient_id: int = Form(...),
    doctor_id: int = Form(...),
    appointment_date: str = Form(...),
    appointment_time: str = Form(...),
    status: str = Form(...)

):

    cursor.execute("""

    INSERT INTO Appointment

    (patient_id,doctor_id,appointment_date,appointment_time,status)

    VALUES(%s,%s,%s,%s,%s)

    """,

    (

        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        status

    )

    )

    conn.commit()

    return RedirectResponse(
        url="/appointment",
        status_code=303
    )


# ================= VIEW APPOINTMENTS =================

@app.get("/appointments")
async def appointments(request: Request):

    cursor.execute(
        "SELECT * FROM Appointment ORDER BY appointment_id DESC"
    )

    appointments = cursor.fetchall()

    return templates.TemplateResponse(
        request=request,
        name="appointments.html",
        context={
            "appointments": appointments
        }
    )


# ================= DELETE APPOINTMENT =================

@app.get("/delete_appointment/{appointment_id}")
async def delete_appointment(appointment_id: int):

    cursor.execute(
        "DELETE FROM Appointment WHERE appointment_id=%s",
        (appointment_id,)
    )

    conn.commit()

    return RedirectResponse(
        url="/appointments",
        status_code=303
    )
    
# ================= MEDICINE PAGE =================

@app.get("/medicine")
async def medicine_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="medicine.html",
        context={}
    )


# ================= ADD MEDICINE =================

@app.post("/add_medicine")
async def add_medicine(

    medicine_name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...)

):

    cursor.execute("""

    INSERT INTO Medicine

    (medicine_name,price,stock)

    VALUES(%s,%s,%s)

    """,

    (

        medicine_name,
        price,
        stock

    )

    )

    conn.commit()

    return RedirectResponse(
        url="/medicine",
        status_code=303
    )


# ================= VIEW MEDICINES =================

@app.get("/medicines")
async def medicines(request: Request):

    cursor.execute(
        "SELECT * FROM Medicine ORDER BY medicine_id DESC"
    )

    medicines = cursor.fetchall()

    return templates.TemplateResponse(
        request=request,
        name="medicines.html",
        context={
            "medicines": medicines
        }
    )


# ================= DELETE MEDICINE =================

@app.get("/delete_medicine/{medicine_id}")
async def delete_medicine(medicine_id: int):

    cursor.execute(
        "DELETE FROM Medicine WHERE medicine_id=%s",
        (medicine_id,)
    )

    conn.commit()

    return RedirectResponse(
        url="/medicines",
        status_code=303
    )
    
# ================= BILLING PAGE =================

@app.get("/billing")
async def billing_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="billing.html",
        context={}
    )


# ================= ADD BILL =================

@app.post("/add_bill")
async def add_bill(

    patient_id: int = Form(...),
    amount: float = Form(...),
    payment_status: str = Form(...),
    bill_date: str = Form(...)

):

    cursor.execute("""

    INSERT INTO Billing

    (patient_id,amount,payment_status,bill_date)

    VALUES(%s,%s,%s,%s)

    """,

    (

        patient_id,
        amount,
        payment_status,
        bill_date

    )

    )

    conn.commit()

    return RedirectResponse(
        url="/billing",
        status_code=303
    )


# ================= VIEW BILLS =================

@app.get("/bills")
async def bills(request: Request):

    cursor.execute(
        "SELECT * FROM Billing ORDER BY bill_id DESC"
    )

    bills = cursor.fetchall()

    return templates.TemplateResponse(
        request=request,
        name="bills.html",
        context={
            "bills": bills
        }
    )


# ================= DELETE BILL =================

@app.get("/delete_bill/{bill_id}")
async def delete_bill(bill_id: int):

    cursor.execute(
        "DELETE FROM Billing WHERE bill_id=%s",
        (bill_id,)
    )

    conn.commit()

    return RedirectResponse(
        url="/bills",
        status_code=303
    )
    
    # ================= EDIT PATIENT =================

@app.get("/edit_patient/{patient_id}")
async def edit_patient(request: Request, patient_id: int):

    cursor.execute(
        "SELECT * FROM Patient WHERE patient_id=%s",
        (patient_id,)
    )

    patient = cursor.fetchone()

    return templates.TemplateResponse(
        request=request,
        name="edit_patient.html",
        context={
            "patient": patient
        }
    )


@app.post("/update_patient/{patient_id}")
async def update_patient(

    patient_id: int,

    patient_name: str = Form(...),
    gender: str = Form(...),
    age: int = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    blood_group: str = Form(...)

):

    cursor.execute("""

    UPDATE Patient

    SET

    patient_name=%s,
    gender=%s,
    age=%s,
    phone=%s,
    address=%s,
    blood_group=%s

    WHERE patient_id=%s

    """,

    (

        patient_name,
        gender,
        age,
        phone,
        address,
        blood_group,
        patient_id

    )

    )

    conn.commit()

    return RedirectResponse(
        url="/patients",
        status_code=303
    )
    
@app.get("/logout")
async def logout():

    response = RedirectResponse(
        url="/login",
        status_code=303
    )

    response.delete_cookie("user")

    return response

@app.get("/print_bill/{bill_id}")
async def print_bill(bill_id: int):

    cursor.execute("SELECT * FROM Billing WHERE bill_id=%s", (bill_id,))
    bill = cursor.fetchone()

    pdf = f"bill_{bill_id}.pdf"

    doc = SimpleDocTemplate(pdf)

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = Paragraph(
        "<font color='darkblue'><b>HOSPITAL MANAGEMENT SYSTEM</b></font>",
        title
    )

    address = Paragraph(
        "<b>City Care Hospital</b><br/>"
        "Meerut, Uttar Pradesh<br/>"
        "Phone : +91-9876543210<br/>"
        "Email : hospital@gmail.com",
        styles["Normal"]
    )

    invoice = Paragraph(
        f"<b>Invoice No :</b> INV-{bill['bill_id']}<br/>"
        f"<b>Date :</b> {bill['bill_date']}",
        styles["Normal"]
    )

    data = [

    ["Patient ID", bill["patient_id"]],

    ["Bill Amount", f"₹ {bill['amount']}"],

    ["Payment Status", bill["payment_status"]],

    ["Bill Date", str(bill["bill_date"])]

    ]

    table = Table(data, colWidths=[180,220])

    table.setStyle(TableStyle([

    ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#0d6efd")),

    ("TEXTCOLOR",(0,0),(0,-1),colors.white),

    ("BACKGROUND",(1,0),(1,-1),colors.beige),

    ("GRID",(0,0),(-1,-1),1,colors.black),

    ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

    ("BOTTOMPADDING",(0,0),(-1,-1),10),

    ("TOPPADDING",(0,0),(-1,-1),10),

    ("ALIGN",(0,0),(-1,-1),"CENTER")

    ]))

    thank = Paragraph(
        "<br/><br/><b>Thank You For Visiting Our Hospital.</b>",
        title
    )

    sign = Paragraph(
        "<br/><br/>Authorized Signature<br/><br/>_____________________",
        styles["Normal"]
    )

    doc.build([
        heading,
        Spacer(1,15),
        address,
        Spacer(1,15),
        invoice,
        Spacer(1,20),
        table,
        Spacer(1,40),
        sign,
        Spacer(1,20),
        thank
    ])
    return FileResponse(
            pdf,
            media_type="application/pdf",
            filename=pdf
    )