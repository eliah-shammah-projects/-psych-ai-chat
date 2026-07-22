# ── AMI: Ubuntu 24.04 LTS (latest) ───────────────────────────────────────────
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# ── IAM: permite EC2 fazer docker pull do ECR sem credenciais manuais ─────────
resource "aws_iam_role" "ec2_ecr" {
  name = "psych-ai-chat-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecr_read" {
  role       = aws_iam_role.ec2_ecr.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "ec2_ecr" {
  name = "psych-ai-chat-ec2-profile"
  role = aws_iam_role.ec2_ecr.name
}

# ── Security Group ────────────────────────────────────────────────────────────
resource "aws_security_group" "app" {
  name        = "psych-ai-chat-sg"
  description = "SSH + HTTP + app port"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "App"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ── EC2 ───────────────────────────────────────────────────────────────────────
resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  key_name               = "psych-ai-chat-key"
  vpc_security_group_ids = [aws_security_group.app.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_ecr.name

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io nginx

    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu

    # instala AWS CLI para autenticar no ECR
    apt-get install -y awscli

    # nginx: proxy reverso porta 80 → 5000
    cat > /etc/nginx/sites-available/default << 'NGINX'
    server {
        listen 80;
        location / {
            proxy_pass http://localhost:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
    NGINX

    systemctl restart nginx
    systemctl enable nginx
  EOF

  tags = {
    Name = "psych-ai-chat"
  }
}

# ── Elastic IP (IP fixo) ──────────────────────────────────────────────────────
resource "aws_eip" "app" {
  instance = aws_instance.app.id
  domain   = "vpc"
}
