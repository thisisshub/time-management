import pandas as pd
from todoist.api import TodoistAPI

api = TodoistAPI('df864d9cbf7b4e669e50bf626fa088eef855ff5e')
api.sync()

# .data attribute retrieves a python dictionary rather than todoist.models.Project
projects = [project.data for project in api.state['projects']] 

# I can easily create a DataFrame on the 'projects' list of dicts
df_projects = pd.DataFrame(projects)

df_projects.head()

tasks = [task.data for task in api.state['items']]
df_tasks = pd.DataFrame(tasks)
df_tasks.head()

df_tasks['date_added'] = pd.to_datetime(
	(pd.to_datetime(df_tasks['date_added'], utc=True)
	.dt.tz_convert('Europe/Budapest') # my current timezone
	.dt.strftime("%Y-%m-%d %H:%M:%S"))) # easier to handle format

df_tasks['due_date_utc'] = pd.to_datetime(
	(pd.to_datetime(df_tasks['due_date_utc'], utc=True)
	.dt.tz_convert('Europe/Budapest')
	.dt.strftime("%Y-%m-%d %H:%M:%S")))

df_tasks['date_completed'] = pd.to_datetime(
	(pd.to_datetime(df_tasks['date_completed'], utc=True)
    .dt.tz_convert('Europe/Budapest')
    .dt.strftime("%Y-%m-%d %H:%M:%S")))

# Many of my tasks are recurrent, and I want to identify them 
# by searching for the string 'every' in the 'date_sting' field
df_tasks['recurring'] = (df_tasks['date_string'].str.contains('every')
	.map({True: "Yes", False: "No"}))

# The 'project_id' is present in this DataFrame, but I want the actual project name
# So I create a 'mapper' consisting of 'project_id: name' (from df_projects)
# and map it to df_tasks (pd.merge could also have been used)
map_project = dict(df_projects[['id', 'name']].values) 
df_tasks['project_name'] = df_tasks.project_id.map(map_project)

# Check new date formats/new fields
df_tasks.head()
