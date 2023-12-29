# K8S App Bootstrap

## Build

### Nix

```bash
nix build '.#dockerImage'
docker load < result
docker run -it k8s-app-bootstrap:$HASH
```

For `$HASH` see `docker images` output.

**NOTE: The nix build container is broken. The `os.system` instructions do not work inside the container?! For now we use a standard Dockerfile to build the container**


