# AIPR
A Github action to create PRs using ChatGPT for improved issue resolution

## How to Use AIPR in Your Project
1. Install the AIPR repository as a dependency in your project.
2. Create an issue in your project repository and label it with "AIPR"
3. Once the issue is labeled, the AIPR Github action will automatically create a PR to solve the issue using ChatGPT.
4. Alternatively, you can also manually trigger AIPR by making a comment on the issue such as "Create PR with AIPR 🚀". This will also create a PR using ChatGPT.

## Setting Up AIPR in Your Project
1. Fork the [AIPR repository](https://github.com/alexanmtz/AIPR) into your own Github account.
2. Add the following snippet to the end of your workflow file:

```
- name: AIPR
  uses: <your_github_username>/AIPR@main
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

3. Commit and push your changes to the workflow file. 
4. Label an issue with "AIPR" to see the action in action! (haha get it?) 

## Sample Workflow File
A sample workflow file `main.yaml` could look like this:

```
name: AIPR-Workflow

on:
  issues:
    types: [labeled, reopened]

jobs:
  AIPR-job:
    runs-on: ubuntu-latest
    name: AIPR Job
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      # your other steps here

      - name: AIPR
      uses: <your_github_username>/AIPR@main
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

This workflow file will trigger the AIPR action when an issue is labeled or reopened.

## General Instructions for Github Actions
Github Actions are automated workflows that you can customize to automatically build, test, and deploy projects in your repository. You can create your own custom actions or use pre-made actions from the [Github Marketplace](https://github.com/marketplace?type=actions). 

To use a Github Action, you need to create a workflow file (.yaml) in your project repository. This file contains the steps that need to be executed when a specific event occurs, such as pushing code, creating an issue, or adding a label. These steps can be a combination of shell commands and actions from the Github Marketplace.

Once a workflow file is created and pushed to your repository, it will start running when the specified event occurs. You can view the status of your workflows in the "Actions" tab of your repository. 

For more detailed instructions on how to use Github Actions in your project, check out the [Github Actions documentation](https://docs.github.com/en/actions).
