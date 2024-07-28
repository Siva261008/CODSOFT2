import tkinter as tk
from tkinter import messagebox
import sqlite3

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("665x400+550+250")
        self.root.resizable(0, 0)
        self.root.configure(bg="skyblue")

        self.tasks = []
        self.conn = sqlite3.connect('listOfTasks.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists tasks (title text)')

        self.functions_frame = tk.Frame(self.root, bg="red")
        self.functions_frame.pack(side="top", expand=True, fill="both")

        self.task_label = tk.Label(self.functions_frame, text="TO-DO-LIST :",
                                   font=("arial", "14", "bold"), background="black", foreground="pink")
        self.task_label.place(x=20, y=30)

        self.task_field = tk.Entry(self.functions_frame, font=("Arial", "14"), width=42, foreground="black", background="white")
        self.task_field.place(x=180, y=30)

        self.add_button = tk.Button(self.functions_frame, text="Add", width=15, bg='#D4AC0D', font=("arial", "14", "bold"), command=self.add_task)
        self.add_button.place(x=18, y=80)

        self.del_button = tk.Button(self.functions_frame, text="Remove", width=15, bg='grey', font=("arial", "14", "bold"), command=self.delete_task)
        self.del_button.place(x=240, y=80)

        self.del_all_button = tk.Button(self.functions_frame, text="Delete All", width=15, font=("arial", "14", "bold"), bg="orange", command=self.delete_all_tasks)
        self.del_all_button.place(x=17, y=330)

        self.exit_button = tk.Button(self.functions_frame, text="Exit / Close", width=52, bg='dark blue', font=("arial", "14", "bold"), command=self.close)
        self.exit_button.place(x=17, y=360)

        self.task_listbox = tk.Listbox(self.functions_frame, width=70, height=9, font="bold", selectmode='SINGLE', background="WHITE", foreground="BLACK", selectbackground="pink", selectforeground="black")
        self.task_listbox.place(x=17, y=140)

        self.retrieve_database()
        self.list_update()

    def add_task(self):
        task_string = self.task_field.get()
        if not task_string:
            messagebox.showinfo('Error', 'Field is Empty.')
        else:
            self.tasks.append(task_string)
            self.cursor.execute('insert into tasks values (?)', (task_string,))
            self.list_update()
            self.task_field.delete(0, 'end')

    def list_update(self):
        self.clear_list()
        for task in self.tasks:
            self.task_listbox.insert('end', task)

    def delete_task(self):
        try:
            the_value = self.task_listbox.get(self.task_listbox.curselection())
            if the_value in self.tasks:
                self.tasks.remove(the_value)
                self.list_update()
                self.cursor.execute('delete from tasks where title = ?', (the_value,))
        except:
            messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

    def delete_all_tasks(self):
        message_box = messagebox.askyesno('Delete All', 'Are you sure?')
        if message_box:
            self.tasks.clear()
            self.cursor.execute('delete from tasks')
            self.list_update()

    def clear_list(self):
        self.task_listbox.delete(0, 'end')

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.root.destroy()

    def retrieve_database(self):
        self.tasks.clear()
        for row in self.cursor.execute('select title from tasks'):
            self.tasks.append(row[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
