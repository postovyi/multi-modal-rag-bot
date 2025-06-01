import pytest
from deepeval.test_case import LLMTestCase
from langsmith import Client

client = Client()


@pytest.fixture(scope='module')
def llm_test_cases() -> list[LLMTestCase]:
    examples = list(client.list_examples(dataset_name='softserve-test-v2'))
    test_cases = []
    for e in examples:
        test_cases.append(
            LLMTestCase(
                input=e.inputs['messages'][0]['content'],
                actual_output=e.outputs['messages'][0]['content'],
                context=[d['page_content'] for d in e.outputs['relevant_docs']],
                retrieval_context=[d['page_content'] for d in e.outputs['relevant_docs']],
            )
        )
        break  # can be deleted if you want to run all the examples
    return test_cases
