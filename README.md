# AIPR
A Github action to create PRs using ChatGPT for improved issue resolution

## How to Use AIPR in Your Project
1. Install the AIPR repository as a dependency in your project.
2. Create an issue in your project repository and label it with "AIPR"
3. Once the issue is labeled, the AIPR Github action will automatically create a PR to solve the issue using ChatGPT.
4. Alternatively, you can manually trigger AIPR by commenting on the issue, such as "Create PR with AIPR 🚀." This will also create a PR using ChatGPT.

## Sample Workflow File
A sample workflow file `AIPR.yaml` inside workflow folder could look like this:

```
on:
  issues:
    types: [labeled]
  issue_comment:
    types: [created]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  Creating-PR-using-AIPR:
    if: ${{ (github.event_name == 'issues' && 
             contains( github.event.label.name, 'AIPR')) || 
            (github.event_name == 'issue_comment' && 
             github.event.issue.pull_request &&
             contains( github.event.comment.body, 'Create PR with AIPR 🚀')) }}
    runs-on: ubuntu-latest
    steps:
    - name: Executing AIPR action
      uses: alexanmtz/AIPR@main
      with:
        openai_api_key: ${{ secrets.OPENAI_API_KEY }}
        openai_tokens: 200 # default is 200
 ```

This workflow file will trigger the AIPR action when an issue is labeled or reopened.

## General Instructions for Github Actions
Github Actions are automated workflows that you can customize to build, test, and deploy projects automatically in your repository. You can create custom actions or use pre-made ones from the [Github Marketplace](https://github.com/marketplace?type=actions). 

To use a GitHub Action, you must create a workflow file (.yaml) in your project repository. This file contains the steps to execute when a specific event occurs, such as pushing code, creating an issue, or adding a label. These steps can combine shell commands and actions from the GitHub Marketplace.

Once a workflow file is created and pushed to your repository, it will start running when the specified event occurs. You can view the status of your workflows in the "Actions" tab of your repository. 

For more detailed instructions on using Github Actions in your project, check out the [Github Actions documentation](https://docs.github.com/en/actions).

## Colaborate with AIPR

## Setting Up AIPR in Your Project
1. Fork the [AIPR repository](https://github.com/alexanmtz/AIPR) into your own Github account.
3. Commit and push your changes to your fork. 
4. Create a PULL REQUEST
