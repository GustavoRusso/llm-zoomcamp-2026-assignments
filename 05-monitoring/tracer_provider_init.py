from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from sqlite_span_exporter import SQLiteSpanExporter

def setup_tracing():
    provider = TracerProvider()
    #provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    provider.add_span_processor(SimpleSpanProcessor(SQLiteSpanExporter("traces.db")))
    trace.set_tracer_provider(provider)
