import sys
import os
import subprocess

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
import threading


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nebula Pro")
        self.state('zoomed')  # Start maximized

        self.agenda = []

        self.load_agenda()
        self.create_widgets()

    def create_widgets(self):
        # Create a custom style for the application
        self.style = ttk.Style()

        # Set the base color scheme
        self.style.theme_create("HarmoniousTheme", parent="alt", settings={
            "TFrame": {"configure": {"background": "#6495ED"}},
            "TNotebook": {"configure": {"background": "#6495ED"}},
            "TNotebook.Tab": {
                "configure": {"padding": [10, 5], "background": "#6495ED", "foreground": "black"},
                "map": {"background": [("selected", "orange")], "foreground": [("selected", "white")]}
            },
            "TButton": {
                "configure": {
                    "background": "#4682B4",
                    "foreground": "black",
                    "font": ('Helvetica', 10, 'bold'),
                    "relief": "raised",
                    "borderwidth": 2,
                    "bordercolor": "gray",
                    "anchor": "center",
                    "width": 15,
                    "height": 2,
                    "highlightthickness": 2,
                    "highlightbackground": "gray",
                    "highlightcolor": "gray"
                }
            },
            "TEntry": {"configure": {"background": "white", "foreground": "black"}},
            "Treeview": {
                "configure": {"background": "white", "foreground": "purple", "font": ('Helvetica', 10)},
                "fieldbackground": "white"
            },
            "Treeview.Heading": {"font": ('Helvetica', 10, 'bold')}
        })

        # Use the custom style
        self.style.theme_use("HarmoniousTheme")

        # Create and configure widgets below

        self.tabControl = ttk.Notebook(self)

        self.tabControl.pack(expand=1, fill="both")

        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="View Agenda")

        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Add Event")

        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text="Edit Event")

        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4, text="Delete Event")

        self.tab5 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab5, text="About")

        self.view_agenda()
        self.add_event()
        self.edit_event()
        self.delete_event()
        self.about()
        self.add_search()
        self.add_reload_button()


    def load_agenda(self):
        def task():
            self.loading_label = ttk.Label(self, text="Loading...", font=('Helvetica', 12, 'bold'))
            self.loading_label.pack(pady=10)
            try:
                with open("userdata/nebula-agenda.txt", "r") as file:
                    for line_num, line in enumerate(file, 1):
                        try:
                            date, time, description = line.strip().split(",")
                            self.agenda.append({"date": date, "time": time, "description": description})
                        except ValueError as e:
                            print(f"Error parsing line {line_num}: {line.strip()} -> {e}")
            except FileNotFoundError:
                print("Agenda file not found.")
            finally:
                self.refresh_agenda_view()
                self.update_entry_count()  # Update after loading
                self.loading_label.destroy()
    
        threading.Thread(target=task, daemon=True).start()

    def save_agenda(self):
        def task():
            with open("userdata/nebula-agenda.txt", "w") as file:
                for event in self.agenda:
                    file.write(f"{event['date']},{event['time']},{event['description']}\n")
    
        threading.Thread(target=task, daemon=True).start()

    def view_agenda(self):
        self.viewFrame = ttk.Frame(self.tab1)
        self.viewFrame.pack(fill="both", expand=1)
    
        # Selected entry display label
        self.selected_label = tk.Label(self.viewFrame, text="Selected: None", background="#87CEEB", anchor="w")
        self.selected_label.pack(fill="x", padx=10, pady=5)
    
        self.tree = ttk.Treeview(self.viewFrame, columns=("Date", "Time", "Description"), show="headings")
        self.tree.heading("Date", text="Date", command=lambda: self.sort_by_column("Date"))
        self.tree.heading("Time", text="Time", command=lambda: self.sort_by_column("Time"))
        self.tree.heading("Description", text="Description", command=lambda: self.sort_by_column("Description"))
        self.tree.pack(fill="both", expand=1)
    
        for event in self.agenda:
            self.tree.insert("", "end", values=(event["date"], event["time"], event["description"]))
    
        self.sort_by_column("Date")
    
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def update_scrollbar(self, event):
        self.y_scrollbar.set(*self.tree.yview())


    def show_description(self, event):
        # Identify the item at the clicked position
        item = self.tree.identify('item', event.x, event.y)
        
        if item:
            # Fetch description of the item (assuming it's in the 3rd column)
            description = self.tree.item(item, 'values')[2]
            self.display_description(description)
            
            # Highlight the selected row
            self.tree.tag_configure("selected", background="light green")
            
            # Remove highlight from the previously selected item, if it exists and is different
            if hasattr(self, 'selected_item') and self.selected_item and self.selected_item != item:
                self.tree.item(self.selected_item, tags=())  # Remove highlight from previous item
            
            # Add the highlight to the new selected item
            self.tree.item(item, tags=("selected",))
            
            # Update selected_item with the new item
            self.selected_item = item
        else:
            # If no item is identified, clear the description and remove highlight from previous item
            self.display_description('')
            
            if hasattr(self, 'selected_item') and self.selected_item:
                self.tree.item(self.selected_item, tags=())  # Remove highlight from previous item
                self.selected_item = None  # Reset selected item



    def display_description(self, description):
        if hasattr(self, 'description_label') and self.description_label:
            self.description_label.destroy()
        if description:
            self.description_label = tk.Label(self.viewFrame, text=description, background="#6495ED", wraplength=400, justify="left")
            self.description_label.place(relx=0.5, rely=0.49, anchor='center')
        else:
            self.description_label = None


    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            self.selected_label.config(text=f"Selected: {item_values[0]} {item_values[1]} - {item_values[2]}")
            self.highlight_selected_item(selected_item[0])
        else:
            self.selected_label.config(text="Selected: None")
            
    def highlight_selected_item(self, item_id):
        # Check if a previously selected item exists and is valid
        if hasattr(self, 'selected_item') and self.selected_item:
            try:
                # Remove the highlight from the previously selected item
                self.tree.item(self.selected_item, tags=())
            except tk.TclError:
                # Ignore the error if the item no longer exists
                pass
    
        # Highlight the newly selected item
        self.tree.tag_configure("selected", background="light green")
        self.tree.item(item_id, tags=("selected",))
        self.selected_item = item_id  # Update the reference to the current selected item

        


    def sort_by_column(self, column):
        items = self.tree.get_children("")
        values = [(self.tree.set(child, column), child) for child in items]
        values.sort()  # Sort in ascending order
        for index, (val, child) in enumerate(values):
            self.tree.move(child, '', index)

    def add_event(self):
        def add():
            date = self.cal.get_date()
            time = f"{self.hourVar.get():02d}:{self.minVar.get():02d}"
            description = self.descriptionEntry.get()

            if description:
                self.agenda.append({"date": date, "time": time, "description": description})
                self.save_agenda()
                self.tree.insert("", "end", values=(date, time, description))
                self.update_entry_count()  # Refresh the count
                messagebox.showinfo("Success", "Event added successfully.")
            else:
                messagebox.showerror("Error", "Description is required.")


        self.addFrame = ttk.Frame(self.tab2)
        self.addFrame.pack(fill="both", expand=1)

        self.cal = Calendar(
            self.addFrame, 
            selectmode="day", 
            date_pattern="yyyy-mm-dd",
            selectbackground="lightblue",  # Background color of selected day
            selectforeground="white"        # Text color of selected day
        )
        self.cal.pack(padx=5, pady=5)
    
 
        self.hourVar = tk.IntVar(self.addFrame, value=datetime.now().hour)
        self.minVar = tk.IntVar(self.addFrame, value=datetime.now().minute)

        self.hourLabel = ttk.Label(self.addFrame, text="Hour:")
        self.hourLabel.pack(padx=5, pady=5)
        self.hourSpin = tk.Spinbox(self.addFrame, from_=0, to=23, width=5, textvariable=self.hourVar)
        self.hourSpin.pack(padx=5, pady=5)

        self.minLabel = ttk.Label(self.addFrame, text="Minute:")
        self.minLabel.pack(padx=5, pady=5)
        self.minSpin = tk.Spinbox(self.addFrame, from_=0, to=59, width=5, textvariable=self.minVar)
        self.minSpin.pack(padx=5, pady=5)

        self.descriptionLabel = ttk.Label(self.addFrame, text="Description:")
        self.descriptionLabel.pack(padx=5, pady=5)
        self.descriptionEntry = ttk.Entry(self.addFrame)
        self.descriptionEntry.pack(padx=5, pady=5)

        self.addButton = ttk.Button(self.addFrame, text="Add Event", command=add)
        self.addButton.pack(padx=5, pady=5)


    def add_reload_button(self):
        reload_button_frame = ttk.Frame(self.tab1)
        reload_button_frame.pack()

        reload_button = ttk.Button(reload_button_frame, text="Restart", command=self.reload_program)
        reload_button.pack(padx=10, pady=10)


    def reload_program(self):
        try:
            python = sys.executable
            subprocess.Popen([python] + sys.argv)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while reloading the program: {str(e)}")

    def edit_event(self):
        def edit():
            selected_item = self.tree.selection()
            if selected_item:
                date, time, description = self.tree.item(selected_item, 'values')
                # Open a dialog to edit event details
                edit_window = tk.Toplevel(self)
                edit_window.title("Edit Event")
                edit_window.geometry("300x200")

                tk.Label(edit_window, text="Date:").grid(row=0, column=0)
                tk.Label(edit_window, text="Time:").grid(row=1, column=0)
                tk.Label(edit_window, text="Description:").grid(row=2, column=0)

                date_entry = ttk.Entry(edit_window)
                date_entry.insert(0, date)
                date_entry.grid(row=0, column=1)

                time_entry = ttk.Entry(edit_window)
                time_entry.insert(0, time)
                time_entry.grid(row=1, column=1)

                desc_entry = ttk.Entry(edit_window)
                desc_entry.insert(0, description)
                desc_entry.grid(row=2, column=1)

                def save_changes():
                    new_date = date_entry.get()
                    new_time = time_entry.get()
                    new_desc = desc_entry.get()
                    # Update the event details in the agenda
                    for event in self.agenda:
                        if event["date"] == date and event["time"] == time and event["description"] == description:
                            event["date"] = new_date
                            event["time"] = new_time
                            event["description"] = new_desc
                            break
                    self.save_agenda()
                    self.refresh_agenda_view()
                    messagebox.showinfo("Success", "Event edited successfully.")
                    edit_window.destroy()

                save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)
                save_button.grid(row=3, columnspan=2)
            else:
                messagebox.showerror("Error", "Please select an event to edit.")

        self.editFrame = ttk.Frame(self.tab3)
        self.editFrame.pack(fill="both", expand=1)

        self.editButton = ttk.Button(self.editFrame, text="Edit Event", command=edit)
        self.editButton.pack(padx=5, pady=5)

    def delete_event(self):
        def delete():
            selected_item = self.tree.selection()
            if selected_item:
                date, time, description = self.tree.item(selected_item, 'values')
                self.tree.delete(selected_item)
                self.agenda = [event for event in self.agenda if not (event["date"] == date and event["time"] == time and event["description"] == description)]
                self.save_agenda()
                self.update_entry_count()  # Refresh the count
                messagebox.showinfo("Success", "Event deleted successfully.")
            else:
                messagebox.showerror("Error", "Please select an event to delete.")


        def delete_day():
            date_to_delete = self.dateDeleteEntry.get()
            if date_to_delete:
                self.agenda = [event for event in self.agenda if event["date"] != date_to_delete]
                self.save_agenda()
                self.refresh_agenda_view()
                messagebox.showinfo("Success", f"All events for {date_to_delete} deleted successfully.")
            else:
                messagebox.showerror("Error", "Please enter a date to delete.")

        def delete_all():
            self.agenda = []
            self.save_agenda()
            self.refresh_agenda_view()
            messagebox.showinfo("Success", "All events deleted successfully.")

        self.deleteFrame = ttk.Frame(self.tab4)
        self.deleteFrame.pack(fill="both", expand=1)

        self.deleteButton = ttk.Button(self.deleteFrame, text="Delete Selected Event", command=delete)
        self.deleteButton.pack(padx=5, pady=5)

