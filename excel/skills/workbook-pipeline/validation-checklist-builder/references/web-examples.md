# Web Examples

Web scan date: 2026-04-11

## Potentially useful references

- `collective/pytest-jsonschema`
  https://github.com/collective/pytest-jsonschema
  Why it matters: example of schema-based validation thinking for structured checklist artifacts.

- Example using Pydantic as Schema for YAML Files
  https://gist.github.com/ericvenarusso/dcaefd5495230a33ef2eb2bdca262011
  Why it matters: useful pattern for defining checklist items as validated data instead of ad hoc text.

- JSON Schema Validate Action
  https://github.com/marketplace/actions/json-schema-validate
  Why it matters: another concrete schema-validation example if we want machine-checkable checklist files.

- `steipete/Peekaboo`
  https://github.com/steipete/Peekaboo
  Why it matters: interesting prior art for turning visible UI expectations into executable desktop checks.

## Takeaway

The most reusable external idea here is to make the checklist structured and validated. UI assertion execution can stay with the existing screen-interaction skills.
