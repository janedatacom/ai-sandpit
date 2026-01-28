# Chapter 03 — Red Hat OpenShift Lab (CLI + Jupyter)

[Back to all lab instructions](../../LAB_INSTRUCTIONS.md)

**Duration**: ~20 minutes (hands-on)

## Goal

Set up your first **Project**, **Pod**, and a **workspace** so you can run **Jupyter Notebooks** for your first Python script.

## Learning outcomes

By the end of this lab you can:

- Log in to the OpenShift console
- Navigate the Developer Console
- Open the built-in CLI terminal and run basic `oc` commands
- Create (or request access to create) the resources needed for a Jupyter-based workspace

## Prerequisites

| Item | Notes |
|---|---|
| OpenShift access | Cluster URL + credentials |
| Permissions | Ability to create or be granted access to a project/namespace |

> Facilitator note: If students cannot create resources, pre-create projects or ensure they have the right RBAC before the session.

---

## Lab steps

![Lab Overview](assets/lab-overview.png)

### 1) Log in to OpenShift

- [ ] Open the OpenShift console in your browser.

- [ ] Sign in with your provided credentials to the Axis Portal (Datacom Training) or other portal (Customer Training), then choose **AI Lab - OpenShift Console (Web)**.

    ![Axis Portal: OpenShift Console link](assets/axis-portal-openshift-console-link.png)

- [ ] Sign in with your provided credentials to AI Lab - OpenShift Console (Web).

    ![OpenShift landing page after login](assets/openshift-landing-page-after-login.png)

---

### 2) Take the guided tour (Developer Console)

![Step 2 Powerpoint page](assets/step-2-powerpoint-page.png)

When prompted, click **Get started** to begin the tour.

- [ ] Start the tour and click through the next few pop-up screens.

    ![Start guided tour prompt](assets/start-guided-tour-prompt.png)

- [ ] Click **Next** through the tour screens.
- [ ] Pay attention to the different **Perspectives** (Administrator vs Developer).

    ![Perspective switcher (Administrator/Developer)](assets/perspective-switcher-administrator-developer.png)

Along the way you’ll see:
- Where to find metrics about application performance.

    ![Observe](assets/observe.png)
- How to search and list resources in your project.

    ![Search for resources in your project](assets/search-resources-in-project.png)
- How to use command line tools (CLI) to create and check on resources.

    ![Web Terminal](assets/web-terminal.png)
- Where to get help for quick starts, restarting the tour, deploying applications, etc.

    ![Help page](assets/help-page.png)
- Where to set up your preferences (default views, colour, etc.).

    ![You're ready to go](assets/youre-ready-to-go.png)

- [ ] Finish the tour (**Okay, got it**).

    ![Create a pod (overview)](assets/create-a-pod-overview.png)

### 3) Create your project (via GUI or CLI)
![Step 3 Powerpoint page](assets/step-3-powerpoint-page.png)

**GUI option**

- [ ] Go to **Developer** perspective.

    ![Developer perspective and choose Topology](assets/developer-perspective-topology.png)

- [ ] Create a **Project**, enter name, display name and description and click Create

    ![Enter the name, display name and description](assets/create-project-enter-details.png)

- [ ] Your project has been created

    ![You Project is created](assets/project-created.png)

**CLI option**
- [ ] You can also create a project via the Command Line Interface (CLI). 
      Start with the CLI Button from the top left menu.

    ![top menu with command line](assets/top-menu-command-line.png)
    ![CLI Prompt](assets/cli-prompt.png)

- [ ] Type the `oc new-project` command in the CLI and hit enter.

    ![cli command](assets/cli-command.png)

    ```bash
    oc new-project ai-students \
      --display-name="AI Training – Students" \
      --description="Projects for student notebooks and AI experiments"
    ```

- [ ] Review your project here in Developer Perspective → Project.

    ![Project view from menu](assets/project-view-menu.png)

- [ ] See your project information and metrics

    ![Project Screen](assets/project-screen.png)

### 4) Create a Workbench with a Jupyter Image

![Step 4 PowerPoint page](assets/step-4-powerpoint-page.png)

- [ ] Give the workbench a name like `Study1`, provide a description, and choose an image.

    ![Workbench name, description, and image](assets/workbench-name-description-image.png)

- [ ] Image Options - choose one with Jupyter, Data Science for eg.

    ![Workbench image](assets/workbench-image.png)

- [ ] You can also choose the version of python

    ![Version of Python](assets/version-of-python.png)

- [ ] Leave everything else as default - deployment size, accelerator

    ![Deployment size](assets/deployment-size.png)

- [ ] Environment variables, cluster storage and connections

    ![Then Enviro vars, cluster and connections](assets/env-vars-cluster-storage-connections.png)

- [ ] Click **Create Workbench**.

    ![Create workbench button](assets/create-workbench-button.png)

- [ ] Wait for the project to be created.

    ![Pod status after create](assets/pod-status-after-create.png)

- [ ] Your project is not created and listed.

    ![new project listed](assets/new-project-listed.png)

### 5) Explore Jupyter Notebooks

![Step 5 - powerpoint slide](assets/step-5-powerpoint-slide.png)

- [ ] From your previous step 4, choose the Project Workbench

    ![Project workbench](assets/project-workbench.png)

- [ ] and click on the Workbench (Study1)

    ![Study1 workbench](assets/study1-workbench.png)

- [ ] Choose Python Notebook

    ![Jupyter notebook icon](assets/jupyter-notebook-icon.png)

- [ ] Write some code, rename the file, create and move cells, experiment with code

    ![Jupyter Code example](assets/jupyter-code-example.png)

**Lab Completed**