# Create a custom style for the label
        self.style.configure("DeleteLabel.TLabel", background="#F5F5F5", foreground="#333333", font=('Helvetica', 10))

# Apply the custom style to the label
        self.deleteDayLabel = ttk.Label(self.deleteFrame, text="Delete all events for a specific day (YYYY-MM-DD):", style="DeleteLabel.TLabel")
        self.deleteDayLabel.pack(padx=5, pady=5)

        self.deleteDayLabel.pack(padx=5, pady=5)
        self.dateDeleteEntry = ttk.Entry(self.deleteFrame)
        self.dateDeleteEntry.pack(padx=5, pady=5)
        self.deleteDayButton = ttk.Button(self.deleteFrame, text="Delete Specified", command=delete_day)
        self.deleteDayButton.pack(padx=5, pady=5)

        self.deleteAllButton = ttk.Button(self.deleteFrame, text="Delete All Events", command=delete_all)
        self.deleteAllButton.pack(padx=5, pady=5)

    def refresh_agenda_view(self):
        # Clear all items from the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert updated agenda data
        for event in self.agenda:
            self.tree.insert("", "end", values=(event["date"], event["time"], event["description"]))
        
        # Optionally, re-sort by date or other columns if needed
        self.sort_by_column("Date")


    def about(self):
        about_text = "(c) Nebula PRO 12.0 - Peter De Ceuster 2024\nhttps://peterdeceuster.uk/"
        self.aboutFrame = ttk.Frame(self.tab5)
        self.aboutFrame.pack(fill="both", expand=1)
        about_label = tk.Label(self.aboutFrame, text=about_text, fg="blue", cursor="hand2", background="#6495ED")
        about_label.pack(expand=True)
        about_label.bind("<Button-1>", lambda e: self.open_url("https://peterdeceuster.uk/"))

        # Add the count label dynamically
        self.count_label = tk.Label(self.aboutFrame, font=('Helvetica', 10), background="#6495ED")
        self.count_label.pack(pady=5)
        self.update_entry_count()

    def update_entry_count(self):
        # Update the count label dynamically
        entry_count = len(self.agenda)
        self.count_label.config(text=f"Total Entries: {entry_count}")


    def open_url(self, url):
        import webbrowser
        webbrowser.open_new(url)

    def add_search(self):
        search_frame = ttk.Frame(self.tab1)
        search_frame.pack(fill="x", pady=10)
    
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
    
        search_button = ttk.Button(search_frame, text="Search/Date", command=self.perform_search)
        search_button.pack(side="left")
    
        reset_button = ttk.Button(search_frame, text="Reset", command=self.refresh_agenda_view)
        reset_button.pack(side="left", padx=5)

    def perform_search(self):
        query = self.search_entry.get().lower()
        if query:
            filtered_agenda = [event for event in self.agenda if query in event["date"].lower() or query in event["time"].lower() or query in event["description"].lower()]
            self.refresh_agenda_view_with_search(filtered_agenda)
        else:
            self.refresh_agenda_view()

    def refresh_agenda_view_with_search(self, filtered_agenda):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for event in filtered_agenda:
            self.tree.insert("", "end", values=(event["date"], event["time"], event["description"]))
    def update_scrollbar(self, event):
        self.y_scrollbar.set(*self.tree.yview())


if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()
