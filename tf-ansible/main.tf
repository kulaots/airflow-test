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
 
resource "docker_image" "ansible" {
  build {
    context = "."
}
 
resource "docker_container" "ansible" {
  image = docker_image.ansible.image_id
  name  = "ansible"
}
