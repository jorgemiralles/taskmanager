Feature: Task Management

  Scenario: View empty task list
    When I fetch all tasks
    Then the response status should be 200
    And the task list should be empty

  Scenario: Create a task
    When I create a task named "Buy milk"
    Then the response status should be 201
    And the task should exist with title "Buy milk"

  Scenario: Create with priority and due date
    When I create a task priority "high" due "2026-04-15" named "File taxes"
    Then the response status should be 201
    And the task should have priority "high"
    And the task should have due date "2026-04-15"

  Scenario: List tasks after creation
    Given a task titled "Task A"
    And a task titled "Task B"
    When I fetch all tasks
    Then I should see 2 tasks

  Scenario: Update a task
    Given a task with priority "low" titled "Old title"
    When I set priority "high" and title "New title" on the task
    Then the task title should be "New title"
    And the task should have priority "high"

  Scenario: Toggle task completion
    Given a task titled "Toggler"
    When I flip completion
    Then the task should be completed
    When I flip completion again
    Then the task should not be completed

  Scenario: Delete a task
    Given a task titled "Delete me"
    When I remove the task
    Then the task should no longer exist

  Scenario: Full task lifecycle
    Given a task titled "Cycle"
    When I flip completion
    Then the task should be completed
    When I set the task title to "Updated"
    Then the task title should be "Updated"
    When I remove the task
    Then the task should no longer exist
