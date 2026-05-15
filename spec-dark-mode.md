# Dark Mode — Implementation Plan

## Branch
`feat/dark-mode` (from current `master`)

## Gherkin Spec

```gherkin
Feature: Dark Mode Toggle
  As a user
  I want to switch between light and dark themes
  So that I can use the app comfortably in different lighting conditions

  Background:
    Given I am on the task manager page

  Scenario: Default theme is light
    Then the page should be displayed in light mode
    And the toggle button should show a happy face icon

  Scenario: Toggle to dark mode
    When I click the theme toggle button
    Then the page should switch to dark mode
    And the toggle button should show a sad face icon
    And the preference should be saved in localStorage

  Scenario: Persist dark mode on reload
    Given I have switched to dark mode
    When I reload the page
    Then the page should still be in dark mode

  Scenario: Toggle back to light mode
    Given I am in dark mode
    When I click the theme toggle button
    Then the page should switch back to light mode
    And the toggle button should show a happy face icon
    And localStorage should reflect light mode

  Scenario: Task cards respect dark theme
    Given I am in dark mode
    Then task cards should use dark theme colors
    And all text should be readable against the dark background
    And form inputs should have dark-themed styling

  Scenario: Toggle icon matches current theme
    When the theme is light
    Then the toggle button shows a happy face icon (switch to dark)
    When the theme is dark
    Then the toggle button shows a sad face icon (switch to light)
```

## Changes — all in `templates/index.html`

### 1. Toggle button in header
Add a sad face/happy face icon button next to "Add Task" to switch themes.

### 2. Dark-mode-ready CSS
Update custom styles to use Bootstrap CSS variables so they respond to the theme:
- `body { background: var(--bs-body-bg); }` (instead of hardcoded `#f5f7fa`)
- `.task-title-edit:focus { background: var(--bs-tertiary-bg); }`
- `.completed .task-title { color: var(--bs-secondary-color); }`

### 3. `<html>` data-bs-theme toggle via localStorage
- On load: read `localStorage.theme` → default to `'light'`
- Toggle switches between `'light'` / `'dark'`
- Persist choice to `localStorage.theme`
- Swap the toggle icon (sad face ↔ happy face)

### 4. No backend changes
Dark mode is purely frontend. Bootstrap 5.3 natively supports `data-bs-theme="dark"` on `<html>`, which recolorizes all components automatically. Custom CSS uses Bootstrap variables so everything responds to the theme.
