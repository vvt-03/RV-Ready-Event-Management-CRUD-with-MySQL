import mysql.connector
import pymysql
import streamlit as st

# Establish connection to MySQL server
mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="vaishnavi",
        database="event_management"
)
mycursor = mydb.cursor()
print("Connection Established....")

# Create Streamlit app
def main():
    st.title("CRUD Operations with MySQL")

    # Display options for CRUD Operations
    option = st.sidebar.selectbox("Select an Operation", ("Create", "Read", "Update", "Delete", "Search"))
    
    if option == "Create":
        st.subheader("Create a Record")
        name = st.text_input("Enter the event name:")
        location = st.text_input("Enter the event location:")
        date = st.date_input("Enter the event date:")
        description = st.text_input("Enter the event description:")
        
        if st.button("Create"):
            sql = "INSERT INTO events(name, location, date, description) VALUES(%s, %s, %s, %s)"
            val = (name, location, date.strftime('%Y-%m-%d'), description)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Created Successfully")

    elif option == "Read":
        st.subheader("Read Records")
        mycursor.execute("SELECT * FROM events")
        result = mycursor.fetchall()
        
        for row in result:
            st.write(row)

    elif option == "Update":
        st.subheader("Update a Record")
        id = st.number_input("Enter ID", min_value=1)
        name = st.text_input("Enter updated event name")
        location = st.text_input("Enter updated event location")
        date = st.date_input("Enter updated event date")
        description = st.text_input("Enter updated event description")
        
        if st.button("Update"):
            sql = "UPDATE events SET name=%s, location=%s, date=%s, description=%s WHERE id=%s"
            val = (name, location, date.strftime('%Y-%m-%d'), description, id)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Updated Successfully")

    elif option == "Delete":
        st.subheader("Delete a Record")
        id = st.number_input("Enter ID", min_value=1)
        
        if st.button("Delete"):
            sql = "DELETE FROM events WHERE id=%s"
            val = (id,)
            mycursor.execute(sql, val)
            mydb.commit()
            st.success("Record Deleted Successfully")

    elif option == "Search":
        st.subheader("Search for a Record")
        search_by = st.selectbox("Search by:", ("ID", "Name"))
        
        if search_by == "ID":
            id = st.number_input("Enter Event ID", min_value=1)
            if st.button("Search by ID"):
                sql = "SELECT * FROM events WHERE id=%s"
                val = (id,)
                mycursor.execute(sql, val)
                result = mycursor.fetchone()
                
                if result:
                    st.write(result)
                else:
                    st.warning("No record found with that ID.")
        
        elif search_by == "Name":
            name = st.text_input("Enter Event Name")
            if st.button("Search by Name"):
                sql = "SELECT * FROM events WHERE name LIKE %s"
                val = ('%' + name + '%',)
                mycursor.execute(sql, val)
                result = mycursor.fetchall()
                
                if result:
                    for row in result:
                        st.write(row)
                else:
                    st.warning("No record found with that name.")

if __name__ == "_main_":
    main()