# Chapter 04 — Lab 2: Set up a Policy (Governance + Multi-tenancy)

[Back to all lab instructions](../../LAB_INSTRUCTIONS.md)

**Duration**: ~15 minutes (hands-on)

## Goal

Apply practical guardrails to a shared OpenShift project so workloads are safer and resource usage is controlled (a foundation for multi-tenancy).

This lab uses two common “policy” controls:

1) **ResourceQuota** — caps total usage in a namespace
2) **LimitRange** — enforces defaults/maximums per Pod/Container

## Learning outcomes

By the end of this lab you can:

- Apply a ResourceQuota and LimitRange to a namespace
- Explain how quotas/limits support multi-tenancy
- Validate the policy by attempting to exceed limits

## Prerequisites

| Item | Notes |
|---|---|
| OpenShift access | Cluster URL + credentials |
| Permissions | Ability to create/modify objects in the project (edit/admin) |
| Target project | A project/namespace you control |

---

## Lab steps

### 1) Choose your target project

```bash
oc project <project>
```

---

### 2) Apply a ResourceQuota

Create a quota that caps total pods and total requested CPU/memory.

```bash
oc apply -n <project> -f - <<'YAML'
apiVersion: v1
kind: ResourceQuota
metadata:
  name: training-quota
spec:
  hard:
    pods: "10"
    requests.cpu: "2"
    requests.memory: 4Gi
    limits.cpu: "4"
    limits.memory: 8Gi
YAML
```

Check it:

```bash
oc describe resourcequota training-quota -n <project>
```

---

### 3) Apply a LimitRange

This enforces default requests/limits so “noisy neighbor” workloads are less likely.

```bash
oc apply -n <project> -f - <<'YAML'
apiVersion: v1
kind: LimitRange
metadata:
  name: training-limits
spec:
  limits:
  - type: Container
    defaultRequest:
      cpu: 100m
      memory: 256Mi
    default:
      cpu: 500m
      memory: 512Mi
    max:
      cpu: "1"
      memory: 1Gi
YAML
```

Check it:

```bash
oc describe limitrange training-limits -n <project>
```

---

### 4) Validate the policy

- [ ] Create a small test pod/deployment without specifying resources and observe defaults.
- [ ] Try to create a container that exceeds the `max` limit and observe the error.

Example (intentionally too large):

```bash
oc apply -n <project> -f - <<'YAML'
apiVersion: v1
kind: Pod
metadata:
  name: too-big
spec:
  containers:
  - name: app
    image: registry.access.redhat.com/ubi9/ubi-minimal
    command: ["sleep", "3600"]
    resources:
      limits:
        cpu: "2"
        memory: 2Gi
YAML
```

You should see an admission error about exceeding the LimitRange max.

---

### 5) (Optional) Discuss what “policy” means here

Prompt questions:

- [ ] Which policy is about *fairness* (multi-tenancy) vs *safety*?
- [ ] How would you choose sane defaults for notebooks vs services?
- [ ] Where would you insist on human approval (change control) for policy changes?

**Lab completed**
