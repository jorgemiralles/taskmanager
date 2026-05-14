## 1. Theme Initialization

- [x] 1.1 Add synchronous `<script>` block in `<head>` that reads `localStorage.getItem('theme')` or falls back to `prefers-color-scheme` media query and sets `document.documentElement.dataset.bsTheme` before any rendering
- [x] 1.2 Remove hardcoded `data-bs-theme="light"` from the `<html>` tag

## 2. Toggle Button UI

- [x] 2.1 Add a theme toggle button (icon-only, `btn btn-sm btn-outline-secondary`) next to the "Add Task" button in the header, using `bi-sun-fill` / `bi-moon-fill` Bootstrap Icons

## 3. Toggle Logic

- [x] 3.1 Implement click handler that flips between `light` and `dark` on `document.documentElement.dataset.bsTheme`, updates the toggle icon, and saves preference to `localStorage`
- [x] 3.2 Set initial toggle icon based on current theme when page loads

## 4. Dark Theme CSS Overrides

- [x] 4.1 Add `[data-bs-theme="dark"]` prefixed CSS overrides for custom styles: body background, task-card hover shadow, priority border colors, overdue text, and inline edit background
