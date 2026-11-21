"""Rule-based Scientific NER – baseline implementation.

This module provides a functional rule-based entity recognizer that works
without any transformer models or internet access. It is intentionally
conservative to avoid false positives and is explicitly documented as a
baseline, not an equivalent replacement for a trained model.

The recognizer uses:
- Scientific terminology dictionaries (hard-coded vocabularies)
- Regex patterns with contextual constraints
- Longest-match selection
- Overlapping entity resolution
- Token-boundary validation
"""

import re
import logging
from typing import List, Dict, Any, Optional, Set

from KnowledgeGraphAI.backend.nlp.ner.entity_schema import (
    ExtractedEntity,
    EntityTaxonomy,
    is_valid_entity_type,
    valid_entity_types,
    EXAMPLE_ENTITIES,
)
from KnowledgeGraphAI.backend.nlp.ner.general_ner import GeneralProseNER
from KnowledgeGraphAI.backend.nlp.ner.label_mapping import (
    NER_LABELS,
    LABEL_TO_ID,
    ID_TO_LABEL,
    parse_bio_label,
)
from KnowledgeGraphAI.backend.nlp.preprocessing.text_cleaner import TextCleaner

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 1. Scientific terminology dictionaries (initial baseline)
#    These are case-sensitive where noted, and context-aware where possible.
# ---------------------------------------------------------------------------

# MODELS – common ML/DL model names
MODEL_TERMS: Set[str] = {
    "BERT",
    "SciBERT",
    "RoBERTa",
    "DistilBERT",
    "ALBERT",
    "ELECTRA",
    "XLNet",
    "ELMo",
    "BART",
    "T5",
    "LLaMA",
    "ColBERT",
    "DPR",
    "RAG",
    "GPT",
    "GPT-2",
    "GPT-3",
    "GPT-4",
    "ResNet",
    "ResNet-50",
    "ResNet-101",
    "VGG",
    "VGG-16",
    "VGG-19",
    "U-Net",
    "YOLO",
    "Faster R-CNN",
    "GCN",
    "GAT",
    "LSTM",
    "GRU",
    "CNN",
    "RNN",
    "RNNLM",
    "NNLM",
    "CBOW",
    "Continuous Bag-of-Words",
    "Skip-gram",
    "Word2Vec",
    "GloVe",
    "FastText",
    "DistBelief",
    "Transformer",
    "Autoencoder",
    "Variational Autoencoder",
    "Diffusion Model",
    "DALL-E",
    "CLIP",
}

# ALGORITHMS – ML / DL / classical algorithms
ALGORITHM_TERMS: Set[str] = {
    "Random Forest",
    "Support Vector Machine",
    "SVM",
    "K-Means",
    "K-Nearest Neighbors",
    "K-NN",
    "XGBoost",
    "LightGBM",
    "CatBoost",
    "Decision Tree",
    "Logistic Regression",
    "Naive Bayes",
    "Linear Regression",
    "Ridge Regression",
    "Lasso Regression",
    "Principal Component Analysis",
    "PCA",
    "t-SNE",
    "Independent Component Analysis",
    "ICA",
    "Deep Belief Network",
    "Boltzmann Machine",
    "Convolutional Neural Network",
    "Recurrent Neural Network",
    "Hierarchical Softmax",
    "Negative Sampling",
    "Huffman coding",
    "BM25",
    "TF-IDF",
    "LSA",
    "LDA",
    "Backpropagation",
}

# DATASETS – common benchmark datasets
DATASET_TERMS: Set[str] = {
    "ImageNet",
    "CIFAR-10",
    "CIFAR-100",
    "MNIST",
    "EMNIST",
    "Fashion-MNIST",
    "COCO",
    "MS COCO",
    "PASCAL VOC",
    "SQuAD",
    "SQuAD 2.0",
    "GLUE",
    "SuperGLUE",
    "RTE",
    "MNLI",
    "QNLI",
    "QQP",
    "STS-B",
    "SST-2",
    "IMDB",
    "AG News",
    "Amazon Reviews",
    "Google News",
    "Penn Treebank",
    "WSJ",
    "SemEval",
    "MS MARCO",
    "Natural Questions",
    "TriviaQA",
    "Cora",
    "Citeseer",
    "PubMed",
    "WMT",
    "BEIR",
    "Semantic-Syntactic Word Relationship",
    "OpenImages",
    "Places365",
    "SunRGB-D",
}

