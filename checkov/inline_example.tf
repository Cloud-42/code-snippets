data "aws_ec2_managed_prefix_list" "legacy" {
  name = "legacy"
}

data "aws_vpc" "legacy_dev_vpc" {
  filter {
    name   = "tag:Name"
    values = ["legacy-dev"]
  }
}

resource "aws_security_group" "this" {
  # checkov:skip=CKV_AWS_23: Description are added via for loop
  # checkov:skip=CKV2_AWS_5: TODO : remove once attached
  name        = "this-sg"
  description = "Security group for this"
  vpc_id      = data.aws_vpc.legacy_dev.id

  dynamic "ingress" {
    for_each = [
      { port = 80, desc = "HTTP Web Traffic" },
      { port = 135, desc = "RPC Endpoint Mapper" },
      { port = 139, desc = "NetBIOS Session Service" },
      { port = 445, desc = "SMB/CIFS File Sharing" },
      { port = 1801, desc = "Microsoft MSMQ" },
      { port = 2103, desc = "MSMQ RPC Endpoint" },
      { port = 2105, desc = "MSMQ Multicasting" },
      { port = 2107, desc = "MSMQ Replication" },
      { port = 3389, desc = "Windows Remote Desktop Protocol (RDP)" },
      { port = 47001, desc = "Windows Remote Management HTTP" }
    ]
    content {
      from_port       = ingress.value.port
      to_port         = ingress.value.port
      protocol        = "tcp"
      prefix_list_ids = [data.aws_ec2_managed_prefix_list.legacy.id]
      description     = ingress.value.desc
    }
  }

  # High ports TCP
  ingress {
    from_port       = 49152
    to_port         = 65535
    protocol        = "tcp"
    prefix_list_ids = [data.aws_ec2_managed_prefix_list.legacy.id]
    description     = "TCP High ports"
  }

  # High ports UDP
  ingress {
    from_port       = 49152
    to_port         = 65535
    protocol        = "udp"
    prefix_list_ids = [data.aws_ec2_managed_prefix_list.legacy.id]
    description     = "UDP High ports"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name      = "this"
    ManagedBy = "Terraform"
  }
}
