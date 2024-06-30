import mysql.connector
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send an email
def send_email(recipient, subject, body):
    sender_email = "yuva557489334@gmail.com"
    sender_password = "tqbg nfsp xdwe xbqj"  # Replace with a secure method of storing your password
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to handle movie list selection and booking
def movie_list():
    movies_list = {
        "1": {"movie_name": "Aranmanai4"},
        "2": {"movie_name": "Aavesham"},
        "3": {"movie_name": "Dear"},
        "4": {"movie_name": "The Family star"},
        "5": {"movie_name": "PT sir"}
    }
    
    print("-----Today's Movies List------")
    for num, m_name in movies_list.items():
        print(f"no: {num} movie_name: {m_name['movie_name']}")
    
    user = input("Enter your movie number: ")
    how_many=int(input("How many people are there: "))
    price=200
    gst_percent = 18 

    if user in movies_list:
        movie_name = movies_list[user]['movie_name']
        total=how_many*price
        gst_amount = total * gst_percent / 100
        total_with_gst = total + gst_amount
    
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Writing to the file
            with open("movies.txt", "a") as f:
                user_entry = f"Your movie_name is {movie_name} - {timestamp} total price is {total} + GST: {gst_amount} ({gst_percent}%) = {total_with_gst}\n %\n"
                f.write(user_entry)
                f.write("You registered successfully.\n")
                print(user_entry)
                print("You registered successfully.")
        except Exception as e:
            print(f"Failed to write to the file: {e}")

        try:
            # Database connection
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345",
                database="movie_list_db"
            )
            mycursor = mydb.cursor()
            update_sql = "UPDATE movie_list SET number_of_customer = number_of_customer + 1 WHERE id = %s"
            mycursor.execute(update_sql, (user,))
            mydb.commit()
            print("Customer count updated in the database successfully")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            if 'mycursor' in locals():
                mycursor.close()
            if 'mydb' in locals():
                mydb.close()

        email = input("Enter your email to receive a movie confirmation: ")
        email_body = f"Thanks for your booking\n\nYou booked the movie: {movie_name}\nBooking Time: {timestamp} and  total price is {total} to GST is {gst_percent} %"
        send_email(email, "Booking Confirmation", email_body)
    else:
        print("Invalid choice. You did not book.")

movie_list()
