terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}
 
provider "docker" {
  host    = "npipe:////.//pipe//podman-machine-default"
}
 
resource "docker_image" "ssh_and_python" {
  name         = "kulaots/ssh_and_python"
  keep_locally = false
}
 
resource "docker_container" "airflow" {
  image = docker_image.ssh_and_python.image_id
  name  = "airflow"
  ports {
    internal = 80
    external = 8080
  }
    ports {
    internal = 22
    external = 2222
    }
} 