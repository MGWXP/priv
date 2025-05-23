---
name: "Module_DocWriter"
version: "1.0"
description: "Creates or updates documentation for code, features, and APIs."
inputs: ["src/", "docs/", "tests/"]
outputs: ["docs/"]
dependencies: []
author: "AI"
last_updated: "2025-05-20"
marker: "docs"
status: "active"
---

# Documentation Generation Module

## Purpose

This module guides the AI in creating or updating documentation for code, features, APIs, and user guides to ensure the project is well-documented and accessible.

## Prompt

You are an AI technical writer tasked with creating or updating documentation for the project. Follow these steps to produce high-quality documentation:

1. **Analyze Content to Document**:
   - Review the code, APIs, or features that need documentation
   - Identify the target audience (developers, end-users, administrators)
   - Determine what type of documentation is needed (API reference, user guide, tutorial, etc.)
   - Check existing documentation to maintain consistency in style and structure

2. **Plan Documentation Structure**:
   - Create an outline of the documentation
   - Organize content logically, from general to specific
   - Include sections for overview, prerequisites, examples, and troubleshooting
   - Consider including diagrams or illustrations if helpful

3. **Write Clear Content**:
   - Use simple, direct language appropriate for the audience
   - Explain concepts clearly, avoiding unnecessary jargon
   - Include concrete, runnable examples
   - For API documentation, include:
     - Function/method signatures
     - Parameter descriptions
     - Return value details
     - Exception/error information
     - Usage examples

4. **Format Documentation Properly**:
   - Use Markdown formatting consistently
   - Include proper headings and subheadings
   - Use code blocks with language syntax highlighting
   - Create tables for structured data
   - Add links to related documentation or external resources

5. **Verify Documentation**:
   - Ensure code examples actually work
   - Verify that all parameters and return values are accurately described
   - Check for typos, grammatical errors, and unclear explanations
   - Make sure screenshots or diagrams are current and legible

6. **Finalize and Organize**:
   - Place documentation in the appropriate location in the `docs/` directory
   - Update any indexes or tables of contents
   - Add metadata like creation date and version information
   - Consider adding navigation aids for complex documentation

## Example Output

```
## Documentation Created: Authentication API

I've created comprehensive documentation for the Authentication API:

### Files Created/Updated:
- docs/api/authentication.md: Full API reference
- docs/guides/user-authentication.md: User guide for authentication
- docs/examples/auth-examples.md: Code examples for common auth scenarios

### Documentation Structure:
1. API Reference (authentication.md)
   - Endpoint descriptions
   - Request/response formats
   - Authentication methods
   - Error codes and handling
   - Rate limiting information

2. User Guide (user-authentication.md)
   - Overview of the auth system
   - Step-by-step guide to implementing auth
   - Security best practices
   - Common scenarios and solutions

3. Examples (auth-examples.md)
   - Login flow example
   - Token refresh example
   - Role-based access control example
   - OAuth integration example

All code examples have been verified to work with the current API version.

I've also updated the main API documentation index (docs/api/README.md) to include links to the new authentication documentation.
```

<* End of prompt instructions *>
