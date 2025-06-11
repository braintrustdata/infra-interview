resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-key"
  public_key = ""
}

resource "aws_security_group" "ssh_access" {
  name        = "${var.project_name}-ssh-sg"
  description = "Security group for SSH access"
  vpc_id      = data.aws_vpc.interview_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "server" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  subnet_id                   = data.aws_subnets.subnets.ids[0]
  associate_public_ip_address = true

  vpc_security_group_ids = []
  key_name               = aws_key_pair.deployer.key_name

  root_block_device {
    volume_type           = "gp3"
    volume_size           = 20
    delete_on_termination = true
    encrypted             = true

    tags = {
      Name    = "${var.project_name}-root-volume"
      Project = var.project_name
    }
  }

  # User data script
  user_data = base64encode(local.user_data)

  tags = {
    Name    = "${var.project_name}-web-server"
    Project = var.project_name
    Type    = "interview-instance"
  }
}

locals {
  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y htop curl wget
  EOF

  vpc_id = "vpc-0687fb9b947f706d2"
}

data "aws_vpc" "interview_vpc" {
  filter {
    name   = "tag:Name"
    values = ["interview-vpc"]
  }
}

data "aws_subnets" "subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.interview_vpc.id]
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

