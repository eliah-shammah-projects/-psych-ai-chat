resource "aws_ecr_repository" "app" {
  name                 = "psych-ai-chat"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
