# Monitor sensor data with Raspberry Pi and Grafana

![image](https://github.com/user-attachments/assets/81caee2b-63ae-47db-bdf5-9f90bc7c10e0)

In this project, we leverage a Python script to simulate sensor data. The data is exposed via an HTTP endpoint, which is then scraped by Prometheus. Prometheus collects these metrics and stores them in its time-series database, where they can be queried. Grafana is used to visualize this data, offering real-time dashboards to track sensor metrics like temperature, and humidity.

For the full step-by-step instructions including hardware and software requirements, Raspberry Pi sensor wiring, code explanation, and overview of the tech stack needed (Python, Prometheus, Docker), see this [blog post](https://grafana.com/blog/2023/10/23/monitor-temperature-and-humidity-with-grafana-and-raspberry-pi/). 

## How to use these files

Here is an overview of the steps that you need to take: 

- Install the requirements:
  - Git
  - Docker
  - Docker compose

- Set up the Grafana stack
- Monitor your data from Grafana

## Install the requirements

### [Git](https://git-scm.com/)

First, update your package list to ensure you get the latest version available.

```
sudo apt update
sudo apt upgrade -y
```

Install Git with a single command:

``` 
sudo apt install -y git build-essential vim starship python3-dev
```

To confirm Git is installed correctly, check the version:

``` 
git --version
```

### [Docker](https://docs.docker.com/install/) & [Docker compose](https://docs.docker.com/compose/)

Ensure **Docker** is already installed on your Raspberry Pi. If Docker is not installed, you can follow these instructions to install it:

``` bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

** Optional: add your user to the docker group (this lets you run Docker without `sudo`):

```
sudo usermod -aG docker $USER
```

Run the following commands to install the latest version of **Docker Compose**:

``` bash
sudo apt install -y libffi-dev libssl-dev
sudo apt install -y python3 python3-pip
sudo pip3 install docker-compose
```

> Note: Docker Compose requires these additional libraries to work properly, and Python 3, which will be used to run Docker Compose.

To confirm that Docker Compose was installed correctly, check the version:

```
docker compose version
```

## Set up the Grafana stack

Clone the tutorial environment repository.
```
git clone https://github.com/tonypowa/sensor-data-monitoring-grafana
```

Change to the directory where you cloned the repository:
```
cd sensor-data-monitoring-grafana
```

Run the Grafana stack:
```
docker compose build
```

Bring up the containers

```
docker compose up -d
```


The first time you run `docker compose up build`, and `docker compose up -d`,   Docker will rebuild the images and then bring up the containers. This might take a few minutes, depending on your internet connection.

>Note
If you already have Grafana, or Prometheus running on your system, you might see errors, because the Docker image is trying to use ports that your local installations are already using. If this is the case, stop the services, then run the command again.

## Monitor your temperature and humidity data from Grafana

- From your machine, access your Raspberry Pi by entering the IP address into the browser: `http://{you-raspberry-pi-IP-address}:3000`.
- You should be automatically logged in to Grafana
- Open the side menu.
- Click Explore.
- Select `Prometheus` from the dropdown menu at the top left corner.
- Click Metrics browser and select `current_temperature`. Select the metrics
- Click the **run query** button at the top right corner.
 You should see temperature data graphed.
- Repeat the above steps to explore `current_humidty`.

You made it! 

## Next steps

For inspiration or reference, import a sample dashboard built for this tutorial by entering its ID. In Grafana, go to **Home > Dashboards > Import**, enter the ID `22406`, and click **Load**. Feel free to adjust it to fit your needs.
