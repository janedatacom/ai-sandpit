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

- [ ] Finish the tour (e.g., **Okay, got it**).

  ![Create a pod (overview)](image-38.png)

### 3) Create your project and pod (via GUI or CLI)
**GUI option**

- [ ] Go to **Administrator** perspective.
  ![Switch to Administrator perspective](image-21.png)

- [ ] Go to **Workloads** → **Pods**.
  ![Navigate to Workloads > Pods](image-22.png)

- [ ] Click **Create Pod**.
  ![Create Pod button](image-23.png)

- [ ] Review (and optionally edit) the YAML that is shown.
  ![Pod YAML editor](image-24.png)

- [ ] Give the pod a name like `student1pod` (use your student number).
  ![Pod name field](image-26.png)

- [ ] Review the right-hand schema/help panel (optional).
- [ ] Click **Create**.
  ![Create pod confirmation](image-27.png)

- [ ] Wait for the pod to be created.
  ![Pod status after create](image-28.png)

- [ ] Confirm the status changes from **Pending/ContainerCreating** to **Running**.

**CLI option**

Open the built-in terminal:

- [ ] Click the `>_` icon (top-right) to open the **Command Line Interface**.

  ![Open the built-in web terminal](image-15.png)

At the bottom of the screen you should see a terminal area.

![CLI terminal](image-16.png)

This is where you run `oc` commands to create and manage resources.

Run a few basic commands (replace `1` with your student number):

```bash
oc whoami
oc project

# Create (or switch to) your project/namespace
oc new-project student1

# Create a simple pod
oc run student1pod --image=registry.access.redhat.com/ubi9/ubi --restart=Never

# Check status
oc get pods
```

Tip: the exact pod command is also in `oc-commands` in this folder.

> If you see a **forbidden** or permissions error: ask your facilitator/admin to grant access or provide a pre-created project for you.

---

### 4) Create your Jupyter workspace

- [ ] Create your workspace using an image that includes Jupyter Notebooks.

> Facilitator note: Add the exact steps for your environment here (OpenShift AI / Workbenches / image name / size limits / project naming conventions).

---

### 5) Explore Jupyter Notebooks

- [ ] Launch Jupyter.
- [ ] Create a notebook.
- [ ] Run a first Python cell.



---

## Save your work

- [ ] Save your notes in this folder (or a file like `my-notes.md`).

## Deliverables

- Notes or screenshots showing you successfully logged in and accessed the CLI terminal
- (Optional) Evidence of a running Jupyter workspace/notebook
