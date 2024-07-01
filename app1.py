from flask import Flask, render_template, request
import csv
from jinja2 import Template
import matplotlib.pyplot as plt

app = Flask(__name__)

class csvreader:
    def __init__(self,path) -> None:        
        def csvread(path):
            with open(path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                data= list(csv_reader)
                return data
        
        self.data = csvread(path)
    
    def student_data(self, sid):
        lst= []
        i = 0
        while i<len(self.data):            
            if self.data[i][0] == sid:
                lst.append({"Student ID": sid.strip(), "Course ID": self.data[i][1].strip(), "Marks": self.data[i][2].strip()})
            i +=1
        return lst
    
    def course_data(self, cid):
        lst= []
        i=0
        while i<len(self.data):
            if self.data[i][1].strip() == cid.strip():
                lst.append(int(self.data[i][2]))
            i +=1
        return lst


def average(lst):
    return sum(lst)/len(lst)


def barchart(lst_values):
    plt.bar(lst_values, color='deepskyblue', height = 1, width=7)
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    # plt.title("Marks vs Frequency")
    plt.savefig('static\img.png')
    # plt.show()

# def render_course_page(lst, avg, maxi):
#     my_html_document_file = open('templates\course_details.html', 'w')
#     my_html_document_file.write(render_template('templates\course_details.html', lst=lst, average_marks=avg, maximum_marks=maxi))
#     my_html_document_file.close()

# def  render_student_page(lst_values, sum):
#     my_html_document_file = open('templates\student_details.html', 'w')
#     my_html_document_file.write(render_template(lst_values=lst_values, total_marks_data = sum))
#     my_html_document_file.close()

def sum_marks(lst):
    add= 0
    for x in lst:
        add += int(x['Marks'])
    return add

#data =  csvreader('data.csv')
def isvalidPath(rqust):
    idr  = rqust.form.get("ID")
    txtvalue = rqust.form.get("id_value")
    if idr == None:
        print("Nothing is  selected in radio")
        return (False,idr,txtvalue)
   
    if txtvalue == '':
        print("No input paramete")
        return (False,idr,txtvalue)
        
    #paths =  + "data.csv"
    paths = "./data.csv"
    data =  csvreader(paths)
    if idr == 'student_id':
        lst =  data.student_data(txtvalue.strip())
        if len(lst) == 0 :
            print("Invalid student ranges")
            return (False,idr,txtvalue.strip())
        else:
            return (True,idr,txtvalue.strip())
    if idr == 'course_id':
        lst =  data.course_data(txtvalue.strip())
        print(txtvalue.strip())
        if len(lst) == 0 :
            print("Invalid course ranges")
            return (False,idr,txtvalue.strip())
        else:
            return (True,idr,txtvalue.strip())
    
    return (False,None,None)
    



    

@app.route("/",methods =["GET", "POST"])
def index():    
    if request.method == "POST":         
         val = isvalidPath(request)
         if val[0] == False:
             return render_template("error.html",template_folder='templates')         
         if val[0] == True:
             #paths = app.root_path + "\\data.csv"
             paths = "./data.csv"
             data =  csvreader(paths)    
             if  val[1] == 'course_id':                              
                 lst_values = data.course_data(str(val[2]))
                 barchart(lst_values)
                 avg = average(lst_values)
                 maxi = max(lst_values)
                 lst = []
                 lst.append(avg)
                 lst.append(maxi)
                #  print(avg)
                #  print(maxi)
                #  render_course_page(lst, avg, maxi)
                 return render_template("course_details.html",template_folder='templates',lst=lst, average_marks=avg, maximum_marks=maxi)
             if val[1] == 'student_id':
                 lst_values = data.student_data(str(val[2]))
                 add = sum_marks(lst_values)
                 print(add)
                #  render_student_page(lst_values, add)
                 return render_template("student_details.html",template_folder='templates', total_marks_data = add)                  
    return render_template("index.html",template_folder='templates')








if __name__ == '__main__':
    #app.debug=True
    
    #app.run(port=7765)
    # app.run()
    app.run(debug=True, port=7765)
