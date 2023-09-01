from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import imutils
import dlib
from pygame import mixer
import tkinter as tk
from tkinter import Button, Label, Toplevel
from imutils import face_utils
import numpy as np
import datetime
import os

def main():
    win=Tk()
    app=Login_window(win)
    win.mainloop()



class Login_window:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
     

        img=Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\bbg.jpg")
        img=img.resize((1550,800))
        self.photoimg=ImageTk.PhotoImage(img)
        
        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=1550,height=800)


        frame=Frame(self.root,bg="#81808E")
        frame.place(x=610,y=170,width=340,height=450)


        img1=Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\logfr.png")
        img1=img1.resize((100,100))
        self.photoimg1=ImageTk.PhotoImage(img1)

        lblimg1=Label(image=self.photoimg1,bg="black",borderwidth=0)
        lblimg1.place(x=730,y=175,width=100,height=85)

        get_str=Label(frame,text="Get Started",font=("times new roman",20,"bold"),fg="#312B35",bg="white")
        get_str.place(x=95,y=100)

        ##############label user name #################3333
        usernamee=lbl=Label(frame,text="Username:",font=("times new roman",15,"bold"),fg="#312B35",bg="white")
        usernamee.place(x=40,y=140)

        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)

        password=lbl=Label(frame,text="Password:",font=("times new roman",15,"bold"),fg="#312B35",bg="white")
        password.place(x=40,y=215)

        self.txtpass=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtpass.place(x=40,y=250,width=270)

        
###### login button ############

        loginbtn=Button(frame,text="Login",command=self.login,font=("times new roman",15,"bold"),bd=3,cursor="hand2",relief=RIDGE,fg="#312B35",bg="white",activeforeground="white",activebackground="black")
        loginbtn.place(x=110,y=300,width=120,height=35)

##################register button ###########33
        registerbtn=Button(frame,text=" New User Register",cursor="hand2",borderwidth=0,command=self.register_window,font=("times new roman",10,"bold"),fg="#312B35",bg="white",activeforeground="white",activebackground="black")
        registerbtn.place(x=20,y=350,width=160)
        
        forgetbtn=Button(frame,text="Forget Password",cursor="hand2",command=self.forgot_password_window,borderwidth=0,font=("times new roman",10,"bold"),fg="#312B35",bg="white",activeforeground="white",activebackground="black")
        forgetbtn.place(x=16,y=380,width=160)


    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)


    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Eroor","all field required")
        elif self.txtuser.get()=="bhavesh" and self.txtpass.get()=="066":
             messagebox.showinfo("Success","Welcome to Face Recognition Attendence System ")  
        else:
            conn=mysql.connector.connect(host="localhost",port="3306",user="root",password="root",database="Drowsiness")
            my_cursor=conn.cursor()
            query = "SELECT * FROM register WHERE email = %s AND password = %s"
            my_cursor.execute(query, (self.txtuser.get(), self.txtpass.get()))
                     
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Username and password")
            else:
                open_main=messagebox.askyesno("YesNo","Acess only admin")
            if open_main>0:
                new_window = Toplevel(self.root)  # Create a new Toplevel instance
                app = DrowsinessDetectionApp(new_window)
            else:
                if not open_main:
                    return
        conn.commit()
        conn.close()

        ################## reset passowrd #################
    def reset_pass(self):
        if self.combo_security_Q.get() == "select":
            messagebox.showerror("Error", "Select the security Question")
        elif self.security_A_entry.get() == "":
            messagebox.showerror("Error", "Please enter the answer")
        elif self.txt_newpass.get() == "":
            messagebox.showerror("Error", "Please enter the new password")
        else:
            conn = mysql.connector.connect(host="localhost", port="3306", user="root", password="root", database="Drowsiness")
            my_cursor = conn.cursor()
            query = ("select * from register where email=%s and securityQ=%s and securityA=%s")
            value = (self.txtuser.get(), self.combo_security_Q.get(), self.security_A_entry.get())
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Please enter correct Answer")
            else:
                query = ("update register set password=%s where email=%s")
                value = (self.txt_newpass.get(), self.txtuser.get())
                my_cursor.execute(query, value)
    
                conn.commit()
                conn.close()
                messagebox.showinfo("Info", "Your password has been reset, please login with the new password")

