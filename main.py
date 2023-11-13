from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel

from kivymd.uix.pickers import MDDatePicker
from kivy.clock import Clock
from datetime import datetime, timedelta

KV = '''
BoxLayout:
    orientation: 'vertical'
    spacing: '10dp'
    padding: '10dp'

    MDTextField:
        id: assignment_name_input
        multiline: False
        hint_text: 'Assignment Name'

    MDTextField:
        id: due_date_input
        multiline: False
        hint_text: 'Due Date (mm/dd/yyyy hh:mm)'
        on_focus: app.show_date_picker()

    MDTextField:
        id: subject_input
        multiline: False
        hint_text: 'Subject'

    
    MDRaisedButton:
        text: 'Add Assignment'
        on_press: app.add_assignment()

    MDRaisedButton:
        text: 'View Assignments'
        on_press: app.view_assignments()

    MDRaisedButton:
        text: 'View Missing Assignments'
        on_press: app.view_missing_assignments()

    MDRaisedButton:
        text: 'Mark Assignment as Done'
        on_press: app.mark_assignment_done()

    ScrollView:
        MDBoxLayout:
            id: task_list
            orientation: 'vertical'
            spacing: '5dp'
'''

class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_text = self.ids.date_text
        self.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))
    
    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, value):
        date = value.strftime('%A %d %B %Y')
        self.date_text.text = str(date)

class ToDoListApp(MDApp):
    def build(self):
        self.tasks = []
        self.assignments = []
        self.task_widgets = {}
        Clock.schedule_interval(self.update_due_status, 60)  # Update every 60 seconds
        return Builder.load_string(KV)
    
    def show_date_picker(self):
        picker = MDDatePicker()
        picker.bind(on_save=self.on_date_picker_selected)
        picker.open()
 
    def on_date_picker_selected(self, instance, value, date_range):
        self.root.ids.due_date_input.text = value.strftime("%m/%d/%Y %H:%M")

    def add_assignment(self):
        assignment_name = self.root.ids.assignment_name_input.text
        due_date_str = self.root.ids.due_date_input.text
        subject = self.root.ids.subject_input.text

        if assignment_name and due_date_str and subject:
            due_date = datetime.strptime(due_date_str, "%m/%d/%Y %H:%M")
            self.assignments.append({
                "name": assignment_name,
                "due_date": due_date,
                "subject": subject
            })
            task_label = MDLabel(text=f"{assignment_name} - Due: {due_date} - Subject: {subject} - {self.get_due_status(due_date)}")
            self.task_widgets[assignment_name] = task_label
            self.root.ids.task_list.add_widget(task_label)

            # Clear input fields
            self.root.ids.assignment_name_input.text = ''
            self.root.ids.due_date_input.text = ''
            self.root.ids.subject_input.text = ''

    def view_assignments(self):
        for assignment in self.assignments:
            task_label = MDLabel(text=f"{assignment['name']} - Due: {assignment['due_date']} - Subject: {assignment['subject']} - {self.get_due_status(assignment['due_date'])}")
            self.root.ids.task_list.add_widget(task_label)

    def view_missing_assignments(self):
        missing_assignments_exist = False

        for assignment in self.assignments:
            due_status = self.get_due_status(assignment['due_date'])
        if due_status != "Done" and due_status != "Not Yet Done":
            task_label = MDLabel(text=f"{assignment['name']} - Due: {assignment['due_date']} - Subject: {assignment['subject']} - {due_status}")
            self.root.ids.task_list.add_widget(task_label)
            missing_assignments_exist = True

        if not missing_assignments_exist:
            task_label = MDLabel(text="No missing assigments. You're doing great!")
            self.root.ids.task_list.add_widget(task_label)

    def mark_assignment_done(self):
        assignment_name = self.root.ids.assignment_name_input.text
        if assignment_name in self.task_widgets:
            self.task_widgets[assignment_name].text = f"{assignment_name} - Done"
            self.assignments = [a for a in self.assignments if a["name"] != assignment_name]
            del self.task_widgets[assignment_name]

    def update_due_status(self, dt):
        for assignment in self.assignments:
            due_status = self.get_due_status(assignment['due_date'])
            self.task_widgets[assignment['name']].text = f"{assignment['name']} - Due: {assignment['due_date']} - Subject: {assignment['subject']} - {due_status}"

    def get_due_status(self, due_date):
        now = datetime.now()
        if now > due_date:
            return "Done"
        elif due_date - now < timedelta(minutes=30):
            return f"Due in {int((due_date - now).seconds / 60)} mins"
        else:
            return "Not Yet Done"
        


if __name__ == '__main__':
    ToDoListApp().run()