## Why

Dark mode reduces eye strain in low-light environments and is a standard feature users expect from modern web apps. The app currently hardcodes `data-bs-theme="light"` with no toggle mechanism.

## What Changes

- Add a dark mode toggle button in the header area
- Persist the user's preference in `localStorage`
- Leverage Bootstrap 5's built-in `data-bs-theme` attribute to switch between light and dark themes
- Update inline CSS to work correctly in both themes
- Remove hardcoded `data-bs-theme="light"` and default to system preference or saved preference

## Capabilities

### New Capabilities
- `dark-mode`: User-controlled dark mode toggle with persistent preference across sessions

### Modified Capabilities

None.

## Impact

- `templates/index.html` — frontend-only changes to add toggle UI, theme switching logic, localStorage persistence, and CSS adjustments
