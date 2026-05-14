# Dark Mode — Implementation Plan

## Branch
`feat/dark-mode` (from current `master`)

## Changes — all in `templates/index.html`

### 1. Toggle button in header
Add a sun/moon icon button next to "Add Task" to switch themes.

### 2. Dark-mode-ready CSS
Update custom styles to use Bootstrap CSS variables so they respond to the theme:
- `body { background: var(--bs-body-bg); }` (instead of hardcoded `#f5f7fa`)
- `.task-title-edit:focus { background: var(--bs-tertiary-bg); }`
- `.completed .task-title { color: var(--bs-secondary-color); }`

### 3. `<html>` data-bs-theme toggle via localStorage
- On load: read `localStorage.theme` → default to `'light'`
- Toggle switches between `'light'` / `'dark'`
- Persist choice to `localStorage.theme`
- Swap the toggle icon (sun ↔ moon)

### 4. No backend changes
Dark mode is purely frontend. Bootstrap 5.3 natively supports `data-bs-theme="dark"` on `<html>`, which recolorizes all components automatically. Custom CSS uses Bootstrap variables so everything responds to the theme.
