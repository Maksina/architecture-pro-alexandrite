# services/service-b/app.py
import os
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

resource = Resource(attributes={"service.name": "service-b"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
span_processor = BatchSpanProcessor(exporter)
provider.add_span_processor(span_processor)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/test")
def test():
    return {"test_field1": 1, "test_field2": 2}