##################################forot passsowrd #################3

    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter the email address to reset password ")
        else:
            conn=mysql.connector.connect(host="localhost",port="3306",user="root",password="root",database="Drowsiness")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
           # print(row)

            if row==None:
                messagebox.showerror("Error","Please Enter The Valid Username")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forgot Password")
                self.root2.geometry("340x450+610+170")

                l=Label(self.root2,text="Forgot Password",font=("times new roman",15,"bold"),fg="black",bg="white")
                l.place(x=0,y=10,relwidth=1)

                security_Q=Label(self.root2,text="Select Security Question",font=("times new roman",15,"bold"),fg="black",bg="white")
                security_Q.place(x=50,y=80)
          
                self.combo_security_Q=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo_security_Q["values"]=("Select","Your Birth Place","Your Nick Name")
                self.combo_security_Q.place(x=50,y=110,width=250)
                self.combo_security_Q.current(0)
          
                 
                security_A=Label(self.root2,text="Security answer",font=("times new roman",15,"bold"),fg="black",bg="white")
                security_A.place(x=50,y=150)
          
                self.security_A_entry=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.security_A_entry.place(x=50,y=180,width=250)



                new_password_A=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),fg="black",bg="white")
                new_password_A.place(x=50,y=220)
                                     
                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",15,"bold"))
                self.txt_newpass.place(x=50,y=250,width=150)

                btn=Button(self.root2,text="Reset",command=self.reset_pass,font=("times new roman",15,"bold"),fg="black",bg="white")
                btn.place(x=50,y=280,width=150)



class Register:
    def __init__(self,root):
      self.root=root
      self.root.title("Register")
      self.root.geometry("1500x840+0+0")
      
      ######################### variables ############3333
      self.var_fname=StringVar()
      self.var_lname=StringVar()
      self.var_contact=StringVar()
      self.var_email=StringVar()
      self.var_securityQ=StringVar(value="Select")
      self.var_securityA=StringVar()
      self.var_pass=StringVar()
      self.var_confpass=StringVar()



      ###################background image #################
      img=Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\bbg.jpg")
      img=img.resize((1550,800))
      self.photoimg=ImageTk.PhotoImage(img)
        
      bg_lbl=Label(self.root,image=self.photoimg)
      bg_lbl.place(x=0,y=0,width=1550,height=800)
 #####################333frame#############

      frame=Frame(self.root,bg="white")
      frame.place(x=100,y=160,width=850,height=550)

      register_lbl=Label(frame,text="Register Here",font=("times new roman",20,"bold"),fg="black",bg="white")
      register_lbl.place(x=20,y=20)
   
    ####lables#################### and entry ##########33

      fname=Label(frame,text="First Name",font=("times new roman",15,"bold"),fg="black",bg="white")
      fname.place(x=50,y=100)

      fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
      fname_entry.place(x=50,y=130,width=250)

      lname=Label(frame,text="Last Name",font=("times new roman",15,"bold"),fg="black",bg="white")
      lname.place(x=370,y=100)

      lname_entry=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
      lname_entry.place(x=370,y=130,width=250)

      contact=Label(frame,text="Contact No",font=("times new roman",15,"bold"),fg="black",bg="white")
      contact.place(x=50,y=170)

      fname_entry=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15,"bold"))
      fname_entry.place(x=50,y=200,width=250)

      email=Label(frame,text="Email",font=("times new roman",15,"bold"),fg="black",bg="white")
      email.place(x=370,y=170)

      email_entry=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15,"bold"))
      email_entry.place(x=370,y=200,width=250)

      security_Q=Label(frame,text="Select Security Question",font=("times new roman",15,"bold"),fg="black",bg="white")
      security_Q.place(x=50,y=240)

      self.combo_security_Q=ttk.Combobox(frame,textvariable=self.var_securityQ,font=("times new roman",15,"bold"),state="readonly")
      self.combo_security_Q["values"]=("Select","Your Birth Place","Your Nick Name")
      self.combo_security_Q.place(x=50,y=270,width=250)
      self.combo_security_Q.current(0)

       
      security_A=Label(frame,text="Security answer",font=("times new roman",15,"bold"),fg="black",bg="white")
      security_A.place(x=370,y=240)

      security_A_entry=ttk.Entry(frame,textvariable=self.var_securityA,font=("times new roman",15,"bold"))
      security_A_entry.place(x=370,y=270,width=250)
    
      pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="black",bg="white")
      pswd.place(x=50,y=310)

      pswd_entry=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15,"bold"))
      pswd_entry.place(x=50,y=340,width=250)

      confirm_pswd=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),fg="black",bg="white")
      confirm_pswd.place(x=370,y=310)

      confirm_pswd_entry=ttk.Entry(frame,textvariable=self.var_confpass,font=("times new roman",15,"bold"))
      confirm_pswd_entry.place(x=370,y=340,width=250)
      

    
      #########################check button #################
      self.var_check=IntVar()
      self.Checkbtn=Checkbutton(frame,variable=self.var_check,text="I Agree The Terms & Conditions",font=("times new roman",15,"bold"),onvalue=1,offvalue=0,bg="white")
      self.Checkbtn.place(x=50,y=400)




