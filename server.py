from flask import Flask, jsonify
from flask import request
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient(
    "mongodb+srv://moshemoshe:qazQAZ123@cluster0.fandl.mongodb.net/?retryWrites=true&w=majority")
app.config['DB'] = client.get_database('salarymanagement')
db = app.config['DB']
col_employees = db.employees


@app.route("/get_all_employees")
def get_all_employees():
    try:
        employees_list = []
        cursor = col_employees.find({})  # find all employees
        for employee in cursor:
            employees_list.append({'Name': employee['Name'], 'Email': employee['Email'],
                                   'Address': employee["Address"], "Phone": employee["Phone"],
                                   'MaritalStatus': employee['MaritalStatus'], 'Gender': employee['Gender'],
                                   'Salary': employee['Salary'], 'id': employee['id']})
        return jsonify(list_employees=employees_list), 200
    except:
        return jsonify(message="Error in get_all_employees"), 500


@app.route("/get_employee", methods=['POST'])
def get_employee():
    try:
        request_json = request.get_json()
        email = request_json["Email"]
        cursor = col_employees.find({'Email': email})[0]
        employee = {}
        for key in cursor:
            if key != '_id':
                employee[key] = cursor[key]
                return jsonify(employee=employee), 200
    except:
        return jsonify(message="Error in get_employee"), 500


@app.route("/upload_employee", methods=['POST'])
def upload_employee():
    if request.method == 'POST':
        request_json = request.get_json()
        name = request_json["Name"]
        email = request_json["Email"]
        address = request_json["Address"]
        phone = request_json["Phone"]
        maritalStatus = request_json['MaritalStatus']
        gender = request_json['Gender']
        salary = request_json['Salary']
        try:
            employee_email_mongo = col_employees.find_one({"Email": email})
            if employee_email_mongo == None:  # if employee does not exist in DB
                col_employees.insert_one(
                    {'Name': name, 'Email': email, 'Address': address,
                     'Phone': phone, 'MaritalStatus': maritalStatus, 'Gender': gender, 'Salary': salary})
                return jsonify(message="Employee Uploaded"), 200
            else:
                return jsonify(message="Employee Already Exists"), 404
        except:
            return jsonify(message="Error in uploading Employee"), 500


@app.route("/update_employee", methods=['PATCH'])
def update_employee():
    if request.method == 'PATCH':
        request_json = request.get_json()
        email = request_json["Email"]
        address = request_json["Address"]
        phone = request_json["Phone"]
        maritalStatus = request_json['MaritalStatus']
        gender = request_json['Gender']
        id = request_json['id']
        salary = request_json['Salary']
        try:
            employee_email_mongo = col_employees.find_one({"id": id})
            if employee_email_mongo != None:  # if employee exist in DB
                col_employees.update_one({"id": id}, {"$set": {'Address': address}})
                col_employees.update_one({"id": id}, {"$set": {'Phone': phone}})
                col_employees.update_one({"id": id}, {"$set": {'MaritalStatus': maritalStatus}})
                col_employees.update_one({"id": id}, {"$set": {'Email': email}})
                col_employees.update_one({"id": id}, {"$set": {'Gender': gender}})
                col_employees.update_one({"id": id}, {"$set": {'Salary': salary}})

                return jsonify(message="Employee Updated"), 200
            else:
                return jsonify(message="Employee Not Exists"), 404
        except:
            return jsonify(message="Error in updating Employee"), 500


@app.route("/compare_between_employees", methods=['POST'])
def compare_between_employees():
    try:
        request_json = request.get_json()
        employee1_email = request_json["employee1_email"]
        employee2_email = request_json["employee2_email"]
        employees_list = []
        cursor = col_employees.find({})  # find all employees
        for employee in cursor:
            employees_list.append({'Name': employee['Name'], 'Email': employee['Email'], 'Address': employee["Address"],
                                   "Phone": employee["Phone"], 'MaritalStatus': employee['MaritalStatus'],
                                   'Gender': employee['Gender'], 'Salary': employee['Salary']})
            employee1 = [cdict for cdict in employees_list if cdict["Email"] == employee1_email][0]
            employee2 = [cdict for cdict in employees_list if cdict["Email"] == employee2_email][0]
            print(employee1, "dd")
            chosen_name_employee = employee1["Name"] if employee1["Salary"] > employee2["Salary"] else employee2["Name"]
            richer = 1 if employee1["Salary"] > employee2["Salary"] else 2
            salary1 = employee1["Salary"] if richer == 1 else employee2["Salary"]
            salary2 = employee1["Salary"] if not richer == 1 else employee2["Salary"]

        return jsonify(chosen_name_employee=chosen_name_employee, salary1=salary1, salary2=salary2), 200
    except:
        return jsonify(message="error in compare_between_employees"), 500


@app.route("/delete_all_employees", methods=['POST'])
def delete_all_employees():
    try:
        col_employees.delete_many({})
        return jsonify(message="employees data deleted"), 200
    except:
        return jsonify(message="error in compare_between_employees"), 500


if __name__ == '__main__':
    app.run(debug=True)
