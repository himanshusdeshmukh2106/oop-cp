# Django 5.0 Compatibility Fix

## Issue
Django 5.0.1 removed the deprecated `{% ifequal %}` and `{% ifnotequal %}` template tags that were used in older Django versions.

## Error
```
TemplateSyntaxError: Invalid block tag on line 4: 'ifequal', expected 'endblock'. 
Did you forget to register or load this tag?
```

## Fix Applied

### File: `health/templates/login.html`

**Before (Django 3.x syntax):**
```django
{% ifequal error "pat1" %}
    <script>alert('logged in successfully');</script>
{% endifequal %}
```

**After (Django 5.x syntax):**
```django
{% if error == "pat1" %}
    <script>alert('logged in successfully');</script>
{% endif %}
```

## Changes Made

Replaced all instances of:
- `{% ifequal variable value %}` → `{% if variable == value %}`
- `{% endifequal %}` → `{% endif %}`

## Files Modified
1. ✅ `health/templates/login.html` - Fixed 4 instances

## Testing
After this fix, the login page should work correctly:
1. Navigate to `/login`
2. The page should load without errors
3. Login functionality should work as expected

## Django Version Compatibility
- ✅ Django 5.0+
- ✅ Django 4.x
- ✅ Django 3.x (still compatible)

## Additional Notes
- The `{% if variable == value %}` syntax is the modern Django template syntax
- It's more readable and consistent with Python syntax
- No other deprecated tags were found in the templates
