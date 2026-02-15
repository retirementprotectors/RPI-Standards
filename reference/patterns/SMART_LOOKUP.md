# Smart Lookup Component — Reference Implementation

> **Mandatory for ALL person-selection fields that reference known entities.**

---

## Rule

Any UI field that selects a person from a known data source (team members, agents, producers, clients) **MUST** use the Smart Lookup type-ahead component. Plain `<select>` dropdowns and free `<input type="text">` fields are **forbidden** for this use case.

### What Counts as "Known Entity"
- RPI team members (`_USER_HIERARCHY`, `Users` sheet)
- Agents/Producers (`_PRODUCER_MASTER`, revenue records, comp cycles)
- Clients (`_CLIENT_MASTER`)
- Any person stored in a MATRIX sheet or project database

### Exceptions (Free Text IS Correct)
- Self-identification (user entering their own name, e.g., NPN lookup flow)
- External contacts not in any RPI database
- Multi-select assignment (use checkbox checklists instead)

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│ <div id="field-wrapper">  (smart-lookup class)  │
│   ┌──────────────────────────┐ ┌──┐            │
│   │ Text Input (id-input)    │ │ × │ clear btn  │
│   └──────────────────────────┘ └──┘            │
│   <input type="hidden" id="field">  ← SAME ID  │
│   ┌──────────────────────────┐                  │
│   │ Results dropdown         │                  │
│   │   Item 1                 │                  │
│   │   Item 2                 │                  │
│   │   Item 3                 │                  │
│   └──────────────────────────┘                  │
└─────────────────────────────────────────────────┘
```

**Key design decision:** The hidden input carries the **same ID** as the original `<select>` or `<input>` it replaces. This means all existing `document.getElementById('fieldId').value` reads continue to work with zero changes.

### Element IDs
| Element | ID Pattern | Purpose |
|---------|-----------|---------|
| Wrapper div | `{id}-wrapper` | Contains all smart lookup elements |
| Text input | `{id}-input` | Visible type-ahead field |
| Hidden input | `{id}` | Stores selected value (SAME ID as original) |
| Results dropdown | `{id}-results` | Filterable list of options |

---

## CSS (Adapt to Project Theme)

### Light Theme (C3, PRODASH, sentinel-v2)
```css
.smart-lookup { position: relative; }
.smart-lookup input[type="text"] {
  width: 100%; padding: 10px 32px 10px 14px;
  border: 1px solid var(--gray-300); border-radius: var(--radius-md);
  font-size: 14px; font-family: inherit; background: white;
}
.smart-lookup input[type="text"]:focus {
  outline: none; border-color: var(--rpi-blue);
  box-shadow: 0 0 0 3px rgba(107, 163, 199, 0.15);
}
.smart-lookup-results {
  position: absolute; top: 100%; left: 0; right: 0;
  background: white; border: 1px solid var(--gray-300); border-top: none;
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  max-height: 200px; overflow-y: auto; z-index: 100; display: none;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
.smart-lookup-results.open { display: block; }
.smart-lookup-item {
  padding: 8px 12px; cursor: pointer; font-size: 14px;
  transition: background 0.1s;
}
.smart-lookup-item:hover { background: var(--rpi-blue-pale); }
.smart-lookup-item .item-sub {
  font-size: 12px; color: var(--gray-500); margin-top: 1px;
}
.smart-lookup-clear {
  position: absolute; right: 10px; top: 50%; transform: translateY(-50%);
  background: none; border: none; color: var(--gray-400);
  cursor: pointer; font-size: 1.1rem; padding: 4px; line-height: 1;
}
.smart-lookup-clear:hover { color: var(--gray-700); }
.smart-lookup-empty {
  padding: 8px 12px; font-size: 13px; color: var(--gray-400);
  font-style: italic;
}
```

### Dark Theme (CAM, RIIMO)
```css
/* Same structure, swap colors: */
.smart-lookup input[type="text"] {
  background: var(--bg-dark); /* or var(--rpi-navy-dark) */
  border-color: var(--border); /* or var(--gray-600) */
  color: var(--text-primary); /* or var(--gray-100) */
}
.smart-lookup-results {
  background: var(--bg-card); /* or var(--rpi-navy-dark) */
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.smart-lookup-item:hover { background: var(--primary); color: white; }
```

---

## JavaScript — ES6 Version (C3, CAM, sentinel-v2, PRODASH)

```javascript
function buildSmartLookup(id, items, selectedValue, placeholder) {
  let displayText = '';
  if (selectedValue) {
    const match = items.find(i => i.value === selectedValue);
    if (match) displayText = match.label;
  }

  let html = `<div class="smart-lookup" id="${id}-wrapper">`;
  html += `<input type="text" id="${id}-input" value="${displayText}" placeholder="${placeholder || 'Start typing...'}" autocomplete="off" onfocus="openSmartLookup('${id}')" oninput="filterSmartLookup('${id}')">`;
  html += `<input type="hidden" id="${id}" value="${selectedValue || ''}">`;
  if (displayText) {
    html += `<button class="smart-lookup-clear" onclick="clearSmartLookup('${id}')" title="Clear">&times;</button>`;
  }
  html += `<div class="smart-lookup-results" id="${id}-results">`;
  items.forEach(item => {
    html += `<div class="smart-lookup-item" data-value="${item.value}" data-label="${item.label}" onclick="selectSmartLookup('${id}', this)">`;
    html += item.label;
    if (item.sub) html += `<div class="item-sub">${item.sub}</div>`;
    html += `</div>`;
  });
  if (!items.length) html += `<div class="smart-lookup-empty">No options available</div>`;
  html += `</div></div>`;
  return html;
}

function openSmartLookup(id) {
  const results = document.getElementById(id + '-results');
  if (results) {
    results.querySelectorAll('.smart-lookup-item').forEach(i => i.style.display = '');
    results.classList.add('open');
  }
  const input = document.getElementById(id + '-input');
  if (input) input.select();
}

function filterSmartLookup(id) {
  const input = document.getElementById(id + '-input');
  const results = document.getElementById(id + '-results');
  if (!input || !results) return;

  const query = input.value.toLowerCase();
  let visibleCount = 0;

  results.querySelectorAll('.smart-lookup-item').forEach(item => {
    const label = (item.getAttribute('data-label') || '').toLowerCase();
    if (!query || label.includes(query)) {
      item.style.display = '';
      visibleCount++;
    } else {
      item.style.display = 'none';
    }
  });

  const emptyMsg = results.querySelector('.smart-lookup-empty');
  if (emptyMsg) emptyMsg.style.display = visibleCount === 0 ? '' : 'none';
  results.classList.add('open');

  // Clear hidden value while user is typing (no selection yet)
  document.getElementById(id).value = '';
}

function selectSmartLookup(id, el) {
  const input = document.getElementById(id + '-input');
  const hidden = document.getElementById(id);
  const results = document.getElementById(id + '-results');

  input.value = el.getAttribute('data-label');
  hidden.value = el.getAttribute('data-value');
  results.classList.remove('open');

  // Show clear button
  const wrapper = document.getElementById(id + '-wrapper');
  if (wrapper && !wrapper.querySelector('.smart-lookup-clear')) {
    const btn = document.createElement('button');
    btn.className = 'smart-lookup-clear';
    btn.setAttribute('onclick', `clearSmartLookup('${id}')`);
    btn.title = 'Clear';
    btn.innerHTML = '&times;';
    wrapper.appendChild(btn);
  }

  // Fire change event so dependent logic can react
  hidden.dispatchEvent(new Event('change', { bubbles: true }));
}

function clearSmartLookup(id) {
  const input = document.getElementById(id + '-input');
  const hidden = document.getElementById(id);
  if (input) input.value = '';
  if (hidden) {
    hidden.value = '';
    hidden.dispatchEvent(new Event('change', { bubbles: true }));
  }
  const wrapper = document.getElementById(id + '-wrapper');
  const clearBtn = wrapper ? wrapper.querySelector('.smart-lookup-clear') : null;
  if (clearBtn) clearBtn.remove();
}

function setSmartLookupValue(id, value) {
  const hidden = document.getElementById(id);
  const input = document.getElementById(id + '-input');
  if (!hidden) return;
  hidden.value = value || '';
  if (input) {
    const results = document.getElementById(id + '-results');
    if (results && value) {
      const match = results.querySelector(`.smart-lookup-item[data-value="${value}"]`);
      input.value = match ? match.getAttribute('data-label') : value;
      // Show clear button
      const wrapper = document.getElementById(id + '-wrapper');
      if (wrapper && !wrapper.querySelector('.smart-lookup-clear')) {
        const btn = document.createElement('button');
        btn.className = 'smart-lookup-clear';
        btn.setAttribute('onclick', `clearSmartLookup('${id}')`);
        btn.title = 'Clear';
        btn.innerHTML = '&times;';
        wrapper.appendChild(btn);
      }
    } else {
      input.value = '';
      const wrapper = document.getElementById(id + '-wrapper');
      const clearBtn = wrapper ? wrapper.querySelector('.smart-lookup-clear') : null;
      if (clearBtn) clearBtn.remove();
    }
  }
}

// Close smart lookups on outside click
document.addEventListener('click', function(e) {
  document.querySelectorAll('.smart-lookup-results.open').forEach(r => {
    if (!r.parentElement.contains(e.target)) r.classList.remove('open');
  });
});
```

---

## JavaScript — ES5 Version (RIIMO, legacy GAS apps)

Same logic, but uses `var`, `function(){}`, string concatenation, and `for` loops instead of ES6 features. See RIIMO/Index.html for the canonical ES5 implementation.

---

## Usage Patterns

### 1. Static Container (replace a `<select>`)
```html
<!-- Before -->
<select id="agent-select" onchange="filterData()">
  <option value="">All Agents</option>
</select>

<!-- After -->
<div id="agent-select-container"></div>
```
```javascript
// Populate
const items = agents.map(a => ({ value: a.id, label: a.name, sub: a.role }));
container.innerHTML = buildSmartLookup('agent-select', items, '', 'Search agent...');

// Wire onchange
document.getElementById('agent-select').addEventListener('change', filterData);
```

### 2. Dynamic Rebuild (data changes)
```javascript
// Use rebuildSmartLookupItems to update without full re-render
function rebuildSmartLookupItems(id, items) {
  const results = document.getElementById(id + '-results');
  if (!results) return;
  clearSmartLookup(id);
  let html = '';
  items.forEach(item => {
    html += `<div class="smart-lookup-item" data-value="${item.value}" data-label="${item.label}" onclick="selectSmartLookup('${id}', this)">${item.label}</div>`;
  });
  if (!items.length) html += `<div class="smart-lookup-empty">No options available</div>`;
  results.innerHTML = html;
}
```

### 3. Programmatic Value Setting
```javascript
setSmartLookupValue('agent-select', 'josh@retireprotected.com');
clearSmartLookup('agent-select');
```

---

## Item Format

```javascript
const items = [
  { value: 'josh@retireprotected.com', label: 'Josh Millang', sub: 'Owner' },
  { value: 'john@retireprotected.com', label: 'John Behn', sub: 'Executive' }
];
```

| Field | Required | Purpose |
|-------|----------|---------|
| `value` | Yes | Stored in hidden input, sent to backend |
| `label` | Yes | Displayed in text input and dropdown |
| `sub` | No | Secondary info (role, company, tier) shown below label |

---

## Deployed In

| App | Version | Fields |
|-----|---------|--------|
| RIIMO | v1.8.2 | 6 fields (division exec, unit leader, reports-to, queue forms) |
| C3 | v7.3 | 6 fields (5 owner selects + block editor) |
| CAM | v1.7.2 | 3 fields (bob-agent, history-agent, submit-agent) |
| PRODASH | v166 | 1 field (clientAgentFilter) |
| sentinel-v2 | v3.3.0 | 1 field (dealProducerName) |

---

*This pattern is MANDATORY per `~/.claude/CLAUDE.md` Code Standards.*
