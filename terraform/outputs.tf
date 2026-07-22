output "ec2_ip" {
  description = "IP público fixo do EC2"
  value       = aws_eip.app.public_ip
}

output "ecr_url" {
  description = "URL do repositório ECR"
  value       = aws_ecr_repository.app.repository_url
}
