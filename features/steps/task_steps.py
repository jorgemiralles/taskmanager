from behave import given, when, then

@given('a task titled "{title}"')
def step_given_task(context, title):
    resp = context.client.post('/api/tasks', json={'title': title})
    context.task_id = resp.get_json()['id']

@given('a task with priority "{priority}" titled "{title}"')
def step_given_task_with_priority(context, priority, title):
    resp = context.client.post('/api/tasks', json={'title': title, 'priority': priority})
    context.task_id = resp.get_json()['id']

@when('I create a task named "{title}"')
def step_create_task(context, title):
    context.response = context.client.post('/api/tasks', json={'title': title})
    context.task_id = context.response.get_json()['id']

@when('I create a task priority "{priority}" due "{due_date}" named "{title}"')
def step_create_task_full(context, priority, due_date, title):
    context.response = context.client.post('/api/tasks', json={
        'title': title, 'priority': priority, 'due_date': due_date
    })
    context.task_id = context.response.get_json()['id']

@when('I fetch all tasks')
def step_request_list(context):
    context.response = context.client.get('/api/tasks')

@when('I set priority "{priority}" and title "{title}" on the task')
def step_update_task_full(context, priority, title):
    context.response = context.client.put(f'/api/tasks/{context.task_id}', json={
        'title': title, 'priority': priority
    })

@when('I set the task title to "{title}"')
def step_update_task_title(context, title):
    context.response = context.client.put(f'/api/tasks/{context.task_id}', json={
        'title': title, 'priority': 'medium'
    })

@when('I flip completion')
@when('I flip completion again')
def step_toggle_task(context):
    context.response = context.client.patch(f'/api/tasks/{context.task_id}/toggle')

@when('I remove the task')
def step_delete_task(context):
    context.response = context.client.delete(f'/api/tasks/{context.task_id}')

@then('the response status should be {status_code:d}')
def step_check_status(context, status_code):
    assert context.response.status_code == status_code

@then('the task list should be empty')
def step_check_empty_list(context):
    assert context.response.get_json() == []

@then('the task should exist with title "{title}"')
def step_check_task_exists(context, title):
    tasks = context.client.get('/api/tasks').get_json()
    assert any(t['title'] == title for t in tasks)

@then('the task should have priority "{priority}"')
def step_check_task_priority(context, priority):
    tasks = context.client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == context.task_id)
    assert task['priority'] == priority

@then('the task should have due date "{due_date}"')
def step_check_task_due_date(context, due_date):
    tasks = context.client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == context.task_id)
    assert task['due_date'] == due_date

@then('I should see {count:d} tasks')
def step_check_task_count(context, count):
    tasks = context.response.get_json()
    assert len(tasks) == count

@then('the task title should be "{title}"')
def step_check_task_title(context, title):
    tasks = context.client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == context.task_id)
    assert task['title'] == title

@then('the task should be completed')
def step_check_task_completed(context):
    tasks = context.client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == context.task_id)
    assert task['completed'] is True

@then('the task should not be completed')
def step_check_task_not_completed(context):
    tasks = context.client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == context.task_id)
    assert task['completed'] is False

@then('the task should no longer exist')
def step_check_task_deleted(context):
    tasks = context.client.get('/api/tasks').get_json()
    assert all(t['id'] != context.task_id for t in tasks)
