import asyncio
import aiohttp
import os
import time

from filebrowser_client import FilebrowserClient

def main():
    url = os.getenv("FILEBROWSER_URL", None)
    user = os.getenv("FILEBROWSER_USER", "admin")
    password = os.getenv("FILEBROWSER_PASSWORD", None)
    name = os.getenv("NAME", None)
    strip = os.getenv("STRIP_ARCHIVE_ROOT", True)
    dest = os.getenv("DESTINATION", "/init")
    filebrowserDir = os.getenv("FILEBROWSER_DIR", "bootstrap")

    if name is None:
        raise ValueError("env var NAME not defined")
    
    if url is None:
        raise ValueError("env var FILEBROWSER_URL not defined")
    
    if password is None:
        raise ValueError("env var FILEBROWSER_PASSWORD not defined")
    
    bootstrapArchive = name + ".tar.gz" 

    if os.path.exists(bootstrapArchive):
        os.remove(bootstrapArchive)      
        
    client = FilebrowserClient(url, user, password, insecure=True)

    try:
        asyncio.run(client.connect())
    except aiohttp.client_exceptions.ClientConnectorError:
        print(f"connection to {url} failed, wait 60 seconds...")
        time.sleep(60)
        asyncio.run(client.connect())
            
    try:
        print(f"download {bootstrapArchive}...")
        asyncio.run(client.download(".", f"/{filebrowserDir}/{bootstrapArchive}"))
    except aiohttp.client_exceptions.ClientResponseError:
        print(f"bootstrap archive /{filebrowserDir}/{bootstrapArchive} not exist") 
        return

    os.system(f"echo ensure {dest} exists")
    os.system(f"mkdir -p {dest}")
    os.system(f"rm -rf " + dest + "/{*,.*}")
    if strip:
        os.system(f"tar -C {dest} -xvzf {bootstrapArchive} --strip-components=1")
    else:
        os.system(f"tar -C {dest} -xvzf {bootstrapArchive}")
    print("new directory structure:")
    os.system(f"ls {dest}")
    os.system(f"rm -f {bootstrapArchive}")
    
    print("bootstrap completed")


if __name__ == "__main__":
    main()
