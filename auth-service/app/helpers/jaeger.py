from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)

from settings import settings


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(
        resource=Resource.create({SERVICE_NAME: 'auth-service'})
    ))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.JAEGER_HOST,
                agent_port=settings.JAEGER_PORT,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter(service_name='auth-service')))


def configure_jaeger(app: Flask) -> None:
    if settings.JAEGER_ENABLE_TRACER:
        configure_tracer()
        FlaskInstrumentor().instrument_app(app)
