import tkinter as tk
import tkinter.messagebox
import mysql.connector
db = mysql.connector.connect(user = 'root',password = 'admin123',host='localhost',database = 'hospital')
c = db.cursor()
class HospManagement(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginPage)
    def switch_frame(self, frame_class):
        """De stroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
class LoginPage(tk.Frame):
    def __init__(self,master):
            tk.Frame.__init__(self, master)
            self.heading = tk.Label(self, text="Hospital Management System",height = 5, font=('arial 40 bold'), fg='black', bg='lightgreen').pack()
            self.email = tk.Label(self, text="Email Id", font=('arial 18 bold'), fg='black', bg='yellow').pack()
            self.email_ent = tk.Entry(self,fg='lightgreen', width=30)
            self.email_ent.pack()
            self.password = tk.Label(self, text="Password", font=('arial 18 bold'), fg='black', bg='yellow').pack()
            self.password_ent = tk.Entry(self,show="*" ,width=30)
            self.password_ent.pack()
            self.submit = tk.Button(self, text="Login", width=20, height=2, bg='steelblue', command = lambda : self.genric(master)).pack()
            self.register = tk.Button(self, text="Register", width=20, height=2, bg='steelblue', command = lambda : master.switch_frame(UserRegistration)).pack()
    
    def genric(self,master):
        email = self.email_ent.get();
        password = self.password_ent.get();
        if(email == "" or password == ""):
            tk.messagebox.showinfo("Warning", "Please Fill Up All Boxes")
            return
        c.execute("""Select email,password,role,F_name from user""")
        results = c.fetchall()
        global NAME
        flag = 0;
        for row in results:
            email1 = row[0]
            password1 = row[1]
            role1 = row[2]
            fname1 = row[3]
            if(email1==email and password1 == password and role1 == "Doctor"):
                NAME = fname1
                tk.messagebox.showinfo("Congrats", "Successful!!")
                master.switch_frame(DoctorPage)
                flag=1
                return
            if(email1==email and password1 == password and role1 == "Patient"):
                NAME = fname1
                tk.messagebox.showinfo("Congrats", "Successful!!")
                master.switch_frame(PatientPage)
                flag=1
                return
            if(email1==email and password1 == password and role1 == "ADMIN"):
                NAME = fname1
                tk.messagebox.showinfo("Congrats", "Successful!!")
                master.switch_frame(ReceptionPage)
                flag=1
                return
        if(flag == 0):
            tk.messagebox.showinfo("Warning", "Login Unsuccessful!!")
            return
            
class PatientPage(tk.Frame):
    def __init__(self, master):
        global NAME
        tk.Frame.__init__(self, master)
        self.master = master
        self.heading=tk.Label(self, text="Welcome " + NAME,width = 20,height = 5, font=('arial 18 bold'), fg='black', bg='lightgreen').pack()
        self.appointment = tk.Button(self,text = "Book an appointment",font = ('arial 18 bold'),command = lambda : master.switch_frame(addAppointment)).pack()
        self.result = tk.Button(self,text = "Results",font = ('arial 18 bold'),command = lambda : master.switch_frame(Results)).pack()
        self.logout = tk.Button(self,text = "Logout",font = ('arial 18 bold'),command = lambda : master.switch_frame(LoginPage)).pack()
class Results(tk.Frame):
    def __init__(self, master):
        global NAME
        tk.Frame.__init__(self, master)
        self.master = master
        self.id = tk.Label(self,text = "Enter Appointment Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.id_ent = tk.Entry(self,width = 10)
        self.id_ent.pack()
        self.check = tk.Button(self,text = "Check",font = ('arial 18 bold'),command = lambda : self.generic7(master)).pack()
        self.back = tk.Button(self,text = "Back",font = ('arial 18 bold'),command = lambda : master.switch_frame(PatientPage)).pack()
    def generic7(self,master):
        global a_id,NAME,d_name,issue,p_id,d_id,medicine,description,solution
        a_id = self.id_ent.get()
        if(a_id == ""):
            tk.messagebox.showinfo("Warning","Please Enter Appointment Id")
            return
        c.execute("""Select id,p_name,d_name,issue,p_id,d_id,medicine,description,solution from record""")
        results = c.fetchall()
        flag = 0
        for row in results:
            if(row[0] == int(a_id)):
                if(row[1] == NAME):
                    d_name = row[2]
                    issue = row[3]
                    p_id = row[4]
                    d_id = row[5]
                    medicine = row[6]
                    description = row[7]
                    solution = row[8]
                    flag = 1
                    break;
        if(flag == 0):
            tk.messagebox.showinfo("Warning", "Appointment Does Not Exist!!")
            return
        if(d_name == ""):
            tk.messagebox.showinfo("Warning", "Doctor Not Assigned Yet")
            return
        if(issue == ""):
            tk.messagebox.showinfo("Warning", "Results Pending")
            return
        tk.messagebox.showinfo("Congrats", "Final Results")
        master.switch_frame(final_list)
class final_list(tk.Frame):
    def __init__(self, master):
        global a_id,NAME,d_name,issue,p_id,d_id,medicine,description,solution
        tk.Frame.__init__(self, master)
        self.master = master
        self.fname = tk.Label(self, text="Patient Name", font=('arial 18 bold'), fg='black', bg='yellow').pack()
        self.fname_ent = tk.Entry(self, width=30)
        self.fname_ent.insert(tk.END,NAME)
        self.fname_ent.pack()
        self.id = tk.Label(self,text = "Patient Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.id_ent = tk.Entry(self,width = 10)
        self.id_ent.insert(tk.END,p_id)
        self.id_ent.pack()
        self.aid = tk.Label(self,text = "Appointment Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.aid_ent = tk.Entry(self, width = 10)
        self.aid_ent.insert(tk.END,a_id)
        self.aid_ent.pack()
        self.issue = tk.Label(self,text = "Issue",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.issue_ent = tk.Entry(self, width = 50)
        self.issue_ent.insert(tk.END,issue)
        self.issue_ent.pack()
        self.doctor_name = tk.Label(self,text = "Doctor",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.doctor_ent = tk.Entry(self, width = 50)
        self.doctor_ent.insert(tk.END,d_name)
        self.doctor_ent.pack()
        self.doctor_id = tk.Label(self,text = "Doctor Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.doctor_id_ent = tk.Entry(self, width = 50)
        self.doctor_id_ent.insert(tk.END,d_id)
        self.doctor_id_ent.pack()
        self.solution = tk.Label(self,text = "Solution",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.solution_ent = tk.Entry(self, width = 50)
        self.solution_ent.insert(tk.END,solution)
        self.solution_ent.pack()
        self.medicine = tk.Label(self,text = "Medicine",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.medicine_ent = tk.Entry(self, width = 50)
        self.medicine_ent.insert(tk.END,medicine)
        self.medicine_ent.pack()
        self.description = tk.Label(self,text = "Description",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.description_ent = tk.Entry(self, width = 50)
        self.description_ent.insert(tk.END,description)
        self.description_ent.pack()
        self.Finish= tk.Button(self, text="Finish",  bg='steelblue',width =10, command = lambda: master.switch_frame(PatientPage)).pack(fill="both")
class addAppointment(tk.Frame):
    def __init__(self,master):
        global NAME
        tk.Frame.__init__(self, master)
        self.master = master
        self.heading=tk.Label(self, text="Appointment",width = 20,height = 5, font=('arial 18 bold'), fg='black', bg='lightgreen').pack()
        self.id = tk.Label(self,text = "Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.id_ent = tk.Entry(self,width = 10)
        self.id_ent.pack()
        self.issue = tk.Label(self,text = "Enter the issue",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.issue_ent = tk.Entry(self,width = 50)
        self.issue_ent.pack()
        self.Book = tk.Button(self,text = "Book",font = ('arial 18 bold'),command = lambda : self.book(master)).pack()
    def book(self,master):
        issue = self.issue_ent.get();
        id1 = self.id_ent.get();
        if(issue == "" or id1 == ""):
            tk.messagebox.showinfo("Warning","Please Enter All The Details")
            return
        global NAME
        name = NAME
        sql = "SELECT f_name,id FROM user"
        c.execute(sql);
        results = c.fetchall();
        for row in results:
            if(row[0] == NAME):
                id2 = row[1]
                break;
        c.execute("""Insert into record(id,p_name,p_id,issue) VALUES (%s,%s,%s,%s)""",(id1, NAME,id2,issue))
        db.commit();
        tk.messagebox.showinfo("Congrats","Apointment Booked!!")
        master.switch_frame(PatientPage)

class DoctorPage(tk.Frame):
    def __init__(self,master):
        global NAME
        tk.Frame.__init__(self,master)
        self.master = master
        self.heading=tk.Label(self,text = "Welcome " + NAME,bg = "lightgreen",font = ('arial 20 bold'),width = 30, height = 10).pack();
        self.id = tk.Label(self,text = "Enter Appointment Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.id_ent = tk.Entry(self,width = 10)
        self.id_ent.pack()
        self.Update= tk.Button(self, text="Update Appointment",  bg='steelblue',width =10, command = lambda: self.generic5(master)).pack(fill="both")
        self.Logout= tk.Button(self, text="Logout",  bg='steelblue',width =10, command = lambda: master.switch_frame(LoginPage)).pack(fill="both")
    def generic5(self,master):
        global a_id,name,id2,issue,dname;
        global NAME;
        a_id = self.id_ent.get();
        if(a_id == ""):
            tk.messagebox.showinfo("Warning","Please Enter Appointment Id")
            return
        c.execute("""Select id,p_name,p_id,issue,d_name from record""")
        results = c.fetchall();
        flag = 0
        for row in results:
            if(row[0] == int(a_id)):
                flag =1
                name = row[1]
                id2=row[2]
                issue = row[3]
                dname = row[4]
                break
        if(flag==0):
            tk.messagebox.showinfo("Warning","Id Not Found!!")
            return
        if(dname!=NAME):
            tk.messagebox.showinfo("Warning","Not Assigned to this patient")
            return
        master.switch_frame(UpdateIssue)
class UpdateIssue(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master
        global a_id,name,id2,issue;
        self.fname = tk.Label(self, text="Patient Name", font=('arial 18 bold'), fg='black', bg='yellow').pack()
        self.fname_ent = tk.Entry(self, width=30)
        self.fname_ent.insert(tk.END,name)
        self.fname_ent.pack()
        self.id = tk.Label(self,text = "Patient Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.id_ent = tk.Entry(self,width = 10)
        self.id_ent.insert(tk.END,id2)
        self.id_ent.pack()
        self.aid = tk.Label(self,text = "Appointment Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.aid_ent = tk.Entry(self, width = 10)
        self.aid_ent.insert(tk.END,a_id)
        self.aid_ent.pack()
        self.issue = tk.Label(self,text = "Issue",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.issue_ent = tk.Entry(self, width = 50)
        self.issue_ent.insert(tk.END,issue)
        self.issue_ent.pack()
        self.solution = tk.Label(self,text = "Solution",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.solution_ent = tk.Entry(self, width = 50)
        self.solution_ent.pack()
        self.medicine = tk.Label(self,text = "Medicine",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.medicine_ent = tk.Entry(self, width = 50)
        self.medicine_ent.pack()
        self.description = tk.Label(self,text = "Description",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.description_ent = tk.Entry(self, width = 50)
        self.description_ent.pack()
        self.Update= tk.Button(self, text="Update",  bg='steelblue',width =10, command = lambda: self.generic6(master)).pack(fill="both")
    def generic6(self,master):
        global a_id;
        solution = self.solution_ent.get()
        medicine = self.medicine_ent.get()
        description = self.description_ent.get()
        if(solution == "" or medicine == "" or description == ""):
            tk.messagebox.showinfo("Warning","Please Fill The Required Fields")
            return
        sql = """Update record set solution = %s,medicine = %s,description = %s where id = %s"""
        b = (solution,medicine,description,a_id,)
        c.execute(sql,b)
        db.commit()
        tk.messagebox.showinfo("Congrats","You Updated The Fields!")
        master.switch_frame(DoctorPage)
class ReceptionPage(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master
        self.heading=tk.Label(self, text="Welcome Admin " ,width = 20,height = 10, font=('arial 20 bold'), fg='black', bg='lightgreen').pack()
        self.id = tk.Label(self,text = "Enter Appointment Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.id_ent = tk.Entry(self,width = 10)
        self.id_ent.pack()
        self.Update= tk.Button(self, text="Update Appointment",  bg='steelblue',width =10, command = lambda: self.generic3(master)).pack(fill="both")
        self.Remove= tk.Button(self, text="Delete Appointment",  bg='steelblue',width =10, command = lambda: self.generic4(master)).pack(fill="both")
        self.Logout= tk.Button(self, text="Logout",  bg='steelblue',width =10, command = lambda: master.switch_frame(LoginPage)).pack(fill="both")
        
    def generic3(self,master):
        global a_id,name,id2,issue;
        a_id = self.id_ent.get();
        if(a_id == ""):
            tk.messagebox.showinfo("Warning","Please Enter Appointment Id")
            return
        c.execute("""Select id,p_name,p_id,issue from record""")
        results = c.fetchall();
        flag = 0
        for row in results:
            if(row[0] == int(a_id)):
                flag =1
                name = row[1]
                id2=row[2]
                issue = row[3]
                break
        if(flag==0):
            tk.messagebox.showinfo("Warning","Id Not Found!!")
            return
        master.switch_frame(UpdateAppointment);
    def generic4(self,master):
        global a_id;
        a_id = self.id_ent.get();
        c.execute("""Select id,p_name,p_id,issue from record""")
        results = c.fetchall();
        flag = 0
        for row in results:
            if(row[0] == int(a_id)):
                flag =1
                name = row[1]
                id2=row[2]
                issue = row[3]
                break
        if(flag==0):
            tk.messagebox.showinfo("Warning","Id Not Found!!")
            return
        sql = """delete from record where id = %s"""
        c.execute(sql,(a_id,))
        db.commit()
        tk.messagebox.showinfo("Congrats","Id Deleted")
class UpdateAppointment(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master
        global a_id,name,id2,issue;
        self.fname = tk.Label(self, text="Patient Name", font=('arial 18 bold'), fg='black', bg='yellow').pack()
        self.fname_ent = tk.Entry(self, width=30)
        self.fname_ent.insert(tk.END,name)
        self.fname_ent.pack()
        self.id = tk.Label(self,text = "Patient Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.id_ent = tk.Entry(self,width = 10)
        self.id_ent.insert(tk.END,id2)
        self.id_ent.pack()
        self.aid = tk.Label(self,text = "Appointment Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.aid_ent = tk.Entry(self, width = 10)
        self.aid_ent.insert(tk.END,a_id)
        self.aid_ent.pack()
        self.issue = tk.Label(self,text = "Issue",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.issue_ent = tk.Entry(self, width = 50)
        self.issue_ent.insert(tk.END,issue)
        self.issue_ent.pack()
        self.dname = tk.Label(self, text="Doctor Name", font=('arial 18 bold'), fg='black', bg='yellow').pack()
        self.dname_ent = tk.Entry(self, width=30)
        self.dname_ent.pack()
        self.did = tk.Label(self,text = "Doctor Id",font = ('arial 18 bold'),bg = 'yellow').pack()
        self.did_ent = tk.Entry(self, width = 10)
        self.did_ent.pack()
        self.Update= tk.Button(self, text="Change",  bg='steelblue',width =10, command = lambda: self.generic4(master)).pack(fill="both")
    def generic4(self,master):
        dname = self.dname_ent.get()
        d_id = self.did_ent.get()
        issue = self.issue_ent.get()
        pname = self.fname_ent.get()
        p_id = self.id_ent.get()
        c.execute("Select f_name,id from user")
        results = c.fetchall()
        flag = 0
        for row in results:
            if(dname == row[0] and int(d_id) == row[1]):
                flag = 1
                break;
        if(flag==0):
            tk.messagebox.showinfo("Warning","Doctor Not Found!")
            return
        global a_id
        c.execute("""Update record set d_id = %s,d_name = %s where id = %s""",(d_id,dname,a_id))
        db.commit()
        tk.messagebox.showinfo("Congrats","Values Updated")
        master.switch_frame(ReceptionPage) 
class UserRegistration(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.master = master
        self.heading = tk.Label(self, text="User Registration",width = 20,height = 10, font=('arial 20 bold'), fg='black', bg='lightgreen').pack(fill='both')
        self.id = tk.Label(self,text = "Id",font = ('arial 18 bold'),bg = 'yellow').pack(fill='both')
        self.id_ent = tk.Entry(self,width = 10)
        self.id_ent.pack()
        self.fname = tk.Label(self, text="First Name", font=('arial 18 bold'), fg='black', bg='yellow').pack(fill='both')
        self.fname_ent = tk.Entry(self, width=30)
        self.fname_ent.pack()
        self.lname = tk.Label(self, text="Last Name", font=('arial 18 bold'), fg='black', bg='yellow').pack(fill='both')
        self.lname_ent = tk.Entry(self, width=30)
        self.lname_ent.pack()
        self.email = tk.Label(self, text="Email Id", font=('arial 18 bold'), fg='black', bg='yellow').pack(fill='both')
        self.email_ent = tk.Entry(self, width=30)
        self.email_ent.pack()
        self.password = tk.Label(self, text="Password", font=('arial 18 bold'), fg='black', bg='yellow').pack(fill='both')
        self.password_ent = tk.Entry(self,show="*" ,width=30)
        self.password_ent.pack()
        self.role = tk.Label(self, text="Role", font=('arial 18 bold'), fg='black', bg='yellow').pack(fill='both')
        self.role_ent = tk.Entry(self, width=30)
        self.role_ent.pack()
        self.phone = tk.Label(self, text="Phone", font=('arial 18 bold'), fg='black', bg='yellow').pack(fill='both')
        self.phone_ent = tk.Entry(self, width=30)
        self.phone_ent.pack()
        self.button= tk.Button(self, text="Register",  bg='steelblue',width =10,height = 2, command = lambda: self.genric1(master)).pack(fill="both")
    def genric1(self,master):
        id1 = self.id_ent.get()
        fname = self.fname_ent.get()
        lname = self.lname_ent.get()
        email = self.email_ent.get()
        password = self.password_ent.get()
        role = self.role_ent.get()
        phone = self.phone_ent.get()
        if(id1=="" or fname=="" or lname=="" or email=="" or password=="" or role=="" or phone==""):
            tk.messagebox.showinfo("Warning", "Please Fill Up All Boxes")
            return
        c.execute("""INSERT INTO user VALUES (%s,%s,%s,%s,%s,%s,%s) """,(id1,fname, lname,email,role,phone,password))
        tk.messagebox.showinfo("Congrats","Registration Succesfull!!")
        db.commit()
        master.switch_frame(LoginPage)     
if __name__ == "__main__":
    app = HospManagement()
    app.mainloop()
db.close()