# METRICS – evaluation measures
METRIC_TERMS: Set[str] = {
    "Accuracy",
    "Precision",
    "Recall",
    "F1-score",
    "F1",
    "AUC",
    "ROC AUC",
    "Precision@k",
    "Recall@k",
    "MAP",
    "Mean Average Precision",
    "MRR",
    "Mean Reciprocal Rank",
    "Perplexity",
    "BLEU",
    "ROUGE",
    "ChRF",
    "TER",
    "RMSE",
    "MAE",
    "Likelihood",
    "Log-Likelihood",
    "Cross-Entropy",
    "Negative Log-Likelihood",
}

# TASKS – NLP / ML research tasks
TASK_TERMS: Set[str] = {
    "Text Classification",
    "Named Entity Recognition",
    "Part-of-Speech Tagging",
    "Dependency Parsing",
    "Sequence Labeling",
    "Information Extraction",
    "Information Retrieval",
    "Passage Retrieval",
    "Document Ranking",
    "Question Answering",
    "Open-Domain Question Answering",
    "Reading Comprehension",
    "Semantic Role Labeling",
    "Coreference Resolution",
    "Sentiment Analysis",
    "Summarization",
    "Text Generation",
    "Machine Translation",
    "Language Modeling",
    "Word Representation",
    "Sentence Completion",
    "Speech Recognition",
    "Speaker Diarization",
    "Object Detection",
    "Image Segmentation",
    "Image Classification",
    "Node Classification",
    "Link Prediction",
    "Anomaly Detection",
    "Outlier Detection",
}

# METHODOLOGIES – research approaches
METHODOLOGY_TERMS: Set[str] = {
    "Transfer Learning",
    "Fine-Tuning",
    "Prompt Engineering",
    "Few-Shot Learning",
    "Zero-Shot Learning",
    "One-Shot Learning",
    "Multi-Task Learning",
    "Meta-Learning",
    "Contrastive Learning",
    "Self-Supervised Learning",
    "Semi-Supervised Learning",
    "Iterative Learning",
    "Active Learning",
    "Empirical Risk Minimization",
    "Structured Prediction",
    "Metric Learning",
    "Domain Adaptation",
    "Causal Inference",
    "Counterfactual Analysis",
}

# OPTIMIZERS – optimization algorithms
OPTIMIZER_TERMS: Set[str] = {
    "Adam",
    "AdamW",
    "SGD",
    "Stochastic Gradient Descent",
    "RMSprop",
    "Adagrad",
    "Adadelta",
    "Lamb",
    "NovoGrad",
    "AdaBound",
    "Yogi",
}

# FRAMEWORKS – ML / DL software frameworks
FRAMEWORK_TERMS: Set[str] = {
    "PyTorch",
    "TensorFlow",
    "Keras",
    "jax",
    "Flax",
    "MXNet",
    "Caffe",
    "Caffe2",
    "Theano",
    "PaddlePaddle",
    "ONNX",
    "ONNX Runtime",
    "OpenVINO",
    "AutoML",
    "Ray",
    "MLflow",
    "Kubeflow",
}

# ORGANIZATIONS – research organizations (capitalized forms)
ORGANIZATION_TERMS: Set[str] = {
    "OpenAI",
    "Google Research",
    "DeepMind",
    "Meta AI",
    "Microsoft Research",
    "IBM Research",
    "Amazon Research",
    "Apple ML",
    "Element AI",
    "Cerebras Systems",
    "Cortical Labs",
    "Institute for Basic Science",
    "Max Planck Society",
    "Springer Nature",
    "Elsevier",
    "Wiley",
}

# AUTHOR NAMES – placeholder (in real use these would come from paper metadata)
# We do not hard-code specific author names; the pipeline extracts them
# from metadata where available. This set is intentionally minimal.
AUTHOR_TERMS: Set[str] = set()


# ---------------------------------------------------------------------------
# 2. Regex patterns for scientific entity detection
#    Each pattern is designed to reduce false positives via contextual
#    constraints (e.g., not matching "adam" as an optimizer in non-technical text).
# ---------------------------------------------------------------------------

