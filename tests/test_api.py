def test_empty_list(client):
    resp = client.get('/api/tasks')
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_task(client):
    resp = client.post('/api/tasks', json={'title': 'test task', 'priority': 'high'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'id' in data


def test_create_task_defaults(client):
    resp = client.post('/api/tasks', json={'title': 'defaults'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'id' in data


def test_list_after_create(client):
    client.post('/api/tasks', json={'title': 'task A'})
    client.post('/api/tasks', json={'title': 'task B', 'priority': 'high', 'due_date': '2026-12-31'})
    resp = client.get('/api/tasks')
    tasks = resp.get_json()
    assert len(tasks) == 2
    titles = [t['title'] for t in tasks]
    assert 'task A' in titles
    assert 'task B' in titles


def test_update_task(client):
    resp = client.post('/api/tasks', json={'title': 'old', 'priority': 'low'})
    task_id = resp.get_json()['id']

    client.put(f'/api/tasks/{task_id}', json={
        'title': 'new', 'priority': 'high', 'due_date': '2026-12-31'
    })

    tasks = client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == task_id)
    assert task['title'] == 'new'
    assert task['priority'] == 'high'
    assert task['due_date'] == '2026-12-31'


def test_toggle_task(client):
    resp = client.post('/api/tasks', json={'title': 'toggler'})
    task_id = resp.get_json()['id']

    client.patch(f'/api/tasks/{task_id}/toggle')
    tasks = client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == task_id)
    assert task['completed'] is True

    client.patch(f'/api/tasks/{task_id}/toggle')
    tasks = client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == task_id)
    assert task['completed'] is False


def test_delete_task(client):
    resp = client.post('/api/tasks', json={'title': 'delete me'})
    task_id = resp.get_json()['id']

    resp = client.delete(f'/api/tasks/{task_id}')
    assert resp.status_code == 200

    tasks = client.get('/api/tasks').get_json()
    assert all(t['id'] != task_id for t in tasks)


def test_full_cycle(client):
    resp = client.post('/api/tasks', json={'title': 'cycle'})
    task_id = resp.get_json()['id']

    tasks = client.get('/api/tasks').get_json()
    assert any(t['id'] == task_id for t in tasks)

    client.patch(f'/api/tasks/{task_id}/toggle')
    tasks = client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == task_id)
    assert task['completed'] is True

    client.put(f'/api/tasks/{task_id}', json={'title': 'updated', 'priority': 'low'})
    tasks = client.get('/api/tasks').get_json()
    task = next(t for t in tasks if t['id'] == task_id)
    assert task['title'] == 'updated'

    client.delete(f'/api/tasks/{task_id}')
    tasks = client.get('/api/tasks').get_json()
    assert all(t['id'] != task_id for t in tasks)
