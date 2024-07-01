from flask import render_template
from jinja2 import Template
import sys
import  csv
import matplotlib.pyplot as plt
# COURSE_ID = 'Course ID'
# STUDENT_ID = 'Student ID'
# MARKS = ' Marks'
class csvreader:
    def __init__(self,path) -> None:        
        def csvread(path):
            with open(path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                data= list(csv_reader)
                print(data)
                return data
        
        self.data = csvread(path)
    
    # print(student_data)
    def student_data(self, sid):
        lst= []
        i = 0
        print(self.data)
        while i<len(self.data):            
            if self.data[i][0] == sid:
                lst.append({"Student ID":sid,"Course ID":self.data[i][1],'Marks':self.data[i][2]})
            i +=1
        return lst
    
    def course_data(self, cid):
        lst= []
        i=0
        while i<len(self.data):
            if self.data[i][1] == cid:
                lst.append(int(self.data[i][2]))
            i +=1
        return lst
    
    # def isValidCommandLine(lst):
    #     n = len(lst)
    #     ags = []
    #     for i in range(1, n):
    #         ags.append(lst[i])
    #     if len(ags) != 2:
    #         return (False,None,None)
    #     if ags[0] not  in  ['-s','-c']:
    #         return (False,None,None)
    # # df = csv_reader
    #     if ags[0] == '-s':
    #         lst_students = df[STUDENT_ID]
    #     # .to_list()
    #         if int(ags[1]) in lst_students:
    #             return (True,'-s', int(ags[1]))
    #     if ags[0] == '-c':
    #         lst_courses = df[COURSE_ID]
    #     # .to_list()   
    #         if int(ags[1]) in lst_courses:
    #             return (True,'-c', int(ags[1]))
    

    #     return (False,None,None)
        # console.log(average(counts));
Template_Course = """
<!DOCTYPE html>
<head>
        <meta charset="UTF-8"/>
        <title> Course Details </title>
        <meta name="description" content="This page describes the course details"/>
    <script>
    window.onload = function(){
    var table = document.getElementById("table");
    var js_array = {{ lst_values | safe }};
        const max = Math.max(...js_array);
        var sum = 0
        for (var i = 0; i < js_array.length; i++) {
      sum += js_array[i];
    }
        const average = sum / js_array.length;
        table.rows[table.rows.length - 1].cells[0].innerHTML = average;
        table.rows[table.rows.length - 1].cells[1].innerHTML = max;
    };
    </script>
    <style>
        table,th,td{
        border: 1px solid black;
        }
    </style>
</head>
<body>
    <h1> Course Details </h1>
    <table id="table">
    <tr>
    <th>Average Marks</th>
    <th>Maximum Marks</th>
    </tr>
    <tr>
    <td></td>
    <td></td>
    </tr>
    </table>
<img src="img.png" alt="My Plot">
</body>
</html>
"""





Template_Error ="""
<!DOCTYPE html>
<head>
        <meta charset="UTF-8"/>
        <title> Error Page </title>
        <meta name="description" content="Something went Wrong"/>

</head>
<body>
    <h1> Wrong Inputs </h1>
    <h3>Something Went Wrong</h3>
</body>
</html>
"""




TEMPLATE_Student ="""
<!DOCTYPE html>
<head>
        <meta charset="UTF-8"/>
        <title> Students </title>
        <meta name="description" content="This page lists Student Details"/>
<script>
  window.onload = function() {
    var table = document.getElementById("table");
    var sum = 0;
    for (var i = 1; i < table.rows.length - 1; i++) {
      sum += parseFloat(table.rows[i].cells[2].innerHTML);
    }
    
    table.rows[table.rows.length - 1].cells[1].innerHTML = sum;
  };
</script>
<style>
table,th,td{
    border: 1px solid black;
}
</style>
</head>
<body>
     <h1> Student Details </h1>
    <table id="table">
        <thead>
            <tr>
              <th>Student ID</th>
              <th>Course ID</th>
              <th>Marks</th>
          </tr>
        </thead>
        <tbody>
            {% for row in lst_values %}
            <tr>
            <td>{{row['Student ID']}}</td>
            <td>{{row['Course ID']}}</td>
            <td>{{row['Marks']}}</td>
            </tr>
            {% endfor %}
            <tr>
            <td colspan="2">Total Marks</td>
            {% for row in lst_values %}
            <td rowspan= "3"></td>
            {% endfor %}
            </tr>
        </tbody>
    </table>                  
</body>
</html>
"""



def render_error_page():
    template = Template(Template_Error)
    my_html_document_file = open('Output.html', 'w')
    my_html_document_file.write(template.render())
    my_html_document_file.close()

def  render_student_page(lst_values):
    template = Template(TEMPLATE_Student)
    my_html_document_file = open('Output.html', 'w')
    my_html_document_file.write(template.render(lst_values=lst_values))
    my_html_document_file.close()

def render_course_page(lst_values):
    template = Template(Template_Course)
    my_html_document_file = open('Output.html', 'w')
    my_html_document_file.write(template.render(lst_values=lst_values))
    my_html_document_file.close()

    
def isValidCommandLine(lst):
    a = csvreader('data.csv')
    n = len(lst)
    ags = []
    for i in range(1, n):
        ags.append(lst[i])
    if len(ags) != 2:
        return (False,None,None)
    if ags[0] not  in  ['-s','-c']:
        return (False,None,None)
    # df = csv_reader
    if ags[0] == '-s':
        data = a.student_data(ags[1])
        if len(data) >0:
            # print(int(ags[1]))
            return (True,'-s', int(ags[1]))
            
    if ags[0] == '-c':
        data = a.course_data(ags[1])
        if len(data) > 0:
            return (True,'-c', int(ags[1]))

    return (False,None,None)

def main():
    a = csvreader('data.csv')
    status = isValidCommandLine(sys.argv)
    if status[0] == False:
        render_error_page()
    # df = csv_reader    
    if status[0] == True:
        if status[1] == '-s':
            sid = status[2]
            lst_values = a.student_data(str(sid))
            render_student_page(lst_values)
        else:
            cid = status[2]
            lst_values = a.course_data(str(cid))
            barchart(lst_values)
            
            render_course_page(lst_values)
            #convert result to dictionary
   
def barchart(lst_values):
    plt.bar(lst_values, color='deepskyblue', height = 1, width=7)
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    # plt.title("Marks vs Frequency")
    plt.savefig('img.png')
    # plt.show()
if __name__ == "__main__":
    main()

