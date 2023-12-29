# K8S App Bootstrap

Simple init container to bootstrap any application data in k8s by storing a simple `tar.gz` archive in selfhosted [filebrowser](https://github.com/filebrowser/filebrowser).

## ENV Vars

### Required

- `FILEBROWSER_URL` (str): filebrowser url
- `FILEBROWSER_USER` (str): filebrowser user
- `FILEBROWSER_PASSWORD` (str): filebrowser password
- `NAME` (str): data bootstrap archive name without `.tar.gz` extension

### Optional

- `STRIP_ARCHIVE_ROOT` (bool): strip the top level directory inside the archive (default is `true`)
- `DESTINATION` (str): destination path where to extract the data (default is `/init`)
- `FILEBROWSER_DIR` (str): filebowser directory where the archives are located (default is `bootstrap`)

## Build

### Nix

```bash
nix build '.#dockerImage'
docker load < result
docker run -it k8s-app-bootstrap:$HASH
```

For `$HASH` see `docker images` output.

**NOTE: The nix build container is broken. The `os.system` instructions do not work inside the container?! For now we use a standard Dockerfile to build the container**
