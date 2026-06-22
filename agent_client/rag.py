INSTRUCTIONS = '''
SYSTEM INSTRUCTIONS:
You are given a set of documents. Each document is delimited by
=== DOCUMENT START === and === DOCUMENT END ===.
Each document contains several attrubutes defined as ATTRIBUTE_NAME:ATTRIBUTE_VALUE.
Use only these documents to answer to find relevant information and provide accurate answers.
If the answer is not found in the context, respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()


class RAGBase:

    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        model='gpt-5.4-mini'
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.model = model

    def search(
            self,
            query,
            num_results=5,
            boost: dict[str, float] | None = None,
            filter: dict[str, float] | None = None
    ):
        """
        boost example:
            {
                'question': 3.0,
                'section': 0.5,
            }
        """
        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost,
            filter_dict=filter
        )

    def build_context(
            self,
            search_results,
            result_attributes: list[str] | None = None,
    ):
        """
        result_attributes example:
            [
                'filename',
                'content',
            ]
        """
        lines = []

        for doc in search_results:
            lines.append('=== DOCUMENT START ===')
            for attr_name in result_attributes:
                lines.append(f'{attr_name.upper()}:')
                lines.append(f'{doc.get(attr_name, "N/A")}')
            lines.append('=== DOCUMENT END ===')
            lines.append('')

        return '\n'.join(lines).strip()

    def build_prompt(
            self,
            query,
            search_results,
            result_attributes: list[str] | None = None
    ):
        context = self.build_context(search_results, result_attributes=result_attributes)
        return self.prompt_template.format(
            question=query, context=context
        )

    def llm(self, prompt):
        input_messages = [
            {'role': 'developer', 'content': self.instructions},
            {'role': 'user', 'content': prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages
        )

        return response

    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results, result_attributes=['filename', 'content'])
        answer = self.llm(prompt)
        return answer
