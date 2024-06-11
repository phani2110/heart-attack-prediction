from flask import Flask, render_template, request, url_for, send_file, flash, redirect, make_response
import pickle
import numpy as np
import os
import json
import termcolor
import smtplib

import CurrentStats
# import CancerModel
# import PdfConverter
# from PdfConverter import PDFPageCountError
#import DiseasePred

# import warnings

app = Flask(__name__)
app.config['SECRET_KEY'] = '73a4b6ca8cb647a20b71423e31492452'



# For Heart Disease
with open("HeartDisease", "rb") as f:
    randomForest = pickle.load(f)


@app.route("/")
 
@app.route("/home")
def Homepage():
    # cases, cured, death = CurrentStats.currentStatus()
    return render_template("Homepage.html", feedback="False")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("PageNotFound.html")




@app.route("/about")
def About():
    return render_template("About.html")


@app.route("/contact", methods=["POST", "GET"])
def Contact():
    if request.method == "POST":
        # print(request.form)
        contactDict = request.form
        firstname = contactDict['firstname']
        lastname = contactDict['lastname']
        email = contactDict['email']
        phone = int(contactDict['phone'])
        description = contactDict['description']

        subject = "Medical Website feedback !!"
        message = f"First Name : {firstname} \nLast Name : {lastname} \nEmail : {email}\nPhone Number : {phone}\nDescription : {description}\n"
        content = f"Subject : {subject} \n\n{message}"
        sender = "intmain1221@gmail.com"
        receiver = "intmain1221@gmail.com"
        password = "intmain@11"

        print(content)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as mail:
                mail.ehlo()
                mail.starttls()
                mail.login(sender, password)
                mail.ehlo()
                mail.sendmail(sender, receiver, content)

            print("Mail Send Successfully !")
            cases, cured, death = CurrentStats.currentStatus()
            return render_template("Homepage.html", cases=cases, cured=cured, death=death, feedback="True")

        except:
            pass
    return render_template("Contact.html")


@app.route("/infected")
def Infected():
    return render_template("Infected.htm", disease="Nothing")


@app.route("/noninfected")
def NonInfected():
    return render_template("NonInfected.htm")


@app.route("/download")
def Download():
    file = "static/Example.docx"
    return send_file(file, as_attachment=True)




@app.route("/HeartDisease", methods=["POST", "GET"])
def Heart_disease():
    if request.method == "POST":
        # print(request.form)
        heart_dict = request.form
        age = int(heart_dict['age'])
        gender = int(heart_dict['gender'])
        height = int(heart_dict['height'])
        weight = int(heart_dict['weight'])
        sbp = int(heart_dict['sbp'])
        dbp = int(heart_dict['dbp'])
        cholestrol = int(heart_dict['cholestrol'])
        glucose = int(heart_dict['glucose'])
        smoke = int(heart_dict['smoke'])
        alcohol = int(heart_dict['alcohol'])
        active = int(heart_dict['active'])
        age = age*365
        model_input = [age, gender, height, weight, sbp,
                       dbp, cholestrol, glucose, smoke, alcohol, active]
        prediction = randomForest.predict([model_input])[0]

        if prediction:
            return render_template("HeartInfected.htm", disease="Heart Attack")
        else:
            return render_template("NonInfected.htm")

    return render_template("HeartDisease.html", title="Heart Attack Detector", navTitle="Heart Attack Detector", headText="Heart Attack Probabilty Detector", ImagePath="/static/HeartPulse.png")






if __name__ == '__main__':
    app.run(threaded=True, debug=True)
