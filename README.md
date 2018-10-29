# todo
# Pending To-dos
A User can use this application to Create, Read, Update and Delete their To-dos.
On home page 'localhost:8000' all the To-dos of a user which are "Pending" are listed.

# Completed To-dos
On the bottom of the Page, all the "Completed To-dos" are listed to let the user view how many tasks he/she has completed so far.
Here, there is also an Option for User to edit the Status of their To-do to add some task and put it as "Pending".
And also, they can click on "Delete" to Delete their Todo.
> The To-do which was deleted, is not actually deleted immediately from the Database. It is 'Soft Deleted' and will be automatically gets deleted after 30 Days.

# Alerts
As a user, they can put a Due-Date to a task along with the option to remind them about their To-do before mentioned 'Hours' prior to the dead line.

# Issues
Alerting the user about their tasks should be asynchronous. There is no periodic task wired to this functionality yet.
