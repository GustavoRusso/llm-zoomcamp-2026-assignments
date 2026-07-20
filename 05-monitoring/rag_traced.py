from opentelemetry import trace
from rag_helper_hw5 import RAGBaseHw5

class RAGTraced(RAGBaseHw5):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracer = trace.get_tracer("llm-zoomcamp")

    def search(self, query, num_results=5):
        with self.tracer.start_as_current_span("search") as span:
            span.set_attribute("query", query)
            span.set_attribute("num_results", num_results)
            return super().search(
                query,
                num_results=num_results
            )

    def llm(self, prompt):
        with self.tracer.start_as_current_span("llm") as span:
            span.set_attribute("prompt", prompt)
            return super().llm(prompt)

    def rag(self, query):
        with self.tracer.start_as_current_span("rag") as span:
            span.set_attribute("query", query)
            return super().rag(query)
