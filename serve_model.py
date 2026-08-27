import click
from rich import print
from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import MLFlowModelDeployer
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from zenml.client import Client

@click.command()
@click.option(
    "--stop-service",
    is_flag=True,
    default=False,
    help="Stop the prediction service when done",
)
def serve_latest_model(stop_service: bool):
    """Serves the latest model from the training pipeline."""
    model_name = "prices_predictor"
    pipeline_name = "ml_pipeline"
    step_name = "model_trainer"

    model_deployer = MLFlowModelDeployer.get_active_model_deployer()

    def stop_existing_services():
        existing_services = model_deployer.find_model_server(
            pipeline_name=pipeline_name,
            model_name=model_name,
            running=True,
        )
        for service in existing_services:
            print(f"Stopping service {service.uuid}...")
            service.stop(timeout=60)

    if stop_service:
        stop_existing_services()
        return

    # First, stop any existing services to avoid conflicts
    stop_existing_services()

    # Get the latest successful run of the training pipeline
    try:
        client = Client()
        pipeline_runs = client.list_pipeline_runs(
            pipeline_name=pipeline_name,
            sort_by="created",
            status="completed",
        )
        if not pipeline_runs.items:
            print("No completed training pipelines found. Please run the training pipeline first.")
            return

        latest_run = pipeline_runs.items[0]
        trained_model = latest_run.steps[step_name].output

        # Deploy the model from the latest run
        print(f"Deploying model from pipeline run: {latest_run.name}")
        model_deployer.deploy_model(
            config=trained_model,
            replace_existing=True,
            timeout=120,
            service_type=MLFlowDeploymentService.SERVICE_TYPE,
        )

        service = model_deployer.find_model_server(
            pipeline_name=pipeline_name,
            model_name=model_name,
            running=True,
        )[0]

        if service:
            print(
                f"Prediction server is running and accessible at: {service.prediction_url}"
            )
            print("To stop the server, run: python serve_model.py --stop-service")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    serve_latest_model()
