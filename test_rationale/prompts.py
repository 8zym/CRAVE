LLM_rationale_true_old1 = """
Given the claim, with the relevant evidence: please provide a streamlined explanation associated with the claim and the evidence by using the contextual background and commonsense knowledge, to explicitly explain why the truth of the claim is reasoned as true.

Claim: %s
Evidence: %s
"""


LLM_rationale_false_old1 = """
Given the claim, with the relevant evidence: please provide a streamlined explanation associated with the claim and the evidence by using the contextual background and commonsense knowledge, to explicitly explain why the truth of the claim is reasoned as false.

Claim: %s
Evidence: %s
"""

LLM_rationale_true_old2 = """
Given the claim, with the relevant evidence: please provide a streamlined explanation associated with the claim and the evidence to explicitly explain why the truth of the claim is reasoned as true from the following aspects:
1) Evidence
2) Background
3) Commonsense knowledge
4) Other(Semantic, etc.)

Claim: %s
Evidence: %s
"""

LLM_rationale_false_old2 = """
Given the claim, with the relevant evidence: please provide a streamlined explanation associated with the claim and the evidence to explicitly explain why the truth of the claim is reasoned as false from the following aspects:
1) Evidence
2) Background
3) Commonsense knowledge
4) Other(Semantic, etc.)

Claim: %s
Evidence: %s
"""

LLM_rationale_true_old3 = """
Analyze why the following claim is true based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Semantic features and relationships
- Logical reasoning strictly from the evidence
- Linguistic patterns and connections

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_false_old3 = """
Analyze why the following claim is false based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Semantic features and relationships
- Logical reasoning strictly from the evidence
- Linguistic patterns and connections

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_true_old4 = """
Analyze why the following claim is true based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Semantic features and relationships
- Logical reasoning strictly from the evidence
- Linguistic patterns and connections

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_false_old4 = """
Analyze why the following claim is false based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Semantic features and relationships
- Logical reasoning strictly from the evidence
- Linguistic patterns and connections

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_true_old5 = """
Analyze why the following claim is true based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Logical reasoning strictly from the evidence
- Linguistic patterns and connections

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_false_old5 = """
Analyze why the following claim is false based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Logical reasoning strictly from the evidence
- Linguistic patterns and connections

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_true_old6 = """
Analyze why the following claim is true based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Semantic features and relationships
- Linguistic patterns and connections

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_false_old6 = """
Analyze why the following claim is false based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Semantic features and relationships
- Linguistic patterns and connections

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_true_old7 = """
Analyze why the following claim is true based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Semantic features and relationships
- Logical reasoning strictly from the evidence

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_false_old7 = """
Analyze why the following claim is false based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Semantic features and relationships
- Logical reasoning strictly from the evidence

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_true = """
Analyze why the following claim is true based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Semantic features and relationships
- Linguistic patterns and connections
- Logical reasoning strictly from the evidence

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_rationale_false = """
Analyze why the following claim is false based on the given evidence. Provide a clear and detailed explanation that focuses on:
- Direct evidence analysis
- Semantic features and relationships
- Linguistic patterns and connections
- Logical reasoning strictly from the evidence

### Input
Claim: %s
Evidence: %s

### Instructions
Directly provide your explanation without any preamble or conclusion. Only use information present in the evidence to support your analysis.
"""

LLM_decide = """
Given the claim [%s] and the following two claim rationales: (1) true: [%s]; (2) false: [%s], is this claim true or false?  Just output your prediction as "true" or "false".

"""