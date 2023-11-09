# PDF-splitter - extract pages from a PDF document

PDF-splitter is a user-friendly GUI tool designed to extract pages from a PDF document. GUI part was done via Qt, so (in theory) it should work on all systems

Originally developed as a project for the SCS (Specialized Computer Systems) course, it continues to receive occasional updates.

![Dashboard with a document loaded](https://i.imgur.com/8xZYAGX.png)

## 1. Dependencies

Pip packages that this tool uses aren't required to be installed; that will be handled during the build process inside a virtual environment.

-   `python`
-   `qt5-base` (or whatever the Qt's base package is called for your distro)
-   `patchelf` (required when building the binary)

## 2. Install

Binary `pdf-splitter` will be located at `~/.local/bin/`

```sh
git clone https://github.com/tunalad/pdf-splitter.git
cd pdf-splitter
make install
```
