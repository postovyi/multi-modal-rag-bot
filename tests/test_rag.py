from deepeval import assert_test
from deepeval.metrics import ContextualRelevancyMetric, FaithfulnessMetric


def test_all_cases_for_contextual_relevancy(llm_test_cases) -> None:
    contextual_relevancy_metric = ContextualRelevancyMetric(threshold=0.65, model='gpt-4.1-nano')
    for test_case in llm_test_cases:
        assert_test(test_case, [contextual_relevancy_metric])


def test_all_cases_for_faithfulness(llm_test_cases) -> None:
    faithfulness_metric = FaithfulnessMetric(threshold=0.75)
    for test_case in llm_test_cases:
        assert_test(test_case, [faithfulness_metric])