#####################buttons###################
      img=Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\Register.png")
      img=img.resize((280,50))
      self.photoimage=ImageTk.PhotoImage(img)

      b1=Button(frame,image=self.photoimage,command=self.register_data,borderwidth=0,cursor="hand2")
      b1.place(x=10,y=450,width=280)

      img1=Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\Login.png")
      img1=img1.resize((280,50))
      self.photoimage1=ImageTk.PhotoImage(img1)

      b1=Button(frame,image=self.photoimage1,command=self.register_data,borderwidth=0,cursor="hand2")
      b1.place(x=330,y=450,width=280)


      ###############3333function declaration################3
    def register_data(self):
        if self.var_fname.get() == "" or self.var_email.get() == "" or self.var_securityQ.get() =="Select":
            messagebox.showerror("Error", "All Fields are required")
        elif self.var_pass.get()!= self.var_confpass.get():
            messagebox.showerror("Error", "Password and Confirm Password must be the same")
        elif self.var_check.get()==0:
            messagebox.showerror("Error", "Please Agree to all terms and conditions")
        else:
            messagebox.showinfo("Success", "Welcome")
            

            conn=mysql.connector.connect(host="localhost",port="3306",user="root",password="root",database="Drowsiness")
            my_cursor=conn.cursor()
            query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row !=None:
                messagebox.showerror("Error","User already exist,please try another email")
            else:
                my_cursor.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                                                                                        self.var_fname.get(),
                                                                                        self.var_lname.get(),
                                                                                        self.var_contact.get(),
                                                                                        self.var_email.get(),
                                                                                        self.var_securityQ.get(),
                                                                                        self.var_securityA.get(),
                                                                                        self.var_pass.get()

                                                                                     ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Register Succesfully")


class DrowsinessDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Drowsiness Detection System")
        self.thresh = 0.25
        self.flag = 0
        self.frame_check = 60

        self.detect = dlib.get_frontal_face_detector()
        self.predict = dlib.shape_predictor(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\models\shape_predictor_68_face_landmarks.dat")

        mixer.init()
        mixer.music.load("music.wav")

        self.setup_gui()
        self.camera_frame = None

        
    def setup_gui(self):
        # Set up your GUI as before
        img3 = Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\one1.png")
        img3 = img3.resize((1530, 710))
        self.photoimg3 = ImageTk.PhotoImage(img3)
        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(width=1530, height=750)

        title_lbl = Label(bg_img, text="Drowsiness Detection System", font=(
            "times new roman", 35, "bold"), bg="white", fg="#2e475d")
        title_lbl.place(width=1530, height=70)

        date_time_lbl = Label(bg_img, font=("times new roman", 20, "bold"), bg="white", fg="black")
        date_time_lbl.place(x=1150, y=20)  # Adjust the position as needed

        self.update_date_time(date_time_lbl)  

        img4 = Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\DD.png")
        img4 = img4.resize((275, 125))
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1 = Button(bg_img, image=self.photoimg4, cursor="hand2", command=self.start_detection)
        b1.place(x=30, y=100, width=300, height=150)

        b1_1 = Button(bg_img, text="Drowsiness Detection", cursor="hand2", font=(
            "times new roman", 17, "bold"), bg="white", fg="black", command=self.start_detection)
        b1_1.place(x=31, y=250, width=300, height=50)

        img9 = Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\Saved.png")
        img9 = img9.resize((100, 80), Image.LANCZOS)
        self.photoimg9 = ImageTk.PhotoImage(img9)
        
        # Create a frame or use the main application window as the parent for the button
        button_frame = Frame(self.root)  # You should replace self.root with the appropriate parent widget
        
        b1 = Button(button_frame, image=self.photoimg9, cursor="hand2", command=self.open_img)
        b1.pack()  # Use pack or place, depending on your layout requirements
        
        b1_1 = Button(button_frame, text="Saved", cursor="hand2", command=self.open_img, font=("times new roman", 15, "bold"), bg="white", fg="black")
        b1_1.pack()  # Use pack or place, depending on your layout requirements
        
        # Add the button_frame to your existing layout
        button_frame.place(x=30, y=550)  # Adjust the coordinates as needed

    def open_img(self):
        os.startfile(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\Data")

    def open_camera_frame(self):
        self.root.withdraw()  # Hide the main window
        self.new_window = Toplevel(self.root)
        self.new_window.geometry("1200x720")  # Set the desired window size
        self.camera_frame = tk.Frame(self.new_window, width=1550, height=840)  # Set frame size
        self.app = DrowsinessDetector(self.camera_frame, self.thresh, self.frame_check)
        self.camera_frame.pack()

    def stop_detection(self):
        if self.app:
            self.app.stop_detection()

    def start_detection(self):
        self.open_camera_frame()

    def update_date_time(self, label):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
        formatted_date_time = now.strftime("%b %d, %Y - ") + formatted_time
        label.config(text=formatted_date_time)
        self.root.after(1000, lambda: self.update_date_time(label))

class DrowsinessDetector:
    def __init__(self, window, thresh, frame_check):
        self.window = window
        self.thresh = thresh
        self.frame_check = frame_check
        self.flag = 0
        self.out = None
        
        self.detect = dlib.get_frontal_face_detector()
        self.predict = dlib.shape_predictor(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\models\shape_predictor_68_face_landmarks.dat")

        self.cap = cv2.VideoCapture(0)
        self.video_frame = None
        self.bStart, self.bEnd = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]  # Define these variables
        self.rStart, self.rEnd = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]  # Define these variables
        self.detect_drowsiness()

        stop_image = Image.open(r"C:\Users\BHAVESH\OneDrive\Desktop\TYCS SEM3 PROJECT\images\my2.png")
        stop_image = stop_image.resize((100, 100), Image.LANCZOS)
        self.stop_icon = ImageTk.PhotoImage(stop_image)

        self.stop_button = tk.Button(self.window, image=self.stop_icon, text="Stop Detection", font=("Helvetica", 14, "bold"), compound="top", command=self.stop_detection)
        self.stop_button.image = self.stop_icon  # Store the image reference
        self.stop_button.pack(side="bottom")

    def eye_aspect_ratio(self, eye):
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        C = np.linalg.norm(eye[0] - eye[3])
        ear = (A + B) / (2.0 * C)
        return ear
    
    def stop_detection(self):
        self.cap.release()
        self.window.destroy()

    def detect_drowsiness(self):
        ret, frame = self.cap.read()
        if ret:
            frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.out is None:
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"C:\\Users\\BHAVESH\\OneDrive\\Desktop\\TYCS SEM3 PROJECT\\Data\\Recording_{timestamp}.avi"
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                self.out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640, 480))
            except Exception as e:
                print("Error initializing VideoWriter:", e)
        # Drowsiness detection logic using gray image
        subjects = self.detect(gray, 0)
        for subject in subjects:
            shape = self.predict(gray, subject)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[self.bStart:self.bEnd]
            rightEye = shape[self.rStart:self.rEnd]
            leftEar = self.eye_aspect_ratio(leftEye)
            rightEar = self.eye_aspect_ratio(rightEye)
            ear = (leftEar + rightEar) / 2.0
            leftEyeNull = cv2.convexHull(leftEye)
            rightEyeNull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeNull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeNull], -1, (0, 255, 0), 1)
            if ear < self.thresh:
                self.flag += 1
                print(self.flag)
                if self.flag >= self.frame_check:
                    cv2.putText(frame, "**************ALERT!**************", (150, 50), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 255), 2)  
                    cv2.putText(frame, "**************ALERT!**************", (150, 425), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 255), 2)
                    mixer.music.play()
            else:
                self.flag = 0

        # Record the frame to the output video file
        self.bStart, self.bEnd = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        self.rStart, self.rEnd = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        
        if self.out is not None:
            self.out.write(frame)

        self.out.write(frame)
        # cv2.imshow('Frame', frame)
        # cv2.waitKey(1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        if self.video_frame is None:
            self.video_frame = tk.Label(self.window, image=frame)
            self.video_frame.pack()
        else:
            self.video_frame.configure(image=frame)
            self.video_frame.image = frame

        self.window.after(10, self.detect_drowsiness)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
if __name__=="__main__":
    main()