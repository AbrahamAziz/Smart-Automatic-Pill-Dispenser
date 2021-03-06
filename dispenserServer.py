from flask import Flask, render_template, request
app = Flask(__name__)

# Initialize lists and pill names for the times and the number of pills
pill1_hour_list = []
pill1_minute_list = []
pill1_name = ''
pill1_num = []

pill2_hour_list = []
pill2_minute_list = []
pill2_name = ''
pill2_num = []

pill3_hour_list = []
pill3_minute_list = []
pill3_name = ''
pill3_num = []



# Append to a list the number of minutes (easier to compare)
def convert_to_min(minute, hour, combined):
    for x in range(len(hour)):
        hour_to_minute = int(hour[x]) * 60
        combined.append(int(minute[x]) + hour_to_minute)


# Convert back to the hour and minute format
def convert_back(combined, hour, minute):
    for x in range(len(combined)):
        temp = combined[x] / 60
        hour[x] = int(temp)
        minute[x] = combined[x] - (hour[x] * 60)
        # To display on the web page the correct formatting
        minute[x] = format(minute[x], "02")


# Counting (aka Gravity) Sort
def sort(arr):
    output = [0 for i in range(1441)]
    count = [0 for i in range(1441)]
    for x in arr:
        count[int(x)] += 1
    for a in range(1441):
        count[a] += count[a - 1]
    for i in range(len(arr)):
        output[count[arr[i]] - 1] = arr[i]
        count[arr[i]] -= 1
    for i in range(len(arr)):
        arr[i] = output[i]


@app.route("/")
def main():
    templateData = {
        'Pill1_Hour_List': pill1_hour_list,
        'Pill1_Minute_List': pill1_minute_list,
        'Pill1_Name': pill1_name,
        'Pill1_Num': pill1_num,

        'Pill2_Hour_List': pill2_hour_list,
        'Pill2_Minute_List': pill2_minute_list,
        'Pill2_Name': pill2_name,
        'Pill2_Num': pill2_num,

        'Pill3_Hour_List': pill3_hour_list,
        'Pill3_Minute_List': pill3_minute_list,
        'Pill3_Name': pill3_name,
        'Pill3_Num': pill3_num,

       

    }
    return render_template('arduinotime.html', **templateData)


@app.route("/", methods=['POST'])
def add_time():
    # Yup, still using global variables
    global pill1_name
    global pill2_name
    global pill3_name
    

    # Just for sorting
    pill1_combined = []
    pill2_combined = []
    pill3_combined = []
  

    # Take the input from the html page on when the pills are being dispensed
    pill_type = request.form['pills']
    num_pills = request.form['numberPills']
    hour = request.form['hour']
    minute = request.form['minute']
    name = request.form['name']

    # Put everything in lists
    if pill_type == "pill1":
        pill1_name = name
        pill1_num.append(num_pills)
        pill1_minute_list.append(minute)
        pill1_hour_list.append(hour)
        
    elif pill_type == "pill2":
        pill2_name = name
        pill2_num.append(num_pills)
        pill2_minute_list.append(minute)
        pill2_hour_list.append(hour)
        
    elif pill_type == "pill3":
        pill3_name = name
        pill3_num.append(num_pills)
        pill3_minute_list.append(minute)
        pill3_hour_list.append(hour)

    

    # Convert them all to minutes and store in the corresponding combined time
    convert_to_min(pill1_minute_list, pill1_hour_list, pill1_combined)
    convert_to_min(pill2_minute_list, pill2_hour_list, pill2_combined)
    convert_to_min(pill3_minute_list, pill3_hour_list, pill3_combined)
  

    # Sort the pills for being displayed
    sort(pill1_combined)
    sort(pill2_combined)
    sort(pill3_combined)
   

    # After they are sorted put them back into minute and hour lists
    convert_back(pill1_combined, pill1_hour_list, pill1_minute_list)
    convert_back(pill2_combined, pill2_hour_list, pill2_minute_list)
    convert_back(pill3_combined, pill3_hour_list, pill3_minute_list)


    # This is the data that gets sent to the html page
    templateData = {
        'Pill1_Hour_List': pill1_hour_list,
        'Pill1_Minute_List': pill1_minute_list,
        'Pill1_Name': pill1_name,
        'Pill1_Num': pill1_num,

        'Pill2_Hour_List': pill2_hour_list,
        'Pill2_Minute_List': pill2_minute_list,
        'Pill2_Name': pill2_name,
        'Pill2_Num': pill2_num,

        'Pill3_Hour_List': pill3_hour_list,
        'Pill3_Minute_List': pill3_minute_list,
        'Pill3_Name': pill3_name,
        'Pill3_Num': pill3_num,

     

        'pill_type': pill_type
    }

    # Render the data to be displayed on the html page
    return render_template('arduinotime.html', **templateData)


if __name__ == '__main__':
    # Host this one locally on port 80
    app.run(host='0.0.0.0', port=80, debug=True)
