from flask import Flask, render_template, request,send_from_directory, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials


application = Flask(__name__)

@application.route('/')
def add_request():    
    return render_template('index.html')



def insert_into_gdrive(data_list):
    '''
    insert into the google sheet in the order
    name, contact_num,lat, lon, address,
    rice_qty, wheat_qty, oil_qty, daal_qty,
    request_status
    '''

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    print(creds)
    print(type(creds))


    # print(creds)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Details_People").sheet1
    row = data_list
    index = len(sheet.get_all_values())+1
    sheet.insert_row(row, index)


def get_requests():
    '''
    insert into the google sheet in the order
    name, contact_num,lat, lon, address,
    rice_qty, wheat_qty, oil_qty, daal_qty,
    request_status
    '''

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    print(creds)
    print(type(creds))


    # print(creds)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Details_People").sheet1

    

    list_of_requests=(sheet.get_all_values())
    print("length of data is ",len(sheet.get_all_values()))
    request_status_index=5

    list_requests=[]
    
    # skip the first request since it is heading
    for request in list_of_requests[1:]:
        

        if request[request_status_index]=="Requested":
            dict_request={}
            for val in request:
                dict_request["name"]=val[0]
                dict_request["contact_num"]=val[0]
                dict_request["lat"]=val[0]
                dict_request["lon"]=val[0]
                dict_request["requestor_address"]=val[0]
                dict_request["rice_qty"]=val[0]
                dict_request["wheat_qty"]=val[0]
                dict_request["oil_qty"]=val[0]
                dict_request["daal_qty"]=val[0]
            list_requests.append(dict_request)

    return list_requests

    

@application.route('/pending',methods=["POST"])
def pending():
    '''
    this function shows pending requests
    '''
    list_requests=get_requests()
    print("requests are ",list_requests)

    return render_template("gallery.html", items=list_requests)



@application.route('/load_in_db',methods=["POST"])
def add_mosque():

    data_list=[]
    print(request.form.keys)
    name=str(request.form['requestor_name'])
    contact_num=str(request.form['contact_num'])

    lat=str(request.form['mosque_lat'])
    lon=str(request.form['mosque_lon'])
    requestor_address=str(request.form['requestor_address'])
    request_status="Requested"

    # here get approx location from lat long
    approx_location="Home"
    

    rice_qty=str(request.form['rice_qty'])
    wheat_qty=str(request.form['wheat_qty'])
    oil_qty=str(request.form['oil_qty'])
    daal_qty=str(request.form['daal_qty'])

    

    data_list.append(name)
    data_list.append(contact_num)

    data_list.append(lat)
    data_list.append(lon)
    data_list.append(requestor_address)   
    data_list.append(request_status) 

    data_list.append(rice_qty)
    data_list.append(wheat_qty)
    data_list.append(oil_qty)
    data_list.append(daal_qty)

    



    print(name,lat,lon,contact_num,rice_qty,wheat_qty,oil_qty)



    
    insert_into_gdrive(data_list)

    return "Thanks for requesting. We will get back to you soon."



if __name__ == "__main__":
    
    application.run(debug=True)




