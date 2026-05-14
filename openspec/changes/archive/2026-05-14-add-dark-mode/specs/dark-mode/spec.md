## ADDED Requirements

### Requirement: Theme toggle button
The system SHALL display a theme toggle button in the header area that switches between light and dark themes.

#### Scenario: Toggle from light to dark
- **WHEN** user clicks the theme toggle button while in light mode
- **THEN** the application switches to dark theme
- **AND** the toggle icon changes from sun to moon

#### Scenario: Toggle from dark to light
- **WHEN** user clicks the theme toggle button while in dark mode
- **THEN** the application switches to light theme
- **AND** the toggle icon changes from moon to sun

### Requirement: Persist theme preference
The system SHALL persist the user's theme preference across sessions using localStorage.

#### Scenario: Preference persists after page reload
- **WHEN** user toggles to dark theme
- **AND** user refreshes the page
- **THEN** the application loads in dark theme

#### Scenario: Preference persists after browser restart
- **WHEN** user toggles to dark theme
- **AND** user closes and reopens the browser
- **THEN** the application loads in dark theme

### Requirement: Default to system preference
The system SHALL default to the user's system color scheme preference if no saved preference exists.

#### Scenario: System prefers dark, no saved preference
- **WHEN** user visits the app for the first time
- **AND** their OS is set to dark mode
- **THEN** the application loads in dark theme

#### Scenario: System prefers light, no saved preference
- **WHEN** user visits the app for the first time
- **AND** their OS is set to light mode
- **THEN** the application loads in light theme

### Requirement: Dark theme styling for all UI elements
The system SHALL render all existing UI elements correctly in dark theme, including task cards, modals, forms, badges, and buttons.

#### Scenario: Task card in dark theme
- **WHEN** dark theme is active
- **THEN** task cards have dark background with appropriate text contrast

#### Scenario: Modal in dark theme
- **WHEN** dark theme is active
- **AND** a modal is opened
- **THEN** the modal has dark background with appropriate text contrast

#### Scenario: Priority badges in dark theme
- **WHEN** dark theme is active
- **THEN** priority badges maintain readable contrast

### Requirement: No flash of wrong theme
The system SHALL prevent a flash of the light theme when the user has dark mode preference.

#### Scenario: Theme applied before render
- **WHEN** user has dark mode preference saved
- **AND** the page loads
- **THEN** the dark theme is applied before any content is painted
