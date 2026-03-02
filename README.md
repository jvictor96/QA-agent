# QA agent

This agent is written using langchain, to make architectural and style reviews in pull requests changes.

## Usage 

```yaml
name: QA

on:
  workflow_dispatch:
  pull_request:
    types: [assigned, opened, synchronize, reopened]

jobs:
  qa:
    uses: jvictor96/QA-agent/.github/workflows/qa_agent.yml@main
    permissions:
        pull-requests: write
    with:
      reasoning_model: gpt-5-mini
      target_branch: origin/master
    secrets:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## Tools

The official [github](https://github.com/github/github-mcp-server?tab=readme-ov-file#local-github-mcp-server) MCP server offers dozens of tools.
As permissions should only encompas pull requests, the tools for this agent are:

- add_comment_to_pending_review
- add_reply_to_pull_request_comment
- create_pull_request
- list_pull_requests
- merge_pull_request (which is not be available as the pull-request permissions doesn't allow)
- pull_request_read
- pull_request_review_write
- search_pull_requests
- update_pull_request
- update_pull_request_branch


## About Permissions

https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps?apiVersion=2022-11-28#repository-permissions-for-pull-requests

