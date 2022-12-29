# Restarting Pods Report

This is a Python script that uses the [Kubernetes Python client](https://github.com/kubernetes-client/python) to list the pods that restarted on a given period of time.

## Installation

Run:

`$ make setup`

To install virtualenv and

`$ make install`

To install all dependencies.

This will create a `restpods` file with the path to the pyton file and place it at your home directory. You can add it to your $PATH running:

`$ export PATH="${PATH}:${HOME}/bin`


## Listing your cluster restarting pods

By default, it will list the pods that restarted on all namespaces for the last two days.

`$ restpods`

```
    Listing pods with restarting containers on all namespaces
    Report duration: 2 days.

    POD                                                             CONTAINER                           NAMESPACE                           RESTARTS    READY   LAST TERMINATION
    tools-5dds67b228-r6cp6                                          dnsutils                            default                             11003       False   2022/12/12, 17:12:58 [44 seconds ago]
    xpto-app-6c44d97997-gx5qf                                       xpto-app                            xpto-namespace                      1           True    2022/12/11, 00:28:42 [1 day ago]
    api-xpto-6d9c49db58-tqzsh                                       api-xpto                            xpto-namespace                      5           True    2022/12/12, 16:35:31 [38 minutes ago]
    my-xpto-application-dd4575ko5-44k5g                             my-xpto-application                 xpto-namespace                      1           True    2022/12/12, 10:10:48 [7 hours ago]
    my-xpto-application-dd4575ko5-5jv7g                             my-xpto-application                 xpto-namespace                      122         True    2022/12/12, 10:10:52 [7 hours ago]
    my-xpto-application-dd4575ko5-6h74m                             my-xpto-application                 xpto-namespace                      125         True    2022/12/12, 09:45:49 [7 hours ago]
    my-xpto-application-dd4575ko5-jkdhm                             my-xpto-application                 xpto-namespace                      100         True    2022/12/12, 09:45:48 [7 hours ago]
    my-xpto-application-dd4575ko5-qsrr5                             my-xpto-application                 xpto-namespace                      109         True    2022/12/12, 13:31:59 [3 hours ago]
    ingress-648958bc57-9clc8                                        proxy                               foo-system                          1           True    2022/12/12, 10:09:19 [7 hours ago]
    ingress-648958bc57-cjtfz                                        ingress-controller                  foo-system                          2           True    2022/12/12, 09:54:15 [7 hours ago]
    ingress-648958bc57-xcjgs                                        ingress-controller                  foo-system                          2           True    2022/12/12, 09:52:55 [7 hours ago]
    bar-api-7cfc5bf69d-98fvp                                        bar-api                             squad-bar                           16          True    2022/12/12, 08:07:49 [9 hours ago]
    bar-api-7cfc5bf69d-chzdr                                        bar-api                             squad-bar                           5           True    2022/12/12, 10:16:30 [6 hours ago]
    bar-api-7cfc5bf69d-vpxl9                                        bar-api                             squad-bar                           7           True    2022/12/11, 16:50:13 [1 day ago]

    [WARNING] Pod xpto-bar-api-74ujh4d8768-7t5m2 state is Pending
    [WARNING] Pod xpto-bar-api-74ujh4d8768-cx6p2 state is Pending
    [WARNING] Pod xpto-bar-api-74ujh4d8768-zclh2 state is Pending
    [WARNING] Pod cron-foo-bar-xpto-1670860800-3523852471 state is Failed

    Found 5 containers not running
```

## List restarting pods from a single namespace

You can list the restarting pods from a single namespace by passing the namespace as an argument

`$ restpods [namespace]`

```
    Listing pods with restarting containers on xpto-namespace namespaces
    Report duration: 2 days.

    POD                                                             CONTAINER                           NAMESPACE                           RESTARTS    READY   LAST TERMINATION
    xpto-app-6c44d97997-gx5qf                                       xpto-app                            xpto-namespace                      1           True    2022/12/11, 00:28:42 [1 day ago]
    xpto-api-6d9c49db58-tqzsh                                       xpto-api                            xpto-namespace                      5           True    2022/12/12, 16:35:31 [38 minutes ago]
    my-xpto-application-dd4575ko5-44k5g                             my-xpto-application                 xpto-namespace                      1           True    2022/12/12, 10:10:48 [7 hours ago]
    my-xpto-application-dd4575ko5-5jv7g                             my-xpto-application                 xpto-namespace                      122         True    2022/12/12, 10:10:52 [7 hours ago]
    my-xpto-application-dd4575ko5-6h74m                             my-xpto-application                 xpto-namespace                      125         True    2022/12/12, 09:45:49 [7 hours ago]
    my-xpto-application-dd4575ko5-jkdhm                             my-xpto-application                 xpto-namespace                      100         True    2022/12/12, 09:45:48 [7 hours ago]
    my-xpto-application-dd4575ko5-qsrr5                             my-xpto-application                 xpto-namespace                      109         True    2022/12/12, 13:31:59 [3 hours ago]

    [WARNING] Pod xpto-bar-api-74ujh4d8768-7t5m2 state is Pending
    [WARNING] Pod xpto-bar-api-74ujh4d8768-cx6p2 state is Pending
    [WARNING] Pod xpto-bar-api-74ujh4d8768-zclh2 state is Pending

    Found 0 containers not running
```

## Listing your cluster restarting pods for a longer period of time

You can extend the report period using the `<-p | --period>` flag

`$ restpods -p <days>`

```
    Report duration: 5 days.

    POD                                                             CONTAINER                           NAMESPACE                           RESTARTS    READY   LAST TERMINATION
    xpto-app-6c44d97997-gx5qf                                       xpto-app                            xpto-namespace                      1           True    2022/12/26, 02:43:31 [2 days ago]
    xpto-api-6d9c49db58-tqzsh                                       xpto-api                            xpto-namespace                       5           False   2022/12/28, 20:13:18 [29 minutes ago]
    my-xpto-application-dd4575ko5-44k5g                             my-xpto-application                 xpto-namespace                      1           True    2022/12/25, 10:58:14 [3 days ago]
    my-xpto-application-dd4575ko5-5jv7g                             my-xpto-application                 xpto-namespace                      122         True    2022/12/25, 06:09:02 [3 days ago]
    my-xpto-application-dd4575ko5-6h74m                             my-xpto-application                 xpto-namespace                      125         True    2022/12/23, 06:09:08 [5 days ago]
    my-xpto-application-dd4575ko5-jkdhm                             my-xpto-application                 xpto-namespace                      100         True    2022/12/24, 06:09:13 [4 days ago]
    my-xpto-application-dd4575ko5-qsrr5                             my-xpto-application                 xpto-namespace                      109         True    2022/12/26, 06:09:10 [2 days ago]

    [WARNING] Pod xpto-bar-api-74ujh4d8768-7t5m2 state is Pending
    [WARNING] Pod xpto-bar-api-74ujh4d8768-cx6p2 state is Pending
    [WARNING] Pod xpto-bar-api-74ujh4d8768-zclh2 state is Pending

    Found 0 containers not running
```

## Exporting report

You can export your restarting pods report to a `.csv` file by adding the `-e | --export` flag.
It will generate a file like `<date>_restarting_pods_report.csv` with the following columns:

* Pod name
* Container
* Namespace
* Restart count
* Terminated at
* Reason
