
## Setup

### 1. Clone the repository

Run the following command to clone the repo:
`git clone https://github.com/Fortuz/rl_education.git`

### 2. Install Docker

- **Windows, Mac**: You can install Docker from this link: https://www.docker.com/products/docker-desktop/
- **Linux**: Use your distro's package manager. On Arch, you need to install the `docker` and `docker-desktop`<sup>AUR</sup> packages.
  
### 3. Build the image

Navigate to the project root directory, and run `docker build . -t rl`

This command builds a new Docker image from the Dockerfile in this repo and names it `rl`.

### 4. Start the container

Navigate to the project root directory and run `docker run -p 8888:8888 --user ${uid}:${gid} --name rl -v ${PWD}:/home/jovyan/work/ -itd rl`

This starts a new conatiner based on the image built above, with the following options:
- `-p 8888:8888` connects the port `8888` of the container to the host machine
- `--user ${uid}:${gid}` sets the container user to the local user to avoid permission issues
- `--name rl` names the container `rl`
- `-v ${PWD}:/home/jovyan/work/` binds your local folder (the project root) to the container's folder
- `-itd` runs the container in the background

### 5. Start JupyterLab

Navigate to `localhost:8888` in your browser to start up JupyterLab.

## Starting the container after setup

To start the container, you have two options:

- **CLI**: Run `docker start rl` and navigate to `localhost:8888`
- **GUI**
  - Open the Docker Desktop app
  - Navigate to 'Containers' in the menu
  - Click on `rl`
  - Click the play button in the upper right corner
  - Navigate to `localhost:8888`