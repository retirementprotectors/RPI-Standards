# 🎨 RPI UI Design Guidelines

> **Applies To**: ALL RAPID Projects (SENTINEL, PRODASH, RAPID_IMPORT, RAPID_API)  
> **Version**: v1.0 (December 29, 2025)  
> **Source of Truth**: This document

---

## 🎯 Core Principles

1. **Consistency** - Same patterns across all apps
2. **No Native Dialogs** - Never use alert/confirm/prompt
3. **Mobile First** - Responsive design always
4. **Accessible** - Proper contrast, labels, focus states

---

## 🎨 Brand Colors

### Primary Palette

| Token | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Navy (Primary)** | `#1e3a5f` | `--rpi-navy` | Headers, primary buttons |
| **Navy Dark** | `#152a45` | `--rpi-navy-dark` | Hover states, active |
| **Navy Light** | `#2a4a72` | `--rpi-navy-light` | Secondary backgrounds |
| **Blue (Accent)** | `#6ba3c7` | `--rpi-blue` | Links, highlights |
| **Blue Light** | `#8bbad6` | `--rpi-blue-light` | Hover accents |
| **Blue Pale** | `#d4e6f1` | `--rpi-blue-pale` | Backgrounds, disabled |

### Status Colors

| Status | Hex | CSS Variable | Usage |
|--------|-----|--------------|-------|
| **Success** | `#28a745` | `--success-color` | Confirmations, positive |
| **Warning** | `#ffc107` | `--warning-color` | Alerts, attention |
| **Error** | `#dc3545` | `--error-color` | Errors, destructive |
| **Info** | `#17a2b8` | `--info-color` | Informational |

### CSS Variables Template

```css
:root {
  /* Brand */
  --rpi-navy: #1e3a5f;
  --rpi-navy-dark: #152a45;
  --rpi-navy-light: #2a4a72;
  --rpi-blue: #6ba3c7;
  --rpi-blue-light: #8bbad6;
  --rpi-blue-pale: #d4e6f1;
  
  /* Status */
  --success-color: #28a745;
  --warning-color: #ffc107;
  --error-color: #dc3545;
  --info-color: #17a2b8;
  
  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
}
```

---

## 📝 Typography

| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| **H1** | 24px | 700 (Bold) | Page titles |
| **H2** | 20px | 600 (Semi) | Section headers |
| **H3** | 16px | 600 (Semi) | Card headers |
| **Body** | 14px | 400 (Regular) | Default text |
| **Small** | 12px | 400 (Regular) | Captions |
| **Mono** | 13px | 400 (Regular) | Code, IDs |

### Font Stack

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
```

---

## 📐 Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Tight gaps (icon-to-text) |
| `--space-2` | 8px | Standard gaps |
| `--space-3` | 12px | Small padding (buttons) |
| `--space-4` | 16px | Card padding |
| `--space-6` | 24px | Section margins |
| `--space-8` | 32px | Large section breaks |

---

## 🧩 Component Classes

### Buttons

```css
.btn-primary    /* Navy background, white text */
.btn-secondary  /* Outlined, navy text */
.btn-danger     /* Red background (destructive) */
.btn-icon       /* Icon-only, circular */
```

### Cards & Containers

```css
.card           /* White bg, shadow, rounded */
.summary-card   /* Large number + label */
.section-header /* Collapsible with toggle */
```

### Forms

```css
.form-group     /* Wrapper with margin */
.form-label     /* Bold label above input */
.form-input     /* Text input with border */
.form-select    /* Dropdown select */
```

### Tables

```css
.data-table     /* Full-width with borders */
.data-grid      /* Grid layout for cards */
```

### Modals

```css
.modal-overlay  /* Dark backdrop */
.modal-content  /* White box, centered */
.modal-header   /* Title + close button */
.modal-body     /* Content area */
.modal-footer   /* Action buttons */
```

---

## 🔔 Feedback Patterns

### ✅ Required Functions (All Apps)

Every app MUST implement these utility functions:

```javascript
/**
 * Show a toast notification
 * @param {string} message - Message to display
 * @param {string} type - 'success' | 'error' | 'warning' | 'info'
 */
function showToast(message, type = 'info') {
  // Implementation required
}

/**
 * Show confirmation dialog
 * @param {Object} options
 * @returns {Promise<boolean>}
 */
async function showConfirmation({
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  confirmStyle = 'primary'  // or 'danger'
}) {
  // Implementation required - returns true/false
}

/**
 * Show input modal
 * @param {Object} options
 * @returns {Promise<string|null>}
 */
async function showInputModal({
  title,
  message,
  placeholder,
  confirmText = 'Save'
}) {
  // Implementation required - returns value or null
}

/**
 * Show/hide loading overlay
 */
function showLoading(message = 'Loading...') { }
function hideLoading() { }
```

### Usage Examples

```javascript
// ✅ CORRECT
showToast('Deal saved successfully', 'success');
showToast('Error loading data', 'error');

const confirmed = await showConfirmation({
  title: 'Delete Deal?',
  message: 'This action cannot be undone.',
  confirmText: 'Delete',
  confirmStyle: 'danger'
});

const newName = await showInputModal({
  title: 'Rename Deal',
  message: 'Enter new name:',
  placeholder: 'e.g., Acme Insurance'
});
```

---

## ⛔ FORBIDDEN PATTERNS

### NEVER Use These

```javascript
// ❌ BANNED - Terrible UX
alert('Error!');
confirm('Are you sure?');
prompt('Enter name:');

// ❌ BANNED - Inline styles for colors
element.style.backgroundColor = '#1e3a5f';

// ❌ BANNED - Console for user errors
console.log('User error: ' + message);

// ❌ BANNED - Missing loading states
// (Always show loading on async operations)
```

### ALWAYS Use Instead

```javascript
// ✅ CORRECT
showToast('Error!', 'error');
await showConfirmation({ title: 'Are you sure?', ... });
await showInputModal({ title: 'Enter name', ... });

// ✅ CORRECT - CSS variables
element.classList.add('bg-primary');

// ✅ CORRECT - User-facing feedback
showToast('Something went wrong', 'error');

// ✅ CORRECT - Loading states
showLoading('Saving...');
await saveData();
hideLoading();
```

---

## 📱 Responsive Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| **Mobile** | < 768px | Stack, full-width |
| **Tablet** | 768px - 1024px | Two columns |
| **Desktop** | > 1024px | Full sidebar + main |

### Mobile-First Example

```css
/* Base (mobile) */
.container {
  flex-direction: column;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    flex-direction: row;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .sidebar {
    width: 280px;
  }
}
```

---

## ✅ Validation Checklist

Before deploying ANY frontend changes:

- [ ] No `alert()`, `confirm()`, or `prompt()` calls
- [ ] All async operations have loading states
- [ ] All colors use CSS variables (not hardcoded)
- [ ] Mobile responsive (test at 375px width)
- [ ] Error states show user-friendly toasts
- [ ] All buttons have hover/focus states
- [ ] Modals can be closed with Escape key
- [ ] Form inputs have labels

---

## 📚 App-Specific Extensions

| App | Additional Guidelines |
|-----|----------------------|
| **SENTINEL** | Purple accents for outputs, navy for setup |
| **PRODASH** | B2C-focused, simpler UI |
| **RAPID_IMPORT** | Wizard flows for imports |
| **RAPID_API** | Minimal UI (mostly backend) |

---

*This is the single source of truth for UI patterns across all RPI apps.*

