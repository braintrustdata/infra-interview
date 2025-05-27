variable "my_ip" {
  description = "Your public IP address for SSH access (CIDR format, e.g., 192.168.1.100/32)"
  type        = string
  default     = "0.0.0.0/0" # WARNING: This allows SSH from anywhere - should be restricted!
}

variable "project_name" {
  description = "Name of the project for resource tagging"
  type        = string
  default     = ""
  validation {
    condition     = length(var.project_name) > 0
    error_message = "Project name cannot be empty"
  }
}

output "instance_public_ip" {
  value = aws_instance.server.public_ip
}