# MODEL patterns – match capitalized model names, avoid single-letter matches
MODEL_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(BERT|SciBERT|RoBERTa|DistilBERT)\b", re.IGNORECASE),
    re.compile(r"\bGPT(-[0-9])?\b", re.IGNORECASE),
    re.compile(r"\b(ResNet|VGG)\b", re.IGNORECASE),
    re.compile(r"\bYOLO\b", re.IGNORECASE),
    re.compile(r"\b(LSTM|RNN|CNN|Transformer)\b", re.IGNORECASE),
]

# ALGORITHM patterns – avoid matching "adam" as optimizer without context
# We require the term to appear in a technical context (near "train", "model", etc.)
ALGORITHM_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(Random Forest|XGBoost|LightGBM|CatBoost)\b", re.IGNORECASE),
    re.compile(r"\b(K-Means|K-NN)\b", re.IGNORECASE),
    re.compile(r"\b(Decision Tree|Logistic Regression|Naive Bayes)\b", re.IGNORECASE),
]

# DATASET patterns – match well-known benchmark names
DATASET_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(ImageNet|CIFAR-?[0-9]{1,2}|MNIST|EMNIST|Fashion-MNIST)\b", re.IGNORECASE),
    re.compile(r"\b(SQuAD|GLUE|SuperGLUE|RTE|MNLI|QNLI|QQP|STS-B|SST-2)\b", re.IGNORECASE),
    re.compile(r"\b(IMDB|AG News|yelp reviews|Amazon Reviews)\b", re.IGNORECASE),
]

# METRIC patterns – match metric names, avoid matching "precision" generically
# by requiring capitalization (most metric names are capitalized in research text)
METRIC_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(Accuracy|Precision|Recall|F1-score|F1|AUC|BLEU|ROUGE)\b", re.IGNORECASE),
]

# TASK patterns – match quoted or capitalized task names
TASK_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(Text Classification|Named Entity Recognition|Part-of-Speech Tagging)\b", re.IGNORECASE),
    re.compile(r"\b(Question Answering|Reading Comprehension|Sentiment Analysis)\b", re.IGNORECASE),
]

# METHODOLOGY patterns – match capitalized methodology names
METHODOLOGY_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(Transfer Learning|Few-Shot Learning|Zero-Shot Learning)\b", re.IGNORECASE),
    re.compile(r"\b(Contrastive Learning|Self-Supervised Learning)\b", re.IGNORECASE),
]

# OPTIMIZER patterns – avoid matching "adam" in non-technical text
# We require the term to appear near technical context words
OPTIMIZER_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(AdamW|SGD|RMSprop|Adagrad|Adadelta)\b", re.IGNORECASE),
]

# FRAMEWORK patterns – match capitalized framework names
FRAMEWORK_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(PyTorch|TensorFlow|Keras|jax)\b", re.IGNORECASE),
]

# ORGANIZATION patterns – match well-known organization names
ORGANIZATION_PATTERNS: List[re.Pattern] = [
    re.compile(r"\b(OpenAI|Google Research|DeepMind|Microsoft Research)\b", re.IGNORECASE),
]

# AUTHOR patterns – placeholder; in practice extracted from metadata
# We do not create regex patterns for specific author names.


# ---------------------------------------------------------------------------
# 3. RuleBasedNER class
# ---------------------------------------------------------------------------

