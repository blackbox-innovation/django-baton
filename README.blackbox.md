# Django Baton Development Setup

Quick start guide for Django Baton development environment with the alternative theme.

## Prerequisites

- Node.js and npm
- Python with Django installed
- Git


## Development

Use the start script to run both servers and open admin:

`./start-baton.sh`

This will:
- Start Django development server
- Start Webpack dev server
- Open Django admin interface

Alternatively, run servers manually:

```bash
# Start both servers
cd baton/static/baton/app
npm run dev:all
```


Access the admin interface at:
- http://localhost:8000/admin

Frontend assets are served from:
- http://localhost:8080

## Releases

Releases are automatically handled through GitHub Actions. When commits are pushed to the main branch, the workflow will:
- Build and test the package
- Create a new release if version has been updated
- Publish the package to PyPI
- Generate release notes automatically
