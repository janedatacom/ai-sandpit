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

### 1) Log in to OpenShift

- [ ] Open the OpenShift console in your browser.

![OpenShift console landing page](image-1.png)

- [ ] Sign in with your provided credentials.

![Login prompt](image-6.png)
![Post-login landing view](image-3.png)

---

### 2) Take the guided tour (Developer Console)

When prompted, click **Get started** to begin the tour.

- [ ] Start the tour.

![Tour prompt](image-7.png)
![Tour step](image-8.png)

- [ ] Click **Next** through the tour screens.
- [ ] Pay attention to the different **Perspectives** (Administrator vs Developer).

![Perspectives](image-9.png)

Along the way you’ll see where to:

- Find metrics about application performance

![Metrics](image-10.png)

- Search and list resources in your project

![Search resources](image-11.png)

- Use either the UI or CLI to create resources (pods/projects/workspaces)

![UI or CLI options](image-12.png)

- Access help and documentation

![Help menu](image-13.png)

- Configure user preferences (views/language/import settings)

![User preferences](image-14.png)

- [ ] Finish the tour (e.g., **Okay, got it**).

---

### 3) Create your project and pod (via CLI)

Open the built-in terminal:

- [ ] Click the `>_` icon (top-right) to open the **Command Line Interface**.

![Open CLI](image-15.png)

At the bottom of the screen you should see a terminal area.

![CLI terminal](image-16.png)

This is where you run `oc` commands to create and manage resources.

- [ ] Select the correct **Project** from the dropdown.

![Project dropdown](image-17.png)

- [ ] Click **Start**.

![Start terminal](image-18.png)

If you see an error about permissions, you may not have rights to create resources.

![Permission error](image-19.png)

> If you hit this error: ask your administrator/facilitator to grant access or provide a pre-created project for you.

---

### 4) Create your Jupyter workspace

- [ ] Create your workspace using an image that includes Jupyter Notebooks.

> Facilitator note: Add the exact steps for your environment here (OpenShift AI / Workbenches / image name / size limits / project naming conventions).

---

### 5) Explore Jupyter Notebooks

- [ ] Launch Jupyter.
- [ ] Create a notebook.
- [ ] Run a first Python cell.

![Jupyter / notebook example](image.png)

---

## Save your work

- [ ] Save your notes in this folder (or a file like `my-notes.md`).

## Deliverables

- Notes or screenshots showing you successfully logged in and accessed the CLI terminal
- (Optional) Evidence of a running Jupyter workspace/notebook