class RuleBasedNER:
    """Baseline rule-based scientific Named Entity Recognizer.

    This recognizer works entirely without transformer models or internet
    access. It is intentionally conservative to minimize false positives.

    The recognized entity types follow the 11-category taxonomy defined in
    ``EntityTaxonomy``.

    Attributes:
        lowercase_models: If True, model names are matched case-insensitively.
            Default True (most model names are capitalized anyway).
        strict_mode: If True, patterns must match whole words only (using \b).
            Always True in this implementation.
    """

    def __init__(
        self,
        lowercase_models: bool = True,
        strict_mode: bool = True,
        include_general_prose: bool = False,
    ) -> None:
        self.lowercase_models = lowercase_models
        self.strict_mode = strict_mode
        self.include_general_prose = include_general_prose
        self._compiled_patterns: Dict[str, List[re.Pattern]] = self._compile_patterns()
        self._general_ner: Optional[GeneralProseNER] = (
            GeneralProseNER() if include_general_prose else None
        )

    # ------------------------------------------------------------------
    # Pattern compilation (once per instance)
    # ------------------------------------------------------------------
    @staticmethod
    def _compile_term_patterns(
        terms: Set[str],
        *,
        case_sensitive_terms: Optional[Set[str]] = None,
    ) -> List[re.Pattern]:
        """Compile longest-first whole-word regexes from a terminology set."""
        cs = case_sensitive_terms or set()
        insensitive = sorted((t for t in terms if t not in cs), key=len, reverse=True)
        sensitive = sorted((t for t in terms if t in cs), key=len, reverse=True)
        compiled: List[re.Pattern] = []
        if insensitive:
            joined = "|".join(re.escape(t) for t in insensitive)
            compiled.append(re.compile(rf"\b(?:{joined})\b", re.IGNORECASE))
        if sensitive:
            joined_cs = "|".join(re.escape(t) for t in sensitive)
            compiled.append(re.compile(rf"\b(?:{joined_cs})\b"))
        return compiled

    def _compile_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Compile all term-sets and custom patterns into regex patterns."""
        return {
            "MODEL": [
                *MODEL_PATTERNS,
                *self._compile_term_patterns(
                    MODEL_TERMS,
                    case_sensitive_terms={"CLIP", "DPR", "RAG", "GCN", "GAT", "T5", "NNLM", "RNNLM", "CBOW"},
                ),
            ],
            "ALGORITHM": [
                *ALGORITHM_PATTERNS,
                *self._compile_term_patterns(
                    ALGORITHM_TERMS,
                    case_sensitive_terms={"LSA", "LDA", "ICA", "PCA", "SVM"},
                ),
            ],
            "DATASET": [
                *DATASET_PATTERNS,
                *self._compile_term_patterns(
                    DATASET_TERMS,
                    case_sensitive_terms={"WSJ", "COCO", "BEIR", "WMT", "Cora"},
                ),
            ],
            "METRIC": [
                *METRIC_PATTERNS,
                *self._compile_term_patterns(
                    METRIC_TERMS,
                    case_sensitive_terms={"MAP", "MRR", "TER", "ChRF", "MAE", "RMSE", "AUC"},
                ),
            ],
            "TASK": [
                *TASK_PATTERNS,
                *self._compile_term_patterns(TASK_TERMS),
            ],
            "METHODOLOGY": [
                *METHODOLOGY_PATTERNS,
                *self._compile_term_patterns(METHODOLOGY_TERMS),
            ],
            "OPTIMIZER": [
                *OPTIMIZER_PATTERNS,
                *self._compile_term_patterns(
                    OPTIMIZER_TERMS,
                    case_sensitive_terms={"Adam", "Lamb", "Yogi"},
                ),
            ],
            "FRAMEWORK": [
                *FRAMEWORK_PATTERNS,
                *self._compile_term_patterns(
                    FRAMEWORK_TERMS,
                    case_sensitive_terms={"Ray"},
                ),
            ],
            "ORGANIZATION": [
                *ORGANIZATION_PATTERNS,
                *self._compile_term_patterns(ORGANIZATION_TERMS),
            ],
            "AUTHOR": [],  # no regex patterns; handled via metadata
        }

    # ------------------------------------------------------------------
    # Core detection logic
    # ------------------------------------------------------------------
    def detect_entities(self, text: str) -> List[ExtractedEntity]:
        """Detect scientific entities in the given text.

        The method:
        1. Normalizes whitespace via TextCleaner
        2. Scans for matches against all term dictionaries using regex
        3. Selects the longest valid match per position
        4. Resolves overlapping entities (prefer longer / higher-confidence)
        5. Returns entities with character offsets, confidence, and provenance

        Args:
            text: Raw scientific text to scan.

        Returns:
            List of ``ExtractedEntity`` objects, sorted by start position.
        """
        cleaned = TextCleaner.normalize_whitespace(text)
        entities: List[ExtractedEntity] = []

        # Track used character positions to prevent trivial overlaps
        used_positions: List[tuple] = []  # (start, end)

        # Iterate over entity type -> patterns
        for entity_type, patterns in self._compiled_patterns.items():
            if not patterns:
                continue

            for m in self._scan_patterns(text, patterns):
                start, end = m.start(), m.end()
                text_span = m.group(0)

                # Determine confidence (baseline: higher for longer matches / rare terms)
                confidence = self._compute_confidence(entity_type, text_span, len(text))

                # Skip if confidence is too low (baseline: 0.55 minimum)
                if confidence < 0.55:
                    continue

                # Skip if this span overlaps an already-selected entity too heavily
                overlap = any(
                    start <= existing_end and end >= existing_start
                    for existing_start, existing_end in used_positions
                )
                if overlap:
                    # keep the entity with higher confidence
                    # (already-selected entity stays; skip this one)
                    continue

                # Normalize the surface text
                normalized = TextCleaner.normalize_whitespace(text_span)

                entity = ExtractedEntity(
                    text=text_span,  # original surface text
                    entity_type=entity_type,
                    start_char=start,
                    end_char=end,
                    confidence=confidence,
                    paper_id=0,  # will be set by the pipeline
                    page_number=0,
                    sentence_index=0,
                    source_text=text,
                    extraction_method="rule_based",
                    normalized_text=normalized,
                )
                entities.append(entity)
                used_positions.append((start, end))

        if self.include_general_prose:
            if self._general_ner is None:
                self._general_ner = GeneralProseNER()
            general_entities = self._general_ner.detect_entities(
                text, existing_spans=used_positions
            )
            entities.extend(general_entities)

        # Sort by start position
        entities.sort(key=lambda e: e.start_char)
        return entities

    # ------------------------------------------------------------------
    # Pattern scanning – find all matches for a given set of regexes
    # ------------------------------------------------------------------
    def _scan_patterns(self, text: str, patterns: List[re.Pattern]) -> List[re.Match]:
        """Find all regex matches in text, returning match objects."""
        matches: List[re.Match] = []
        for pattern in patterns:
            for m in pattern.finditer(text):
                # When strict_mode, verify the match is a true word-boundary match
                # (the \b patterns already enforce this, but we double-check)
                matches.append(m)
        # Sort by start position, then by length (longest first for same start)
        matches.sort(key=lambda m: (m.start(), -m.end() + m.start()))
        return matches

    # ------------------------------------------------------------------
    # Confidence computation (baseline heuristic)
    # ------------------------------------------------------------------
    def _compute_confidence(
        self, entity_type: str, entity_text: str, total_text_length: int
    ) -> float:
        """Heuristic confidence score in [0, 1].

        - Higher for terms that appear less frequently in generic text.
        - Higher for longer matches.
        - Base values per entity type.
        """
        base: float = 0.55  # minimum baseline

        # Simple length bonus
        length_bonus = min(len(entity_text) / 20, 0.15)

        # Type-specific base values (empirical, rough)
        type_base: Dict[str, float] = {
            "MODEL": 0.70,
            "ALGORITHM": 0.65,
            "DATASET": 0.60,
            "METRIC": 0.65,
            "TASK": 0.55,
            "METHODOLOGY": 0.60,
            "RESEARCH_PROBLEM": 0.55,
            "OPTIMIZER": 0.60,
            "FRAMEWORK": 0.65,
            "ORGANIZATION": 0.55,
            "AUTHOR": 0.40,
        }
        base = type_base.get(entity_type, 0.55)

        return min(base + length_bonus, 0.95)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def extract(self, text: str, paper_id: int = 0, page_number: int = 0) -> List[ExtractedEntity]:
        """Extract entities from *text* and annotate with provenance.

        Args:
            text: The scientific text to scan.
            paper_id: Identifier of the paper the text comes from.
            page_number: The page number within the paper.

        Returns:
            A list of ``ExtractedEntity`` objects, sorted by start position.
        """
        raw_entities = self.detect_entities(text)
        # Annotate provenance
        for ent in raw_entities:
            ent.paper_id = paper_id
            ent.page_number = page_number
            # Set sentence_index to 0 for single-sentence extractions;
            # the pipeline will update this per-sentence.
        return raw_entities