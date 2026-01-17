# Zefiro Backups

![image](logo.png)

[Zefiro](https://zefiro.me) is a cloud storage provider that, in addition to offering plans to end users, also provides its service to some internet service providers such as Movistar or O2, allowing them to offer it free of charge to their customers when they subscribe to an internet plan.

The main goal of Zefiro Backups is to help you create local backups of the files you have stored in this cloud storage service. However, Zefiro’s user interface makes file organization somewhat complex, so this container also helps you with that task.

Although Zefiro provides folders and albums to organize your photos, videos, and other files, organizing photos and videos can sometimes be difficult because when they are uploaded from the mobile app, everything appears together in a single timeline. This makes it hard to know which items have already been organized into a folder or album.

To solve this, Zefiro Backups proposes creating two folders that the container will work with:

Folder 1: Zefiro Backups will automatically move all multimedia content uploaded from the mobile app into this folder, so you can then review it and move it to the folder you consider appropriate.

Folder 2: This folder will contain the rest of the folders where you will organize all your already reviewed content. It will be treated as the root directory from which local backups are created.

## Your docker-compose.yml

| Var      | Description |
| -------- | ------- |
| PROVIDER_DOMAIN  | Zefiro / Your ISP's domain    |
| EMAIL | your account email     |
| PASSWORD    | your account password    |
| BACKUPS_FOLDER_ID | ID of the root folder to take backups from |
| UNCATEGORIZED_FOLDER_ID | ID of the folder to automatically move all the content uploaded from apps |
| BACKUP_CRON | cronjob expression to schedule your backups |
| UNCATEGORIZED_CRON | cronjob expression to automatically move app uploaded content to UNCATEGORIZED_FOLDER_ID |

Available provider domains:

| Service | Domain |
|---------|--------|
| Zefiro | zefiro.me |
| Movistar (Spain) | micloud.movistar.es |
| O2 (Spain) | cloud.o2online.es |

## How to get a folder's ID?

Login on your ISP or Zefiro storage service from computer and open your browser's developers tools.
Look for the request to /sapi/media/folder?action=get&validationkey=xxxxx
Check the JSON object on the Preview Tab
