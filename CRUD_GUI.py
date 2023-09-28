import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['music_db']

def insert_document(collection_name, document):
    if document.get("name") and document.get("description"):
        collection = db[collection_name]
        collection.insert_one(document)
        messagebox.showinfo("Success", "Document inserted successfully!")
    else:
        messagebox.showerror("Error", "Name and description cannot be empty!")

def read_documents(collection_name):
    collection = db[collection_name]
    return list(collection.find())

def delete_document_by_name(collection_name, name):
    collection = db[collection_name]
    collection.delete_many({"name": name})
    messagebox.showinfo("Success", f"Documents with name '{name}' deleted successfully!")

def update_document_by_name(collection_name, name, updated_data):
    collection = db[collection_name]
    collection.update_many({"name": name}, {"$set": updated_data})
    messagebox.showinfo("Success", f"Documents with name '{name}' updated successfully!")

def retrieve_all_documents(collection_name):
    documents = read_documents(collection_name)
    text_widget.delete(1.0, tk.END)  # Clear existing text
    for document in documents:
        text_widget.insert(tk.END, f"Document ID: {document['_id']}\n")
        text_widget.insert(tk.END, f"Name: {document.get('name', 'N/A')}\n")
        description = document.get('description', 'N/A')
        text_widget.insert(tk.END, f"Description: {description}\n\n")

def handle_submit():
    collection_name = collection_combobox.get()
    document = {
        "name": name_entry.get(),
        "description": description_entry.get()
    }
    insert_document(collection_name, document)
    refresh_textbox()

def handle_delete():
    name_to_delete = name_entry.get()
    if name_to_delete:
        collection_name = collection_combobox.get()
        delete_document_by_name(collection_name, name_to_delete)
        refresh_textbox()
    else:
        messagebox.showerror("Error", "Name cannot be empty!")

def handle_update():
    name_to_update = name_entry.get()
    if name_to_update:
        collection_name = collection_combobox.get()
        updated_data = {
            "description": description_entry.get()
        }
        update_document_by_name(collection_name, name_to_update, updated_data)
        refresh_textbox()
    else:
        messagebox.showerror("Error", "Name cannot be empty!")

def handle_retrieve():
    collection_name = collection_combobox.get()
    retrieve_all_documents(collection_name)

def refresh_textbox():
    collection_name = collection_combobox.get()
    documents = read_documents(collection_name)
    text_widget.delete(1.0, tk.END)  # Clear existing text
    for document in documents:
        text_widget.insert(tk.END, f"Document ID: {document['_id']}\n")
        text_widget.insert(tk.END, f"Name: {document.get('name', 'N/A')}\n")
        description = document.get('description', 'N/A')
        text_widget.insert(tk.END, f"Description: {description}\n\n")

# Create the main application window
app = tk.Tk()
app.title("Music Database")

# Create and configure frames
top_frame = ttk.Frame(app)
top_frame.pack(pady=10)

bottom_frame = ttk.Frame(app)
bottom_frame.pack(pady=10)

# Collection selection combobox
collection_combobox = ttk.Combobox(top_frame, values=["musician", "album", "song", "instrument"])
collection_combobox.set("musician")
collection_combobox.grid(row=0, column=0, padx=10)

# Entry fields for name and description
name_label = ttk.Label(top_frame, text="Name:")
name_label.grid(row=0, column=1)
name_entry = ttk.Entry(top_frame)
name_entry.grid(row=0, column=2, padx=10)

description_label = ttk.Label(top_frame, text="Description:")
description_label.grid(row=0, column=3)
description_entry = ttk.Entry(top_frame)
description_entry.grid(row=0, column=4, padx=10)

# Buttons for CRUD operations
submit_button = ttk.Button(top_frame, text="SUBMIT", command=handle_submit)
delete_button = ttk.Button(top_frame, text="DELETE", command=handle_delete)
update_button = ttk.Button(top_frame, text="UPDATE", command=handle_update)
retrieve_button = ttk.Button(top_frame, text="RETRIEVE", command=handle_retrieve)

submit_button.grid(row=0, column=5, padx=10)
delete_button.grid(row=0, column=6, padx=10)
update_button.grid(row=0, column=7, padx=10)
retrieve_button.grid(row=0, column=8, padx=10)

# Text widget to display documents
text_widget = tk.Text(bottom_frame, wrap=tk.WORD, height=15, width=50)
text_widget.pack()

# Refresh the text widget with initial data
refresh_textbox()

app.mainloop()
