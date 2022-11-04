import webbrowser
from filestack import Client
from fpdf import FPDF


class Bill:
    def __init__(self, amount, period):
        self.amount = amount
        self.period = period


class Flatmate:
    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, flatmate2):
        weight = self.days_in_house / (self.days_in_house + flatmate2.days_in_house)
        to_pay = bill.amount * weight
        return to_pay


class PdfReport:
    def __init__(self, filename):
        self.filename = filename

    def generate(self, flatmate1, flatmate2, bill):
        pdf = FPDF(orientation= "P", unit="pt", format= "A4")
        pdf.add_page()

        # Add icon
        pdf.image("house.png", w=40, h=40)

        # Insert title
        pdf.set_font(family= "Times", size= 24, style= "B")
        pdf.cell(w=0, h=80, txt="Flatmates Bill", border=1, align="C", ln=1)

        # Insert period label and value
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=100, h=40, txt="Period:", border=0)
        pdf.cell(w=150, h=40, txt=bill.period, border=0, ln=1)

        # Insert name and due amount of the first flatmate
        pdf.set_font(family="Times", size=12)
        flatmate1_pay = str(round(flatmate1.pays(bill, flatmate2), 2))
        pdf.cell(w=100, h=25, txt=flatmate1.name, border=0)
        pdf.cell(w=150, h=25, txt=flatmate1_pay, border=0, ln=1)

        # Insert name and due amount of the second flatmate
        pdf.set_font(family="Times", size=12)
        flatmate2_pay = str(round(flatmate2.pays(bill, flatmate1), 2))
        pdf.cell(w=100, h=25, txt=flatmate2.name, border=0)
        pdf.cell(w=150, h=25, txt=flatmate2_pay, border=0, ln=1)

        pdf.output(self.filename)
        webbrowser.open(self.filename)


class FileSharer:
    def __init__(self, filepath, api_key="AViVqp7suSQWWEdrl6hf9z"):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url


amount = float(input("Please enter the bill amount: "))
month = input("Please enter the month. E.g. March 2022: ")
name1 = input("What is your name? ")
days_in_house1 = int(input(f"How long did {name1} stay at the House during the bill period? "))

name2 = input("What is your name? ")
days_in_house2 = int(input(f"How long did {name2} stay at the House during the bill period? "))

the_bill = Bill(amount, month)
flatmate1 = Flatmate(name1, days_in_house1)
flatmate2 = Flatmate(name2, days_in_house2)
print(the_bill.amount)
print(the_bill.period)
print(f"{name1} pays:", flatmate1.pays(the_bill, flatmate2))
print(f"{name2} pays:", flatmate2.pays(the_bill, flatmate1))
pdf_report = PdfReport(filename="../Report1.pdf")
pdf_report.generate(flatmate1, flatmate2, bill=the_bill)

file_sharer = FileSharer(filepath= pdf_report.filename)
print(file_sharer.share())