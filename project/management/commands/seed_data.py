from django.core.management.base import BaseCommand
from project.models import Project


class Command(BaseCommand):
    help = "Seed database with sample projects"

    def handle(self, *args, **options):
        Project.objects.all().delete()

        projects = [
            {
                "title": "Distributed Payment System",
                "category": "Web Development",
                "short_summary": "High-throughput payment processing engine handling millions of transactions with 99.99% uptime.",
                "role": "Lead Backend Engineer",
                "year": 2024,
                "stack": "GOLANG KAFKA REDIS",
                "repository": "https://github.com/example/payment-system",
                "challenge": "The previous monolithic architecture struggled to handle peak loads during holiday sales, resulting in transaction failures and latency spikes. We needed a system capable of processing 50k TPS with strict consistency guarantees.",
                "key_features": "Idempotent transaction processing\nEvent-driven architecture\nAutomated reconciliation\nReal-time fraud detection",
                "description": "We chose Go for its high concurrency capabilities and low memory footprint. The core payment engine was designed as a set of microservices communicating via Kafka topics, ensuring loose coupling and high availability.\n\nTo ensure data consistency across distributed services, we implemented the Saga Pattern. Each step of the payment process (validation, authorization, ledger update) publishes an event. If any step fails, compensating transactions are triggered to roll back changes.",
                "image": None,
            },
            {
                "title": "Cloud Migration API",
                "category": "System Desingn",
                "short_summary": "Automated migration toolset for legacy databases to cloud-native managed services.",
                "role": "Cloud Architect",
                "year": 2023,
                "stack": "PYTHON AWS TERRAFORM",
                "repository": "",
                "challenge": "Legacy on-premise databases needed migration to cloud with zero downtime and data integrity guarantees. The challenge was handling 10TB+ of data across multiple databases.",
                "key_features": "Zero-downtime migration\nData validation pipeline\nRollback capabilities\nProgress monitoring dashboard",
                "description": "Built a comprehensive migration framework using Python that orchestrates the entire migration process. The system uses AWS DMS for continuous replication while validating data integrity at each step.\n\nImplemented infrastructure as code with Terraform to provision cloud resources consistently. Created automated testing suite to verify data consistency post-migration.",
                "image": None,
            },
            {
                "title": "Real-time Analytics Engine",
                "category": "System Desingn",
                "short_summary": "Stream processing pipeline for analyzing user behavior in real-time.",
                "role": "Senior Backend Engineer",
                "year": 2023,
                "stack": "RUST FLINK CLICKHOUSE",
                "repository": "https://github.com/example/analytics-engine",
                "challenge": "Need to process billions of events daily with sub-second latency for real-time dashboards and alerting. Traditional batch processing was too slow for business requirements.",
                "key_features": "Stream processing with Apache Flink\nSub-second query latency\nCustom aggregation functions\nReal-time alerting system",
                "description": "Designed and implemented a real-time analytics pipeline using Apache Flink for stream processing. Events are ingested from Kafka, processed in-memory, and stored in ClickHouse for analytical queries.\n\nOptimized query performance by implementing materialized views and pre-aggregations. The system handles 100k+ events per second with p99 latency under 500ms.",
                "image": None,
            },
        ]

        for project_data in projects:
            Project.objects.create(**project_data)
            self.stdout.write(
                self.style.SUCCESS(f"Created project: {project_data['title']}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nSuccessfully seeded {len(projects)} projects")
        )
