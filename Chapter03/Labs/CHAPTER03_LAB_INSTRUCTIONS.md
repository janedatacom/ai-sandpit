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

![Lab Overview](image-29.png)

### 1) Log in to OpenShift

- [ ] Open the OpenShift console in your browser.

- [ ] Sign in with your provided credentials to the Axis Portal (Datacom Training) or other portal (Customer Training), then choose **AI Lab - OpenShift Console (Web)**.

    ![Axis Portal: OpenShift Console link](image-20.png)

- [ ] Sign in with your provided credentials to AI Lab - OpenShift Console (Web).

    ![OpenShift landing page after login](image-3.png)

---

### 2) Take the guided tour (Developer Console)

![Step 2 Powerpoint page](image-7.png)

When prompted, click **Get started** to begin the tour.

- [ ] Start the tour and click through the next few pop-up screens.

    ![Start guided tour prompt](image-30.png)

- [ ] Click **Next** through the tour screens.
- [ ] Pay attention to the different **Perspectives** (Administrator vs Developer).

    ![Perspective switcher (Administrator/Developer)](image-31.png)

Along the way you’ll see:
- Where to find metrics about application performance.

    ![Observe](image-32.png)
- How to search and list resources in your project.

    ![Search for resources in your project](image-33.png)
- How to use command line tools (CLI) to create and check on resources.

    ![Web Terminal](image-34.png)
- Where to get help for quick starts, restarting the tour, deploying applications, etc.

    ![Help page](image-35.png)
- Where to set up your preferences (default views, colour, etc.).

    ![You're ready to go](image-37.png)

- [ ] Finish the tour (**Okay, got it**).

    ![Create a pod (overview)](image-38.png)

### 3) Create your project (via GUI or CLI)
![Step 3 Powerpoint page](image-49.png)

**GUI option**

- [ ] Go to **Developer** perspective.

    ![Developer perspective and choose Topology](image-42.png)

- [ ] Create a **Project**, enter name, display name and description and click Create

    ![Enter the name, display name and description](image-43.png)

- [ ] Your project has been created

    ![You Project is created](image-44.png)

**CLI option**
- [ ] You can also create a project via the Command Line Interface (CLI). 
      Start with the CLI Button from the top left menu.

    ![top menu with command line](image-47.png)
    ![CLI Prompt](image-48.png)

- [ ] Type the ```oc new-project``` command in the CLI and hit enter

    ![cli command](image-46.png)

    ```bash
    oc new-project ai-students \
    --display-name="AI Training – Students" \
    --description="Projects for student notebooks and AI experiments"
    ```

- [ ] Review your project here in Developer Prespective --> Project.

    ![Project view from menu](image-50.png)

- [ ] See your project information and metrics

    ![Project Screen](image-51.png)

### 4) Create a Workbench with a Jupyter Image

![Step 5 powerpoint](image-53.png)

- [ ] Give the workbench a name like `Study1`, provide a description and choose and image 
    ![Pod name field](image-54.png)

- [ ] Image Options - choose one with Jupyter, Data Science for eg.

    ![Workbench image](image-55.png)

- [ ] You can also choose the version of python

    ![Version of Python](image-58.png)

- [ ] Leave everything else as default - deployment size, accelerator

    ![Deployment size](image-56.png)

- [ ] Environment variables, cluster storage and connections

    ![Then Enviro vars, cluster and connections](image-57.png)

- [ ] Click **Create Workbench**.

    ![Create workbench button](image-59.png)

- [ ] Wait for the project to be created.

    ![Pod status after create](image-28.png)

- [ ] Your project is not created and listed.

    ![new project listed](image-60.png)

### 5) Explore Jupyter Notebooks

![Step 5 - powerpoint slide](image-61.png)

- [ ] From your previous step 4, choose the Project Workbench

    ![Project workbench](image-62.png)

- [ ] and click on the Workbench (Study1)

    ![Study1 workbench](image-63.png)

- [ ] Choose Python Notebook

    ![Jupyter notebook icon](image-64.png)

- [ ] Write some code, rename the file, create and move cells, experiment with code

    ![Jupyter Code example](image-65.png)

**Lab Completed**
