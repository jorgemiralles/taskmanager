## Context

Single-page Flask task manager with Bootstrap 5 frontend. Currently hardcodes `data-bs-theme="light"` on the `<html>` element and uses light-background inline CSS. Bootstrap 5.3+ has built-in dark mode support via the `data-bs-theme` attribute. The app has no build step — all CSS is inline in `templates/index.html`.

## Goals / Non-Goals

**Goals:**
- Add a toggle button in the header to switch between light and dark themes
- Persist the user's preference in `localStorage`
- Respect `prefers-color-scheme` as the default if no saved preference exists
- All existing UI (task cards, modals, badges, buttons) renders correctly in both themes
- Zero server-side changes — frontend only

**Non-Goals:**
- Custom color scheme editor
- Per-task or per-page theme override
- System-level theme sync (beyond initial default)

## Decisions

1. **Bootstrap native dark mode via `data-bs-theme`** over custom CSS variables. Bootstrap 5.3+ fully supports this attribute. Switching the attribute on `<html>` instantly re-themes all Bootstrap components (modals, cards, buttons, forms) with no extra CSS. No external dependency needed.

2. **localStorage for persistence** over cookies or server-side preference. Theme is a purely client-side concern. localStorage has a simple API and persists across sessions. Cookies would add unnecessary request overhead.

3. **`prefers-color-scheme` as default** over always-light or always-dark. This matches user's OS-level setting and is the most respectful default. Falls back to light if the media query is unsupported.

4. **Toggle icon: sun/moon Bootstrap Icons** over a text label. Icons are universally understood and take minimal space. `bi-sun` for light mode, `bi-moon` for dark mode, swapped on toggle.

5. **Inline `<style>` overrides for non-Bootstrap elements** over a separate CSS file. The app currently uses inline `<style>` with a few custom classes (`.task-card`, `.priority-high`, `.overdue`, etc.). Adding `[data-bs-theme="dark"]` prefixed overrides keeps all styling in one place with no additional HTTP request.

## Risks / Trade-offs

- `data-bs-theme` is a Bootstrap 5.3+ feature. If someone downgrades Bootstrap CSS, dark mode breaks → Mitigation: document that Bootstrap 5.3+ is required.
- Inline CSS overrides may not cover all edge cases (e.g., custom form control styling in dark mode) → Mitigation: test all states after implementation; add overrides as needed.
- Flash of light theme on slow connections if localStorage read is deferred → Mitigation: apply theme in a synchronous `<script>` block in `<head>` before rendering.
