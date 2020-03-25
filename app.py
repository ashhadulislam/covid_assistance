from flask import Flask, render_template, request,send_from_directory, jsonify, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials


application = Flask(__name__)

# column number where status is mentioned in the sheet
request_status_index=4
# counting from 0
# when using in sheet, add 1

# column number where benificiary number is mentioned in the sheet
beneficiary_contact_index=9
# counting from 0
# when using in sheet, add 1


@application.route('/')
def show_home():    
    return render_template('base.html')



@application.route('/addneedy')
def addneedy():    
    return render_template('addneedy.html')

@application.route('/contact')
def contact():    
    return render_template('contact.html')


def get_sheet():
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
    return sheet




def get_requests(status):
    '''
    insert into the google sheet in the order
    name, contact_num,lat, lon, address,
    rice_qty, wheat_qty, oil_qty, daal_qty,
    request_status
    '''

    sheet=get_sheet()



    

    list_of_requests=(sheet.get_all_values())
    print("number of rows ",len(sheet.get_all_values()))
    print("number of columns ",len(sheet.get_all_values()[0]))
    

    list_requests=[]
    
    # skip the first request since it is heading
    for the_request in list_of_requests[1:]:
        print(the_request[request_status_index])
        

        if the_request[request_status_index]==status:
            dict_request={}
            dict_request["request_id"]=the_request[0]

            dict_request["name"]=the_request[1]
            dict_request["contact_num"]=the_request[2]
            # dict_request["lat"]=int(float(the_request[3]))
            # dict_request["lon"]=int(float(the_request[4]))
            dict_request["requestor_address"]=the_request[3]
            dict_request["request_status"]=the_request[4]

            dict_request["rice_qty"]=the_request[5]
            dict_request["wheat_qty"]=the_request[6]
            dict_request["oil_qty"]=the_request[7]
            dict_request["daal_qty"]=the_request[8]

            list_requests.append(dict_request)

    return list_requests




@application.route('/pending',methods=["GET"])
def pending():
    '''
    this function shows pending requests
    '''
    list_requests=get_requests(status="Pending")
    print("requests are ",list_requests)

    return render_template("pending.html", items=list_requests)


@application.route('/completed',methods=["GET"])
def complete():
    '''
    this function shows completed requests
    '''    
    list_requests=get_requests(status="Completed")
    print("requests are ",list_requests)

    return render_template("completed.html", items=list_requests)    

@application.route('/mark_as_complete',methods=["POST"])
def mark_as_complete():

    list_ids_to_mark_complete=[]
    print(request.form.keys)
    for key,val in request.form.items():
        print(key)
        if key!="contact_num":
            list_ids_to_mark_complete.append(int(float(val)))
    print(list_ids_to_mark_complete)
    benificiary_contact=request.form['contact_num']

    sheet=get_sheet()
    list_of_requests=(sheet.get_all_values())

    row_count=2
    for the_request in list_of_requests[1:]:

        if int(float(the_request[0])) in list_ids_to_mark_complete:
            sheet.update_cell(row_count, request_status_index+1, "Completed")
            sheet.update_cell(row_count, beneficiary_contact_index+1, str(benificiary_contact))
        row_count+=1

    return render_template('thank-you.html')



def insert_into_gsheet(data_list):
    '''
    insert into the google sheet in the order
    name, contact_num,lat, lon, address,
    rice_qty, wheat_qty, oil_qty, daal_qty,
    request_status
    '''
    sheet=get_sheet()
    
    row = data_list
    index = len(sheet.get_all_values())+1
    print("last id ",sheet.get_all_values()[-1][0])
    if len(sheet.get_all_values())>=2:
        request_id=int(sheet.get_all_values()[-1][0])+1
    else:
        # first request
        request_id=1
    row=[request_id]+row
    sheet.insert_row(row, index)



@application.route('/load_in_sheet',methods=["POST"])
def add_pending_request():

    data_list=[]
    # print(request.form.keys)
    name=str(request.form['requestor_name'])
    contact_num=str(request.form['contact_num'])

    # lat=str(request.form['mosque_lat'])
    # if lat=="":
    #     lat=0

    # lon=str(request.form['mosque_lon'])
    # if lon=="":
    #     lon=0

    requestor_address=str(request.form['requestor_address'])
    request_status="Pending"

    # here get approx location from lat long
    approx_location="Home"
    

    rice_qty=str(request.form['rice_qty'])
    wheat_qty=str(request.form['wheat_qty'])
    oil_qty=str(request.form['oil_qty'])
    daal_qty=str(request.form['daal_qty'])

    

    data_list.append(name)
    data_list.append(contact_num)

    # data_list.append(lat)
    # data_list.append(lon)
    data_list.append(requestor_address)   
    data_list.append(request_status) 

    data_list.append(rice_qty)
    data_list.append(wheat_qty)
    data_list.append(oil_qty)
    data_list.append(daal_qty)

    



    print(name,contact_num,rice_qty,wheat_qty,oil_qty)



    
    insert_into_gsheet(data_list)

    return "Thanks for requesting. We will get back to you soon."



if __name__ == "__main__":
    
    application.run(debug=True)




