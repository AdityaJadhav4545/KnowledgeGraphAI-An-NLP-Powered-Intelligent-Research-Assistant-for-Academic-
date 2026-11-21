# Independent Relevance Annotation Review

Dataset: `phase4.3-arxiv-pilot-v1`
Results generated: `2026-11-06T02:35:38.711943+00:00`

## Reviewer instructions

- Review every paper row for every query using the query, paper title, abstract, and cited source.
- Review every retrieved passage in the chunk worksheet; use the PDF/source link if more context is needed.
- Enter `relevant` or `not_relevant`; leave no judgment blank if marking a query complete.
- Optional grade is an integer from 0 (not relevant) through 3 (highly relevant).
- Fill reviewer, ISO-8601 review time, and set independent-review attestation to `yes` only if applicable.
- Retrieval rank and similarity are descriptive system outputs, not relevance labels.
- Do not mark a candidate relevant solely because it ranked highly.

## Query worksheets

### nlp-attention-01

How can self-attention replace recurrent and convolutional layers in sequence-to-sequence language models?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 6, section UNKNOWN

Chunk `a7775a10446dc4c1d3d17530cc9a7f04981e4590a2e6be3ac495940ae4b33a93`; source `arxiv:1706.03762`; faiss_cosine rank 1 similarity 0.8027443885803223 rerank None; metadata_filtered_cosine rank 1 similarity 0.8027443885803223 rerank None; paper_aggregation rank 1 similarity 0.8027443885803223 rerank None; mmr_diversity rank 1 similarity 0.8027443885803223 rerank 0.5619210720062255

> Table 1: Maximum path lengths, per-layer complexity and minimum number of sequential operations
> for different layer types. n is the sequence length, d is the representation dimension, k is the kernel
> size of convolutions and r the size of the neighborhood in restricted self-attention. Layer Type
> Complexity per Layer
> Sequential
> Maximum Path Length
> Operations
> Self-Attention
> O(n2 · d)
> O(1)
> O(1)
> Recurrent
> O(n · d2)
> O(n)
> O(n)
> Convolutional
> O(k · n · d2)
> O(1)
> O(logk(n))
> Self-Attention (restricted)
> O(r · n · d)
> O(1)
> O(n/r)
> 3.5
> Positional Encoding
> Since our model contains no recurrence and no convolution, in order for the model to make use of the
> order of the sequence, we must inject some information about the relative or absolute position of the
> tokens in the sequence. To this end, we add "positional encodings" to the input embeddings at the
> bottoms of the encoder and decoder stacks. The positional encodings have the same dimension dmodel
> as the embeddings, so that the two can be summed. There are many choices of positional encodings,
> learned and fixed [9]. In this work, we use sine and cosine functions of different frequencies:
> PE(pos,2i) = sin(pos/100002i/dmodel)
> PE(pos,2i+1) = cos(pos/100002i/dmodel)
> where pos is the position and i is the dimension. That is, each dimension of the positional encoding
> corresponds to a sinusoid. The wavelengths form a geometric progression from 2π to 10000 · 2π. We
> chose this function because we hypothesized it would allow the model to easily learn to attend by
> relative positions, since for any fixed offset k, PEpos+k can be represented as a linear function of
> PEpos. We also experimented with using learned positional embeddings [9] instead, and found that the two
> versions produced nearly identical results (see Table 3 row (E)). We chose the sinusoidal version
> because it may allow the model to extrapolate to sequence lengths longer than the ones encountered
> during training. 4
> Why Self-Attention
> In this section we compare various aspects of self-attention layers to the recurrent and convolutional layers commonly used for mapping one variable-length sequence of symbol representations
> (x1, ..., xn) to another sequence of equal length (z1, ..., zn), with xi, zi ∈Rd, such as a hidden
> layer in a typical sequence transduction encoder or decoder. Motivating our use of self-attention we
> consider three desiderata. One is the total computational complexity per layer.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 7, section UNKNOWN

Chunk `a26710f022f4259b63e404a94d2d0daf41c6eb1b9a8d6071ccb1de2bbfced29a`; source `arxiv:1706.03762`; faiss_cosine rank 2 similarity 0.7884760499000549 rerank None; metadata_filtered_cosine rank 2 similarity 0.7884760499000549 rerank None; mmr_diversity rank 5 similarity 0.7884760499000549 rerank 0.2519332349300384

> length n is smaller than the representation dimensionality d, which is most often the case with
> sentence representations used by state-of-the-art models in machine translations, such as word-piece
> [38] and byte-pair [31] representations. To improve computational performance for tasks involving
> very long sequences, self-attention could be restricted to considering only a neighborhood of size r in
> the input sequence centered around the respective output position. This would increase the maximum
> path length to O(n/r). We plan to investigate this approach further in future work. A single convolutional layer with kernel width k < n does not connect all pairs of input and output
> positions. Doing so requires a stack of O(n/k) convolutional layers in the case of contiguous kernels,
> or O(logk(n)) in the case of dilated convolutions [18], increasing the length of the longest paths
> between any two positions in the network. Convolutional layers are generally more expensive than
> recurrent layers, by a factor of k. Separable convolutions [6], however, decrease the complexity
> considerably, to O(k · n · d + n · d2). Even with k = n, however, the complexity of a separable
> convolution is equal to the combination of a self-attention layer and a point-wise feed-forward layer,
> the approach we take in our model. As side benefit, self-attention could yield more interpretable models. We inspect attention distributions
> from our models and present and discuss examples in the appendix. Not only do individual attention
> heads clearly learn to perform different tasks, many appear to exhibit behavior related to the syntactic
> and semantic structure of the sentences. 5
> Training
> This section describes the training regime for our models. 5.1
> Training Data and Batching
> We trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million
> sentence pairs. Sentences were encoded using byte-pair encoding [3], which has a shared sourcetarget vocabulary of about 37000 tokens. For English-French, we used the significantly larger WMT
> 2014 English-French dataset consisting of 36M sentences and split tokens into a 32000 word-piece
> vocabulary [38]. Sentence pairs were batched together by approximate sequence length. Each training
> batch contained a set of sentence pairs containing approximately 25000 source tokens and 25000
> target tokens. 5.2
> Hardware and Schedule
> We trained our models on one machine with 8 NVIDIA P100 GPUs. For our base models using
> the hyperparameters described throughout the paper, each training step took about 0.4 seconds.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 2, section UNKNOWN

Chunk `79455135e516a9a369c43ac756bc5462698a33e28229a3b0c352f8295d7ed0bb`; source `arxiv:1706.03762`; faiss_cosine rank 3 similarity 0.7856385707855225 rerank None; metadata_filtered_cosine rank 3 similarity 0.7856385707855225 rerank None; mmr_diversity rank 6 similarity 0.7856385707855225 rerank 0.24994699954986566

> In these models,
> the number of operations required to relate signals from two arbitrary input or output positions grows
> in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet. This makes
> it more difficult to learn dependencies between distant positions [12]. In the Transformer this is
> reduced to a constant number of operations, albeit at the cost of reduced effective resolution due
> to averaging attention-weighted positions, an effect we counteract with Multi-Head Attention as
> described in section 3.2. Self-attention, sometimes called intra-attention is an attention mechanism relating different positions
> of a single sequence in order to compute a representation of the sequence. Self-attention has been
> used successfully in a variety of tasks including reading comprehension, abstractive summarization,
> textual entailment and learning task-independent sentence representations [4, 27, 28, 22]. End-to-end memory networks are based on a recurrent attention mechanism instead of sequencealigned recurrence and have been shown to perform well on simple-language question answering and
> language modeling tasks [34]. To the best of our knowledge, however, the Transformer is the first transduction model relying
> entirely on self-attention to compute representations of its input and output without using sequencealigned RNNs or convolution. In the following sections, we will describe the Transformer, motivate
> self-attention and discuss its advantages over models such as [17, 18] and [9]. 3
> Model Architecture
> Most competitive neural sequence transduction models have an encoder-decoder structure [5, 2, 35]. Here, the encoder maps an input sequence of symbol representations (x1, ..., xn) to a sequence
> of continuous representations z = (z1, ..., zn). Given z, the decoder then generates an output
> sequence (y1, ..., ym) of symbols one element at a time. At each step the model is auto-regressive
> [10], consuming the previously generated symbols as additional input when generating the next. 2

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 2, section UNKNOWN

Chunk `f08b9157e6e528fb2b32c5aceb0226d7a638fd1f4ef4e3c2626c2d9298ee254f`; source `arxiv:1706.03762`; faiss_cosine rank 4 similarity 0.7832225561141968 rerank None; metadata_filtered_cosine rank 4 similarity 0.7832225561141968 rerank None; mmr_diversity rank 7 similarity 0.7832225561141968 rerank 0.24825578927993763

> 1
> Introduction
> Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks
> in particular, have been firmly established as state of the art approaches in sequence modeling and
> transduction problems such as language modeling and machine translation [35, 2, 5]. Numerous
> efforts have since continued to push the boundaries of recurrent language models and encoder-decoder
> architectures [38, 24, 15]. Recurrent models typically factor computation along the symbol positions of the input and output
> sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden
> states ht, as a function of the previous hidden state ht−1 and the input for position t. This inherently
> sequential nature precludes parallelization within training examples, which becomes critical at longer
> sequence lengths, as memory constraints limit batching across examples. Recent work has achieved
> significant improvements in computational efficiency through factorization tricks [21] and conditional
> computation [32], while also improving model performance in case of the latter. The fundamental
> constraint of sequential computation, however, remains. Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in
> the input or output sequences [2, 19]. In all but a few cases [27], however, such attention mechanisms
> are used in conjunction with a recurrent network. In this work we propose the Transformer, a model architecture eschewing recurrence and instead
> relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in
> translation quality after being trained for as little as twelve hours on eight P100 GPUs. 2
> Background
> The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU
> [16], ByteNet [18] and ConvS2S [9], all of which use convolutional neural networks as basic building
> block, computing hidden representations in parallel for all input and output positions. In these models,
> the number of operations required to relate signals from two arbitrary input or output positions grows
> in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet. This makes
> it more difficult to learn dependencies between distant positions [12].

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 6, section UNKNOWN

Chunk `c586efe60405dc018ea65e3830667f95307d08ebdead6d6183c4ba7675e6828d`; source `arxiv:1706.03762`; faiss_cosine rank 5 similarity 0.7820509672164917 rerank None; metadata_filtered_cosine rank 5 similarity 0.7820509672164917 rerank None; mmr_diversity rank 8 similarity 0.7820509672164917 rerank 0.24743567705154412

> Motivating our use of self-attention we
> consider three desiderata. One is the total computational complexity per layer. Another is the amount of computation that can
> be parallelized, as measured by the minimum number of sequential operations required. The third is the path length between long-range dependencies in the network. Learning long-range
> dependencies is a key challenge in many sequence transduction tasks. One key factor affecting the
> ability to learn such dependencies is the length of the paths forward and backward signals have to
> traverse in the network. The shorter these paths between any combination of positions in the input
> and output sequences, the easier it is to learn long-range dependencies [12]. Hence we also compare
> the maximum path length between any two input and output positions in networks composed of the
> different layer types. As noted in Table 1, a self-attention layer connects all positions with a constant number of sequentially
> executed operations, whereas a recurrent layer requires O(n) sequential operations. In terms of
> computational complexity, self-attention layers are faster than recurrent layers when the sequence
> 6

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 12, section UNKNOWN

Chunk `117db82f92e284317641eb2c073a226438b7b540fd982528bac8f02d0b9aa1dc`; source `arxiv:1706.03762`; faiss_cosine rank 6 similarity 0.7779736518859863 rerank None; metadata_filtered_cosine rank 6 similarity 0.7779736518859863 rerank None; mmr_diversity rank 9 similarity 0.7779736518859863 rerank 0.2445815563201903

> arXiv preprint
> arXiv:1609.08144, 2016. [39] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu. Deep recurrent models with
> fast-forward connections for neural machine translation. CoRR, abs/1606.04199, 2016. [40] Muhua Zhu, Yue Zhang, Wenliang Chen, Min Zhang, and Jingbo Zhu. Fast and accurate
> shift-reduce constituent parsing. In Proceedings of the 51st Annual Meeting of the ACL (Volume
> 1: Long Papers), pages 434–443. ACL, August 2013. 12

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 10, section UNKNOWN

Chunk `13719f4b5f0e7075bd93bd7c7a21f7f856eb6da4fa88577d67241606012d014c`; source `arxiv:1706.03762`; faiss_cosine rank 7 similarity 0.7775738835334778 rerank None; metadata_filtered_cosine rank 7 similarity 0.7775738835334778 rerank None; mmr_diversity rank 10 similarity 0.7775738835334778 rerank 0.2443017184734344

> Table 4: The Transformer generalizes well to English constituency parsing (Results are on Section 23
> of WSJ)
> Parser
> Training
> WSJ 23 F1
> Vinyals & Kaiser el al. (2014) [37]
> WSJ only, discriminative
> 88.3
> Petrov et al. (2006) [29]
> WSJ only, discriminative
> 90.4
> Zhu et al. (2013) [40]
> WSJ only, discriminative
> 90.4
> Dyer et al. (2016) [8]
> WSJ only, discriminative
> 91.7
> Transformer (4 layers)
> WSJ only, discriminative
> 91.3
> Zhu et al. (2013) [40]
> semi-supervised
> 91.3
> Huang & Harper (2009) [14]
> semi-supervised
> 91.3
> McClosky et al. (2006) [26]
> semi-supervised
> 92.1
> Vinyals & Kaiser el al. (2014) [37]
> semi-supervised
> 92.1
> Transformer (4 layers)
> semi-supervised
> 92.7
> Luong et al. (2015) [23]
> multi-task
> 93.0
> Dyer et al. (2016) [8]
> generative
> 93.3
> increased the maximum output length to input length + 300. We used a beam size of 21 and α = 0.3
> for both WSJ only and the semi-supervised setting. Our results in Table 4 show that despite the lack of task-specific tuning our model performs surprisingly well, yielding better results than all previously reported models with the exception of the
> Recurrent Neural Network Grammar [8]. In contrast to RNN sequence-to-sequence models [37], the Transformer outperforms the BerkeleyParser [29] even when training only on the WSJ training set of 40K sentences. 7
> Conclusion
> In this work, we presented the Transformer, the first sequence transduction model based entirely on
> attention, replacing the recurrent layers most commonly used in encoder-decoder architectures with
> multi-headed self-attention. For translation tasks, the Transformer can be trained significantly faster than architectures based
> on recurrent or convolutional layers. On both WMT 2014 English-to-German and WMT 2014
> English-to-French translation tasks, we achieve a new state of the art. In the former task our best
> model outperforms even all previously reported ensembles. We are excited about the future of attention-based models and plan to apply them to other tasks. We
> plan to extend the Transformer to problems involving input and output modalities other than text and
> to investigate local, restricted attention mechanisms to efficiently handle large inputs and outputs
> such as images, audio and video. Making generation less sequential is another research goals of ours. The code we used to train and evaluate our models is available at https://github.com/
> tensorflow/tensor2tensor. Acknowledgements
> We are grateful to Nal Kalchbrenner and Stephan Gouws for their fruitful
> comments, corrections and inspiration. References
> [1] Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. Layer normalization. arXiv preprint
> arXiv:1607.06450, 2016.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 1, section UNKNOWN

Chunk `dd20f12ca4936d72cd4abe64ad7fabe896c453abbacfadb4fbbebada0073146e`; source `arxiv:1706.03762`; faiss_cosine rank 8 similarity 0.7749477028846741 rerank None; metadata_filtered_cosine rank 8 similarity 0.7749477028846741 rerank None

> Provided proper attribution is provided, Google hereby grants permission to
> reproduce the tables and figures in this paper solely for use in journalistic or
> scholarly works. Attention Is All You Need
> Ashish Vaswani∗
> Google Brain
> avaswani@google.com
> Noam Shazeer∗
> Google Brain
> noam@google.com
> Niki Parmar∗
> Google Research
> nikip@google.com
> Jakob Uszkoreit∗
> Google Research
> usz@google.com
> Llion Jones∗
> Google Research
> llion@google.com
> Aidan N. Gomez∗†
> University of Toronto
> aidan@cs.toronto.edu
> Łukasz Kaiser∗
> Google Brain
> lukaszkaiser@google.com
> Illia Polosukhin∗‡
> illia.polosukhin@gmail.com
> Abstract
> The dominant sequence transduction models are based on complex recurrent or
> convolutional neural networks that include an encoder and a decoder. The best
> performing models also connect the encoder and decoder through an attention
> mechanism. We propose a new simple network architecture, the Transformer,
> based solely on attention mechanisms, dispensing with recurrence and convolutions
> entirely. Experiments on two machine translation tasks show these models to
> be superior in quality while being more parallelizable and requiring significantly
> less time to train. Our model achieves 28.4 BLEU on the WMT 2014 Englishto-German translation task, improving over the existing best results, including
> ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task,
> our model establishes a new single-model state-of-the-art BLEU score of 41.8 after
> training for 3.5 days on eight GPUs, a small fraction of the training costs of the
> best models from the literature. We show that the Transformer generalizes well to
> other tasks by applying it successfully to English constituency parsing both with
> large and limited training data. ∗Equal contribution. Listing order is random. Jakob proposed replacing RNNs with self-attention and started
> the effort to evaluate this idea. Ashish, with Illia, designed and implemented the first Transformer models and
> has been crucially involved in every aspect of this work. Noam proposed scaled dot-product attention, multi-head
> attention and the parameter-free position representation and became the other person involved in nearly every
> detail. Niki designed, implemented, tuned and evaluated countless model variants in our original codebase and
> tensor2tensor. Llion also experimented with novel model variants, was responsible for our initial codebase, and
> efficient inference and visualizations. Lukasz and Aidan spent countless long days designing various parts of and
> implementing tensor2tensor, replacing our earlier codebase, greatly improving results and massively accelerating
> our research. †Work performed while at Google Brain. ‡Work performed while at Google Research. 31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA. arXiv:1706.03762v7 [cs.CL] 2 Aug 2023

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 11, section UNKNOWN

Chunk `2c479e9ca7c0278f1d1a4e5f083d8b2bc2e7d3ab4e4af1b4c41504297f97f5ed`; source `arxiv:1706.03762`; faiss_cosine rank 9 similarity 0.7746134400367737 rerank None; metadata_filtered_cosine rank 9 similarity 0.7746134400367737 rerank None

> [5] Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, Fethi Bougares, Holger Schwenk,
> and Yoshua Bengio. Learning phrase representations using rnn encoder-decoder for statistical
> machine translation. CoRR, abs/1406.1078, 2014. [6] Francois Chollet. Xception: Deep learning with depthwise separable convolutions. arXiv
> preprint arXiv:1610.02357, 2016. [7] Junyoung Chung, Çaglar Gülçehre, Kyunghyun Cho, and Yoshua Bengio. Empirical evaluation
> of gated recurrent neural networks on sequence modeling. CoRR, abs/1412.3555, 2014. [8] Chris Dyer, Adhiguna Kuncoro, Miguel Ballesteros, and Noah A. Smith. Recurrent neural
> network grammars. In Proc. of NAACL, 2016. [9] Jonas Gehring, Michael Auli, David Grangier, Denis Yarats, and Yann N. Dauphin. Convolutional sequence to sequence learning. arXiv preprint arXiv:1705.03122v2, 2017. [10] Alex Graves. Generating sequences with recurrent neural networks. arXiv preprint
> arXiv:1308.0850, 2013. [11] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In Proceedings of the IEEE Conference on Computer Vision and Pattern
> Recognition, pages 770–778, 2016. [12] Sepp Hochreiter, Yoshua Bengio, Paolo Frasconi, and Jürgen Schmidhuber. Gradient flow in
> recurrent nets: the difficulty of learning long-term dependencies, 2001. [13] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural computation,
> 9(8):1735–1780, 1997. [14] Zhongqiang Huang and Mary Harper. Self-training PCFG grammars with latent annotations
> across languages. In Proceedings of the 2009 Conference on Empirical Methods in Natural
> Language Processing, pages 832–841. ACL, August 2009. [15] Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu. Exploring
> the limits of language modeling. arXiv preprint arXiv:1602.02410, 2016. [16] Łukasz Kaiser and Samy Bengio. Can active memory replace attention? In Advances in Neural
> Information Processing Systems, (NIPS), 2016. [17] Łukasz Kaiser and Ilya Sutskever. Neural GPUs learn algorithms. In International Conference
> on Learning Representations (ICLR), 2016. [18] Nal Kalchbrenner, Lasse Espeholt, Karen Simonyan, Aaron van den Oord, Alex Graves, and Koray Kavukcuoglu. Neural machine translation in linear time. arXiv preprint arXiv:1610.10099v2,
> 2017. [19] Yoon Kim, Carl Denton, Luong Hoang, and Alexander M. Rush. Structured attention networks. In International Conference on Learning Representations, 2017. [20] Diederik Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In ICLR, 2015. [21] Oleksii Kuchaiev and Boris Ginsburg. Factorization tricks for LSTM networks. arXiv preprint
> arXiv:1703.10722, 2017. [22] Zhouhan Lin, Minwei Feng, Cicero Nogueira dos Santos, Mo Yu, Bing Xiang, Bowen
> Zhou, and Yoshua Bengio. A structured self-attentive sentence embedding. arXiv preprint
> arXiv:1703.03130, 2017. [23] Minh-Thang Luong, Quoc V. Le, Ilya Sutskever, Oriol Vinyals, and Lukasz Kaiser. Multi-task
> sequence to sequence learning.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 11, section UNKNOWN

Chunk `f8aaaaff47c32bee1e2e023f7e18d42d578c3706ae74c42391ea400c08374405`; source `arxiv:1706.03762`; faiss_cosine rank 10 similarity 0.7735873460769653 rerank None; metadata_filtered_cosine rank 10 similarity 0.7735873460769653 rerank None

> arXiv preprint
> arXiv:1703.10722, 2017. [22] Zhouhan Lin, Minwei Feng, Cicero Nogueira dos Santos, Mo Yu, Bing Xiang, Bowen
> Zhou, and Yoshua Bengio. A structured self-attentive sentence embedding. arXiv preprint
> arXiv:1703.03130, 2017. [23] Minh-Thang Luong, Quoc V. Le, Ilya Sutskever, Oriol Vinyals, and Lukasz Kaiser. Multi-task
> sequence to sequence learning. arXiv preprint arXiv:1511.06114, 2015. [24] Minh-Thang Luong, Hieu Pham, and Christopher D Manning. Effective approaches to attentionbased neural machine translation. arXiv preprint arXiv:1508.04025, 2015. 11

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 2, section UNKNOWN

Chunk `b95faf1308418a0a159490d62e3f12fc45ef52d89d94af255877cd2fc0cd0d90`; source `arxiv:1710.10903`; paper_aggregation rank 2 similarity 0.7626593112945557 rerank None; mmr_diversity rank 2 similarity 0.7626593112945557 rerank 0.2599425137042999

> Monti et al. (2016)
> presented mixture model CNNs (MoNet), a spatial approach which provides a unified generalization of CNN architectures to graphs. More recently, Hamilton et al. (2017) introduced GraphSAGE,
> a method for computing node representations in an inductive manner. This technique operates by
> sampling a fixed-size neighborhood of each node, and then performing a specific aggregator over
> it (such as the mean over all the sampled neighbors’ feature vectors, or the result of feeding them
> through a recurrent neural network). This approach has yielded impressive performance across several large-scale inductive benchmarks. Attention mechanisms have become almost a de facto standard in many sequence-based tasks (Bahdanau et al., 2015; Gehring et al., 2016). One of the benefits of attention mechanisms is that they
> allow for dealing with variable sized inputs, focusing on the most relevant parts of the input to make
> decisions. When an attention mechanism is used to compute a representation of a single sequence,
> it is commonly referred to as self-attention or intra-attention. Together with Recurrent Neural Networks (RNNs) or convolutions, self-attention has proven to be useful for tasks such as machine
> reading (Cheng et al., 2016) and learning sentence representations (Lin et al., 2017). However,
> Vaswani et al. (2017) showed that not only self-attention can improve a method based on RNNs or
> convolutions, but also that it is sufficient for constructing a powerful model obtaining state-of-the-art
> performance on the machine translation task. Inspired by this recent work, we introduce an attention-based architecture to perform node classification of graph-structured data. The idea is to compute the hidden representations of each node in the
> graph, by attending over its neighbors, following a self-attention strategy. The attention architecture
> has several interesting properties: (1) the operation is efficient, since it is parallelizable across nodeneighbor pairs; (2) it can be applied to graph nodes having different degrees by specifying arbitrary
> weights to the neighbors; and (3) the model is directly applicable to inductive learning problems,
> including tasks where the model has to generalize to completely unseen graphs. We validate the
> proposed approach on four challenging benchmarks: Cora, Citeseer and Pubmed citation networks
> as well as an inductive protein-protein interaction dataset, achieving or matching state-of-the-art results that highlight the potential of attention-based models when dealing with arbitrarily structured
> graphs.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 7, section UNKNOWN

Chunk `1869c59ea2d0d7dc271a684c00164828e67ae3e7b97941e0123a54a108c63ac5`; source `arxiv:1512.03385`; paper_aggregation rank 3 similarity 0.7616293430328369 rerank None; mmr_diversity rank 3 similarity 0.7616293430328369 rerank 0.25905740261077875

> The deep plain nets suffer from increased depth,
> and exhibit higher training error when going deeper. This
> phenomenon is similar to that on ImageNet (fig. 4, left) and
> on MNIST (see [42]), suggesting that such an optimization
> difficulty is a fundamental problem. fig. 6 (middle) shows the behaviors of ResNets. Also
> similar to the ImageNet cases (fig. 4, right), our ResNets
> manage to overcome the optimization difficulty and demonstrate accuracy gains when the depth increases. We further explore n = 18 that leads to a 110-layer
> ResNet. In this case, we find that the initial learning rate
> of 0.1 is slightly too large to start converging5. So we use
> 0.01 to warm up the training until the training error is below
> 80% (about 400 iterations), and then go back to 0.1 and continue training. The rest of the learning schedule is as done
> previously. This 110-layer network converges well (fig. 6,
> middle). It has fewer parameters than other deep and thin
> 5With an initial learning rate of 0.1, it starts converging (<90% error)
> after several epochs, but still reaches similar accuracy. 7

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 5, section UNKNOWN

Chunk `9212d07d6cc2b7c3532920dbcaff54f5e092fb84128e84bc3d148e040ee73131`; source `arxiv:1810.04805`; paper_aggregation rank 4 similarity 0.7506557703018188 rerank None; mmr_diversity rank 4 similarity 0.7506557703018188 rerank 0.2503055572509765

> [CLS]
> he
> likes
> play
> ##ing
> [SEP]
> my
> dog
> is
> cute
> [SEP]
> Input
> E[CLS]
> Ehe
> Elikes
> Eplay
> E##ing
> E[SEP]
> Emy
> Edog
> Eis
> Ecute
> E[SEP]
> Token
> Embeddings
> EA
> EB
> EB
> EB
> EB
> EB
> EA
> EA
> EA
> EA
> EA
> Segment
> Embeddings
> E0
> E6
> E7
> E8
> E9
> E10
> E1
> E2
> E3
> E4
> E5
> Position
> Embeddings
> Figure 2: BERT input representation. The input embeddings are the sum of the token embeddings, the segmentation embeddings and the position embeddings. The NSP task is closely related to representationlearning objectives used in Jernite et al. (2017) and
> Logeswaran and Lee (2018). However, in prior
> work, only sentence embeddings are transferred to
> down-stream tasks, where BERT transfers all parameters to initialize end-task model parameters. Pre-training data The pre-training procedure
> largely follows the existing literature on language
> model pre-training. For the pre-training corpus we
> use the BooksCorpus (800M words) (Zhu et al.,
> 2015) and English Wikipedia (2,500M words). For Wikipedia we extract only the text passages
> and ignore lists, tables, and headers. It is critical to use a document-level corpus rather than a
> shuffled sentence-level corpus such as the Billion
> Word Benchmark (Chelba et al., 2013) in order to
> extract long contiguous sequences. 3.2
> Fine-tuning BERT
> Fine-tuning is straightforward since the selfattention mechanism in the Transformer allows BERT to model many downstream tasks—
> whether they involve single text or text pairs—by
> swapping out the appropriate inputs and outputs. For applications involving text pairs, a common
> pattern is to independently encode text pairs before applying bidirectional cross attention, such
> as Parikh et al. (2016); Seo et al. (2017). BERT
> instead uses the self-attention mechanism to unify
> these two stages, as encoding a concatenated text
> pair with self-attention effectively includes bidirectional cross attention between two sentences. For each task, we simply plug in the taskspecific inputs and outputs into BERT and finetune all the parameters end-to-end. At the input, sentence A and sentence B from pre-training
> are analogous to (1) sentence pairs in paraphrasing, (2) hypothesis-premise pairs in entailment, (3)
> question-passage pairs in question answering, and
> (4) a degenerate text-∅pair in text classification
> or sequence tagging. At the output, the token representations are fed into an output layer for tokenlevel tasks, such as sequence tagging or question
> answering, and the [CLS] representation is fed
> into an output layer for classification, such as entailment or sentiment analysis. Compared to pre-training, fine-tuning is relatively inexpensive.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 9, section UNKNOWN

Chunk `ceb70decfd1a70e19775ffd2a69ac46e486cdad9d874011dcae864a6c7d262fa`; source `arxiv:2005.11401`; paper_aggregation rank 5 similarity 0.7484406232833862 rerank None

> General-Purpose Architectures for NLP
> Prior work on general-purpose architectures for NLP
> tasks has shown great success without the use of retrieval. A single, pre-trained language model
> has been shown to achieve strong performance on various classification tasks in the GLUE benchmarks [60, 61] after fine-tuning [49, 8]. GPT-2 [50] later showed that a single, left-to-right, pre-trained
> language model could achieve strong performance across both discriminative and generative tasks. For further improvement, BART [32] and T5 [51, 52] propose a single, pre-trained encoder-decoder
> model that leverages bi-directional attention to achieve stronger performance on discriminative
> and generative tasks. Our work aims to expand the space of possible tasks with a single, unified
> architecture, by learning a retrieval module to augment pre-trained, generative language models. Learned Retrieval
> There is significant work on learning to retrieve documents in information
> retrieval, more recently with pre-trained, neural language models [44, 26] similar to ours. Some
> work optimizes the retrieval module to aid in a specific, downstream task such as question answering,
> using search [46], reinforcement learning [6, 63, 62], or a latent variable approach [31, 20] as in our
> work. These successes leverage different retrieval-based architectures and optimization techniques to
> achieve strong performance on a single task, while we show that a single retrieval-based architecture
> can be fine-tuned for strong performance on a variety of tasks. Memory-based Architectures
> Our document index can be seen as a large external memory for
> neural networks to attend to, analogous to memory networks [64, 55]. Concurrent work [14] learns
> to retrieve a trained embedding for each entity in the input, rather than to retrieve raw text as in our
> work. Other work improves the ability of dialog models to generate factual text by attending over
> fact embeddings [15, 13]. A key feature of our memory is that it is comprised of raw text rather
> distributed representations, which makes the memory both (i) human-readable, lending a form of
> interpretability to our model, and (ii) human-writable, enabling us to dynamically update the model’s
> memory by editing the document index. This approach has also been used in knowledge-intensive
> dialog, where generators have been conditioned on retrieved text directly, albeit obtained via TF-IDF
> rather than end-to-end learnt retrieval [9]. Retrieve-and-Edit approaches
> Our method shares some similarities with retrieve-and-edit style
> approaches, where a similar training input-output pair is retrieved for a given input, and then edited
> to provide a final output.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 14, section UNKNOWN

Chunk `0839505d3b7de68977b30ae94ac4219a860f639d6082aaeee8639c6cd346c6db`; source `arxiv:1609.02907`; paper_aggregation rank 6 similarity 0.741104781627655 rerank None

> Published as a conference paper at ICLR 2017
> B
> EXPERIMENTS ON MODEL DEPTH
> In these experiments, we investigate the influence of model depth (number of layers) on classification
> performance. We report results on a 5-fold cross-validation experiment on the Cora, Citeseer and
> Pubmed datasets (Sen et al., 2008) using all labels. In addition to the standard GCN model (eq. 2),
> we report results on a model variant where we use residual connections (He et al., 2016) between
> hidden layers to facilitate training of deeper models by enabling the model to carry over information
> from the previous layer’s input:
> H(l+1) = σ

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 1, section UNKNOWN

Chunk `0031a8c654b940aec72e634b44d1f532aefc5b355b54ec0bc447c81144091d4f`; source `arxiv:1903.10676`; paper_aggregation rank 7 similarity 0.7275469303131104 rerank None

> SCIBERT is a pretrained language model based on BERT but trained
> on a large corpus of scientific text. (ii) We perform extensive experimentation to
> investigate the performance of finetuning versus task-specific architectures atop frozen embeddings, and the effect of having an in-domain vocabulary. (iii) We evaluate SCIBERT on a suite of tasks
> in the scientific domain, and achieve new state-ofthe-art (SOTA) results on many of these tasks. 2
> Methods
> Background
> The
> BERT
> model
> architecture
> (Devlin et al., 2019) is based on a multilayer bidirectional Transformer (Vaswani et al., 2017). Instead of the traditional left-to-right language modeling objective, BERT is trained on two tasks: predicting randomly masked tokens and predicting
> whether two sentences follow each other. SCIBERT follows the same architecture as BERT but is
> instead pretrained on scientific text. Vocabulary
> BERT uses WordPiece (Wu et al.,
> 2016) for unsupervised tokenization of the input
> text. The vocabulary is built such that it contains
> the most frequently used words or subword units. We refer to the original vocabulary released with

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 6, section UNKNOWN

Chunk `c237f9de4afea2f6aa582228a3b563f02671d050fecbdcab6be452ca6594a817`; source `arxiv:2004.04906`; paper_aggregation rank 8 similarity 0.7236154079437256 rerank None

> Sample efficiency
> We explore how many training examples are needed to achieve good passage
> retrieval performance. Figure 1 illustrates the top-k
> retrieval accuracy with respect to different numbers of training examples, measured on the development set of Natural Questions. As is shown, a
> dense passage retriever trained using only 1,000 examples already outperforms BM25. This suggests
> that with a general pretrained language model, it is
> possible to train a high-quality dense retriever with
> a small number of question–passage pairs. Adding
> more training examples (from 1k to 59k) further
> improves the retrieval accuracy consistently. In-batch negative training
> We test different
> training schemes on the development set of Natural
> Questions and summarize the results in Table 3. The top block is the standard 1-of-N training setting, where each question in the batch is paired
> with a positive passage and its own set of n negative passages (eq. (2)). We find that the choice
> of negatives — random, BM25 or gold passages
> (positive passages from other questions) — does
> not impact the top-k accuracy much in this setting
> when k ≥20. The middle bock is the in-batch negative training
> (Section 3.2) setting. We find that using a similar
> configuration (7 gold negative passages), in-batch
> negative training improves the results substantially. The key difference between the two is whether the
> gold negative passages come from the same batch
> or from the whole training set. Effectively, in-batch
> negative training is an easy and memory-efficient
> way to reuse the negative examples already in the
> batch rather than creating new ones. It produces
> more pairs and thus increases the number of training examples, which might contribute to the good
> model performance. As a result, accuracy consistently improves as the batch size grows. Finally, we explore in-batch negative training
> with additional “hard” negative passages that have
> high BM25 scores given the question, but do not
> contain the answer string (the bottom block). These
> additional passages are used as negative passages
> for all questions in the same batch. We find that
> adding a single BM25 negative passage improves
> the result substantially while adding two does not
> help further. Impact of gold passages
> We use passages that
> match the gold contexts in the original datasets
> (when available) as positive examples (Section 4.2). Type
> #N
> IB
> Top-5
> Top-20
> Top-100
> Random
> 7

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 4, section UNKNOWN

Chunk `542f67896add4417df24665a10ebc2d6030f04028398609993b4976acc0feb48`; source `arxiv:2004.12832`; paper_aggregation rank 9 similarity 0.7232216596603394 rerank None

> Even though ColBERT’s late-interaction framework can be applied to a wide variety of architectures (e.g., CNNs, RNNs, transformers, etc.), we choose to focus this work on bi-directional transformerbased encoders (i.e., BERT) owing to their state-of-the-art effectiveness yet very high computational cost. 3.1
> Architecture
> Figure 3 depicts the general architecture of ColBERT, which comprises: (a) a query encoder fQ, (b) a document encoder fD, and (c)
> the late interaction mechanism. Given a query q and document d,
> fQ encodes q into a bag of fixed-size embeddings Eq while fD encodes d into another bag Ed. Crucially, each embeddings in Eq and
> Ed is contextualized based on the other terms in q or d, respectively. We describe our BERT-based encoders in §3.2. Using Eq and Ed, ColBERT computes the relevance score between q and d via late interaction, which we define as a summation
> of maximum similarity (MaxSim) operators. In particular, we find
> the maximum cosine similarity of each v ∈Eq with vectors in Ed,
> and combine the outputs via summation. Besides cosine, we also
> evaluate squared L2 distance as a measure of vector similarity. Intuitively, this interaction mechanism sofly searches for each query
> term tq—in a manner that reflects its context in the query—against
> the document’s embeddings, quantifying the strength of the “match”
> via the largest similarity score between tq and a document term td. Given these term scores, it then estimates the document relevance
> by summing the matching evidence across all query terms. While more sophisticated matching is possible with other choices
> such as deep convolution and atention layers (i.e., as in typical
> interaction-focused models), a summation of maximum similarity
> computations has two distinctive characteristics. First, it stands
> out as a particularly cheap interaction mechanism, as we examine
> its FLOPs in §4.2. Second, and more importantly, it is amenable
> to highly-efficient pruning for top-k retrieval, as we evaluate in
> §4.3. Tis enables using vector-similarity algorithms for skipping
> documents without materializing the full interaction matrix or even
> considering each document in isolation. Other cheap choices (e.g.,
> a summation of average similarity scores, instead of maximum) are
> possible; however, many are less amenable to pruning. In §4.4, we
> conduct an extensive ablation study that empirically verifies the advantage of our MaxSim-based late interaction against alternatives. 3.2
> Qery & Document Encoders
> Prior to late interaction, ColBERT encodes each query or document
> into a bag of embeddings, employing BERT-based encoders.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 8, section UNKNOWN

Chunk `8148e6079133b9f8ec2e84701c8a7fe871c324c58fbb16bfc1668da5839fb009`; source `arxiv:2104.08663`; paper_aggregation rank 10 similarity 0.7182868719100952 rerank None

> BM25
> +CE
> docT5query
> ColBERT
> TAS-B
> GenQ
> ANCE
> SPARTA
> DPR
> DeepCT
> -20
> -10
> BM25
> 10
> 20
> 16
> 12
> 9
> 8
> 6
> 4
> 2
> 1
> 0
> -2
> -6
> -9
> -10
> -12
> -14
> -16
> -17
> -18
> Figure 3: Comparison of zero-shot neural retrieval performances with BM25. Re-ranking based models, i.e.,
> BM25+CE and sparse model: docT5query outperform
> BM25 on more than half the BEIR evaluation datasets. 0
> 100
> 200
> 300
> 400
> 500
> TREC-COVID [58]
> TAS-B
> ANCE
> 0
> 100
> 200
> 300
> 400
> 500
> Touché-2020 [5]
> TAS-B
> ANCE
> Figure 4: Distribution plots [22] for top-10 retrieved
> document lengths (in words) using TAS-B (blue, top)
> or ANCE (orange, bottom). TAS-B has a preference
> towards shorter documents in BEIR. 7. Does domain adaptation help improve generalization of dense-retrievers? We evaluated
> GenQ, which further fine-tunes the TAS-B model on synthetic query data. It outperforms the TAS-B
> model on specialized domains like scientific publications, finance or StackExchange. On broader and
> more generic domains, like Wikipedia, it performs weaker than the original TAS-B model. 5.1
> Efficiency: Retrieval Latency and Index Sizes
> Models need to potentially compare a single query against millions of documents at inference, hence,
> a high computational speed for retrieving results in real-time is desired. Besides speed, index sizes
> are vital and are often stored entirely in memory. We randomly sample 1 million documents from
> DBPedia [21] and evaluate latency. For dense models, we use exact search, while for ColBERT we
> follow the original setup [32] and use approximate nearest neighbor search. Performances on CPU
> were measured with an 8 core Intel Xeon Platinum 8168 CPU @ 2.70GHz and on GPU using a single
> Nvidia Tesla V100, CUDA 11.0. DBPedia [21] (1 Million)
> Retrieval Latency
> Index
> Rank
> Model
> Dim. GPU
> CPU
> Size
> (1)
> BM25+CE
> –
> 450ms
> 6100ms
> 0.4GB
> (2)
> ColBERT
> 128
> 350ms
> –
> 20GB
> (3)
> docT5query
> –
> –
> 30ms
> 0.4GB
> (4)
> BM25
> –
> –
> 20ms
> 0.4GB
> (5)
> TAS-B
> 768
> 14ms
> 125ms
> 3GB
> (6)
> GenQ
> 768
> 14ms
> 125ms
> 3GB
> (7)
> ANCE
> 768
> 20ms
> 275ms
> 3GB
> (8)
> SPARTA
> 2000
> –
> 20ms
> 12GB
> (9)
> DeepCT
> –
> –
> 25ms
> 0.4GB
> (10)
> DPR
> 768
> 19ms
> 230ms
> 3GB
> Table 3: Estimated average retrieval latency and
> index sizes for a single query in DBPedia [21]. Ranked from best to worst on zero-shot BEIR. Lower the latency or memory is desired.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### nlp-bert-02

How does bidirectional transformer pretraining produce contextual representations for language understanding?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 1, section UNKNOWN

Chunk `fa9340aed1650a4f15ba11215126dfa789bc0959d5d6538c8f417bad14e0ceaa`; source `arxiv:1810.04805`; faiss_cosine rank 1 similarity 0.8282355070114136 rerank None; metadata_filtered_cosine rank 1 similarity 0.8282355070114136 rerank None; paper_aggregation rank 1 similarity 0.8282355070114136 rerank None; mmr_diversity rank 1 similarity 0.8282355070114136 rerank 0.5797648549079895

> The two approaches share the
> same objective function during pre-training, where
> they use unidirectional language models to learn
> general language representations. We argue that current techniques restrict the
> power of the pre-trained representations, especially for the fine-tuning approaches. The major limitation is that standard language models are
> unidirectional, and this limits the choice of architectures that can be used during pre-training. For
> example, in OpenAI GPT, the authors use a left-toright architecture, where every token can only attend to previous tokens in the self-attention layers
> of the Transformer (Vaswani et al., 2017). Such restrictions are sub-optimal for sentence-level tasks,
> and could be very harmful when applying finetuning based approaches to token-level tasks such
> as question answering, where it is crucial to incorporate context from both directions. In this paper, we improve the fine-tuning based
> approaches by proposing BERT: Bidirectional
> Encoder
> Representations
> from
> Transformers. BERT alleviates the previously mentioned unidirectionality constraint by using a “masked language model” (MLM) pre-training objective, inspired by the Cloze task (Taylor, 1953). The
> masked language model randomly masks some of
> the tokens from the input, and the objective is to
> predict the original vocabulary id of the masked
> arXiv:1810.04805v2 [cs.CL] 24 May 2019

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 12, section UNKNOWN

Chunk `a8f6c60b445c4eb467a1f720a489928caa1ffb1e7092756fbc9aa6601a6609cd`; source `arxiv:1810.04805`; faiss_cosine rank 2 similarity 0.8180498480796814 rerank None; metadata_filtered_cosine rank 2 similarity 0.8180498480796814 rerank None; mmr_diversity rank 3 similarity 0.8180498480796814 rerank 0.27263489365577687

> for natural language understanding. In Proceedings
> of the 2018 EMNLP Workshop BlackboxNLP: Analyzing and Interpreting Neural Networks for NLP,
> pages 353–355. Wei Wang, Ming Yan, and Chen Wu. 2018b. Multigranularity hierarchical attention fusion networks
> for reading comprehension and question answering. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1:
> Long Papers). Association for Computational Linguistics. Alex Warstadt, Amanpreet Singh, and Samuel R Bowman. 2018. Neural network acceptability judgments. arXiv preprint arXiv:1805.12471. Adina Williams, Nikita Nangia, and Samuel R Bowman. 2018. A broad-coverage challenge corpus
> for sentence understanding through inference. In
> NAACL. Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V
> Le,
> Mohammad Norouzi,
> Wolfgang Macherey,
> Maxim Krikun,
> Yuan Cao,
> Qin Gao,
> Klaus
> Macherey, et al. 2016. Google’s neural machine translation system: Bridging the gap between
> human and machine translation. arXiv preprint
> arXiv:1609.08144. Jason Yosinski, Jeff Clune, Yoshua Bengio, and Hod
> Lipson. 2014. How transferable are features in deep
> neural networks? In Advances in neural information
> processing systems, pages 3320–3328. Adams Wei Yu, David Dohan, Minh-Thang Luong, Rui
> Zhao, Kai Chen, Mohammad Norouzi, and Quoc V
> Le. 2018. QANet: Combining local convolution
> with global self-attention for reading comprehension. In ICLR. Rowan Zellers, Yonatan Bisk, Roy Schwartz, and Yejin
> Choi. 2018. Swag: A large-scale adversarial dataset
> for grounded commonsense inference. In Proceedings of the 2018 Conference on Empirical Methods
> in Natural Language Processing (EMNLP). Yukun Zhu, Ryan Kiros, Rich Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Torralba, and Sanja
> Fidler. 2015. Aligning books and movies: Towards
> story-like visual explanations by watching movies
> and reading books. In Proceedings of the IEEE
> international conference on computer vision, pages
> 19–27. Appendix for “BERT: Pre-training of
> Deep Bidirectional Transformers for
> Language Understanding”
> We organize the appendix into three sections:
> • Additional implementation details for BERT
> are presented in Appendix A;
> • Additional details for our experiments are
> presented in Appendix B; and
> • Additional ablation studies are presented in
> Appendix C. We present additional ablation studies for
> BERT including:
> – Effect of Number of Training Steps; and
> – Ablation for Different Masking Procedures. A
> Additional Details for BERT
> A.1
> Illustration of the Pre-training Tasks
> We provide examples of the pre-training tasks in
> the following.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 8, section UNKNOWN

Chunk `9e8b608e901d6547f3e8ef83c8ddb3569ff12ef22fb645a9c570e4bfbe74393e`; source `arxiv:1810.04805`; faiss_cosine rank 3 similarity 0.8103311061859131 rerank None; metadata_filtered_cosine rank 3 similarity 0.8103311061859131 rerank None; mmr_diversity rank 4 similarity 0.8103311061859131 rerank 0.2672317743301391

> The BiLSTM hurts
> performance on the GLUE tasks. We recognize that it would also be possible to
> train separate LTR and RTL models and represent
> each token as the concatenation of the two models, as ELMo does. However: (a) this is twice as
> expensive as a single bidirectional model; (b) this
> is non-intuitive for tasks like QA, since the RTL
> model would not be able to condition the answer
> on the question; (c) this it is strictly less powerful
> than a deep bidirectional model, since it can use
> both left and right context at every layer. 5.2
> Effect of Model Size
> In this section, we explore the effect of model size
> on fine-tuning task accuracy. We trained a number
> of BERT models with a differing number of layers,
> hidden units, and attention heads, while otherwise
> using the same hyperparameters and training procedure as described previously. Results on selected GLUE tasks are shown in
> Table 6. In this table, we report the average Dev
> Set accuracy from 5 random restarts of fine-tuning. We can see that larger models lead to a strict accuracy improvement across all four datasets, even
> for MRPC which only has 3,600 labeled training examples, and is substantially different from
> the pre-training tasks. It is also perhaps surprising that we are able to achieve such significant
> improvements on top of models which are already quite large relative to the existing literature. For example, the largest Transformer explored in
> Vaswani et al. (2017) is (L=6, H=1024, A=16)
> with 100M parameters for the encoder, and the
> largest Transformer we have found in the literature
> is (L=64, H=512, A=2) with 235M parameters
> (Al-Rfou et al., 2018). By contrast, BERTBASE
> contains 110M parameters and BERTLARGE contains 340M parameters. It has long been known that increasing the
> model size will lead to continual improvements
> on large-scale tasks such as machine translation
> and language modeling, which is demonstrated
> by the LM perplexity of held-out training data
> shown in Table 6. However, we believe that
> this is the first work to demonstrate convincingly that scaling to extreme model sizes also
> leads to large improvements on very small scale
> tasks, provided that the model has been sufficiently pre-trained. Peters et al. (2018b) presented

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 11, section UNKNOWN

Chunk `2e966bb434bd8439f4d799fbdcbfa458f09a7c0c53ff5a037f049ac31b3b225c`; source `arxiv:1810.04805`; faiss_cosine rank 4 similarity 0.8090724349021912 rerank None; metadata_filtered_cosine rank 4 similarity 0.8090724349021912 rerank None; mmr_diversity rank 5 similarity 0.8090724349021912 rerank 0.26635070443153375

> Mandar Joshi, Eunsol Choi, Daniel S Weld, and Luke
> Zettlemoyer. 2017. Triviaqa: A large scale distantly
> supervised challenge dataset for reading comprehension. In ACL. Ryan Kiros, Yukun Zhu, Ruslan R Salakhutdinov,
> Richard Zemel, Raquel Urtasun, Antonio Torralba,
> and Sanja Fidler. 2015. Skip-thought vectors. In
> Advances in neural information processing systems,
> pages 3294–3302. Quoc Le and Tomas Mikolov. 2014. Distributed representations of sentences and documents. In International Conference on Machine Learning, pages
> 1188–1196. Hector J Levesque, Ernest Davis, and Leora Morgenstern. 2011. The winograd schema challenge. In
> Aaai spring symposium: Logical formalizations of
> commonsense reasoning, volume 46, page 47. Lajanugen Logeswaran and Honglak Lee. 2018. An
> efficient framework for learning sentence representations. In International Conference on Learning
> Representations. Bryan McCann, James Bradbury, Caiming Xiong, and
> Richard Socher. 2017. Learned in translation: Contextualized word vectors. In NIPS. Oren Melamud, Jacob Goldberger, and Ido Dagan. 2016. context2vec: Learning generic context embedding with bidirectional LSTM. In CoNLL. Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S Corrado, and Jeff Dean. 2013. Distributed representations of words and phrases and their compositionality. In Advances in Neural Information Processing
> Systems 26, pages 3111–3119. Curran Associates,
> Inc. Andriy Mnih and Geoffrey E Hinton. 2009. A scalable hierarchical distributed language model. In
> D. Koller, D. Schuurmans, Y. Bengio, and L. Bottou, editors, Advances in Neural Information Processing Systems 21, pages 1081–1088. Curran Associates, Inc. Ankur P Parikh, Oscar T ̈ackstr ̈om, Dipanjan Das, and
> Jakob Uszkoreit. 2016. A decomposable attention
> model for natural language inference. In EMNLP. Jeffrey Pennington, Richard Socher, and Christopher D. Manning. 2014. Glove: Global vectors for
> word representation. In Empirical Methods in Natural Language Processing (EMNLP), pages 1532–
> 1543. Matthew Peters, Waleed Ammar, Chandra Bhagavatula, and Russell Power. 2017. Semi-supervised sequence tagging with bidirectional language models. In ACL. Matthew Peters, Mark Neumann, Mohit Iyyer, Matt
> Gardner, Christopher Clark, Kenton Lee, and Luke
> Zettlemoyer. 2018a. Deep contextualized word representations. In NAACL. Matthew Peters, Mark Neumann, Luke Zettlemoyer,
> and Wen-tau Yih. 2018b. Dissecting contextual
> word embeddings: Architecture and representation. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, pages
> 1499–1509. Alec Radford, Karthik Narasimhan, Tim Salimans, and
> Ilya Sutskever. 2018. Improving language understanding with unsupervised learning. Technical report, OpenAI. Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and
> Percy Liang. 2016. Squad: 100,000+ questions for
> machine comprehension of text. In Proceedings of
> the 2016 Conference on Empirical Methods in Natural Language Processing, pages 2383–2392.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 11, section UNKNOWN

Chunk `62830aae7b2e71398df62a687bbd740b75a116290767e84160cad7a66ecc4982`; source `arxiv:1810.04805`; faiss_cosine rank 5 similarity 0.8084112405776978 rerank None; metadata_filtered_cosine rank 5 similarity 0.8084112405776978 rerank None; mmr_diversity rank 6 similarity 0.8084112405776978 rerank 0.2658878684043884

> 2018. Improving language understanding with unsupervised learning. Technical report, OpenAI. Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and
> Percy Liang. 2016. Squad: 100,000+ questions for
> machine comprehension of text. In Proceedings of
> the 2016 Conference on Empirical Methods in Natural Language Processing, pages 2383–2392. Minjoon Seo, Aniruddha Kembhavi, Ali Farhadi, and
> Hannaneh Hajishirzi. 2017. Bidirectional attention
> flow for machine comprehension. In ICLR. Richard Socher, Alex Perelygin, Jean Wu, Jason
> Chuang, Christopher D Manning, Andrew Ng, and
> Christopher Potts. 2013. Recursive deep models
> for semantic compositionality over a sentiment treebank. In Proceedings of the 2013 conference on
> empirical methods in natural language processing,
> pages 1631–1642. Fu Sun, Linyang Li, Xipeng Qiu, and Yang Liu. 2018. U-net:
> Machine reading comprehension
> with unanswerable questions. arXiv preprint
> arXiv:1810.06638. Wilson L Taylor. 1953. Cloze procedure:
> A new
> tool for measuring readability. Journalism Bulletin,
> 30(4):415–433. Erik F Tjong Kim Sang and Fien De Meulder. 2003. Introduction to the conll-2003 shared task:
> Language-independent named entity recognition. In
> CoNLL. Joseph Turian, Lev Ratinov, and Yoshua Bengio. 2010. Word representations: A simple and general method
> for semi-supervised learning. In Proceedings of the
> 48th Annual Meeting of the Association for Computational Linguistics, ACL ’10, pages 384–394. Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
> Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz
> Kaiser, and Illia Polosukhin. 2017. Attention is all
> you need. In Advances in Neural Information Processing Systems, pages 6000–6010. Pascal Vincent, Hugo Larochelle, Yoshua Bengio, and
> Pierre-Antoine Manzagol. 2008. Extracting and
> composing robust features with denoising autoencoders. In Proceedings of the 25th international
> conference on Machine learning, pages 1096–1103. ACM. Alex Wang, Amanpreet Singh, Julian Michael, Felix Hill, Omer Levy, and Samuel Bowman. 2018a. Glue: A multi-task benchmark and analysis platform

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 10, section References

Chunk `44a66d2bdbabe7c12a33ae5a95b47242d5fb4519f92a1e1d0d7d732305f3e870`; source `arxiv:1810.04805`; faiss_cosine rank 6 similarity 0.8081873655319214 rerank None; metadata_filtered_cosine rank 6 similarity 0.8081873655319214 rerank None; mmr_diversity rank 7 similarity 0.8081873655319214 rerank 0.26573115587234486

> References
> Alan Akbik, Duncan Blythe, and Roland Vollgraf. 2018. Contextual string embeddings for sequence
> labeling. In Proceedings of the 27th International
> Conference on Computational Linguistics, pages
> 1638–1649. Rami Al-Rfou, Dokook Choe, Noah Constant, Mandy
> Guo, and Llion Jones. 2018. Character-level language modeling with deeper self-attention. arXiv
> preprint arXiv:1808.04444. Rie Kubota Ando and Tong Zhang. 2005. A framework
> for learning predictive structures from multiple tasks
> and unlabeled data. Journal of Machine Learning
> Research, 6(Nov):1817–1853. Luisa Bentivogli,
> Bernardo Magnini,
> Ido Dagan,
> Hoa Trang Dang, and Danilo Giampiccolo. 2009. The fifth PASCAL recognizing textual entailment
> challenge. In TAC. NIST. John Blitzer, Ryan McDonald, and Fernando Pereira. 2006. Domain adaptation with structural correspondence learning. In Proceedings of the 2006 conference on empirical methods in natural language processing, pages 120–128. Association for Computational Linguistics. Samuel R. Bowman, Gabor Angeli, Christopher Potts,
> and Christopher D. Manning. 2015. A large annotated corpus for learning natural language inference. In EMNLP. Association for Computational Linguistics. Peter F Brown, Peter V Desouza, Robert L Mercer,
> Vincent J Della Pietra, and Jenifer C Lai. 1992. Class-based n-gram models of natural language. Computational linguistics, 18(4):467–479. Daniel Cer, Mona Diab, Eneko Agirre, Inigo LopezGazpio, and Lucia Specia. 2017. Semeval-2017
> task 1: Semantic textual similarity multilingual and
> crosslingual focused evaluation. In Proceedings
> of the 11th International Workshop on Semantic
> Evaluation (SemEval-2017), pages 1–14, Vancouver, Canada. Association for Computational Linguistics. Ciprian Chelba, Tomas Mikolov, Mike Schuster, Qi Ge,
> Thorsten Brants, Phillipp Koehn, and Tony Robinson. 2013. One billion word benchmark for measuring progress in statistical language modeling. arXiv
> preprint arXiv:1312.3005. Z. Chen, H. Zhang, X. Zhang, and L. Zhao. 2018. Quora question pairs. Christopher Clark and Matt Gardner. 2018. Simple
> and effective multi-paragraph reading comprehension. In ACL. Kevin Clark, Minh-Thang Luong, Christopher D Manning, and Quoc Le. 2018. Semi-supervised sequence modeling with cross-view training. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, pages 1914–
> 1925. Ronan Collobert and Jason Weston. 2008. A unified
> architecture for natural language processing: Deep
> neural networks with multitask learning. In Proceedings of the 25th international conference on
> Machine learning, pages 160–167. ACM. Alexis Conneau, Douwe Kiela, Holger Schwenk, Lo ̈ıc
> Barrault, and Antoine Bordes. 2017. Supervised
> learning of universal sentence representations from
> natural language inference data. In Proceedings of
> the 2017 Conference on Empirical Methods in Natural Language Processing, pages 670–680, Copenhagen, Denmark. Association for Computational
> Linguistics. Andrew M Dai and Quoc V Le. 2015.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 9, section UNKNOWN

Chunk `acf33779a9a85c43d564cad705be361388853f3bcc8f1685247900b05e9e16e1`; source `arxiv:1810.04805`; faiss_cosine rank 7 similarity 0.807227611541748 rerank None; metadata_filtered_cosine rank 7 similarity 0.807227611541748 rerank None; mmr_diversity rank 8 similarity 0.807227611541748 rerank 0.2650593280792235

> #L = the
> number of layers; #H = hidden size; #A = number of attention heads. “LM (ppl)” is the masked LM perplexity
> of held-out training data. System
> Dev F1 Test F1
> ELMo (Peters et al., 2018a)
> 95.7
> 92.2
> CVT (Clark et al., 2018)
> -
> 92.6
> CSE (Akbik et al., 2018)
> -
> 93.1
> Fine-tuning approach
> BERTLARGE
> 96.6
> 92.8
> BERTBASE
> 96.4
> 92.4
> Feature-based approach (BERTBASE)
> Embeddings
> 91.0
> -
> Second-to-Last Hidden
> 95.6
> -
> Last Hidden
> 94.9
> -
> Weighted Sum Last Four Hidden
> 95.9
> -
> Concat Last Four Hidden
> 96.1
> -
> Weighted Sum All 12 Layers
> 95.5
> -
> Table 7: CoNLL-2003 Named Entity Recognition results. Hyperparameters were selected using the Dev
> set. The reported Dev and Test scores are averaged over
> 5 random restarts using those hyperparameters. layer in the output. We use the representation of
> the first sub-token as the input to the token-level
> classifier over the NER label set. To ablate the fine-tuning approach, we apply the
> feature-based approach by extracting the activations from one or more layers without fine-tuning
> any parameters of BERT. These contextual embeddings are used as input to a randomly initialized two-layer 768-dimensional BiLSTM before
> the classification layer. Results are presented in Table 7. BERTLARGE
> performs competitively with state-of-the-art methods. The best performing method concatenates the
> token representations from the top four hidden layers of the pre-trained Transformer, which is only
> 0.3 F1 behind fine-tuning the entire model. This
> demonstrates that BERT is effective for both finetuning and feature-based approaches. 6
> Conclusion
> Recent empirical improvements due to transfer
> learning with language models have demonstrated
> that rich, unsupervised pre-training is an integral
> part of many language understanding systems. In
> particular, these results enable even low-resource
> tasks to benefit from deep unidirectional architectures. Our major contribution is further generalizing these findings to deep bidirectional architectures, allowing the same pre-trained model to successfully tackle a broad set of NLP tasks.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 3, section UNKNOWN

Chunk `fa699eb3c5cddedd61a30dd13c1d093b7e0803f121ac1f670c7ef5dd4bb2b5d4`; source `arxiv:1810.04805`; faiss_cosine rank 8 similarity 0.8053969144821167 rerank None; metadata_filtered_cosine rank 8 similarity 0.8053969144821167 rerank None; mmr_diversity rank 9 similarity 0.8053969144821167 rerank 0.2637778401374816

> BERT
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Question
> Paragraph
> Start/End Span
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Masked Sentence A
> Masked Sentence B
> Pre-training
> Fine-Tuning
> NSP
> Mask LM
> Mask LM
> Unlabeled Sentence A and B Pair 
> SQuAD
> Question Answer Pair
> NER
> MNLI
> Figure 1: Overall pre-training and fine-tuning procedures for BERT. Apart from output layers, the same architectures are used in both pre-training and fine-tuning. The same pre-trained model parameters are used to initialize
> models for different down-stream tasks. During fine-tuning, all parameters are fine-tuned. [CLS] is a special
> symbol added in front of every input example, and [SEP] is a special separator token (e.g. separating questions/answers). ing and auto-encoder objectives have been used
> for pre-training such models (Howard and Ruder,
> 2018; Radford et al., 2018; Dai and Le, 2015). 2.3
> Transfer Learning from Supervised Data
> There has also been work showing effective transfer from supervised tasks with large datasets, such
> as natural language inference (Conneau et al.,
> 2017) and machine translation (McCann et al.,
> 2017). Computer vision research has also demonstrated the importance of transfer learning from
> large pre-trained models, where an effective recipe
> is to fine-tune models pre-trained with ImageNet (Deng et al., 2009; Yosinski et al., 2014). 3
> BERT
> We introduce BERT and its detailed implementation in this section. There are two steps in our
> framework: pre-training and fine-tuning. During pre-training, the model is trained on unlabeled
> data over different pre-training tasks. For finetuning, the BERT model is first initialized with
> the pre-trained parameters, and all of the parameters are fine-tuned using labeled data from the
> downstream tasks. Each downstream task has separate fine-tuned models, even though they are initialized with the same pre-trained parameters. The
> question-answering example in Figure 1 will serve
> as a running example for this section. A distinctive feature of BERT is its unified architecture across different tasks. There is minimal difference between the pre-trained architecture and the final downstream architecture.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 6, section UNKNOWN

Chunk `b0c755805932d49f45f08e6f3dccdf1b29ef04b47bfcbb1b8a18703e915651e8`; source `arxiv:1810.04805`; faiss_cosine rank 9 similarity 0.8053790926933289 rerank None; metadata_filtered_cosine rank 9 similarity 0.8053790926933289 rerank None; mmr_diversity rank 10 similarity 0.8053790926933289 rerank 0.2637653648853301

> System
> MNLI-(m/mm)
> QQP
> QNLI
> SST-2
> CoLA
> STS-B
> MRPC
> RTE
> Average
> 392k
> 363k
> 108k
> 67k
> 8.5k
> 5.7k
> 3.5k
> 2.5k
> -
> Pre-OpenAI SOTA
> 80.6/80.1
> 66.1
> 82.3
> 93.2
> 35.0
> 81.0
> 86.0
> 61.7
> 74.0
> BiLSTM+ELMo+Attn
> 76.4/76.1
> 64.8
> 79.8
> 90.4
> 36.0
> 73.3
> 84.9
> 56.8
> 71.0
> OpenAI GPT
> 82.1/81.4
> 70.3
> 87.4
> 91.3
> 45.4
> 80.0
> 82.3
> 56.0
> 75.1
> BERTBASE
> 84.6/83.4
> 71.2
> 90.5
> 93.5
> 52.1
> 85.8
> 88.9
> 66.4
> 79.6
> BERTLARGE
> 86.7/85.9
> 72.1
> 92.7
> 94.9
> 60.5
> 86.5
> 89.3
> 70.1
> 82.1
> Table 1: GLUE Test results, scored by the evaluation server (https://gluebenchmark.com/leaderboard). The number below each task denotes the number of training examples. The “Average” column is slightly different
> than the official GLUE score, since we exclude the problematic WNLI set.8 BERT and OpenAI GPT are singlemodel, single task. F1 scores are reported for QQP and MRPC, Spearman correlations are reported for STS-B, and
> accuracy scores are reported for the other tasks. We exclude entries that use BERT as one of their components. We use a batch size of 32 and fine-tune for 3
> epochs over the data for all GLUE tasks. For each
> task, we selected the best fine-tuning learning rate
> (among 5e-5, 4e-5, 3e-5, and 2e-5) on the Dev set. Additionally, for BERTLARGE we found that finetuning was sometimes unstable on small datasets,
> so we ran several random restarts and selected the
> best model on the Dev set. With random restarts,
> we use the same pre-trained checkpoint but perform different fine-tuning data shuffling and classifier layer initialization.9
> Results are presented in Table 1. Both
> BERTBASE and BERTLARGE outperform all systems on all tasks by a substantial margin, obtaining
> 4.5% and 7.0% respective average accuracy improvement over the prior state of the art. Note that
> BERTBASE and OpenAI GPT are nearly identical
> in terms of model architecture apart from the attention masking. For the largest and most widely
> reported GLUE task, MNLI, BERT obtains a 4.6%
> absolute accuracy improvement. On the official
> GLUE leaderboard10, BERTLARGE obtains a score
> of 80.5, compared to OpenAI GPT, which obtains
> 72.8 as of the date of writing. We find that BERTLARGE significantly outperforms BERTBASE across all tasks, especially those
> with very little training data. The effect of model
> size is explored more thoroughly in Section 5.2. 4.2
> SQuAD v1.1
> The
> Stanford
> Question
> Answering
> Dataset
> (SQuAD v1.1) is a collection of 100k crowdsourced question/answer pairs (Rajpurkar et al.,
> 2016).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 13, section UNKNOWN

Chunk `ae0c9e5bcd08c27a8c8965a36449e6b1a16b51a66fa1d9eb4c034aedeffa176f`; source `arxiv:1810.04805`; faiss_cosine rank 10 similarity 0.8053458333015442 rerank None; metadata_filtered_cosine rank 10 similarity 0.8053458333015442 rerank None

> BERT (Ours)
> Trm
> Trm
> Trm
> Trm
> Trm
> Trm
> ... ... Trm
> Trm
> Trm
> Trm
> Trm
> Trm
> ... ... OpenAI GPT
> Lstm
> ELMo
> Lstm
> Lstm
> Lstm
> Lstm
> Lstm
> Lstm
> Lstm
> Lstm
> Lstm
> Lstm
> Lstm
>  T1
> T2
>  TN
> ... ... ... ... ... E1
> E2
>  EN
> ... T1
> T2
> TN
> ... E1
> E2
>  EN
> ... T1
> T2
>  TN
> ... E1
> E2
>  EN
> ... Figure 3: Differences in pre-training model architectures. BERT uses a bidirectional Transformer. OpenAI GPT
> uses a left-to-right Transformer. ELMo uses the concatenation of independently trained left-to-right and right-toleft LSTMs to generate features for downstream tasks. Among the three, only BERT representations are jointly
> conditioned on both left and right context in all layers. In addition to the architecture differences, BERT and
> OpenAI GPT are fine-tuning approaches, while ELMo is a feature-based approach. to converge. In Section C.1 we demonstrate that
> MLM does converge marginally slower than a leftto-right model (which predicts every token), but
> the empirical improvements of the MLM model
> far outweigh the increased training cost. Next Sentence Prediction
> The next sentence
> prediction task can be illustrated in the following
> examples. Input = [CLS] the man went to [MASK] store [SEP]
> he bought a gallon [MASK] milk [SEP]
> Label = IsNext
> Input = [CLS] the man [MASK] to the store [SEP]
> penguin [MASK] are flight ##less birds [SEP]
> Label = NotNext
> A.2
> Pre-training Procedure
> To generate each training input sequence, we sample two spans of text from the corpus, which we
> refer to as “sentences” even though they are typically much longer than single sentences (but can
> be shorter also). The first sentence receives the A
> embedding and the second receives the B embedding. 50% of the time B is the actual next sentence
> that follows A and 50% of the time it is a random
> sentence, which is done for the “next sentence prediction” task. They are sampled such that the combined length is ≤512 tokens. The LM masking is
> applied after WordPiece tokenization with a uniform masking rate of 15%, and no special consideration given to partial word pieces. We train with batch size of 256 sequences (256
> sequences * 512 tokens = 128,000 tokens/batch)
> for 1,000,000 steps, which is approximately 40
> epochs over the 3.3 billion word corpus.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 9, section UNKNOWN

Chunk `e4c664d8069367afd383cc4603c5d4c66ade54d601249970eb6671b4e0946b6f`; source `arxiv:1706.03762`; paper_aggregation rank 2 similarity 0.7944087982177734 rerank None; mmr_diversity rank 2 similarity 0.7944087982177734 rerank 0.28307240009307855

> This task presents specific challenges: the output is subject to strong structural
> constraints and is significantly longer than the input. Furthermore, RNN sequence-to-sequence
> models have not been able to attain state-of-the-art results in small-data regimes [37]. We trained a 4-layer transformer with dmodel = 1024 on the Wall Street Journal (WSJ) portion of the
> Penn Treebank [25], about 40K training sentences. We also trained it in a semi-supervised setting,
> using the larger high-confidence and BerkleyParser corpora from with approximately 17M sentences
> [37]. We used a vocabulary of 16K tokens for the WSJ only setting and a vocabulary of 32K tokens
> for the semi-supervised setting. We performed only a small number of experiments to select the dropout, both attention and residual
> (section 5.4), learning rates and beam size on the Section 22 development set, all other parameters
> remained unchanged from the English-to-German base translation model. During inference, we
> 9

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 10, section UNKNOWN

Chunk `009965ae2e5d5bf9e5311e46e9fda7e6cd0aa90cc1de57383d40ff94162a2ac5`; source `arxiv:2005.11401`; paper_aggregation rank 3 similarity 0.7666534185409546 rerank None

> Springer, 2015. URL https://link.springer.com/chapter/10.1007%
> 2F978-3-319-24027-5_20. [3] Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. Semantic Parsing on Freebase
> from Question-Answer Pairs. In Proceedings of the 2013 Conference on Empirical Methods
> in Natural Language Processing, pages 1533–1544, Seattle, Washington, USA, October 2013. Association for Computational Linguistics. URL http://www.aclweb.org/anthology/
> D13-1160. [4] Bin Bi, Chenliang Li, Chen Wu, Ming Yan, and Wei Wang. Palm: Pre-training an autoencoding&autoregressive language model for context-conditioned generation. ArXiv, abs/2004.07159,
> 2020. URL https://arxiv.org/abs/2004.07159. [5] Danqi Chen, Adam Fisch, Jason Weston, and Antoine Bordes. Reading Wikipedia to Answer
> Open-Domain Questions. In Proceedings of the 55th Annual Meeting of the Association for
> Computational Linguistics (Volume 1: Long Papers), pages 1870–1879, Vancouver, Canada,
> July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1171. URL
> https://www.aclweb.org/anthology/P17-1171. [6] Eunsol Choi, Daniel Hewlett, Jakob Uszkoreit, Illia Polosukhin, Alexandre Lacoste, and
> Jonathan Berant. Coarse-to-fine question answering for long documents. In Proceedings of the
> 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
> pages 209–220, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi:
> 10.18653/v1/P17-1020. URL https://www.aclweb.org/anthology/P17-1020. 10

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 1, section UNKNOWN

Chunk `0031a8c654b940aec72e634b44d1f532aefc5b355b54ec0bc447c81144091d4f`; source `arxiv:1903.10676`; paper_aggregation rank 4 similarity 0.7553359270095825 rerank None

> SCIBERT is a pretrained language model based on BERT but trained
> on a large corpus of scientific text. (ii) We perform extensive experimentation to
> investigate the performance of finetuning versus task-specific architectures atop frozen embeddings, and the effect of having an in-domain vocabulary. (iii) We evaluate SCIBERT on a suite of tasks
> in the scientific domain, and achieve new state-ofthe-art (SOTA) results on many of these tasks. 2
> Methods
> Background
> The
> BERT
> model
> architecture
> (Devlin et al., 2019) is based on a multilayer bidirectional Transformer (Vaswani et al., 2017). Instead of the traditional left-to-right language modeling objective, BERT is trained on two tasks: predicting randomly masked tokens and predicting
> whether two sentences follow each other. SCIBERT follows the same architecture as BERT but is
> instead pretrained on scientific text. Vocabulary
> BERT uses WordPiece (Wu et al.,
> 2016) for unsupervised tokenization of the input
> text. The vocabulary is built such that it contains
> the most frequently used words or subword units. We refer to the original vocabulary released with

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 7, section UNKNOWN

Chunk `1869c59ea2d0d7dc271a684c00164828e67ae3e7b97941e0123a54a108c63ac5`; source `arxiv:1512.03385`; paper_aggregation rank 5 similarity 0.7447400689125061 rerank None

> The deep plain nets suffer from increased depth,
> and exhibit higher training error when going deeper. This
> phenomenon is similar to that on ImageNet (fig. 4, left) and
> on MNIST (see [42]), suggesting that such an optimization
> difficulty is a fundamental problem. fig. 6 (middle) shows the behaviors of ResNets. Also
> similar to the ImageNet cases (fig. 4, right), our ResNets
> manage to overcome the optimization difficulty and demonstrate accuracy gains when the depth increases. We further explore n = 18 that leads to a 110-layer
> ResNet. In this case, we find that the initial learning rate
> of 0.1 is slightly too large to start converging5. So we use
> 0.01 to warm up the training until the training error is below
> 80% (about 400 iterations), and then go back to 0.1 and continue training. The rest of the learning schedule is as done
> previously. This 110-layer network converges well (fig. 6,
> middle). It has fewer parameters than other deep and thin
> 5With an initial learning rate of 0.1, it starts converging (<90% error)
> after several epochs, but still reaches similar accuracy. 7

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 3, section UNKNOWN

Chunk `5e503ef1d99a78cd350e19c5a8899dcceccd7e3955ca5a7dcd6950444ee1ad58`; source `arxiv:1609.02907`; paper_aggregation rank 6 similarity 0.7429403066635132 rerank None

> ˆA ReLU

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 5, section UNKNOWN

Chunk `2c65293e316e2e2f8763a5a9ef2e1f336f29cf695913d66aa34bfe3009a79d51`; source `arxiv:1710.10903`; paper_aggregation rank 7 similarity 0.7412468194961548 rerank None

> Published as a conference paper at ICLR 2018
> all nodes. No eigendecompositions or similar costly matrix operations are required. The
> time complexity of a single GAT attention head computing F ′ features may be expressed
> as O(|V |FF ′ + |E|F ′), where F is the number of input features, and |V | and |E| are the
> numbers of nodes and edges in the graph, respectively. This complexity is on par with
> the baseline methods such as Graph Convolutional Networks (GCNs) (Kipf & Welling,
> 2017). Applying multi-head attention multiplies the storage and parameter requirements
> by a factor of K, while the individual heads’ computations are fully independent and can
> be parallelized. • As opposed to GCNs, our model allows for (implicitly) assigning different importances to
> nodes of a same neighborhood, enabling a leap in model capacity. Furthermore, analyzing
> the learned attentional weights may lead to benefits in interpretability, as was the case in
> the machine translation domain (e.g. the qualitative analysis of Bahdanau et al. (2015)). • The attention mechanism is applied in a shared manner to all edges in the graph, and therefore it does not depend on upfront access to the global graph structure or (features of) all of
> its nodes (a limitation of many prior techniques). This has several desirable implications:
> – The graph is not required to be undirected (we may simply leave out computing αij if
> edge j →i is not present). – It makes our technique directly applicable to inductive learning—including tasks
> where the model is evaluated on graphs that are completely unseen during training. • The recently published inductive method of Hamilton et al. (2017) samples a fixed-size
> neighborhood of each node, in order to keep its computational footprint consistent; this
> does not allow it access to the entirety of the neighborhood while performing inference. Moreover, this technique achieved some of its strongest results when an LSTM (Hochreiter
> & Schmidhuber, 1997)-based neighborhood aggregator is used. This assumes the existence
> of a consistent sequential node ordering across neighborhoods, and the authors have rectified it by consistently feeding randomly-ordered sequences to the LSTM. Our technique
> does not suffer from either of these issues—it works with the entirety of the neighborhood
> (at the expense of a variable computational footprint, which is still on-par with methods
> like the GCN), and does not assume any ordering within it.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 6, section UNKNOWN

Chunk `83d02e42ef72cdcbfbcc1703e7ef7b4229d88dbce9af220c9b45cc5741edd1b1`; source `arxiv:2004.04906`; paper_aggregation rank 8 similarity 0.7390421628952026 rerank None

> 50.0
> 63.3
> 74.8
> Gold
> 7

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 4, section UNKNOWN

Chunk `542f67896add4417df24665a10ebc2d6030f04028398609993b4976acc0feb48`; source `arxiv:2004.12832`; paper_aggregation rank 9 similarity 0.7284733057022095 rerank None

> Even though ColBERT’s late-interaction framework can be applied to a wide variety of architectures (e.g., CNNs, RNNs, transformers, etc.), we choose to focus this work on bi-directional transformerbased encoders (i.e., BERT) owing to their state-of-the-art effectiveness yet very high computational cost. 3.1
> Architecture
> Figure 3 depicts the general architecture of ColBERT, which comprises: (a) a query encoder fQ, (b) a document encoder fD, and (c)
> the late interaction mechanism. Given a query q and document d,
> fQ encodes q into a bag of fixed-size embeddings Eq while fD encodes d into another bag Ed. Crucially, each embeddings in Eq and
> Ed is contextualized based on the other terms in q or d, respectively. We describe our BERT-based encoders in §3.2. Using Eq and Ed, ColBERT computes the relevance score between q and d via late interaction, which we define as a summation
> of maximum similarity (MaxSim) operators. In particular, we find
> the maximum cosine similarity of each v ∈Eq with vectors in Ed,
> and combine the outputs via summation. Besides cosine, we also
> evaluate squared L2 distance as a measure of vector similarity. Intuitively, this interaction mechanism sofly searches for each query
> term tq—in a manner that reflects its context in the query—against
> the document’s embeddings, quantifying the strength of the “match”
> via the largest similarity score between tq and a document term td. Given these term scores, it then estimates the document relevance
> by summing the matching evidence across all query terms. While more sophisticated matching is possible with other choices
> such as deep convolution and atention layers (i.e., as in typical
> interaction-focused models), a summation of maximum similarity
> computations has two distinctive characteristics. First, it stands
> out as a particularly cheap interaction mechanism, as we examine
> its FLOPs in §4.2. Second, and more importantly, it is amenable
> to highly-efficient pruning for top-k retrieval, as we evaluate in
> §4.3. Tis enables using vector-similarity algorithms for skipping
> documents without materializing the full interaction matrix or even
> considering each document in isolation. Other cheap choices (e.g.,
> a summation of average similarity scores, instead of maximum) are
> possible; however, many are less amenable to pruning. In §4.4, we
> conduct an extensive ablation study that empirically verifies the advantage of our MaxSim-based late interaction against alternatives. 3.2
> Qery & Document Encoders
> Prior to late interaction, ColBERT encodes each query or document
> into a bag of embeddings, employing BERT-based encoders.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 5, section UNKNOWN

Chunk `83ea73cf6a63ef8b5b62c893992b80a5839edd8ac5cf7809013cc84c2de4d7e0`; source `arxiv:2104.08663`; paper_aggregation rank 10 similarity 0.705150306224823 rerank None

> Decision support metrics such as Precision and Recall which are both rank unaware
> are not suitable. Binary rank-aware metrics such as MRR (Mean Reciprocal Rate) and MAP (Mean
> Average Precision) fail to evaluate tasks with graded relevance judgements. We find that Normalised
> Cumulative Discount Gain (nDCG@k) provides a good balance suitable for both tasks involving
> binary and graded relevance judgements. We refer the reader to Wang et al. [71] for understanding
> the theoretical advantages of the metric. For our experiments, we utilize the Python interface of the
> official TREC evaluation tool [63] and compute nDCG@10 for all datasets. 4
> Experimental Setup
> We use BEIR to compare diverse, recent, state-of-the-art retrieval architectures with a focus on
> transformer-based neural approaches. We evaluate on publicly available pre-trained checkpoints,
> which we provide in Table 6. Due to the length limitations of transformer-based networks, we use
> only the first 512 word pieces within all documents in our experiments across all neural architectures. We group the models based on their architecture: (i) lexical, (ii) sparse, (iii) dense, (iv) late-interaction,
> and (v) re-ranking. Besides the included models, the BEIR benchmark is model agnostic and in future
> different model configurations can be easily incorporated within the benchmark. (i) Lexical Retrieval: (a) BM25 [55] is a commonly-used bag-of-words retrieval function based on
> token-matching between two high-dimensional sparse vectors with TF-IDF token weights. We use
> Anserini [36] with the default Lucene parameters (k=0.9 and b=0.4). We index the title (if available)
> and passage as separate fields for documents. In our leaderboard, we also tested Elasticsearch BM25
> and Anserini + RM3 expansion, but found Anserini BM25 to perform the best. 5

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### nlp-scientific-03

What changes are needed to pretrain language models effectively on scientific publications?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 5, section UNKNOWN

Chunk `d5a1a6356609841ece7fbf6d0a0536a8a781f968ceb0976667e21c9a6d4f5dc1`; source `arxiv:1903.10676`; faiss_cosine rank 1 similarity 0.7866581082344055 rerank None; metadata_filtered_cosine rank 1 similarity 0.7866581082344055 rerank None; paper_aggregation rank 1 similarity 0.7866581082344055 rerank None; mmr_diversity rank 1 similarity 0.7866581082344055 rerank 0.5506606757640838

> 2018. Construction of the literature graph in semantic scholar. In NAACL. Arman
> Cohan,
> Waleed
> Ammar,
> Madeleine
> van
> Zuylen,
> and
> Field
> Cady. 2019. Structural scaffolds for citation intent classification in scientific public
> In NAACL-HLT, pages 3586–3596, Minneapolis,
> Minnesota. Association for Computational Linguistics. Nigel Collier and Jin-Dong Kim. 2004. Introduction
> to the bio-entity recognition task at jnlpba. In NLPBA/BioNLP. Tim
> Dettmers. 2019. TPUs
> vs
> GPUs
> for
> Transformers
> (BERT). http://timdettmers.com/2018/10/17/tpus-vs-gpus
> Accessed: 2019-02-22. Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
> Kristina Toutanova. 2019. BERT: Pre-training of
> deep bidirectional transformers for language understanding. In NAACL-HLT. Rezarta Islamaj Dogan, Robert Leaman, and Zhiyong
> Lu. 2014. NCBI disease corpus: A resource for disease name recognition and concept normalization. Journal of biomedical informatics, 47:1–10. Timothy Dozat and Christopher D. Manning. 2017. Deep biaffine attention for neural dependency parsing. ICLR. Matt Gardner, Joel Grus, Mark Neumann, Oyvind
> Tafjord, Pradeep Dasigi, Nelson F. Liu, Matthew
> Peters, Michael Schmitz, and Luke S. Zettlemoyer. 2017. Allennlp: A deep semantic natural language
> processing platform. In arXiv:1803.07640. Jeremy Howard and Sebastian Ruder. 2018. Universal
> language model fine-tuning for text classification. In
> ACL. Kexin Huang, Jaan Altosaar, and Rajesh Ranganath. 2019. Clinicalbert: Modeling clinical notes and predicting hospital readmission. arXiv:1904.05342. Alistair e. W. Johnson, Tom J. Pollard aand Lu Shen,
> Liwei
> H. Lehman,
> Mengling
> Feng,
> Mohammad Ghassemi, Benjamin Moody, Peter Szolovits,
> Leo Anthony Celi, , and Roger g. Mark. 2016.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 5, section UNKNOWN

Chunk `da8f408fc72cbfc67233d77f126bad748dacb4637e21261e9f0ce0a1137d9b4b`; source `arxiv:1903.10676`; faiss_cosine rank 2 similarity 0.783585786819458 rerank None; metadata_filtered_cosine rank 2 similarity 0.783585786819458 rerank None; mmr_diversity rank 5 similarity 0.783585786819458 rerank 0.24851005077362054

> main, we observe +0.76 F1 for biomedical tasks,
> +0.61 F1 for computer science tasks, and +0.11 F1
> for multidomain tasks. Given the disjoint vocabularies (Section 2) and
> the magnitude of improvement over BERT-Base
> (Section 4), we suspect that while an in-domain
> vocabulary is helpful, SCIBERT benefits most
> from the scientific corpus pretraining. 6
> Related Work
> Recent work on domain adaptation of BERT includes BIOBERT (Lee et al., 2019) and CLINICALBERT (Alsentzer et al., 2019; Huang et al.,
> 2019). BIOBERT is trained on PubMed abstracts and PMC full text articles, and CLINICALBERT is trained on clinical text from the
> MIMIC-III database (Johnson et al., 2016). In
> contrast, SCIBERT is trained on the full text of
> 1.14M biomedical and computer science papers
> from the Semantic Scholar corpus (Ammar et al.,
> 2018). Furthermore, SCIBERT uses an in-domain
> vocabulary (SCIVOCAB) while the other abovementioned models use the original BERT vocabulary (BASEVOCAB). 7
> Conclusion and Future Work
> We released SCIBERT, a pretrained language
> model for scientific text based on BERT. We evaluated SCIBERT on a suite of tasks and datasets from
> scientific domains. SCIBERT significantly outperformed BERT-Base and achieves new SOTA results on several of these tasks, even compared to
> some reported BIOBERT (Lee et al., 2019) results
> on biomedical tasks. For future work, we will release a version of
> SCIBERT analogous to BERT-Large, as well as experiment with different proportions of papers from
> each domain. Because these language models are
> costly to train, we aim to build a single resource
> that’s useful across multiple domains. Acknowledgment
> We thank the anonymous reviewers for their comments and suggestions. We also thank Waleed
> Ammar, Noah Smith, Yoav Goldberg, Daniel
> King, Doug Downey, and Dan Weld for their helpful discussions and feedback. All experiments
> were performed on beaker.org and supported
> in part by credits from Google Cloud. References
> Emily Alsentzer, John R. Murphy, Willie Boag, WeiHung Weng, Di Jin, Tristan Naumann, and Matthew
> B. A. McDermott. 2019. Publicly available clinical bert embeddings. In ClinicalNLP workshop at
> NAACL. Waleed Ammar, Dirk Groeneveld, Chandra Bhagavatula, Iz Beltagy, Miles Crawford, Doug Downey, Jason Dunkelberger, Ahmed Elgohary, Sergey Feldman, Vu Ha, Rodney Kinney, Sebastian Kohlmeier,
> Kyle Lo, Tyler Murray, Hsu-Han Ooi, Matthew Peters, Joanna Power, Sam Skjonsberg, Lucy Lu Wang,
> Chris Wilhelm, Zheng Yuan, Madeleine van Zuylen,
> and Oren Etzioni. 2018. Construction of the literature graph in semantic scholar. In NAACL. Arman
> Cohan,
> Waleed
> Ammar,
> Madeleine
> van
> Zuylen,
> and
> Field
> Cady. 2019.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 1, section UNKNOWN

Chunk `5d58d2108f38d79111c103aaa31814acb345dbf17afa089c15667fc3d7f4f221`; source `arxiv:1903.10676`; faiss_cosine rank 3 similarity 0.7835094332695007 rerank None; metadata_filtered_cosine rank 3 similarity 0.7835094332695007 rerank None; mmr_diversity rank 6 similarity 0.7835094332695007 rerank 0.24845660328865038

> arXiv:1903.10676v3 [cs.CL] 10 Sep 2019
> SCIBERT: A Pretrained Language Model for Scientific Text
> Iz Beltagy
> Kyle Lo
> Arman Cohan
> Allen Institute for Artificial Intelligence, Seattle, WA, USA
> {beltagy,kylel,armanc}@allenai.org
> Abstract
> Obtaining large-scale annotated data for NLP
> tasks in the scientific domain is challenging and expensive. We release SCIBERT,
> a
> pretrained
> language
> model
> based
> on
> BERT (Devlin et al., 2019) to address the lack
> of high-quality, large-scale labeled scientific
> data. SCIBERT
> leverages
> unsupervised
> pretraining on a large multi-domain corpus
> of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including
> sequence tagging, sentence classification and
> dependency parsing, with datasets from a
> variety of scientific domains. We demonstrate statistically significant improvements
> over BERT and achieve new state-of-theart results on several of these tasks. The
> code and pretrained models are available at
> https://github.com/allenai/scibert/. 1
> Introduction
> The exponential increase in the volume of scientific publications in the past decades has made
> NLP an essential tool for large-scale knowledge
> extraction and machine reading of these documents. Recent progress in NLP has been driven
> by the adoption of deep neural models, but training such models often requires large amounts of
> labeled data. In general domains, large-scale training data is often possible to obtain through crowdsourcing, but in scientific domains, annotated data
> is difficult and expensive to collect due to the expertise required for quality annotation. As
> shown
> through
> ELMo
> (Peters et al.,
> 2018),
> GPT
> (Radford et al.,
> 2018)
> and
> BERT (Devlin et al., 2019), unsupervised pretraining of language models on large corpora
> significantly
> improves performance
> on many
> NLP tasks. These models return contextualized
> embeddings for each token which can be passed
> into minimal task-specific neural architectures. Leveraging the success of unsupervised pretraining has become especially important especially
> when task-specific annotations are difficult to
> obtain, like in scientific NLP. Yet while both
> BERT and ELMo have released pretrained models,
> they are still trained on general domain corpora
> such as news articles and Wikipedia. In this work, we make the following contributions:
> (i) We release SCIBERT, a new resource demonstrated to improve performance on a range of NLP
> tasks in the scientific domain. SCIBERT is a pretrained language model based on BERT but trained
> on a large corpus of scientific text. (ii) We perform extensive experimentation to
> investigate the performance of finetuning versus task-specific architectures atop frozen embeddings, and the effect of having an in-domain vocabulary.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 6, section UNKNOWN

Chunk `f42c3525eb077952a1462d9dda965c751de6bba32bd081f42fc60314e93304b1`; source `arxiv:1903.10676`; faiss_cosine rank 4 similarity 0.7794519066810608 rerank None; metadata_filtered_cosine rank 4 similarity 0.7794519066810608 rerank None; mmr_diversity rank 7 similarity 0.7794519066810608 rerank 0.2456163346767425

> In EMNLP. Arnab Sinha, Zhihong Shen, Yang Song, Hao Ma, Darrin Eide, Bo-June Paul Hsu, and Kuansan Wang. 2015. An overview of microsoft academic service
> (MAS) and applications. In WWW. Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
> Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz
> Kaiser, and Illia Polosukhin. 2017. Attention is all
> you need. In NIPS. Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V. Le,
> Mohammad Norouzi,
> Wolfgang Macherey,
> Maxim Krikun, Yuan Cao, Qin Gao, Jeff Klingner,
> Apurva Shah,
> Melvin Johnson,
> Xiaobing Liu,
> Lukasz Kaiser, Stephan Gouws, Yoshikiyo Kato,
> Taku Kudo, Hideto Kazawa, Keith Stevens, George
> Kurian, Nishant Patil, Wei Wang, Cliff Young, Jason
> Smith, Jason Riesa, Alex Rudnick, Oriol Vinyals,
> Gregory S. Corrado, Macduff Hughes, and Jeffrey
> Dean. 2016. Google’s neural machine translation
> system: Bridging the gap between human and machine translation. abs/1609.08144. Wonjin Yoon, Chan Ho So, Jinhyuk Lee, and Jaewoo
> Kang. 2018. CollaboNet: collaboration of deep neural networks for biomedical named entity recognition. In DTMBio workshop at CIKM.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 2, section UNKNOWN

Chunk `500b06e80541b31a6410d18fca419dc7e4e6a8c1f65b7bd57d5954b3a02ca9ee`; source `arxiv:1903.10676`; faiss_cosine rank 5 similarity 0.7763820886611938 rerank None; metadata_filtered_cosine rank 5 similarity 0.7763820886611938 rerank None; mmr_diversity rank 8 similarity 0.7763820886611938 rerank 0.24346746206283565

> BERT as BASEVOCAB. We construct SCIVOCAB, a new WordPiece vocabulary on our scientific corpus using the SentencePiece1 library. We produce both cased and
> uncased vocabularies and set the vocabulary size
> to 30K to match the size of BASEVOCAB. The resulting token overlap between BASEVOCAB and
> SCIVOCAB is 42%, illustrating a substantial difference in frequently used words between scientific and general domain texts. Corpus
> We
> train
> SCIBERT
> on
> a
> random
> sample
> of
> 1.14M
> papers
> from
> Semantic
> Scholar (Ammar et al., 2018). This corpus
> consists of 18% papers from the computer science
> domain and 82% from the broad biomedical
> domain. We use the full text of the papers, not
> just the abstracts. The average paper length is
> 154 sentences (2,769 tokens) resulting in a corpus
> size of 3.17B tokens, similar to the 3.3B tokens
> on which BERT was trained. We split sentences
> using ScispaCy (Neumann et al., 2019),2 which is
> optimized for scientific text. 3
> Experimental Setup
> 3.1
> Tasks
> We experiment on the following core NLP tasks:
> 1. Named Entity Recognition (NER)
> 2. PICO Extraction (PICO)
> 3. Text Classification (CLS)
> 4. Relation Classification (REL)
> 5. Dependency Parsing (DEP)
> PICO, like NER, is a sequence labeling task where
> the model extracts spans describing the Participants, Interventions, Comparisons, and Outcomes
> in a clinical trial paper (Kim et al., 2011). REL
> is a special case of text classification where the
> model predicts the type of relation expressed between two entities, which are encapsulated in the
> sentence by inserted special tokens. 3.2
> Datasets
> For brevity, we only describe the newer datasets
> here, and refer the reader to the references in Table 1 for the older datasets. EBM-NLP (Nye et al.,
> 2018) annotates PICO spans in clinical trial abstracts. SciERC (Luan et al., 2018) annotates entities and relations from computer science ab1https://github.com/google/sentencepiece
> 2https://github.com/allenai/SciSpaCy
> stracts. ACL-ARC (Jurgens et al., 2018) and SciCite (Cohan et al., 2019) assign intent labels (e.g.
> Comparison, Extension, etc.) to sentences from
> scientific papers that cite other papers. The Paper
> Field dataset is built from the Microsoft Academic
> Graph (Sinha et al., 2015)3 and maps paper titles
> to one of 7 fields of study. Each field of study
> (i.e. geography, politics, economics, business, sociology, medicine, and psychology) has approximately 12K training examples. 3.3
> Pretrained BERT Variants
> BERT-Base
> We use the pretrained weights for
> BERT-Base (Devlin et al., 2019) released with the
> original BERT code.4 The vocabulary is BASEVOCAB.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 4, section UNKNOWN

Chunk `88c0b4ab21070dd8600e466ddcb4dc4a784ad46113f0a69e6a97a45ab845fb4b`; source `arxiv:1903.10676`; faiss_cosine rank 6 similarity 0.7730863094329834 rerank None; metadata_filtered_cosine rank 6 similarity 0.7730863094329834 rerank None; mmr_diversity rank 9 similarity 0.7730863094329834 rerank 0.2411604166030883

> Field
> Task
> Dataset
> SOTA
> BERT-Base
> SCIBERT
> Frozen
> Finetune
> Frozen
> Finetune
> Bio
> NER
> BC5CDR (Li et al., 2016)
> 88.857
> 85.08
> 86.72
> 88.73
> 90.01
> JNLPBA (Collier and Kim, 2004)
> 78.58
> 74.05
> 76.09
> 75.77
> 77.28
> NCBI-disease (Dogan et al., 2014)
> 89.36
> 84.06
> 86.88
> 86.39
> 88.57
> PICO
> EBM-NLP (Nye et al., 2018)
> 66.30
> 61.44
> 71.53
> 68.30
> 72.28
> DEP
> GENIA (Kim et al., 2003) - LAS
> 91.92
> 90.22
> 90.33
> 90.36
> 90.43
> GENIA (Kim et al., 2003) - UAS
> 92.84
> 91.84
> 91.89
> 92.00
> 91.99
> REL
> ChemProt (Kringelum et al., 2016)
> 76.68
> 68.21
> 79.14
> 75.03
> 83.64
> CS
> NER
> SciERC (Luan et al., 2018)
> 64.20
> 63.58
> 65.24
> 65.77
> 67.57
> REL
> SciERC (Luan et al., 2018)
> n/a
> 72.74
> 78.71
> 75.25
> 79.97
> CLS
> ACL-ARC (Jurgens et al., 2018)
> 67.9
> 62.04
> 63.91
> 60.74
> 70.98
> Multi
> CLS
> Paper Field
> n/a
> 63.64
> 65.37
> 64.38
> 65.71
> SciCite (Cohan et al., 2019)
> 84.0
> 84.31
> 84.85
> 85.42
> 85.49
> Average
> 73.58
> 77.16
> 76.01
> 79.27
> Table 1: Test performances of all BERT variants on all tasks and datasets. Bold indicates the SOTA result (multiple
> results bolded if difference within 95% bootstrap confidence interval). Keeping with past work, we report macro
> F1 scores for NER (span-level), macro F1 scores for REL and CLS (sentence-level), and macro F1 for PICO
> (token-level), and micro F1 for ChemProt specifically. For DEP, we report labeled (LAS) and unlabeled (UAS)
> attachment scores (excluding punctuation) for the same model with hyperparameters tuned for LAS. All results
> are the average of multiple runs with different random seeds. Task
> Dataset
> BIOBERT
> SCIBERT
> NER
> BC5CDR
> 88.85
> 90.01
> JNLPBA
> 77.59
> 77.28
> NCBI-disease
> 89.36
> 88.57
> REL
> ChemProt
> 76.68
> 83.64
> Table 2:
> Comparing SCIBERT with the reported
> BIOBERT results on biomedical datasets. BC5CDR and ChemProt, and performs similarly
> on JNLPBA despite being trained on a substantially smaller biomedical corpus. 4.2
> Computer Science Domain
> We observe that SCIBERT outperforms BERTBase on computer science tasks (+3.55 F1 with
> finetuning and +1.13 F1 without). In addition,
> SCIBERT achieves new SOTA results on ACLARC (Cohan et al., 2019), and the NER part of
> SciERC (Luan et al., 2018). For relations in SciERC, our results are not comparable with those in
> Luan et al. (2018) because we are performing relation classification given gold entities, while they
> perform joint entity and relation extraction. 4.3
> Multiple Domains
> We observe that SCIBERT outperforms BERTBase on the multidomain tasks (+0.49 F1 with
> finetuning and +0.93 F1 without). In addition, SCIBERT outperforms the SOTA on SciCite (Cohan et al., 2019).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 14, section UNKNOWN

Chunk `f7f46d59ca966b0002a03869ab70bd6b3a2a74387ed5f895f57768ad7347463b`; source `arxiv:2005.11401`; faiss_cosine rank 7 similarity 0.7725571393966675 rerank None; metadata_filtered_cosine rank 7 similarity 0.7725571393966675 rerank None; paper_aggregation rank 2 similarity 0.7725571393966675 rerank None; mmr_diversity rank 2 similarity 0.7725571393966675 rerank 0.2765346705913543

> How much knowledge can you pack into
> the parameters of a language model? arXiv e-prints, 2020. URL https://arxiv.org/abs/
> 2002.08910. [53] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: Bm25 and
> beyond. Found. Trends Inf. Retr., 3(4):333–389, April 2009. ISSN 1554-0669. doi: 10.1561/
> 1500000019. URL https://doi.org/10.1561/1500000019. [54] Irene Solaiman, Miles Brundage, Jack Clark, Amanda Askell, Ariel Herbert-Voss, Jeff Wu, Alec
> Radford, and Jian-Bing Wang. Release strategies and the social impacts of language models. ArXiv, abs/1908.09203, 2019. [55] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors, Advances
> in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates, Inc., 2015. URL http://papers.nips.cc/paper/5846-end-to-end-memory-networks.pdf. 14

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 2, section UNKNOWN

Chunk `ed137c27e0396f4c9f9d1a7190da5c02a6368e18627ca9e36cc763fed70f83af`; source `arxiv:1903.10676`; faiss_cosine rank 8 similarity 0.7725446224212646 rerank None; metadata_filtered_cosine rank 8 similarity 0.7725446224212646 rerank None; mmr_diversity rank 10 similarity 0.7725446224212646 rerank 0.2407812356948852

> Each field of study
> (i.e. geography, politics, economics, business, sociology, medicine, and psychology) has approximately 12K training examples. 3.3
> Pretrained BERT Variants
> BERT-Base
> We use the pretrained weights for
> BERT-Base (Devlin et al., 2019) released with the
> original BERT code.4 The vocabulary is BASEVOCAB. We evaluate both cased and uncased versions of this model. SCIBERT
> We use the original BERT code to
> train SCIBERT on our corpus with the same configuration and size as BERT-Base. We train 4
> different versions of SCIBERT: (i) cased or uncased and (ii) BASEVOCAB or SCIVOCAB. The
> two models that use BASEVOCAB are finetuned
> from the corresponding BERT-Base models. The
> other two models that use the new SCIVOCAB are
> trained from scratch. Pretraining BERT for long sentences can be
> slow. Following the original BERT code, we set a
> maximum sentence length of 128 tokens, and train
> the model until the training loss stops decreasing. We then continue training the model allowing sentence lengths up to 512 tokens. We use a single TPU v3 with 8 cores. Training
> the SCIVOCAB models from scratch on our corpus
> takes 1 week5 (5 days with max length 128, then
> 2 days with max length 512). The BASEVOCAB
> models take 2 fewer days of training because they
> aren’t trained from scratch. All pretrained BERT models are converted to
> be compatible with PyTorch using the pytorchtransformers library.6
> All our models (Sections 3.4 and 3.5) are implemented in PyTorch using AllenNLP (Gardner et al., 2017). Casing
> We follow Devlin et al. (2019) in using
> the cased models for NER and the uncased models
> 3https://academic.microsoft.com/
> 4https://github.com/google-research/bert
> 5BERT’s largest model was trained on 16 Cloud TPUs for
> 4 days. Expected 40-70 days (Dettmers, 2019) on an 8-GPU
> machine. 6https://github.com/huggingface/pytorch-transformers

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 6, section UNKNOWN

Chunk `2ff8932a0256a68cc20776ae21b6b7de4f17faaa4e8e96bbcac8addc4443f324`; source `arxiv:1903.10676`; faiss_cosine rank 9 similarity 0.7705025672912598 rerank None; metadata_filtered_cosine rank 9 similarity 0.7705025672912598 rerank None

> Mimic-iii, a freely accessible critical care database. In Scientific Data, 3:160035. David Jurgens, Srijan Kumar, Raine Hoover, Daniel A. McFarland, and Daniel Jurafsky. 2018. Measuring
> the evolution of a scientific field through citation
> frames. TACL, 06:391–406. Jin-Dong Kim, Tomoko Ohta, Yuka Tateisi, and
> Jun’ichi Tsujii. 2003. GENIA corpus - a semantically annotated corpus for bio-textmining. Bioinformatics, 19:i180i182. Su Kim, David Mart ́ınez, Lawrence Cavedon, and Lars
> Yencken. 2011. Automatic classification of sentences to support evidence based medicine. In BMC
> Bioinformatics. Diederik P. Kingma and Jimmy Ba. 2015. Adam: A
> method for stochastic optimization. ICLR. Jens Kringelum, Sonny Kim Kjærulff, Søren Brunak,
> Ole Lund, Tudor i. Oprea, and Olivier Taboureau. 2016. ChemProt-3.0: a global chemical biology diseases mapping. In Database. Jinhyuk
> Lee,
> Wonjin
> Yoon,
> Sungdong
> Kim,
> Donghyeon Kim,
> Sunkyu Kim,
> Chan Ho So,
> and Jaewoo Kang. 2019. BioBERT: a pre-trained
> biomedical
> language
> representation
> model
> for
> biomedical text mining. In arXiv:1901.08746. Jiao Li, Yueping Sun, Robin J. Johnson, Daniela Sciaky, Chih-Hsuan Wei, Robert Leaman, Allan Peter
> Davis, Carolyn J. Mattingly, Thomas C. Wiegers,
> and Zhiyong Lu. 2016. BioCreative V CDR task
> corpus: a resource for chemical disease relation
> extraction. Database : the journal of biological
> databases and curation. Yi Luan, Luheng He, Mari Ostendorf, and Hannaneh
> Hajishirzi. 2018. Multi-task identification of entities, relations, and coreference for scientific knowledge graph construction. In EMNLP. Mark Neumann, Daniel King, Iz Beltagy, and Waleed
> Ammar. 2019. ScispaCy: Fast and robust models for biomedical natural language processing. In
> arXiv:1902.07669. Dat Quoc Nguyen and Karin M. Verspoor. 2019. From
> pos tagging to dependency parsing for biomedical
> event extraction. BMC Bioinformatics, 20:1–13. Benjamin Nye, Junyi Jessy Li, Roma Patel, Yinfei
> Yang, Iain James Marshall, Ani Nenkova, and Byron C. Wallace. 2018. A corpus with multi-level annotations of patients, interventions and outcomes to
> support language processing for medical literature. In ACL. Matthew e. Peters, Mark Neumann, Mohit Iyyer,
> Matt Gardner, Christopher Clark, Kenton Lee, and
> Luke S. Zettlemoyer. 2018. Deep contextualized
> word representations. In NAACL-HLT. Alec Radford, Karthik Narasimhan, Tim Salimans, and
> Ilya Sutskever. 2018. Improving language understanding by generative pre-training. Nils Reimers and Iryna Gurevych. 2017. Optimal hyperparameters for deep lstm-networks for sequence
> labeling tasks. In EMNLP. Arnab Sinha, Zhihong Shen, Yang Song, Hao Ma, Darrin Eide, Bo-June Paul Hsu, and Kuansan Wang. 2015. An overview of microsoft academic service
> (MAS) and applications. In WWW. Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
> Uszkoreit, Llion Jones, Aidan N.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 4, section UNKNOWN

Chunk `588a931baf5e8f0ae89f34782afbf2addac733125be7409e2639f94d7199d26b`; source `arxiv:1903.10676`; faiss_cosine rank 10 similarity 0.7679643630981445 rerank None; metadata_filtered_cosine rank 10 similarity 0.7679643630981445 rerank None

> 4.3
> Multiple Domains
> We observe that SCIBERT outperforms BERTBase on the multidomain tasks (+0.49 F1 with
> finetuning and +0.93 F1 without). In addition, SCIBERT outperforms the SOTA on SciCite (Cohan et al., 2019). No prior published
> SOTA results exist for the Paper Field dataset. 5
> Discussion
> 5.1
> Effect of Finetuning
> We observe improved results via BERT finetuning
> rather than task-specific architectures atop frozen
> embeddings (+3.25 F1 with SCIBERT and +3.58
> with BERT-Base, on average). For each scientific
> domain, we observe the largest effects of finetuning on the computer science (+5.59 F1 with SCIBERT and +3.17 F1 with BERT-Base) and biomedical tasks (+2.94 F1 with SCIBERT and +4.61 F1
> with BERT-Base), and the smallest effect on multidomain tasks (+0.7 F1 with SCIBERT and +1.14
> F1 with BERT-Base). On every dataset except
> BC5CDR and SciCite, BERT-Base with finetuning
> outperforms (or performs similarly to) a model using frozen SCIBERT embeddings. 5.2
> Effect of SCIVOCAB
> We assess the importance of an in-domain scientific vocabulary by repeating the finetuning experiments for SCIBERT with BASEVOCAB. We
> find the optimal hyperparameters for SCIBERTBASEVOCAB often coincide with those of SCIBERT-SCIVOCAB. Averaged across datasets, we observe +0.60 F1
> when using SCIVOCAB. For each scientific do-

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 4, section UNKNOWN

Chunk `5c95702ca7a2cf8c83dcb2ae7bc8d10bf83b9f4c75f6a49d5087482ee78bb276`; source `arxiv:2104.08663`; paper_aggregation rank 3 similarity 0.7459538578987122 rerank None; mmr_diversity rank 3 similarity 0.7459538578987122 rerank 0.24727578759193408

> 3-level
> —-
> 67
> 400
> 4,635,922
> 38.2
> 5.39
> 49.68
> Citation-Prediction
> Scientific
> SCIDOCS [9]

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 10, section UNKNOWN

Chunk `1fa61c1826336d0f7d1309850ae1add788abd16ddcb96e3667c4aa657c1bf984`; source `arxiv:1706.03762`; paper_aggregation rank 4 similarity 0.7413963675498962 rerank None; mmr_diversity rank 4 similarity 0.7413963675498962 rerank 0.2439644694328308

> The code we used to train and evaluate our models is available at https://github.com/
> tensorflow/tensor2tensor. Acknowledgements
> We are grateful to Nal Kalchbrenner and Stephan Gouws for their fruitful
> comments, corrections and inspiration. References
> [1] Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton. Layer normalization. arXiv preprint
> arXiv:1607.06450, 2016. [2] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. Neural machine translation by jointly
> learning to align and translate. CoRR, abs/1409.0473, 2014. [3] Denny Britz, Anna Goldie, Minh-Thang Luong, and Quoc V. Le. Massive exploration of neural
> machine translation architectures. CoRR, abs/1703.03906, 2017. [4] Jianpeng Cheng, Li Dong, and Mirella Lapata. Long short-term memory-networks for machine
> reading. arXiv preprint arXiv:1601.06733, 2016. 10

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 16, section UNKNOWN

Chunk `f6ee6fe7084fcd16c971e89355cc0020c38b119a41f61e8629bac2e3e87b8022`; source `arxiv:1810.04805`; paper_aggregation rank 5 similarity 0.7268943786621094 rerank None

> jority class. C
> Additional Ablation Studies
> C.1
> Effect of Number of Training Steps
> Figure 5 presents MNLI Dev accuracy after finetuning from a checkpoint that has been pre-trained
> for k steps. This allows us to answer the following
> questions:
> 1. Question:
> Does BERT really need such
> a large amount of pre-training (128,000
> words/batch * 1,000,000 steps) to achieve
> high fine-tuning accuracy? Answer: Yes, BERTBASE achieves almost
> 1.0% additional accuracy on MNLI when
> trained on 1M steps compared to 500k steps. 2. Question: Does MLM pre-training converge
> slower than LTR pre-training, since only 15%
> of words are predicted in each batch rather
> than every word? Answer: The MLM model does converge
> slightly slower than the LTR model. However, in terms of absolute accuracy the MLM
> model begins to outperform the LTR model
> almost immediately. C.2
> Ablation for Different Masking
> Procedures
> In Section 3.1, we mention that BERT uses a
> mixed strategy for masking the target tokens when
> pre-training with the masked language model
> (MLM) objective. The following is an ablation
> study to evaluate the effect of different masking
> strategies. 200
> 400
> 600
> 800
> 1,000
> 76
> 78
> 80
> 82
> 84
> Pre-training Steps (Thousands)
> MNLI Dev Accuracy
> BERTBASE (Masked LM)
> BERTBASE (Left-to-Right)
> Figure 5: Ablation over number of training steps. This
> shows the MNLI accuracy after fine-tuning, starting
> from model parameters that have been pre-trained for
> k steps. The x-axis is the value of k. Note that the purpose of the masking strategies
> is to reduce the mismatch between pre-training
> and fine-tuning, as the [MASK] symbol never appears during the fine-tuning stage. We report the
> Dev results for both MNLI and NER. For NER,
> we report both fine-tuning and feature-based approaches, as we expect the mismatch will be amplified for the feature-based approach as the model
> will not have the chance to adjust the representations. Masking Rates
> Dev Set Results
> MASK SAME
> RND
> MNLI
> NER
> Fine-tune Fine-tune Feature-based
> 80%
> 10%
> 10%
> 84.2
> 95.4
> 94.9
> 100%
> 0%
> 0%
> 84.3
> 94.9
> 94.0
> 80%
> 0%
> 20%
> 84.1
> 95.2
> 94.6
> 80%
> 20%
> 0%
> 84.4
> 95.2
> 94.7
> 0%
> 20%
> 80%
> 83.7
> 94.8
> 94.6
> 0%
> 0% 100%
> 83.6
> 94.9
> 94.6
> Table 8: Ablation over different masking strategies. The results are presented in Table 8.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 6, section UNKNOWN

Chunk `f52778fd5df9d8e5a74b7cb536120f46007ecd8dd5dde7374c2ef1585bb87e48`; source `arxiv:2004.04906`; paper_aggregation rank 6 similarity 0.7245553731918335 rerank None

> 51.1
> 69.1
> 80.8
> Gold
> 31

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 6, section UNKNOWN

Chunk `bcd9418b179cf36e8cb914d1a339d305a3d1eba19445abb72a8a688c942fc541`; source `arxiv:1710.10903`; paper_aggregation rank 7 similarity 0.7211630344390869 rerank None

> Published as a conference paper at ICLR 2018
> Table 1: Summary of the datasets used in our experiments. Cora
> Citeseer
> Pubmed
> PPI
> Task
> Transductive
> Transductive
> Transductive
> Inductive
> # Nodes
> 2708 (1 graph)
> 3327 (1 graph)
> 19717 (1 graph)
> 56944 (24 graphs)
> # Edges
> 5429
> 4732
> 44338
> 818716
> # Features/Node
> 1433
> 3703
> 500
> 50
> # Classes
> 7
> 6
> 3
> 121 (multilabel)
> # Training Nodes
> 140
> 120
> 60
> 44906 (20 graphs)
> # Validation Nodes
> 500
> 500
> 500
> 6514 (2 graphs)
> # Test Nodes
> 1000
> 1000
> 1000
> 5524 (2 graphs)
> well as inductive), achieving or matching state-of-the-art performance across all of them. This section summarizes our experimental setup, results, and a brief qualitative analysis of a GAT model’s
> extracted feature representations. 3.1
> DATASETS
> Transductive learning
> We utilize three standard citation network benchmark datasets—Cora,
> Citeseer and Pubmed (Sen et al., 2008)—and closely follow the transductive experimental setup of
> Yang et al. (2016). In all of these datasets, nodes correspond to documents and edges to (undirected)
> citations. Node features correspond to elements of a bag-of-words representation of a document. Each node has a class label. We allow for only 20 nodes per class to be used for training—however,
> honoring the transductive setup, the training algorithm has access to all of the nodes’ feature vectors. The predictive power of the trained models is evaluated on 1000 test nodes, and we use 500
> additional nodes for validation purposes (the same ones as used by Kipf & Welling (2017)). The
> Cora dataset contains 2708 nodes, 5429 edges, 7 classes and 1433 features per node. The Citeseer
> dataset contains 3327 nodes, 4732 edges, 6 classes and 3703 features per node. The Pubmed dataset
> contains 19717 nodes, 44338 edges, 3 classes and 500 features per node. Inductive learning
> We make use of a protein-protein interaction (PPI) dataset that consists of
> graphs corresponding to different human tissues (Zitnik & Leskovec, 2017). The dataset contains
> 20 graphs for training, 2 for validation and 2 for testing. Critically, testing graphs remain completely unobserved during training. To construct the graphs, we used the preprocessed data provided
> by Hamilton et al. (2017). The average number of nodes per graph is 2372. Each node has 50
> features that are composed of positional gene sets, motif gene sets and immunological signatures.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 8, section UNKNOWN

Chunk `337e42a3db00091a409d561fcbda9d3407105b8874ff01ff24d006c7537d6035`; source `arxiv:1512.03385`; paper_aggregation rank 8 similarity 0.7147998213768005 rerank None

> ResNet-20
> ResNet-32
> ResNet-44
> ResNet-56
> ResNet-110
> 56-layer
> 20-layer
> 110-layer
> 20-layer
> 4
> 5
> 6
> 0
> 1
> 5
> 10
> 20
> iter. (1e4)
> error (%)

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 1, section UNKNOWN

Chunk `5d6e32be40a6b0f1e43bce42b00ca8078785054df8f24ddd38648fbe58ec0ea0`; source `arxiv:2004.12832`; paper_aggregation rank 9 similarity 0.711269736289978 rerank None

> ColBERT: Efficient and Effective Passage Search via
> Contextualized Late Interaction over BERT
> Omar Khatab
> Stanford University
> okhatab@stanford.edu
> Matei Zaharia
> Stanford University
> matei@cs.stanford.edu
> ABSTRACT
> Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed
> to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs
> increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query–document pair
> through a massive neural network to compute a single relevance
> score. To tackle this, we present ColBERT, a novel ranking model
> that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then
> employs a cheap yet powerful interaction step that models their
> fine-grained similarity. By delaying and yet retaining this finegranular interaction, ColBERT can leverage the expressiveness of
> deep LMs while simultaneously gaining the ability to pre-compute
> document representations offline, considerably speeding up query
> processing. Beyond reducing the cost of re-ranking the documents
> retrieved by a traditional model, ColBERT’s pruning-friendly interaction mechanism enables leveraging vector-similarity indexes
> for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search
> datasets. Results show that ColBERT’s effectiveness is competitive
> with existing BERT-based models (and outperforms every nonBERT baseline), while executing two orders-of-magnitude faster
> and requiring four orders-of-magnitude fewer FLOPs per query. ACM Reference format:
> Omar Khatab and Matei Zaharia. 2020. ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. In Proceedings
> of Proceedings of the 43rd International ACM SIGIR Conference on Research
> and Development in Information Retrieval, Virtual Event, China, July 25–30,
> 2020 (SIGIR ’20), 10 pages. DOI: 10.1145/3397271.3401075
> 1
> INTRODUCTION
> Over the past few years, the Information Retrieval (IR) community
> has witnessed the introduction of a host of neural ranking models,
> including DRMM [7], KNRM [4, 36], and Duet [20, 22]. In contrast
> Permission to make digital or hard copies of all or part of this work for personal or
> classroom use is granted without fee provided that copies are not made or distributed
> for profit or commercial advantage and that copies bear this notice and the full citation
> on the first page. Copyrights for components of this work owned by others than the
> author(s) must be honored. Abstracting with credit is permited.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 14, section UNKNOWN

Chunk `aecac117a3f6e37c31b97e62615c4821eadd1634758980f19d83d48eb7a9d17a`; source `arxiv:1609.02907`; paper_aggregation rank 10 similarity 0.7091061472892761 rerank None

> ̃D−1
> 2 ̃A ̃D−1
> 2 H(l)W (l)
> + H(l) . (14)
> On each cross-validation split, we train for 400 epochs (without early stopping) using the Adam
> optimizer (Kingma & Ba, 2015) with a learning rate of 0.01. Other hyperparameters are chosen as
> follows: 0.5 (dropout rate, first and last layer), 5 · 10−4 (L2 regularization, first layer), 16 (number
> of units for each hidden layer) and 0.01 (learning rate). Results are summarized in Figure 5. 1
> 2
> 3
> 4
> 5
> 6
> 7
> 8
> 9
> 10
> Number of layers
> 0.50
> 0.55
> 0.60
> 0.65
> 0.70
> 0.75
> 0.80
> 0.85
> 0.90
> Accuracy
> Citeseer
> Train
> Train (Residual)
> Test
> Test (Residual)
> 1
> 2
> 3
> 4
> 5
> 6
> 7
> 8
> 9
> 10
> Number of layers
> 0.55
> 0.60
> 0.65
> 0.70
> 0.75
> 0.80
> 0.85
> 0.90
> 0.95
> Accuracy
> Cora
> Train
> Train (Residual)
> Test
> Test (Residual)
> 1
> 2
> 3
> 4
> 5
> 6
> 7
> 8
> 9
> 10
> Number of layers
> 0.76
> 0.78
> 0.80
> 0.82
> 0.84
> 0.86
> 0.88
> Accuracy
> Pubmed
> Train
> Train (Residual)
> Test
> Test (Residual)
> Figure 5: Influence of model depth (number of layers) on classification performance. Markers
> denote mean classification accuracy (training vs. testing) for 5-fold cross-validation. Shaded areas
> denote standard error. We show results both for a standard GCN model (dashed lines) and a model
> with added residual connections (He et al., 2016) between hidden layers (solid lines). For the datasets considered here, best results are obtained with a 2- or 3-layer model. We observe
> that for models deeper than 7 layers, training without the use of residual connections can become
> difficult, as the effective context size for each node increases by the size of its Kth-order neighborhood (for a model with K layers) with each additional layer. Furthermore, overfitting can become
> an issue as the number of parameters increases with model depth. 14

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### ir-dense-04

How can dense passage representations retrieve evidence for open-domain question answering?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 1, section UNKNOWN

Chunk `8e256b826c036d04fc0cd4cbaa6a88232612b5f8f6040c59a5f7ce57d6bd96c2`; source `arxiv:2004.04906`; faiss_cosine rank 1 similarity 0.8357921242713928 rerank None; metadata_filtered_cosine rank 1 similarity 0.8357921242713928 rerank None; paper_aggregation rank 1 similarity 0.8357921242713928 rerank None; mmr_diversity rank 1 similarity 0.8357921242713928 rerank 0.585054486989975

> Conversely, the dense, latent semantic encoding is complementary to sparse representations by design. For
> example, synonyms or paraphrases that consist of
> completely different tokens may still be mapped to
> vectors close to each other. Consider the question
> “Who is the bad guy in lord of the rings?”, which can
> be answered from the context “Sala Baker is best
> known for portraying the villain Sauron in the Lord
> of the Rings trilogy.” A term-based system would
> have difficulty retrieving such a context, while
> a dense retrieval system would be able to better
> match “bad guy” with “villain” and fetch the correct context. Dense encodings are also learnable
> by adjusting the embedding functions, which provides additional flexibility to have a task-specific
> representation. With special in-memory data structures and indexing schemes, retrieval can be done
> efficiently using maximum inner product search
> (MIPS) algorithms (e.g., Shrivastava and Li (2014);
> Guo et al. (2016)). However, it is generally believed that learning a good dense vector representation needs a
> large number of labeled pairs of question and contexts. Dense retrieval methods have thus never
> be shown to outperform TF-IDF/BM25 for opendomain QA before ORQA (Lee et al., 2019), which
> proposes a sophisticated inverse cloze task (ICT)
> objective, predicting the blocks that contain the
> masked sentence, for additional pretraining. The
> question encoder and the reader model are then finetuned using pairs of questions and answers jointly. Although ORQA successfully demonstrates that
> dense retrieval can outperform BM25, setting new
> state-of-the-art results on multiple open-domain
> arXiv:2004.04906v3 [cs.CL] 30 Sep 2020

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 10, section UNKNOWN

Chunk `f8acd754640f96b0f41c9f309f7a4b103b6d444c8364e5a7ac0c90b006d3c06d`; source `arxiv:2004.04906`; faiss_cosine rank 2 similarity 0.8309302926063538 rerank None; metadata_filtered_cosine rank 2 similarity 0.8309302926063538 rerank None; mmr_diversity rank 3 similarity 0.8309302926063538 rerank 0.2816512048244475

> question-answer pairs. In Empirical Methods in Natural Language Processing (EMNLP). Jane Bromley, Isabelle Guyon, Yann LeCun, Eduard
> S ̈ackinger, and Roopak Shah. 1994. Signature verification using a “Siamese” time delay neural network. In NIPS, pages 737–744. Chris Burges, Tal Shaked, Erin Renshaw, Ari Lazier,
> Matt Deeds, Nicole Hamilton, and Greg Hullender. 2005. Learning to rank using gradient descent. In
> Proceedings of the 22nd international conference on
> Machine learning, pages 89–96. Danqi Chen, Adam Fisch, Jason Weston, and Antoine
> Bordes. 2017. Reading Wikipedia to answer opendomain questions. In Association for Computational Linguistics (ACL), pages 1870–1879. Rajarshi Das, Shehzaad Dhuliawala, Manzil Zaheer,
> and Andrew McCallum. 2019. Multi-step retrieverreader interaction for scalable open-domain question
> answering. In International Conference on Learning Representations (ICLR). Scott Deerwester, Susan T Dumais, George W Furnas, Thomas K Landauer, and Richard Harshman. 1990. Indexing by latent semantic analysis. Journal of the American society for information science,
> 41(6):391–407. Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
> Kristina Toutanova. 2019. BERT: Pre-training of
> deep bidirectional transformers for language understanding. In North American Association for Computational Linguistics (NAACL). David A Ferrucci. 2012. Introduction to “This is Watson”. IBM Journal of Research and Development,
> 56(3.4):1–1. Daniel
> Gillick,
> Sayali
> Kulkarni,
> Larry
> Lansing,
> Alessandro Presta, Jason Baldridge, Eugene Ie, and
> Diego Garcia-Olano. 2019. Learning dense representations for entity retrieval. In Computational Natural Language Learning (CoNLL). Ruiqi Guo, Sanjiv Kumar, Krzysztof Choromanski, and
> David Simcha. 2016. Quantization based fast inner
> product search. In Artificial Intelligence and Statistics, pages 482–490. Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Ming-Wei Chang. 2020. REALM:
> Retrieval-augmented language model pre-training. ArXiv, abs/2002.08909. Matthew Henderson, Rami Al-Rfou, Brian Strope, Yunhsuan Sung, L ́aszl ́o Luk ́acs, Ruiqi Guo, Sanjiv Kumar, Balint Miklos, and Ray Kurzweil. 2017. Efficient natural language response suggestion for smart
> reply. ArXiv, abs/1705.00652. Po-Sen Huang, Xiaodong He, Jianfeng Gao, Li Deng,
> Alex Acero, and Larry Heck. 2013. Learning deep
> structured semantic models for Web search using
> clickthrough data. In ACM International Conference on Information and Knowledge Management
> (CIKM), pages 2333–2338. Samuel Humeau, Kurt Shuster, Marie-Anne Lachaux,
> and Jason Weston. 2020. Poly-encoders: Architectures and pre-training strategies for fast and accurate
> multi-sentence scoring. In International Conference
> on Learning Representations (ICLR). Gautier Izacard and Edouard Grave. 2020. Leveraging
> passage retrieval with generative models for open domain question answering. ArXiv, abs/2007.01282. Jeff Johnson, Matthijs Douze, and Herv ́e J ́egou. 2017. Billion-scale similarity search with GPUs. ArXiv,
> abs/1702.08734.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 9, section UNKNOWN

Chunk `b0a4393b46edfaa665fc64fc19ce6a0d3d6f786c5b296a14be218badec60438f`; source `arxiv:2004.04906`; faiss_cosine rank 3 similarity 0.8250645399093628 rerank None; metadata_filtered_cosine rank 3 similarity 0.8250645399093628 rerank None; mmr_diversity rank 4 similarity 0.8250645399093628 rerank 0.27754517793655387

> In contrast, our model provides a simple and yet
> effective solution that shows stronger empirical performance, without relying on additional pretraining
> or complex joint training schemes. DPR has also been used as an important module in very recent work. For instance, extending
> the idea of leveraging hard negatives, Xiong et al.
> (2020a) use the retrieval model trained in the previous iteration to discover new negatives and construct a different set of examples in each training
> iteration. Starting from our trained DPR model,
> they show that the retrieval performance can be
> further improved. Recent work (Izacard and Grave,
> 2020; Lewis et al., 2020b) have also shown that
> DPR can be combined with generation models
> such as BART (Lewis et al., 2020a) and T5 (Raffel et al., 2019), achieving good performance on
> open-domain QA and other knowledge-intensive
> tasks. 8
> Conclusion
> In this work, we demonstrated that dense retrieval
> can outperform and potentially replace the traditional sparse retrieval component in open-domain
> question answering. While a simple dual-encoder
> approach can be made to work surprisingly well,
> we showed that there are some critical ingredients
> to training a dense retriever successfully. Moreover,
> our empirical analysis and ablation studies indicate
> that more complex model frameworks or similarity
> functions do not necessarily provide additional values. As a result of improved retrieval performance,
> we obtained new state-of-the-art results on multiple
> open-domain question answering benchmarks. Acknowledgments
> We thank the anonymous reviewers for their helpful
> comments and suggestions. References
> Akari Asai, Kazuma Hashimoto, Hannaneh Hajishirzi,
> Richard Socher, and Caiming Xiong. 2020. Learning to retrieve reasoning paths over Wikipedia graph
> for question answering. In International Conference
> on Learning Representations (ICLR). Petr Baudiˇs and Jan ˇSediv`y. 2015. Modeling of the
> question answering task in the yodaqa system. In International Conference of the Cross-Language Evaluation Forum for European Languages, pages 222–
> 228. Springer. Jonathan Berant, Andrew Chou, Roy Frostig, and Percy
> Liang. 2013. Semantic parsing on Freebase from

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 11, section UNKNOWN

Chunk `10581b2ea9ed1e7381096291bba0ceeadb84192718cac4ef45e1db5ff4b98550`; source `arxiv:2004.04906`; faiss_cosine rank 4 similarity 0.824959397315979 rerank None; metadata_filtered_cosine rank 4 similarity 0.824959397315979 rerank None; mmr_diversity rank 5 similarity 0.824959397315979 rerank 0.27747157812118517

> In Advances in Neural Information Processing Systems (NIPS), pages 2321–
> 2329. Ellen M Voorhees. 1999. The TREC-8 question answering track report. In TREC, volume 99, pages
> 77–82. Shuohang Wang, Mo Yu, Xiaoxiao Guo, Zhiguo Wang,
> Tim Klinger, Wei Zhang, Shiyu Chang, Gerry
> Tesauro, Bowen Zhou, and Jing Jiang. 2018. Rˆ3:
> Reinforced ranker-reader for open-domain question
> answering. In Conference on Artificial Intelligence
> (AAAI). Zhiguo Wang, Patrick Ng, Xiaofei Ma, Ramesh Nallapati, and Bing Xiang. 2019. Multi-passage BERT:
> A globally normalized bert model for open-domain
> question answering. In Empirical Methods in Natural Language Processing (EMNLP). Tomer Wolfson, Mor Geva, Ankit Gupta, Matt Gardner, Yoav Goldberg, Daniel Deutch, and Jonathan
> Berant. 2020. Break it down: A question understanding benchmark. Transactions of the Association of Computational Linguistics (TACL). Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang,
> Jialin Liu, Paul Bennett, Junaid Ahmed, and Arnold
> Overwijk. 2020a. Approximate nearest neighbor
> negative contrastive learning for dense text retrieval. ArXiv, abs/2007.00808. Wenhan Xiong, Hankang Wang, and William Yang
> Wang. 2020b. Progressively pretrained dense corpus
> index for open-domain question answering. ArXiv,
> abs/2005.00038. Wei Yang, Yuqing Xie, Aileen Lin, Xingyu Li, Luchen
> Tan, Kun Xiong, Ming Li, and Jimmy Lin. 2019a. End-to-end open-domain question answering with
> bertserini. In North American Association for Computational Linguistics (NAACL), pages 72–77. Wei Yang, Yuqing Xie, Luchen Tan, Kun Xiong, Ming
> Li, and Jimmy Lin. 2019b. Data augmentation for
> bert fine-tuning in open-domain question answering. ArXiv, abs/1904.06652. Wen-tau Yih, Kristina Toutanova, John C Platt, and
> Christopher Meek. 2011. Learning discriminative
> projections for text similarity measures. In Computational Natural Language Learning (CoNLL),
> pages 247–256.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 2, section UNKNOWN

Chunk `8cd9d2df0b1b414de28f45f2079dfe2961b97e558fc05f418ebc6aaee6050771`; source `arxiv:2004.04906`; faiss_cosine rank 5 similarity 0.8209848403930664 rerank None; metadata_filtered_cosine rank 5 similarity 0.8209848403930664 rerank None; mmr_diversity rank 6 similarity 0.8209848403930664 rerank 0.27468938827514644

> QA datasets, it also suffers from two weaknesses. First, ICT pretraining is computationally intensive
> and it is not completely clear that regular sentences
> are good surrogates of questions in the objective
> function. Second, because the context encoder is
> not fine-tuned using pairs of questions and answers,
> the corresponding representations could be suboptimal. In this paper, we address the question: can we
> train a better dense embedding model using only
> pairs of questions and passages (or answers), without additional pretraining? By leveraging the now
> standard BERT pretrained model (Devlin et al.,
> 2019) and a dual-encoder architecture (Bromley
> et al., 1994), we focus on developing the right
> training scheme using a relatively small number
> of question and passage pairs. Through a series
> of careful ablation studies, our final solution is
> surprisingly simple: the embedding is optimized
> for maximizing inner products of the question and
> relevant passage vectors, with an objective comparing all pairs of questions and passages in a batch. Our Dense Passage Retriever (DPR) is exceptionally strong. It not only outperforms BM25 by a
> large margin (65.2% vs. 42.9% in Top-5 accuracy),
> but also results in a substantial improvement on
> the end-to-end QA accuracy compared to ORQA
> (41.5% vs. 33.3%) in the open Natural Questions
> setting (Lee et al., 2019; Kwiatkowski et al., 2019). Our contributions are twofold. First, we demonstrate that with the proper training setup, simply fine-tuning the question and passage encoders
> on existing question-passage pairs is sufficient to
> greatly outperform BM25. Our empirical results
> also suggest that additional pretraining may not be
> needed. Second, we verify that, in the context of
> open-domain question answering, a higher retrieval
> precision indeed translates to a higher end-to-end
> QA accuracy. By applying a modern reader model
> to the top retrieved passages, we achieve comparable or better results on multiple QA datasets in the
> open-retrieval setting, compared to several, much
> complicated systems. 2
> Background
> The problem of open-domain QA studied in this
> paper can be described as follows. Given a factoid
> question, such as “Who first voiced Meg on Family
> Guy?” or “Where was the 8th Dalai Lama born?”, a
> system is required to answer it using a large corpus
> of diversified topics. More specifically, we assume
> the extractive QA setting, in which the answer is
> restricted to a span appearing in one or more passages in the corpus. Assume that our collection
> contains D documents, d1, d2, · · · , dD.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 1, section UNKNOWN

Chunk `ff08c347456fb2a7cd4dd19ec96aebde5d8512f0e0eb1de2733ce72f3e255c98`; source `arxiv:2004.04906`; faiss_cosine rank 6 similarity 0.8195112943649292 rerank None; metadata_filtered_cosine rank 6 similarity 0.8195112943649292 rerank None; mmr_diversity rank 7 similarity 0.8195112943649292 rerank 0.2736579060554504

> Dense Passage Retrieval for Open-Domain Question Answering
> Vladimir Karpukhin∗, Barlas O ̆guz∗, Sewon Min†, Patrick Lewis,
> Ledell Wu, Sergey Edunov, Danqi Chen‡, Wen-tau Yih
> Facebook AI
> †University of Washington
> ‡Princeton University
> {vladk, barlaso, plewis, ledell, edunov, scottyih}@fb.com
> sewon@cs.washington.edu
> danqic@cs.princeton.edu
> Abstract
> Open-domain question answering relies on efficient passage retrieval to select candidate
> contexts, where traditional sparse vector space
> models, such as TF-IDF or BM25, are the de
> facto method. In this work, we show that
> retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number
> of questions and passages by a simple dualencoder framework. When evaluated on a
> wide range of open-domain QA datasets, our
> dense retriever outperforms a strong LuceneBM25 system greatly by 9%-19% absolute in
> terms of top-20 passage retrieval accuracy, and
> helps our end-to-end QA system establish new
> state-of-the-art on multiple open-domain QA
> benchmarks.1
> 1
> Introduction
> Open-domain question answering (QA) (Voorhees,
> 1999) is a task that answers factoid questions using a large collection of documents. While early
> QA systems are often complicated and consist of
> multiple components (Ferrucci (2012); Moldovan
> et al. (2003), inter alia), the advances of reading
> comprehension models suggest a much simplified
> two-stage framework: (1) a context retriever first
> selects a small subset of passages where some
> of them contain the answer to the question, and
> then (2) a machine reader can thoroughly examine the retrieved contexts and identify the correct
> answer (Chen et al., 2017). Although reducing
> open-domain QA to machine reading is a very reasonable strategy, a huge performance degradation
> is often observed in practice2, indicating the needs
> of improving retrieval. ∗Equal contribution
> 1The code and trained models have been released at
> https://github.com/facebookresearch/DPR. 2For instance, the exact match score on SQuAD v1.1 drops
> from above 80% to less than 40% (Yang et al., 2019a). Retrieval in open-domain QA is usually implemented using TF-IDF or BM25 (Robertson and
> Zaragoza, 2009), which matches keywords efficiently with an inverted index and can be seen
> as representing the question and context in highdimensional, sparse vectors (with weighting). Conversely, the dense, latent semantic encoding is complementary to sparse representations by design. For
> example, synonyms or paraphrases that consist of
> completely different tokens may still be mapped to
> vectors close to each other.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 10, section UNKNOWN

Chunk `78b391580b2746c825258fc0b779d54b20d4c852521ee603722ec8e8671134a5`; source `arxiv:2004.04906`; faiss_cosine rank 7 similarity 0.8193849325180054 rerank None; metadata_filtered_cosine rank 7 similarity 0.8193849325180054 rerank None; mmr_diversity rank 8 similarity 0.8193849325180054 rerank 0.2735694527626037

> In International Conference
> on Learning Representations (ICLR). Gautier Izacard and Edouard Grave. 2020. Leveraging
> passage retrieval with generative models for open domain question answering. ArXiv, abs/2007.01282. Jeff Johnson, Matthijs Douze, and Herv ́e J ́egou. 2017. Billion-scale similarity search with GPUs. ArXiv,
> abs/1702.08734. Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke
> Zettlemoyer. 2017. TriviaQA: A large scale distantly supervised challenge dataset for reading comprehension. In Association for Computational Linguistics (ACL), pages 1601–1611. Omar Khattab and Matei Zaharia. 2020. ColBERT:
> Efficient and effective passage search via contextualized late interaction over BERT. In ACM SIGIR
> Conference on Research and Development in Information Retrieval (SIGIR), pages 39–48. Brian Kulis. 2013. Metric learning: A survey. Foundations and Trends in Machine Learning, 5(4):287–
> 364. Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti,
> Danielle Epstein, Illia Polosukhin, Matthew Kelcey,
> Jacob Devlin, Kenton Lee, Kristina N. Toutanova,
> Llion Jones, Ming-Wei Chang, Andrew Dai, Jakob
> Uszkoreit, Quoc Le, and Slav Petrov. 2019. Natural questions: a benchmark for question answering
> research. Transactions of the Association of Computational Linguistics (TACL). Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. 2019. Latent retrieval for weakly supervised open
> domain question answering. In Association for Computational Linguistics (ACL), pages 6086–6096. Mike
> Lewis,
> Yinhan
> Liu,
> Naman
> Goyal,
> Marjan Ghazvininejad, Abdelrahman Mohamed, Omer
> Levy, Veselin Stoyanov, and Luke Zettlemoyer. 2020a. BART: Denoising sequence-to-sequence pretraining for natural language generation, translation,
> and comprehension. In Association for Computational Linguistics (ACL), pages 7871–7880. Patrick Lewis,
> Ethan Perez,
> Aleksandara Piktus,
> Fabio Petroni, Vladimir Karpukhin, Naman Goyal,
> Heinrich
> K ̈uttler,
> Mike
> Lewis,
> Wen-tau
> Yih,
> Tim Rockt ̈aschel, Sebastian Riedel, and Douwe
> Kiela. 2020b. Retrieval-augmented generation for
> knowledge-intensive NLP tasks. In Advances in
> Neural Information Processing Systems (NeurIPS).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 2, section UNKNOWN

Chunk `e96fb0ba83f1fbf8d87d883e422b402a7f67f41f806883ffbc440cf2c1d9e389`; source `arxiv:2004.04906`; faiss_cosine rank 8 similarity 0.8180532455444336 rerank None; metadata_filtered_cosine rank 8 similarity 0.8180532455444336 rerank None; mmr_diversity rank 9 similarity 0.8180532455444336 rerank 0.2726372718811034

> 3.1
> Overview
> Our dense passage retriever (DPR) uses a dense
> encoder EP (·) which maps any text passage to a ddimensional real-valued vectors and builds an index
> for all the M passages that we will use for retrieval. 3The ideal size and boundary of a text passage are functions of both the retriever and reader. We also experimented
> with natural paragraphs in our preliminary trials and found that
> using fixed-length passages performs better in both retrieval
> and final QA accuracy, as observed by Wang et al. (2019). 4Exceptions include (Seo et al., 2019) and (Roberts et al.,
> 2020), which retrieves and generates the answers, respectively.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 9, section UNKNOWN

Chunk `c10ccdb3d73d47b4c56609b09f61f238a1be0edf56f40f6e1757a26ae2078dbf`; source `arxiv:2004.04906`; faiss_cosine rank 9 similarity 0.8169106245040894 rerank None; metadata_filtered_cosine rank 9 similarity 0.8169106245040894 rerank None; mmr_diversity rank 10 similarity 0.8169106245040894 rerank 0.27183743715286246

> been used as the standard method applied broadly
> to various QA tasks (e.g., Chen et al., 2017; Yang
> et al., 2019a,b; Nie et al., 2019; Min et al., 2019a;
> Wolfson et al., 2020). Augmenting text-based retrieval with external structured information, such
> as knowledge graph and Wikipedia hyperlinks, has
> also been explored recently (Min et al., 2019b; Asai
> et al., 2020). The use of dense vector representations for retrieval has a long history since Latent Semantic
> Analysis (Deerwester et al., 1990). Using labeled
> pairs of queries and documents, discriminatively
> trained dense encoders have become popular recently (Yih et al., 2011; Huang et al., 2013; Gillick
> et al., 2019), with applications to cross-lingual
> document retrieval, ad relevance prediction, Web
> search and entity retrieval. Such approaches complement the sparse vector methods as they can potentially give high similarity scores to semantically
> relevant text pairs, even without exact token matching. The dense representation alone, however, is
> typically inferior to the sparse one. While not the
> focus of this work, dense representations from pretrained models, along with cross-attention mechanisms, have also been shown effective in passage
> or dialogue re-ranking tasks (Nogueira and Cho,
> 2019; Humeau et al., 2020). Finally, a concurrent
> work (Khattab and Zaharia, 2020) demonstrates
> the feasibility of full dense retrieval in IR tasks. Instead of employing the dual-encoder framework,
> they introduced a late-interaction operator on top
> of the BERT encoders. Dense retrieval for open-domain QA has been
> explored by Das et al. (2019), who propose to retrieve relevant passages iteratively using reformulated question vectors. As an alternative approach
> that skips passage retrieval, Seo et al. (2019) propose to encode candidate answer phrases as vectors
> and directly retrieve the answers to the input questions efficiently. Using additional pretraining with
> the objective that matches surrogates of questions
> and relevant passages, Lee et al. (2019) jointly train
> the question encoder and reader. Their approach
> outperforms the BM25 plus reader paradigm on
> multiple open-domain QA datasets in QA accuracy,
> and is further extended by REALM (Guu et al.,
> 2020), which includes tuning the passage encoder
> asynchronously by re-indexing the passages during training. The pretraining objective has also
> recently been improved by Xiong et al. (2020b). In contrast, our model provides a simple and yet
> effective solution that shows stronger empirical performance, without relying on additional pretraining
> or complex joint training schemes. DPR has also been used as an important module in very recent work.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 8, section UNKNOWN

Chunk `9065eedc6a7292e59bf9fa03a176c523184ef9506cd09eda65ccc7bfa77bc561`; source `arxiv:2004.04906`; faiss_cosine rank 10 similarity 0.8131476044654846 rerank None; metadata_filtered_cosine rank 10 similarity 0.8131476044654846 rerank None

> Training
> Model
> NQ
> TriviaQA
> WQ
> TREC
> SQuAD
> Single
> BM25+BERT (Lee et al., 2019)
> 26.5
> 47.1
> 17.7
> 21.3
> 33.2
> Single
> ORQA (Lee et al., 2019)
> 33.3
> 45.0
> 36.4
> 30.1
> 20.2
> Single
> HardEM (Min et al., 2019a)
> 28.1
> 50.9
> -
> -
> -
> Single
> GraphRetriever (Min et al., 2019b)
> 34.5
> 56.0
> 36.4
> -
> -
> Single
> PathRetriever (Asai et al., 2020)
> 32.6
> -
> -
> -
> 56.5
> Single
> REALMWiki (Guu et al., 2020)
> 39.2
> -
> 40.2
> 46.8
> -
> Single
> REALMNews (Guu et al., 2020)
> 40.4
> -
> 40.7
> 42.9
> -
> Single
> BM25
> 32.6
> 52.4
> 29.9
> 24.9
> 38.1
> DPR
> 41.5
> 56.8
> 34.6
> 25.9
> 29.8
> BM25+DPR
> 39.0
> 57.0
> 35.2
> 28.0
> 36.7
> Multi
> DPR
> 41.5
> 56.8
> 42.4
> 49.4
> 24.1
> BM25+DPR
> 38.8
> 57.9
> 41.1
> 50.6
> 35.8
> Table 4: End-to-end QA (Exact Match) Accuracy. The first block of results are copied from their cited papers. REALMWiki and REALMNews are the same model but pretrained on Wikipedia and CC-News, respectively. Single
> and Multi denote that our Dense Passage Retriever (DPR) is trained using individual or combined training datasets
> (all except SQuAD). For WQ and TREC in the Multi setting, we fine-tune the reader trained on NQ. see that higher retriever accuracy typically leads to
> better final QA results: in all cases except SQuAD,
> answers extracted from the passages retrieved by
> DPR are more likely to be correct, compared to
> those from BM25. For large datasets like NQ and
> TriviaQA, models trained using multiple datasets
> (Multi) perform comparably to those trained using
> the individual training set (Single). Conversely,
> on smaller datasets like WQ and TREC, the multidataset setting has a clear advantage. Overall, our
> DPR-based models outperform the previous stateof-the-art results on four out of the five datasets,
> with 1% to 12% absolute differences in exact match
> accuracy. It is interesting to contrast our results to
> those of ORQA (Lee et al., 2019) and also the
> concurrently developed approach, REALM (Guu
> et al., 2020). While both methods include additional pretraining tasks and employ an expensive
> end-to-end training regime, DPR manages to outperform them on both NQ and TriviaQA, simply
> by focusing on learning a strong passage retrieval
> model using pairs of questions and answers. The
> additional pretraining tasks are likely more useful
> only when the target training sets are small. Although the results of DPR on WQ and TREC in the
> single-dataset setting are less competitive, adding
> more question–answer pairs helps boost the performance, achieving the new state of the art.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 4, section UNKNOWN

Chunk `f00274dd9f87e1d04851349f72a0a64b024ff6fa07f663b9fd57f9f5d2637055`; source `arxiv:2005.11401`; paper_aggregation rank 2 similarity 0.7658059000968933 rerank None; mmr_diversity rank 2 similarity 0.7658059000968933 rerank 0.2645367264747619

> Each Wikipedia article is split into disjoint
> 100-word chunks, to make a total of 21M documents. We use the document encoder to compute an
> embedding for each document, and build a single MIPS index using FAISS [23] with a Hierarchical
> Navigable Small World approximation for fast retrieval [37]. During training, we retrieve the top
> k documents for each query. We consider k ∈{5, 10} for training and set k for test time using dev
> data. We now discuss experimental details for each task. 3.1
> Open-domain Question Answering
> Open-domain question answering (QA) is an important real-world application and common testbed
> for knowledge-intensive tasks [20]. We treat questions and answers as input-output text pairs (x, y)
> and train RAG by directly minimizing the negative log-likelihood of answers. We compare RAG to
> the popular extractive QA paradigm [5, 7, 31, 26], where answers are extracted spans from retrieved
> documents, relying primarily on non-parametric knowledge. We also compare to “Closed-Book
> QA” approaches [52], which, like RAG, generate answers, but which do not exploit retrieval, instead
> relying purely on parametric knowledge. We consider four popular open-domain QA datasets: Natural
> Questions (NQ) [29], TriviaQA (TQA) [24]. WebQuestions (WQ) [3] and CuratedTrec (CT) [2]. As
> CT and WQ are small, we follow DPR [26] by initializing CT and WQ models with our NQ RAG
> model. We use the same train/dev/test splits as prior work [31, 26] and report Exact Match (EM)
> scores. For TQA, to compare with T5 [52], we also evaluate on the TQA Wiki test set. 3.2
> Abstractive Question Answering
> RAG models can go beyond simple extractive QA and answer questions with free-form, abstractive
> text generation. To test RAG’s natural language generation (NLG) in a knowledge-intensive setting,
> we use the MSMARCO NLG task v2.1 [43]. The task consists of questions, ten gold passages
> retrieved from a search engine for each question, and a full sentence answer annotated from the
> retrieved passages. We do not use the supplied passages, only the questions and answers, to treat
> 4

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 2, section UNKNOWN

Chunk `0b001009879392c9654a9ae956a8dc6d82bcdba4d3845b9309439f7ef1ae6b3a`; source `arxiv:2104.08663`; paper_aggregation rank 3 similarity 0.7530900835990906 rerank None

> Fact Checking
> Citation-Prediction
> Wiki
> FEVER
> QUERY
> DOCS
> Natural Claim
> Wikipedia Articles
> Wiki
> Climate-FEVER
> QUERY
> DOCS
> Climate-based Claim
> Wikipedia Articles
> SciFact
> QUERY
> DOCS
> Scientific claim
> PubMed Articles
> Scientific
> SCIDOCS
> QUERY
> DOCS
> Article Title
> PubMed Articles
> Scientific
> Dup. Question Retrieval
> Quora
> Quora
> QUERY
> DOCS
> StackEx. CQADupStack
> QUERY
> DOCS
> Argument Retrieval
> Misc. QUERY
> DOCS
> Misc. ArguAna
> QUERY
> DOCS
> Tóuche-2020
> Query Title
> Query Title + Body
> Query Title
> Quora Questions
> Argument
> Idebate Arguments
> Args.me Arguments
> News Retrieval
> TREC-NEWS
> QUERY
> DOCS
> News Articles
> News
> Tweet Retrieval
> Signal-1M
> QUERY
> DOCS
> News Headline
> Twitter Tweets
> Twitter
> Question-Answering
> Wiki
> NQ
> QUERY
> DOCS
> Wiki
> HotpotQA
> QUERY
> DOCS
> FiQA-2018
> QUERY
> DOCS
> Finance
> Bio-Medical IR
> QUERY
> DOCS
> Scientific
> BioASQ
> QUERY
> DOCS
> NFCorpus
> QUERY
> DOCS
> Scientific
> Entity Retrieval
> DBPedia
> QUERY
> DOCS
> Entity-based Query
> DBPedia Articles
> Wiki
> TREC-COVID
> Scientific
> Wikipedia Articles
> Wikipedia Articles
> Natural Query
> Multi-Hop Query
> CORD-19 Articles
> PubMed Articles
> PubMed Articles
> COVID-19 Query
> Nutrition Facts
> Bio-Medical Query
> Financial Query
> Investment Articles
> Controversial Query
> 9 Tasks
> 18 Datasets
> News Headline
> Robust04
> QUERY
> DOCS
> News
> News Articles
> News Query
> Figure 1: An overview of the diverse tasks and datasets in BEIR benchmark. So far, it is unclear how well existing trained neural models will perform for other text domains or
> textual retrieval tasks. Even more important, it is unclear how well different approaches, like sparse
> embeddings vs. dense embeddings, generalize to out-of-distribution data. In this work, we present a novel robust and heterogeneous benchmark called BEIR (Benchmarking
> IR), comprising of 18 retrieval datasets for comparison and evaluation of model generalization. Prior
> retrieval benchmarks [19, 50] have issues of a comparatively narrow evaluation focusing either only
> on a single task, like question-answering, or on a certain domain. In BEIR, we focus on Diversity, we
> include nine different retrieval tasks: Fact checking, citation prediction, duplicate question retrieval,
> argument retrieval, news retrieval, question answering, tweet retrieval, bio-medical IR, and entity
> retrieval. Further, we include datasets from diverse text domains, datasets that cover broad topics (like
> Wikipedia) and specialized topics (like COVID-19 publications), different text types (news articles vs.
> Tweets), datasets of various sizes (3.6k - 15M documents), and datasets with different query lengths
> (average query length between 3 and 192 words) and document lengths (average document length
> between 11 and 635 words). We use BEIR to evaluate ten diverse retrieval methods from five broad architectures: lexical, sparse,
> dense, late interaction, and re-ranking.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 1, section UNKNOWN

Chunk `5d6e32be40a6b0f1e43bce42b00ca8078785054df8f24ddd38648fbe58ec0ea0`; source `arxiv:2004.12832`; paper_aggregation rank 4 similarity 0.7476580142974854 rerank None

> ColBERT: Efficient and Effective Passage Search via
> Contextualized Late Interaction over BERT
> Omar Khatab
> Stanford University
> okhatab@stanford.edu
> Matei Zaharia
> Stanford University
> matei@cs.stanford.edu
> ABSTRACT
> Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed
> to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs
> increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query–document pair
> through a massive neural network to compute a single relevance
> score. To tackle this, we present ColBERT, a novel ranking model
> that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then
> employs a cheap yet powerful interaction step that models their
> fine-grained similarity. By delaying and yet retaining this finegranular interaction, ColBERT can leverage the expressiveness of
> deep LMs while simultaneously gaining the ability to pre-compute
> document representations offline, considerably speeding up query
> processing. Beyond reducing the cost of re-ranking the documents
> retrieved by a traditional model, ColBERT’s pruning-friendly interaction mechanism enables leveraging vector-similarity indexes
> for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search
> datasets. Results show that ColBERT’s effectiveness is competitive
> with existing BERT-based models (and outperforms every nonBERT baseline), while executing two orders-of-magnitude faster
> and requiring four orders-of-magnitude fewer FLOPs per query. ACM Reference format:
> Omar Khatab and Matei Zaharia. 2020. ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. In Proceedings
> of Proceedings of the 43rd International ACM SIGIR Conference on Research
> and Development in Information Retrieval, Virtual Event, China, July 25–30,
> 2020 (SIGIR ’20), 10 pages. DOI: 10.1145/3397271.3401075
> 1
> INTRODUCTION
> Over the past few years, the Information Retrieval (IR) community
> has witnessed the introduction of a host of neural ranking models,
> including DRMM [7], KNRM [4, 36], and Duet [20, 22]. In contrast
> Permission to make digital or hard copies of all or part of this work for personal or
> classroom use is granted without fee provided that copies are not made or distributed
> for profit or commercial advantage and that copies bear this notice and the full citation
> on the first page. Copyrights for components of this work owned by others than the
> author(s) must be honored. Abstracting with credit is permited.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 12, section UNKNOWN

Chunk `031f9cd08bc2ad3612c947978c2bd7c316d55ca755b3fc81719a2df5b72353a1`; source `arxiv:1706.03762`; paper_aggregation rank 5 similarity 0.7469270825386047 rerank None

> [25] Mitchell P Marcus, Mary Ann Marcinkiewicz, and Beatrice Santorini. Building a large annotated
> corpus of english: The penn treebank. Computational linguistics, 19(2):313–330, 1993. [26] David McClosky, Eugene Charniak, and Mark Johnson. Effective self-training for parsing. In
> Proceedings of the Human Language Technology Conference of the NAACL, Main Conference,
> pages 152–159. ACL, June 2006. [27] Ankur Parikh, Oscar Täckström, Dipanjan Das, and Jakob Uszkoreit. A decomposable attention
> model. In Empirical Methods in Natural Language Processing, 2016. [28] Romain Paulus, Caiming Xiong, and Richard Socher. A deep reinforced model for abstractive
> summarization. arXiv preprint arXiv:1705.04304, 2017. [29] Slav Petrov, Leon Barrett, Romain Thibaux, and Dan Klein. Learning accurate, compact,
> and interpretable tree annotation. In Proceedings of the 21st International Conference on
> Computational Linguistics and 44th Annual Meeting of the ACL, pages 433–440. ACL, July
> 2006. [30] Ofir Press and Lior Wolf. Using the output embedding to improve language models. arXiv
> preprint arXiv:1608.05859, 2016. [31] Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words
> with subword units. arXiv preprint arXiv:1508.07909, 2015. [32] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton,
> and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts
> layer. arXiv preprint arXiv:1701.06538, 2017. [33] Nitish Srivastava, Geoffrey E Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov. Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine
> Learning Research, 15(1):1929–1958, 2014. [34] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory
> networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors,
> Advances in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates,
> Inc., 2015. [35] Ilya Sutskever, Oriol Vinyals, and Quoc VV Le. Sequence to sequence learning with neural
> networks. In Advances in Neural Information Processing Systems, pages 3104–3112, 2014. [36] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. CoRR, abs/1512.00567, 2015. [37] Vinyals & Kaiser, Koo, Petrov, Sutskever, and Hinton. Grammar as a foreign language. In
> Advances in Neural Information Processing Systems, 2015. [38] Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le, Mohammad Norouzi, Wolfgang
> Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al. Google’s neural machine
> translation system: Bridging the gap between human and machine translation. arXiv preprint
> arXiv:1609.08144, 2016. [39] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 6, section UNKNOWN

Chunk `827613f6d766371c219ac63617928cdede74545c59e6b15a1b1525b9d456a27f`; source `arxiv:1810.04805`; paper_aggregation rank 6 similarity 0.7292488813400269 rerank None

> The effect of model
> size is explored more thoroughly in Section 5.2. 4.2
> SQuAD v1.1
> The
> Stanford
> Question
> Answering
> Dataset
> (SQuAD v1.1) is a collection of 100k crowdsourced question/answer pairs (Rajpurkar et al.,
> 2016). Given a question and a passage from
> 9The GLUE data set distribution does not include the Test
> labels, and we only made a single GLUE evaluation server
> submission for each of BERTBASE and BERTLARGE. 10https://gluebenchmark.com/leaderboard
> Wikipedia containing the answer, the task is to
> predict the answer text span in the passage. As shown in Figure 1, in the question answering task, we represent the input question and passage as a single packed sequence, with the question using the A embedding and the passage using
> the B embedding. We only introduce a start vector S ∈RH and an end vector E ∈RH during
> fine-tuning. The probability of word i being the
> start of the answer span is computed as a dot product between Ti and S followed by a softmax over
> all of the words in the paragraph: Pi =
> eS·Ti
> P
> j eS·Tj . The analogous formula is used for the end of the
> answer span. The score of a candidate span from
> position i to position j is defined as S·Ti + E·Tj,
> and the maximum scoring span where j ≥i is
> used as a prediction. The training objective is the
> sum of the log-likelihoods of the correct start and
> end positions. We fine-tune for 3 epochs with a
> learning rate of 5e-5 and a batch size of 32. Table 2 shows top leaderboard entries as well
> as results from top published systems (Seo et al.,
> 2017; Clark and Gardner, 2018; Peters et al.,
> 2018a; Hu et al., 2018). The top results from the
> SQuAD leaderboard do not have up-to-date public
> system descriptions available,11 and are allowed to
> use any public data when training their systems. We therefore use modest data augmentation in
> our system by first fine-tuning on TriviaQA (Joshi
> et al., 2017) befor fine-tuning on SQuAD. Our best performing system outperforms the top
> leaderboard system by +1.5 F1 in ensembling and
> +1.3 F1 as a single system. In fact, our single
> BERT model outperforms the top ensemble system in terms of F1 score. Without TriviaQA fine11QANet is described in Yu et al. (2018), but the system
> has improved substantially after publication.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 6, section UNKNOWN

Chunk `bcd9418b179cf36e8cb914d1a339d305a3d1eba19445abb72a8a688c942fc541`; source `arxiv:1710.10903`; paper_aggregation rank 7 similarity 0.7209019064903259 rerank None

> Published as a conference paper at ICLR 2018
> Table 1: Summary of the datasets used in our experiments. Cora
> Citeseer
> Pubmed
> PPI
> Task
> Transductive
> Transductive
> Transductive
> Inductive
> # Nodes
> 2708 (1 graph)
> 3327 (1 graph)
> 19717 (1 graph)
> 56944 (24 graphs)
> # Edges
> 5429
> 4732
> 44338
> 818716
> # Features/Node
> 1433
> 3703
> 500
> 50
> # Classes
> 7
> 6
> 3
> 121 (multilabel)
> # Training Nodes
> 140
> 120
> 60
> 44906 (20 graphs)
> # Validation Nodes
> 500
> 500
> 500
> 6514 (2 graphs)
> # Test Nodes
> 1000
> 1000
> 1000
> 5524 (2 graphs)
> well as inductive), achieving or matching state-of-the-art performance across all of them. This section summarizes our experimental setup, results, and a brief qualitative analysis of a GAT model’s
> extracted feature representations. 3.1
> DATASETS
> Transductive learning
> We utilize three standard citation network benchmark datasets—Cora,
> Citeseer and Pubmed (Sen et al., 2008)—and closely follow the transductive experimental setup of
> Yang et al. (2016). In all of these datasets, nodes correspond to documents and edges to (undirected)
> citations. Node features correspond to elements of a bag-of-words representation of a document. Each node has a class label. We allow for only 20 nodes per class to be used for training—however,
> honoring the transductive setup, the training algorithm has access to all of the nodes’ feature vectors. The predictive power of the trained models is evaluated on 1000 test nodes, and we use 500
> additional nodes for validation purposes (the same ones as used by Kipf & Welling (2017)). The
> Cora dataset contains 2708 nodes, 5429 edges, 7 classes and 1433 features per node. The Citeseer
> dataset contains 3327 nodes, 4732 edges, 6 classes and 3703 features per node. The Pubmed dataset
> contains 19717 nodes, 44338 edges, 3 classes and 500 features per node. Inductive learning
> We make use of a protein-protein interaction (PPI) dataset that consists of
> graphs corresponding to different human tissues (Zitnik & Leskovec, 2017). The dataset contains
> 20 graphs for training, 2 for validation and 2 for testing. Critically, testing graphs remain completely unobserved during training. To construct the graphs, we used the preprocessed data provided
> by Hamilton et al. (2017). The average number of nodes per graph is 2372. Each node has 50
> features that are composed of positional gene sets, motif gene sets and immunological signatures.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 5, section UNKNOWN

Chunk `dcad8c65fc188a446b2a56a49c2b68ac9f9408656ee578f8c5e973b59ae24289`; source `arxiv:1609.02907`; paper_aggregation rank 8 similarity 0.7147341966629028 rerank None

> Our method is based on spectral graph convolutional neural networks, introduced in Bruna et al.
> (2014) and later extended by Defferrard et al. (2016) with fast localized convolutions. In contrast
> to these works, we consider here the task of transductive node classification within networks of
> significantly larger scale. We show that in this setting, a number of simplifications (see Section 2.2)
> can be introduced to the original frameworks of Bruna et al. (2014) and Defferrard et al. (2016) that
> improve scalability and classification performance in large-scale networks. 5
> EXPERIMENTS
> We test our model in a number of experiments: semi-supervised document classification in citation networks, semi-supervised entity classification in a bipartite graph extracted from a knowledge
> graph, an evaluation of various graph propagation models and a run-time analysis on random graphs. 5.1
> DATASETS
> We closely follow the experimental setup in Yang et al. (2016). Dataset statistics are summarized
> in Table 1. In the citation network datasets—Citeseer, Cora and Pubmed (Sen et al., 2008)—nodes
> are documents and edges are citation links. Label rate denotes the number of labeled nodes that are
> used for training divided by the total number of nodes in each dataset. NELL (Carlson et al., 2010;
> Yang et al., 2016) is a bipartite graph dataset extracted from a knowledge graph with 55,864 relation
> nodes and 9,891 entity nodes. Table 1: Dataset statistics, as reported in Yang et al. (2016). Dataset
> Type
> Nodes
> Edges
> Classes
> Features
> Label rate
> Citeseer
> Citation network
> 3,327
> 4,732
> 6
> 3,703
> 0.036
> Cora
> Citation network
> 2,708
> 5,429
> 7
> 1,433
> 0.052
> Pubmed
> Citation network
> 19,717
> 44,338
> 3
> 500
> 0.003
> NELL
> Knowledge graph
> 65,755
> 266,144
> 210
> 5,414
> 0.001
> 5

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 4, section UNKNOWN

Chunk `88c0b4ab21070dd8600e466ddcb4dc4a784ad46113f0a69e6a97a45ab845fb4b`; source `arxiv:1903.10676`; paper_aggregation rank 9 similarity 0.7108524441719055 rerank None

> Field
> Task
> Dataset
> SOTA
> BERT-Base
> SCIBERT
> Frozen
> Finetune
> Frozen
> Finetune
> Bio
> NER
> BC5CDR (Li et al., 2016)
> 88.857
> 85.08
> 86.72
> 88.73
> 90.01
> JNLPBA (Collier and Kim, 2004)
> 78.58
> 74.05
> 76.09
> 75.77
> 77.28
> NCBI-disease (Dogan et al., 2014)
> 89.36
> 84.06
> 86.88
> 86.39
> 88.57
> PICO
> EBM-NLP (Nye et al., 2018)
> 66.30
> 61.44
> 71.53
> 68.30
> 72.28
> DEP
> GENIA (Kim et al., 2003) - LAS
> 91.92
> 90.22
> 90.33
> 90.36
> 90.43
> GENIA (Kim et al., 2003) - UAS
> 92.84
> 91.84
> 91.89
> 92.00
> 91.99
> REL
> ChemProt (Kringelum et al., 2016)
> 76.68
> 68.21
> 79.14
> 75.03
> 83.64
> CS
> NER
> SciERC (Luan et al., 2018)
> 64.20
> 63.58
> 65.24
> 65.77
> 67.57
> REL
> SciERC (Luan et al., 2018)
> n/a
> 72.74
> 78.71
> 75.25
> 79.97
> CLS
> ACL-ARC (Jurgens et al., 2018)
> 67.9
> 62.04
> 63.91
> 60.74
> 70.98
> Multi
> CLS
> Paper Field
> n/a
> 63.64
> 65.37
> 64.38
> 65.71
> SciCite (Cohan et al., 2019)
> 84.0
> 84.31
> 84.85
> 85.42
> 85.49
> Average
> 73.58
> 77.16
> 76.01
> 79.27
> Table 1: Test performances of all BERT variants on all tasks and datasets. Bold indicates the SOTA result (multiple
> results bolded if difference within 95% bootstrap confidence interval). Keeping with past work, we report macro
> F1 scores for NER (span-level), macro F1 scores for REL and CLS (sentence-level), and macro F1 for PICO
> (token-level), and micro F1 for ChemProt specifically. For DEP, we report labeled (LAS) and unlabeled (UAS)
> attachment scores (excluding punctuation) for the same model with hyperparameters tuned for LAS. All results
> are the average of multiple runs with different random seeds. Task
> Dataset
> BIOBERT
> SCIBERT
> NER
> BC5CDR
> 88.85
> 90.01
> JNLPBA
> 77.59
> 77.28
> NCBI-disease
> 89.36
> 88.57
> REL
> ChemProt
> 76.68
> 83.64
> Table 2:
> Comparing SCIBERT with the reported
> BIOBERT results on biomedical datasets. BC5CDR and ChemProt, and performs similarly
> on JNLPBA despite being trained on a substantially smaller biomedical corpus. 4.2
> Computer Science Domain
> We observe that SCIBERT outperforms BERTBase on computer science tasks (+3.55 F1 with
> finetuning and +1.13 F1 without). In addition,
> SCIBERT achieves new SOTA results on ACLARC (Cohan et al., 2019), and the NER part of
> SciERC (Luan et al., 2018). For relations in SciERC, our results are not comparable with those in
> Luan et al. (2018) because we are performing relation classification given gold entities, while they
> perform joint entity and relation extraction. 4.3
> Multiple Domains
> We observe that SCIBERT outperforms BERTBase on the multidomain tasks (+0.49 F1 with
> finetuning and +0.93 F1 without). In addition, SCIBERT outperforms the SOTA on SciCite (Cohan et al., 2019).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 2, section UNKNOWN

Chunk `10262d39646c8df07da06b11aeaf29995eb9c1a880a6e2a84521064f1d8e41cd`; source `arxiv:1512.03385`; paper_aggregation rank 10 similarity 0.7036342620849609 rerank None

> On the ImageNet classification dataset [36], we obtain
> excellent results by extremely deep residual nets. Our 152layer residual net is the deepest network ever presented on
> ImageNet, while still having lower complexity than VGG
> nets [41]. Our ensemble has 3.57% top-5 error on the
> ImageNet test set, and won the 1st place in the ILSVRC
> 2015 classification competition. The extremely deep representations also have excellent generalization performance
> on other recognition tasks, and lead us to further win the
> 1st places on: ImageNet detection, ImageNet localization,
> COCO detection, and COCO segmentation in ILSVRC &
> COCO 2015 competitions. This strong evidence shows that
> the residual learning principle is generic, and we expect that
> it is applicable in other vision and non-vision problems. 2. Related Work
> Residual Representations. In image recognition, VLAD
> [18] is a representation that encodes by the residual vectors
> with respect to a dictionary, and Fisher Vector [30] can be
> formulated as a probabilistic version [18] of VLAD. Both
> of them are powerful shallow representations for image retrieval and classification [4, 48]. For vector quantization,
> encoding residual vectors [17] is shown to be more effective than encoding original vectors. In low-level vision and computer graphics, for solving Partial Differential Equations (PDEs), the widely used
> Multigrid method [3] reformulates the system as subproblems at multiple scales, where each subproblem is responsible for the residual solution between a coarser and a finer
> scale. An alternative to Multigrid is hierarchical basis preconditioning [45, 46], which relies on variables that represent residual vectors between two scales. It has been shown
> [3, 45, 46] that these solvers converge much faster than standard solvers that are unaware of the residual nature of the
> solutions. These methods suggest that a good reformulation
> or preconditioning can simplify the optimization. Shortcut Connections. Practices and theories that lead to
> shortcut connections [2, 34, 49] have been studied for a long
> time. An early practice of training multi-layer perceptrons
> (MLPs) is to add a linear layer connected from the network
> input to the output [34, 49]. In [44, 24], a few intermediate layers are directly connected to auxiliary classifiers
> for addressing vanishing/exploding gradients. The papers
> of [39, 38, 31, 47] propose methods for centering layer responses, gradients, and propagated errors, implemented by
> shortcut connections. In [44], an “inception” layer is composed of a shortcut branch and a few deeper branches.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### ir-colbert-05

How does late interaction between contextualized query and document tokens support efficient passage ranking?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 1, section UNKNOWN

Chunk `f0cb95aafaae7cc44800ff74335f91cc30dc9d9fdc9d8377565152d61748d340`; source `arxiv:2004.12832`; faiss_cosine rank 1 similarity 0.840611457824707 rerank None; metadata_filtered_cosine rank 1 similarity 0.840611457824707 rerank None; paper_aggregation rank 1 similarity 0.840611457824707 rerank None; mmr_diversity rank 1 similarity 0.840611457824707 rerank 0.5884280204772949

> It reports retrieval effectiveness (MRR@10) on the official
> validation set as well as average query latency (log-scale) using a
> high-end server that dedicates one Tesla V100 GPU per query for
> neural re-rankers. Following the re-ranking setup of MS MARCO,
> ColBERT (re-rank), the Neural Matching Models, and the Deep LMs
> re-rank the MS MARCO’s official top-1000 documents per query. 1htps://blog.google/products/search/search-language-understanding-bert/
> 2htps://azure.microsof.com/en-us/blog/bing-delivers-its-largest-improvementin-search-experience-using-azure-gpus/
> arXiv:2004.12832v2 [cs.IR] 4 Jun 2020

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 1, section UNKNOWN

Chunk `5d6e32be40a6b0f1e43bce42b00ca8078785054df8f24ddd38648fbe58ec0ea0`; source `arxiv:2004.12832`; faiss_cosine rank 2 similarity 0.8294703960418701 rerank None; metadata_filtered_cosine rank 2 similarity 0.8294703960418701 rerank None; mmr_diversity rank 3 similarity 0.8294703960418701 rerank 0.28062927722930897

> ColBERT: Efficient and Effective Passage Search via
> Contextualized Late Interaction over BERT
> Omar Khatab
> Stanford University
> okhatab@stanford.edu
> Matei Zaharia
> Stanford University
> matei@cs.stanford.edu
> ABSTRACT
> Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed
> to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs
> increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query–document pair
> through a massive neural network to compute a single relevance
> score. To tackle this, we present ColBERT, a novel ranking model
> that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then
> employs a cheap yet powerful interaction step that models their
> fine-grained similarity. By delaying and yet retaining this finegranular interaction, ColBERT can leverage the expressiveness of
> deep LMs while simultaneously gaining the ability to pre-compute
> document representations offline, considerably speeding up query
> processing. Beyond reducing the cost of re-ranking the documents
> retrieved by a traditional model, ColBERT’s pruning-friendly interaction mechanism enables leveraging vector-similarity indexes
> for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search
> datasets. Results show that ColBERT’s effectiveness is competitive
> with existing BERT-based models (and outperforms every nonBERT baseline), while executing two orders-of-magnitude faster
> and requiring four orders-of-magnitude fewer FLOPs per query. ACM Reference format:
> Omar Khatab and Matei Zaharia. 2020. ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. In Proceedings
> of Proceedings of the 43rd International ACM SIGIR Conference on Research
> and Development in Information Retrieval, Virtual Event, China, July 25–30,
> 2020 (SIGIR ’20), 10 pages. DOI: 10.1145/3397271.3401075
> 1
> INTRODUCTION
> Over the past few years, the Information Retrieval (IR) community
> has witnessed the introduction of a host of neural ranking models,
> including DRMM [7], KNRM [4, 36], and Duet [20, 22]. In contrast
> Permission to make digital or hard copies of all or part of this work for personal or
> classroom use is granted without fee provided that copies are not made or distributed
> for profit or commercial advantage and that copies bear this notice and the full citation
> on the first page. Copyrights for components of this work owned by others than the
> author(s) must be honored. Abstracting with credit is permited.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 10, section UNKNOWN

Chunk `40be89f415c1e2ca5d389c08ea455173c3dd6ba47a4d8ca6a92b43ae7b270c3a`; source `arxiv:2004.12832`; faiss_cosine rank 3 similarity 0.8278868794441223 rerank None; metadata_filtered_cosine rank 3 similarity 0.8278868794441223 rerank None; mmr_diversity rank 4 similarity 0.8278868794441223 rerank 0.2795208156108855

> [38] Wei Yang, Kuang Lu, Peilin Yang, and Jimmy Lin. 2019. Critically Examining
> the” Neural Hype” Weak Baselines and the Additivity of Effectiveness Gains
> from Neural Ranking Models. In Proceedings of the 42nd International ACM SIGIR
> Conference on Research and Development in Information Retrieval. 1129–1132. [39] Zeynep Akkalyoncu Yilmaz, Wei Yang, Haotian Zhang, and Jimmy Lin. 2019. Cross-domain modeling of sentence-level evidence for document retrieval. In
> Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing
> (EMNLP-IJCNLP). 3481–3487. [40] Ofir Zafrir, Guy Boudoukh, Peter Izsak, and Moshe Wasserblat. 2019. Q8bert:
> Qantized 8bit bert. arXiv preprint arXiv:1910.06188 (2019). [41] Hamed Zamani, Mostafa Dehghani, W Bruce Crof, Erik Learned-Miller, and
> Jaap Kamps. 2018. From neural re-ranking to neural ranking: Learning a sparse
> representation for inverted indexing. In Proceedings of the 27th ACM International
> Conference on Information and Knowledge Management. ACM, 497–506. [42] Le Zhao. 2012. Modeling and solving term mismatch for full-text retrieval. Ph.D. Dissertation. Carnegie Mellon University.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 1, section UNKNOWN

Chunk `6dfb21541a590b7682d503d7685f87dd41e75a8baad3fcdcdfce76eff6816271`; source `arxiv:2004.12832`; faiss_cosine rank 4 similarity 0.8210347890853882 rerank None; metadata_filtered_cosine rank 4 similarity 0.8210347890853882 rerank None; mmr_diversity rank 5 similarity 0.8210347890853882 rerank 0.27472435235977166

> Copyrights for components of this work owned by others than the
> author(s) must be honored. Abstracting with credit is permited. To copy otherwise, or
> republish, to post on servers or to redistribute to lists, requires prior specific permission
> and/or a fee. Request permissions from permissions@acm.org. SIGIR ’20, Virtual Event, China
> © 2020 Copyright held by the owner/author(s). Publication rights licensed to ACM. 978-1-4503-8016-4/20/07...$15.00
> DOI: 10.1145/3397271.3401075
> 0.15
> 0.20
> 0.25
> 0.30
> 0.35
> 0.40
> MRR@10
> 101
> 102
> 103
> 104
> 105
> Query Latency (ms)
> BM25
> doc2query
> KNRM
> Duet
> DeepCT
> fT+ConvKNRM
> docTTTTTquery
> BERT-base
> BERT-large
> ColBERT (re-rank)
> ColBERT (full retrieval)
> Bag-of-Words (BoW) Model
> BoW Model with NLU Augmentation
> Neural Matching Model
> Deep Language Model
> ColBERT (ours)
> Figure 1: Effectiveness (MRR@10) versus Mean Qery Latency (log-scale) for a number of representative ranking
> models on MS MARCO Ranking [24]. Te figure also shows
> ColBERT. Neural re-rankers run on top of the official BM25
> top-1000 results and use a Tesla V100 GPU. Methodology and
> detailed results are in §4. to prior learning-to-rank methods that rely on hand-crafed features, these models employ embedding-based representations of
> queries and documents and directly model local interactions (i.e.,
> fine-granular relationships) between their contents. Among them,
> a recent approach has emerged that fine-tunes deep pre-trained
> language models (LMs) like ELMo [29] and BERT [5] for estimating
> relevance. By computing deeply-contextualized semantic representations of query–document pairs, these LMs help bridge the
> pervasive vocabulary mismatch [21, 42] between documents and
> queries [30]. Indeed, in the span of just a few months, a number
> of ranking models based on BERT have achieved state-of-the-art
> results on various retrieval benchmarks [3, 18, 25, 39] and have
> been proprietarily adapted for deployment by Google1 and Bing2. However, the remarkable gains delivered by these LMs come
> at a steep increase in computational cost. Hofst ̈ater et al. [9] and
> MacAvaney et al. [18] observe that BERT-based models in the literature are 100-1000× more computationally expensive than prior
> models—some of which are arguably not inexpensive to begin with
> [13]. Tis quality–cost tradeoffis summarized by Figure 1, which
> compares two BERT-based rankers [25, 27] against a representative
> set of ranking models. Te figure uses MS MARCO Ranking [24],
> a recent collection of 9M passages and 1M queries from Bing’s
> logs. It reports retrieval effectiveness (MRR@10) on the official
> validation set as well as average query latency (log-scale) using a
> high-end server that dedicates one Tesla V100 GPU per query for
> neural re-rankers.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 10, section UNKNOWN

Chunk `463ef270b0abe83aa514df9f6db629927a534171d0404fb15078f6b61d303929`; source `arxiv:2004.12832`; faiss_cosine rank 5 similarity 0.8206322193145752 rerank None; metadata_filtered_cosine rank 5 similarity 0.8206322193145752 rerank None; mmr_diversity rank 6 similarity 0.8206322193145752 rerank 0.2744425535202025

> NSF under CAREER grant CNS-1651570. Any opinions, findings,
> and conclusions or recommendations expressed in this material are
> those of the authors and do not necessarily reflect the views of the
> National Science Foundation. REFERENCES
> [1] Firas Abuzaid, Geet Sethi, Peter Bailis, and Matei Zaharia. 2019. To Index or Not
> to Index: Optimizing Exact Maximum Inner Product Search. In 2019 IEEE 35th
> International Conference on Data Engineering (ICDE). IEEE, 1250–1261. [2] Zhuyun Dai and Jamie Callan. 2019. Context-Aware Sentence/Passage Term
> Importance Estimation For First Stage Retrieval. arXiv preprint arXiv:1910.10687
> (2019). [3] Zhuyun Dai and Jamie Callan. 2019. Deeper Text Understanding for IR with
> Contextual Neural Language Modeling. arXiv preprint arXiv:1905.09217 (2019). [4] Zhuyun Dai, Chenyan Xiong, Jamie Callan, and Zhiyuan Liu. 2018. Convolutional
> neural networks for sof-matching n-grams in ad-hoc search. In Proceedings of the
> eleventh ACM international conference on web search and data mining. 126–134. [5] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. Bert:
> Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805 (2018). [6] Laura Dietz, Manisha Verma, Filip Radlinski, and Nick Craswell. 2017. TREC
> Complex Answer Retrieval Overview.. In TREC. [7] Jiafeng Guo, Yixing Fan, Qingyao Ai, and W Bruce Crof. 2016. A deep relevance
> matching model for ad-hoc retrieval. In Proceedings of the 25th ACM International
> on Conference on Information and Knowledge Management. ACM, 55–64. [8] Jiafeng Guo, Yixing Fan, Liang Pang, Liu Yang, Qingyao Ai, Hamed Zamani,
> Chen Wu, W Bruce Crof, and Xueqi Cheng. 2019. A deep look into neural
> ranking models for information retrieval. arXiv preprint arXiv:1903.06902 (2019). [9] Sebastian Hofst ̈ater and Allan Hanbury. 2019. Let’s measure run time! Extending
> the IR replicability infrastructure to include performance aspects. arXiv preprint
> arXiv:1907.04614 (2019). [10] Sebastian Hofst ̈ater, Navid Rekabsaz, Carsten Eickhoff, and Allan Hanbury. 2019. On the effect of low-frequency terms on neural-IR models. In Proceedings
> of the 42nd International ACM SIGIR Conference on Research and Development in
> Information Retrieval. 1137–1140. [11] Sebastian Hofst ̈ater, Markus Zlabinger, and Allan Hanbury. 2019. TU Wien@
> TREC Deep Learning’19–Simple Contextualization for Re-ranking. arXiv preprint
> arXiv:1912.01385 (2019). [12] Po-Sen Huang, Xiaodong He, Jianfeng Gao, Li Deng, Alex Acero, and Larry
> Heck. 2013. Learning deep structured semantic models for web search using
> clickthrough data. In Proceedings of the 22nd ACM international conference on
> Information & Knowledge Management. 2333–2338. [13] Shiyu Ji, Jinjin Shao, and Tao Yang. 2019.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 10, section UNKNOWN

Chunk `68b88e625f3e9f1ef8c579ea57365498a1760482206e5ed4904db8497dec722e`; source `arxiv:2004.12832`; faiss_cosine rank 6 similarity 0.8182801604270935 rerank None; metadata_filtered_cosine rank 6 similarity 0.8182801604270935 rerank None; mmr_diversity rank 7 similarity 0.8182801604270935 rerank 0.2727961122989654

> [12] Po-Sen Huang, Xiaodong He, Jianfeng Gao, Li Deng, Alex Acero, and Larry
> Heck. 2013. Learning deep structured semantic models for web search using
> clickthrough data. In Proceedings of the 22nd ACM international conference on
> Information & Knowledge Management. 2333–2338. [13] Shiyu Ji, Jinjin Shao, and Tao Yang. 2019. Efficient Interaction-based Neural
> Ranking with Locality Sensitive Hashing. In Te World Wide Web Conference. ACM, 2858–2864. [14] Xiaoqi Jiao, Yichun Yin, Lifeng Shang, Xin Jiang, Xiao Chen, Linlin Li, Fang Wang,
> and Qn Liu. 2019. Tinybert: Distilling bert for natural language understanding. arXiv preprint arXiv:1909.10351 (2019). [15] JeffJohnson, Mathijs Douze, and Herv ́e J ́egou. 2017. Billion-scale similarity
> search with GPUs. arXiv preprint arXiv:1702.08734 (2017). [16] Diederik P Kingma and Jimmy Ba. 2014. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 (2014). [17] Ron Kohavi, Alex Deng, Brian Frasca, Toby Walker, Ya Xu, and Nils Pohlmann. 2013. Online controlled experiments at large scale. In SIGKDD. [18] Sean MacAvaney, Andrew Yates, Arman Cohan, and Nazli Goharian. 2019. Cedr:
> Contextualized embeddings for document ranking. In Proceedings of the 42nd
> International ACM SIGIR Conference on Research and Development in Information
> Retrieval. ACM, 1101–1104. [19] Paul Michel, Omer Levy, and Graham Neubig. 2019. Are Sixteen Heads Really
> Beter than One?. In Advances in Neural Information Processing Systems. 14014–
> 14024. [20] Bhaskar Mitra and Nick Craswell. 2019. An Updated Duet Model for Passage
> Re-ranking. arXiv preprint arXiv:1903.07666 (2019). [21] Bhaskar Mitra, Nick Craswell, et al. 2018. An introduction to neural information
> retrieval. Foundations and Trends® in Information Retrieval 13, 1 (2018), 1–126. [22] Bhaskar Mitra, Fernando Diaz, and Nick Craswell. 2017. Learning to match using
> local and distributed representations of text for web search. In Proceedings of
> the 26th International Conference on World Wide Web. International World Wide
> Web Conferences Steering Commitee, 1291–1299. [23] Bhaskar Mitra, Corby Rosset, David Hawking, Nick Craswell, Fernando Diaz,
> and Emine Yilmaz. 2019. Incorporating query term independence assumption
> for efficient retrieval and ranking using deep neural networks. arXiv preprint
> arXiv:1907.03693 (2019). [24] Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, Rangan
> Majumder, and Li Deng. 2016. MS MARCO: A Human-Generated MAchine
> Reading COmprehension Dataset. (2016). [25] Rodrigo Nogueira and Kyunghyun Cho. 2019. Passage Re-ranking with BERT. arXiv preprint arXiv:1901.04085 (2019). [26] Rodrigo Nogueira, Jimmy Lin, and AI Epistemic. 2019. From doc2query to
> docTTTTTquery. (2019). [27] Rodrigo Nogueira, Wei Yang, Kyunghyun Cho, and Jimmy Lin. 2019.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 2, section UNKNOWN

Chunk `bd7fdd808fe36233187d46c17a839a69994ecf4f0d7b9d89962381a8dc01e51f`; source `arxiv:2004.12832`; faiss_cosine rank 7 similarity 0.8152682185173035 rerank None; metadata_filtered_cosine rank 7 similarity 0.8152682185173035 rerank None; mmr_diversity rank 8 similarity 0.8152682185173035 rerank 0.27068775296211234

> Query
> Document
> MaxSim
> ∑
> MaxSim
> MaxSim
> s
> Query
> CNN / Match Kernels
> CNN / Match Kernels / MLP
> MLP
> s
> Document
> (c) All-to-all Interaction
> (e.g., BERT)
> (b) Query-Document Interaction
> (e.g., DRMM, KNRM, Conv-KNRM)
> (d) Late Interaction
> (i.e., the proposed ColBERT)
> (a) Representation-based Similarity
> (e.g., DSSM, SNRM)
> Query
> Document
> s
> Query
> Document
> s
> Figure 2: Schematic diagrams illustrating query–document matching paradigms in neural IR. Te figure contrasts existing
> approaches (sub-figures (a), (b), and (c)) with the proposed late interaction paradigm (sub-figure (d)). Other methods, including ColBERT (full retrieval), directly retrieve
> the top-1000 results from the entire collection. As the figure shows, BERT considerably improves search precision, raising MRR@10 by almost 7% against the best previous methods; simultaneously, it increases latency by up to tens of thousands
> of milliseconds even with a high-end GPU. Tis poses a challenging
> tradeoffsince raising query response times by as litle as 100ms is
> known to impact user experience and even measurably diminish
> revenue [17]. To tackle this problem, recent work has started exploring using Natural Language Understanding (NLU) techniques
> to augment traditional retrieval models like BM25 [32]. For example, Nogueira et al. [26, 28] expand documents with NLU-generated
> queries before indexing with BM25 scores and Dai & Callan [2] replace BM25’s term frequency with NLU-estimated term importance. Despite successfully reducing latency, these approaches generally
> reduce precision substantially relative to BERT. To reconcile efficiency and contextualization in IR, we propose
> ColBERT, a ranking model based on contextualized late interaction over BERT. As the name suggests, ColBERT proposes a novel
> late interaction paradigm for estimating relevance between a query
> q and a document d. Under late interaction, q and d are separately
> encoded into two sets of contextual embeddings, and relevance is
> evaluated using cheap and pruning-friendly computations between
> both sets—that is, fast computations that enable ranking without
> exhaustively evaluating every possible candidate. Figure 2 contrasts our proposed late interaction approach with
> existing neural matching paradigms. On the lef, Figure 2 (a) illustrates representation-focused rankers, which independently compute
> an embedding for q and another for d and estimate relevance as
> a single similarity score between two vectors [12, 41]. Moving to
> the right, Figure 2 (b) visualizes typical interaction-focused rankers. Instead of summarizing q and d into individual embeddings, these
> rankers model word- and phrase-level relationships across q and d
> and match them using a deep neural network (e.g., with CNNs/MLPs
> [22] or kernels [36]).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 10, section UNKNOWN

Chunk `72dc9e2b41c5b0ed8d19f3972cf883ef11f4a63337d793203296b15039eb617c`; source `arxiv:2004.12832`; faiss_cosine rank 8 similarity 0.8143899440765381 rerank None; metadata_filtered_cosine rank 8 similarity 0.8143899440765381 rerank None; mmr_diversity rank 9 similarity 0.8143899440765381 rerank 0.27007296085357657

> 2016. MS MARCO: A Human-Generated MAchine
> Reading COmprehension Dataset. (2016). [25] Rodrigo Nogueira and Kyunghyun Cho. 2019. Passage Re-ranking with BERT. arXiv preprint arXiv:1901.04085 (2019). [26] Rodrigo Nogueira, Jimmy Lin, and AI Epistemic. 2019. From doc2query to
> docTTTTTquery. (2019). [27] Rodrigo Nogueira, Wei Yang, Kyunghyun Cho, and Jimmy Lin. 2019. Multi-Stage
> Document Ranking with BERT. arXiv preprint arXiv:1910.14424 (2019). [28] Rodrigo Nogueira, Wei Yang, Jimmy Lin, and Kyunghyun Cho. 2019. Document
> Expansion by Qery Prediction. arXiv preprint arXiv:1904.08375 (2019). [29] Mathew E Peters, Mark Neumann, Mohit Iyyer, Mat Gardner, Christopher
> Clark, Kenton Lee, and Luke Zetlemoyer. 2018. Deep contextualized word
> representations. arXiv preprint arXiv:1802.05365 (2018). [30] Yifan Qiao, Chenyan Xiong, Zhenghao Liu, and Zhiyuan Liu. 2019. Understanding the Behaviors of BERT in Ranking. arXiv preprint arXiv:1904.07531
> (2019). [31] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang,
> Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. 2019. Exploring the
> limits of transfer learning with a unified text-to-text transformer. arXiv preprint
> arXiv:1910.10683 (2019). [32] Stephen E Robertson, Steve Walker, Susan Jones, Micheline M Hancock-Beaulieu,
> Mike Gatford, et al. 1995. Okapi at TREC-3. NIST Special Publication (1995). [33] Raphael Tang, Yao Lu, Linqing Liu, Lili Mou, Olga Vechtomova, and Jimmy Lin. 2019. Distilling task-specific knowledge from BERT into simple neural networks. arXiv preprint arXiv:1903.12136 (2019). [34] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
> Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin. 2017. Atention is all
> you need. In Advances in neural information processing systems. 5998–6008. [35] Yonghui Wu, Mike Schuster, Zhifeng Chen, Qoc V Le, Mohammad Norouzi,
> Wolfgang Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al.
> 2016. Google’s neural machine translation system: Bridging the gap between
> human and machine translation. arXiv preprint arXiv:1609.08144 (2016). [36] Chenyan Xiong, Zhuyun Dai, Jamie Callan, Zhiyuan Liu, and Russell Power. 2017. End-to-end neural ad-hoc ranking with kernel pooling. In Proceedings
> of the 40th International ACM SIGIR conference on research and development in
> information retrieval. 55–64. [37] Peilin Yang, Hui Fang, and Jimmy Lin. 2018. Anserini: Reproducible ranking
> baselines using Lucene. Journal of Data and Information Qality (JDIQ) 10, 4
> (2018), 1–20. [38] Wei Yang, Kuang Lu, Peilin Yang, and Jimmy Lin. 2019. Critically Examining
> the” Neural Hype” Weak Baselines and the Additivity of Effectiveness Gains
> from Neural Ranking Models. In Proceedings of the 42nd International ACM SIGIR
> Conference on Research and Development in Information Retrieval. 1129–1132.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 9, section UNKNOWN

Chunk `24f3e59565ad56c6475df20b583df512020a8447a6c9ccd8711094d75019d8de`; source `arxiv:2004.12832`; faiss_cosine rank 9 similarity 0.8130378723144531 rerank None; metadata_filtered_cosine rank 9 similarity 0.8130378723144531 rerank None; mmr_diversity rank 10 similarity 0.8130378723144531 rerank 0.26912651062011705

> 5
> CONCLUSIONS
> In this paper, we introduced ColBERT, a novel ranking model that
> employs contextualized late interaction over deep LMs (in particular,
> BERT) for efficient retrieval. By independently encoding queries
> and documents into fine-grained representations that interact via
> cheap and pruning-friendly computations, ColBERT can leverage
> the expressiveness of deep LMs while greatly speeding up query
> processing. In addition, doing so allows using ColBERT for end-toend neural retrieval directly from a large document collection. Our
> results show that ColBERT is more than 170× faster and requires
> 14,000× fewer FLOPs/query than existing BERT-based models, all
> while only minimally impacting quality and while outperforming
> every non-BERT baseline. Acknowledgments. OK was supported by the Eltoukhy Family
> Graduate Fellowship at the Stanford School of Engineering. Tis
> research was supported in part by affiliate members and other
> supporters of the Stanford DAWN project—Ant Financial, Facebook,
> Google, Infosys, NEC, and VMware—as well as Cisco, SAP, and the

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 7, section UNKNOWN

Chunk `4d21e231d9f96454c79e53894266a6429b9782bb0ac00f6ffd883dc225af4a7c`; source `arxiv:2004.12832`; faiss_cosine rank 10 similarity 0.8105967044830322 rerank None; metadata_filtered_cosine rank 10 similarity 0.8105967044830322 rerank None

> Method
> MRR@10 (Dev)
> MRR@10 (Eval)
> Re-ranking Latency (ms)
> FLOPs/query
> BM25 (official)
> 16.7
> 16.5
> -
> -
> KNRM
> 19.8
> 19.8
> 3
> 592M (0.085×)
> Duet
> 24.3
> 24.5
> 22
> 159B (23×)
> fastText+ConvKNRM
> 29.0
> 27.7
> 28
> 78B (11×)
> BERTbase [25]
> 34.7
> -
> 10,700
> 97T (13,900×)
> BERTbase (our training)
> 36.0
> -
> 10,700
> 97T (13,900×)
> BERTlarge [25]
> 36.5
> 35.9
> 32,900
> 340T (48,600×)
> ColBERT (over BERTbase)
> 34.9
> 34.9
> 61
> 7B (1×)
> Table 1: “Re-ranking” results on MS MARCO. Each neural model re-ranks the official top-1000 results produced by BM25. Latency is reported for re-ranking only. To obtain the end-to-end latency in Figure 1, we add the BM25 latency from Table 2. Method
> MRR@10 (Dev)
> MRR@10 (Local Eval)
> Latency (ms)
> Recall@50
> Recall@200
> Recall@1000
> BM25 (official)
> 16.7
> -
> -
> -
> -
> 81.4
> BM25 (Anserini)
> 18.7
> 19.5
> 62
> 59.2
> 73.8
> 85.7
> doc2query
> 21.5
> 22.8
> 85
> 64.4
> 77.9
> 89.1
> DeepCT
> 24.3
> -
> 62 (est.)
> 69 [2]
> 82 [2]
> 91 [2]
> docTTTTTquery
> 27.7
> 28.4
> 87
> 75.6
> 86.9
> 94.7
> ColBERTL2 (re-rank)
> 34.8
> 36.4
> -
> 75.3
> 80.5
> 81.4
> ColBERTL2 (end-to-end)
> 36.0
> 36.7
> 458
> 82.9
> 92.3
> 96.8
> Table 2: End-to-end retrieval results on MS MARCO. Each model retrieves the top-1000 documents per query directly from the
> entire 8.8M document collection. retrieval (i.e., for methods with neural computations) but we use
> up to all four GPUs during indexing. 4.2
> Qality–Cost Tradeoff: Top-k Re-ranking
> In this section, we examine ColBERT’s efficiency and effectiveness
> at re-ranking the top-k results extracted by a bag-of-words retrieval
> model, which is the most typical seting for testing and deploying
> neural ranking models. We begin with the MS MARCO dataset. We
> compare against KNRM, Duet, and fastText+ConvKNRM, a representative set of neural matching models that have been previously
> tested on MS MARCO. In addition, we compare against the natural adaptation of BERT for ranking by Nogueira and Cho [25],
> in particular, BERTbase and its deeper counterpart BERTlarge. We
> also report results for “BERTbase (our training)”, which is based on
> Nogueira and Cho’s base model (including hyperparameters) but
> is trained with the same loss function as ColBERT (§3.3) for 200k
> iterations, allowing for a more direct comparison of the results. We report the competition’s official metric, namely MRR@10,
> on the validation set (Dev) and the evaluation set (Eval). We also
> report the re-ranking latency, which we measure using a single
> Tesla V100 GPU, and the FLOPs per query for each neural ranking
> model.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 2, section UNKNOWN

Chunk `8cd9d2df0b1b414de28f45f2079dfe2961b97e558fc05f418ebc6aaee6050771`; source `arxiv:2004.04906`; paper_aggregation rank 2 similarity 0.7814334630966187 rerank None; mmr_diversity rank 2 similarity 0.7814334630966187 rerank 0.2797792136669158

> QA datasets, it also suffers from two weaknesses. First, ICT pretraining is computationally intensive
> and it is not completely clear that regular sentences
> are good surrogates of questions in the objective
> function. Second, because the context encoder is
> not fine-tuned using pairs of questions and answers,
> the corresponding representations could be suboptimal. In this paper, we address the question: can we
> train a better dense embedding model using only
> pairs of questions and passages (or answers), without additional pretraining? By leveraging the now
> standard BERT pretrained model (Devlin et al.,
> 2019) and a dual-encoder architecture (Bromley
> et al., 1994), we focus on developing the right
> training scheme using a relatively small number
> of question and passage pairs. Through a series
> of careful ablation studies, our final solution is
> surprisingly simple: the embedding is optimized
> for maximizing inner products of the question and
> relevant passage vectors, with an objective comparing all pairs of questions and passages in a batch. Our Dense Passage Retriever (DPR) is exceptionally strong. It not only outperforms BM25 by a
> large margin (65.2% vs. 42.9% in Top-5 accuracy),
> but also results in a substantial improvement on
> the end-to-end QA accuracy compared to ORQA
> (41.5% vs. 33.3%) in the open Natural Questions
> setting (Lee et al., 2019; Kwiatkowski et al., 2019). Our contributions are twofold. First, we demonstrate that with the proper training setup, simply fine-tuning the question and passage encoders
> on existing question-passage pairs is sufficient to
> greatly outperform BM25. Our empirical results
> also suggest that additional pretraining may not be
> needed. Second, we verify that, in the context of
> open-domain question answering, a higher retrieval
> precision indeed translates to a higher end-to-end
> QA accuracy. By applying a modern reader model
> to the top retrieved passages, we achieve comparable or better results on multiple QA datasets in the
> open-retrieval setting, compared to several, much
> complicated systems. 2
> Background
> The problem of open-domain QA studied in this
> paper can be described as follows. Given a factoid
> question, such as “Who first voiced Meg on Family
> Guy?” or “Where was the 8th Dalai Lama born?”, a
> system is required to answer it using a large corpus
> of diversified topics. More specifically, we assume
> the extractive QA setting, in which the answer is
> restricted to a span appearing in one or more passages in the corpus. Assume that our collection
> contains D documents, d1, d2, · · · , dD.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 17, section UNKNOWN

Chunk `cade6ef2b414467f1a7464c055d1ee5e6048be44443c62bbaf52ffc95a58174d`; source `arxiv:2104.08663`; paper_aggregation rank 3 similarity 0.7674260139465332 rerank None

> So far we focused only on datasets that have one or two fields. 5. Task-specific Models: In our benchmark, we focus on evaluating models that are able to generalize
> well for a broad range of retrieval tasks. Naturally in real-world, for some few tasks or domains,
> specialized models are available which can easily outperform generic models as they focus and
> perform well on a single task, lets say on question-answering. Such task-specific models do not
> necessarily need to generalize across all diverse tasks. C
> Training and In-domain Evaluation
> We use the MS MARCO Passage Ranking dataset [45], which contains 8.8M Passages and an official
> training set of 532,761 query-passage pairs for fine-tuning for a majority of retrievers. The dataset
> contains queries from Bing search logs with one text passage from various web sources annotated as
> relevant. We find the dataset useful for training, in terms of covering a wide variety of topics and
> providing the highest number of training pairs. It has been extensively explored and used for finetuning dense retrievers in recent works [46, 17, 15]. We use the official MS MARCO development
> set for our in-domain evaluation which has been widely used in prior research [46, 17, 15]. It has
> 6,980 queries. Most of the queries have only 1 document judged relevant; the labels are binary. D
> Zero-shot Evaluation Tasks
> Following the selection criteria mentioned in Section 3, we include 18 evaluation datasets that span
> across 9 heterogeneous tasks. Each dataset mentioned below contains a document corpus denoted
> 17

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 12, section UNKNOWN

Chunk `031f9cd08bc2ad3612c947978c2bd7c316d55ca755b3fc81719a2df5b72353a1`; source `arxiv:1706.03762`; paper_aggregation rank 4 similarity 0.7638074159622192 rerank None

> [25] Mitchell P Marcus, Mary Ann Marcinkiewicz, and Beatrice Santorini. Building a large annotated
> corpus of english: The penn treebank. Computational linguistics, 19(2):313–330, 1993. [26] David McClosky, Eugene Charniak, and Mark Johnson. Effective self-training for parsing. In
> Proceedings of the Human Language Technology Conference of the NAACL, Main Conference,
> pages 152–159. ACL, June 2006. [27] Ankur Parikh, Oscar Täckström, Dipanjan Das, and Jakob Uszkoreit. A decomposable attention
> model. In Empirical Methods in Natural Language Processing, 2016. [28] Romain Paulus, Caiming Xiong, and Richard Socher. A deep reinforced model for abstractive
> summarization. arXiv preprint arXiv:1705.04304, 2017. [29] Slav Petrov, Leon Barrett, Romain Thibaux, and Dan Klein. Learning accurate, compact,
> and interpretable tree annotation. In Proceedings of the 21st International Conference on
> Computational Linguistics and 44th Annual Meeting of the ACL, pages 433–440. ACL, July
> 2006. [30] Ofir Press and Lior Wolf. Using the output embedding to improve language models. arXiv
> preprint arXiv:1608.05859, 2016. [31] Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words
> with subword units. arXiv preprint arXiv:1508.07909, 2015. [32] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton,
> and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts
> layer. arXiv preprint arXiv:1701.06538, 2017. [33] Nitish Srivastava, Geoffrey E Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov. Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine
> Learning Research, 15(1):1929–1958, 2014. [34] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory
> networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors,
> Advances in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates,
> Inc., 2015. [35] Ilya Sutskever, Oriol Vinyals, and Quoc VV Le. Sequence to sequence learning with neural
> networks. In Advances in Neural Information Processing Systems, pages 3104–3112, 2014. [36] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. CoRR, abs/1512.00567, 2015. [37] Vinyals & Kaiser, Koo, Petrov, Sutskever, and Hinton. Grammar as a foreign language. In
> Advances in Neural Information Processing Systems, 2015. [38] Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le, Mohammad Norouzi, Wolfgang
> Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al. Google’s neural machine
> translation system: Bridging the gap between human and machine translation. arXiv preprint
> arXiv:1609.08144, 2016. [39] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 14, section UNKNOWN

Chunk `76902f40b2eee42a8affe066dd9d9b796680400eb5f36c5b5206f76fb37dad09`; source `arxiv:2005.11401`; paper_aggregation rank 5 similarity 0.759353518486023 rerank None

> approaches 2016 co-located with the 30th Annual Conference on Neural Information Processing
> Systems (NIPS 2016), Barcelona, Spain, December 9, 2016, volume 1773 of CEUR Workshop
> Proceedings. CEUR-WS.org, 2016. URL http://ceur-ws.org/Vol-1773/CoCoNIPS_
> 2016_paper9.pdf. [44] Rodrigo Nogueira and Kyunghyun Cho. Passage re-ranking with BERT. arXiv preprint
> arXiv:1901.04085, 2019. URL https://arxiv.org/abs/1901.04085. [45] Myle Ott, Sergey Edunov, Alexei Baevski, Angela Fan, Sam Gross, Nathan Ng, David Grangier,
> and Michael Auli. fairseq: A fast, extensible toolkit for sequence modeling. In Proceedings
> of the 2019 Conference of the North American Chapter of the Association for Computational
> Linguistics (Demonstrations), pages 48–53, Minneapolis, Minnesota, June 2019. Association
> for Computational Linguistics. doi: 10.18653/v1/N19-4009. URL https://www.aclweb. org/anthology/N19-4009. [46] Ethan Perez, Siddharth Karamcheti, Rob Fergus, Jason Weston, Douwe Kiela, and Kyunghyun
> Cho. Finding generalizable evidence by learning to convince q&a models. In Proceedings
> of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th
> International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages
> 2402–2411, Hong Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1244. URL https://www.aclweb.org/anthology/D19-1244. [47] Fabio Petroni, Tim Rocktäschel, Sebastian Riedel, Patrick Lewis, Anton Bakhtin, Yuxiang Wu,
> and Alexander Miller. Language models as knowledge bases? In Proceedings of the 2019
> Conference on Empirical Methods in Natural Language Processing and the 9th International
> Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 2463–2473, Hong
> Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/
> D19-1250. URL https://www.aclweb.org/anthology/D19-1250. [48] Fabio Petroni, Patrick Lewis, Aleksandra Piktus, Tim Rocktäschel, Yuxiang Wu, Alexander H. Miller, and Sebastian Riedel. How context affects language models’ factual predictions. In
> Automated Knowledge Base Construction, 2020. URL https://openreview.net/forum? id=025X0zPfn. [49] Alec
> Radford,
> Karthik
> Narasimhan,
> Tim
> Salimans,
> and
> Ilya
> Sutskever. Improving
> Language
> Understanding
> by
> Generative
> Pre-Training,
> 2018. URL
> https://s3-us-west-2.amazonaws.com/openai-assets/research-covers/
> language-unsupervised/language_understanding_paper.pdf. [50] Alec
> Radford,
> Jeff
> Wu,
> Rewon
> Child,
> David
> Luan,
> Dario
> Amodei,
> and
> Ilya
> Sutskever. Language models are unsupervised multitask learners,
> 2019. URL
> https://d4mucfpksywv.cloudfront.net/better-language-models/language_
> models_are_unsupervised_multitask_learners.pdf. [51] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena,
> Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified
> text-to-text transformer. arXiv e-prints, 2019. URL https://arxiv.org/abs/1910.10683. [52] Adam Roberts, Colin Raffel, and Noam Shazeer. How much knowledge can you pack into
> the parameters of a language model? arXiv e-prints, 2020. URL https://arxiv.org/abs/
> 2002.08910. [53] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: Bm25 and
> beyond. Found. Trends Inf. Retr., 3(4):333–389, April 2009. ISSN 1554-0669. doi: 10.1561/
> 1500000019. URL https://doi.org/10.1561/1500000019.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 15, section UNKNOWN

Chunk `838b0658a647839a7f82db548bcfb038766dd13224a49ef92cbd11f3ffd1d419`; source `arxiv:1810.04805`; paper_aggregation rank 6 similarity 0.73546302318573 rerank None

> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 
> 1
>  [SEP]
> ... Tok 
> N
> Tok 
> 1
> ... Tok
> M
> Question
> Paragraph
> BERT
> E[CLS]
> E1
>  E2
>  EN
> C
> T1
>  T2
>  TN
> Single Sentence 
> ... ... BERT
> Tok 1
>  Tok 2
>  Tok N
> ... [CLS]
> E[CLS]
> E1
>  E2
>  EN
> C
> T1
>  T2
>  TN
> Single Sentence 
> B-PER
> O
> O
> ... ... E[CLS]
> E1
>  E[SEP]
> Class 
> Label
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> Start/End Span
> Class 
> Label
> BERT
> Tok 1
>  Tok 2
>  Tok N
> ... [CLS]
> Tok 1
> [CLS]
> [CLS]
> Tok 
> 1
>  [SEP]
> ... Tok 
> N
> Tok 
> 1
> ... Tok
> M
> Sentence 1
> ... Sentence 2
> Figure 4: Illustrations of Fine-tuning BERT on Different Tasks. SST-2
> The Stanford Sentiment Treebank is a
> binary single-sentence classification task consisting of sentences extracted from movie reviews
> with human annotations of their sentiment (Socher
> et al., 2013). CoLA
> The Corpus of Linguistic Acceptability is
> a binary single-sentence classification task, where
> the goal is to predict whether an English sentence
> is linguistically “acceptable” or not (Warstadt
> et al., 2018). STS-B
> The Semantic Textual Similarity Benchmark is a collection of sentence pairs drawn from
> news headlines and other sources (Cer et al.,
> 2017). They were annotated with a score from 1
> to 5 denoting how similar the two sentences are in
> terms of semantic meaning. MRPC
> Microsoft Research Paraphrase Corpus
> consists of sentence pairs automatically extracted
> from online news sources, with human annotations
> for whether the sentences in the pair are semantically equivalent (Dolan and Brockett, 2005). RTE
> Recognizing Textual Entailment is a binary entailment task similar to MNLI, but with
> much less training data (Bentivogli et al., 2009).14
> WNLI
> Winograd NLI is a small natural language inference dataset (Levesque et al., 2011). The GLUE webpage notes that there are issues
> with the construction of this dataset, 15 and every
> trained system that’s been submitted to GLUE has
> performed worse than the 65.1 baseline accuracy
> of predicting the majority class. We therefore exclude this set to be fair to OpenAI GPT. For our
> GLUE submission, we always predicted the ma14Note that we only report single-task fine-tuning results
> in this paper. A multitask fine-tuning approach could potentially push the performance even further. For example, we
> did observe substantial improvements on RTE from multitask training with MNLI. 15https://gluebenchmark.com/faq

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 4, section UNKNOWN

Chunk `88c0b4ab21070dd8600e466ddcb4dc4a784ad46113f0a69e6a97a45ab845fb4b`; source `arxiv:1903.10676`; paper_aggregation rank 7 similarity 0.732435405254364 rerank None

> Field
> Task
> Dataset
> SOTA
> BERT-Base
> SCIBERT
> Frozen
> Finetune
> Frozen
> Finetune
> Bio
> NER
> BC5CDR (Li et al., 2016)
> 88.857
> 85.08
> 86.72
> 88.73
> 90.01
> JNLPBA (Collier and Kim, 2004)
> 78.58
> 74.05
> 76.09
> 75.77
> 77.28
> NCBI-disease (Dogan et al., 2014)
> 89.36
> 84.06
> 86.88
> 86.39
> 88.57
> PICO
> EBM-NLP (Nye et al., 2018)
> 66.30
> 61.44
> 71.53
> 68.30
> 72.28
> DEP
> GENIA (Kim et al., 2003) - LAS
> 91.92
> 90.22
> 90.33
> 90.36
> 90.43
> GENIA (Kim et al., 2003) - UAS
> 92.84
> 91.84
> 91.89
> 92.00
> 91.99
> REL
> ChemProt (Kringelum et al., 2016)
> 76.68
> 68.21
> 79.14
> 75.03
> 83.64
> CS
> NER
> SciERC (Luan et al., 2018)
> 64.20
> 63.58
> 65.24
> 65.77
> 67.57
> REL
> SciERC (Luan et al., 2018)
> n/a
> 72.74
> 78.71
> 75.25
> 79.97
> CLS
> ACL-ARC (Jurgens et al., 2018)
> 67.9
> 62.04
> 63.91
> 60.74
> 70.98
> Multi
> CLS
> Paper Field
> n/a
> 63.64
> 65.37
> 64.38
> 65.71
> SciCite (Cohan et al., 2019)
> 84.0
> 84.31
> 84.85
> 85.42
> 85.49
> Average
> 73.58
> 77.16
> 76.01
> 79.27
> Table 1: Test performances of all BERT variants on all tasks and datasets. Bold indicates the SOTA result (multiple
> results bolded if difference within 95% bootstrap confidence interval). Keeping with past work, we report macro
> F1 scores for NER (span-level), macro F1 scores for REL and CLS (sentence-level), and macro F1 for PICO
> (token-level), and micro F1 for ChemProt specifically. For DEP, we report labeled (LAS) and unlabeled (UAS)
> attachment scores (excluding punctuation) for the same model with hyperparameters tuned for LAS. All results
> are the average of multiple runs with different random seeds. Task
> Dataset
> BIOBERT
> SCIBERT
> NER
> BC5CDR
> 88.85
> 90.01
> JNLPBA
> 77.59
> 77.28
> NCBI-disease
> 89.36
> 88.57
> REL
> ChemProt
> 76.68
> 83.64
> Table 2:
> Comparing SCIBERT with the reported
> BIOBERT results on biomedical datasets. BC5CDR and ChemProt, and performs similarly
> on JNLPBA despite being trained on a substantially smaller biomedical corpus. 4.2
> Computer Science Domain
> We observe that SCIBERT outperforms BERTBase on computer science tasks (+3.55 F1 with
> finetuning and +1.13 F1 without). In addition,
> SCIBERT achieves new SOTA results on ACLARC (Cohan et al., 2019), and the NER part of
> SciERC (Luan et al., 2018). For relations in SciERC, our results are not comparable with those in
> Luan et al. (2018) because we are performing relation classification given gold entities, while they
> perform joint entity and relation extraction. 4.3
> Multiple Domains
> We observe that SCIBERT outperforms BERTBase on the multidomain tasks (+0.49 F1 with
> finetuning and +0.93 F1 without). In addition, SCIBERT outperforms the SOTA on SciCite (Cohan et al., 2019).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 2, section UNKNOWN

Chunk `b95faf1308418a0a159490d62e3f12fc45ef52d89d94af255877cd2fc0cd0d90`; source `arxiv:1710.10903`; paper_aggregation rank 8 similarity 0.7193138599395752 rerank None

> Monti et al. (2016)
> presented mixture model CNNs (MoNet), a spatial approach which provides a unified generalization of CNN architectures to graphs. More recently, Hamilton et al. (2017) introduced GraphSAGE,
> a method for computing node representations in an inductive manner. This technique operates by
> sampling a fixed-size neighborhood of each node, and then performing a specific aggregator over
> it (such as the mean over all the sampled neighbors’ feature vectors, or the result of feeding them
> through a recurrent neural network). This approach has yielded impressive performance across several large-scale inductive benchmarks. Attention mechanisms have become almost a de facto standard in many sequence-based tasks (Bahdanau et al., 2015; Gehring et al., 2016). One of the benefits of attention mechanisms is that they
> allow for dealing with variable sized inputs, focusing on the most relevant parts of the input to make
> decisions. When an attention mechanism is used to compute a representation of a single sequence,
> it is commonly referred to as self-attention or intra-attention. Together with Recurrent Neural Networks (RNNs) or convolutions, self-attention has proven to be useful for tasks such as machine
> reading (Cheng et al., 2016) and learning sentence representations (Lin et al., 2017). However,
> Vaswani et al. (2017) showed that not only self-attention can improve a method based on RNNs or
> convolutions, but also that it is sufficient for constructing a powerful model obtaining state-of-the-art
> performance on the machine translation task. Inspired by this recent work, we introduce an attention-based architecture to perform node classification of graph-structured data. The idea is to compute the hidden representations of each node in the
> graph, by attending over its neighbors, following a self-attention strategy. The attention architecture
> has several interesting properties: (1) the operation is efficient, since it is parallelizable across nodeneighbor pairs; (2) it can be applied to graph nodes having different degrees by specifying arbitrary
> weights to the neighbors; and (3) the model is directly applicable to inductive learning problems,
> including tasks where the model has to generalize to completely unseen graphs. We validate the
> proposed approach on four challenging benchmarks: Cora, Citeseer and Pubmed citation networks
> as well as an inductive protein-protein interaction dataset, achieving or matching state-of-the-art results that highlight the potential of attention-based models when dealing with arbitrarily structured
> graphs.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 4, section UNKNOWN

Chunk `4358e1cb657d28d446d0eab305cda0c18d76e58391c27db18d885c42702ce0a5`; source `arxiv:1512.03385`; paper_aggregation rank 9 similarity 0.6938337683677673 rerank None

> 7x7 conv, 64, /2
> pool, /2
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 128, /2
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 256, /2
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 512, /2
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> avg pool
> fc 1000
> image
> 3x3 conv, 512
> 3x3 conv, 64
> 3x3 conv, 64
> pool, /2
> 3x3 conv, 128
> 3x3 conv, 128
> pool, /2
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> pool, /2
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> pool, /2
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> pool, /2
> fc 4096
> fc 4096
> fc 1000
> image
> output 
> size: 112
> output 
> size: 224
> output 
> size: 56
> output 
> size: 28
> output 
> size: 14
> output 
> size: 7
> output 
> size: 1
> VGG-19
> 34-layer plain
> 7x7 conv, 64, /2
> pool, /2
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 128, /2
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 256, /2
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 512, /2
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> avg pool
> fc 1000
> image
> 34-layer residual
> Figure 3. Example network architectures for ImageNet. Left: the
> VGG-19 model [41] (19.6 billion FLOPs) as a reference. Middle: a plain network with 34 parameter layers (3.6 billion FLOPs). Right: a residual network with 34 parameter layers (3.6 billion
> FLOPs). The dotted shortcuts increase dimensions. Table 1 shows
> more details and other variants. Residual Network. Based on the above plain network, we
> insert shortcut connections (fig. 3, right) which turn the
> network into its counterpart residual version.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 5, section UNKNOWN

Chunk `dcad8c65fc188a446b2a56a49c2b68ac9f9408656ee578f8c5e973b59ae24289`; source `arxiv:1609.02907`; paper_aggregation rank 10 similarity 0.6927669048309326 rerank None

> Our method is based on spectral graph convolutional neural networks, introduced in Bruna et al.
> (2014) and later extended by Defferrard et al. (2016) with fast localized convolutions. In contrast
> to these works, we consider here the task of transductive node classification within networks of
> significantly larger scale. We show that in this setting, a number of simplifications (see Section 2.2)
> can be introduced to the original frameworks of Bruna et al. (2014) and Defferrard et al. (2016) that
> improve scalability and classification performance in large-scale networks. 5
> EXPERIMENTS
> We test our model in a number of experiments: semi-supervised document classification in citation networks, semi-supervised entity classification in a bipartite graph extracted from a knowledge
> graph, an evaluation of various graph propagation models and a run-time analysis on random graphs. 5.1
> DATASETS
> We closely follow the experimental setup in Yang et al. (2016). Dataset statistics are summarized
> in Table 1. In the citation network datasets—Citeseer, Cora and Pubmed (Sen et al., 2008)—nodes
> are documents and edges are citation links. Label rate denotes the number of labeled nodes that are
> used for training divided by the total number of nodes in each dataset. NELL (Carlson et al., 2010;
> Yang et al., 2016) is a bipartite graph dataset extracted from a knowledge graph with 55,864 relation
> nodes and 9,891 entity nodes. Table 1: Dataset statistics, as reported in Yang et al. (2016). Dataset
> Type
> Nodes
> Edges
> Classes
> Features
> Label rate
> Citeseer
> Citation network
> 3,327
> 4,732
> 6
> 3,703
> 0.036
> Cora
> Citation network
> 2,708
> 5,429
> 7
> 1,433
> 0.052
> Pubmed
> Citation network
> 19,717
> 44,338
> 3
> 500
> 0.003
> NELL
> Knowledge graph
> 65,755
> 266,144
> 210
> 5,414
> 0.001
> 5

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### ir-beir-06

How should information retrieval models be evaluated for zero-shot generalization across heterogeneous tasks?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 2, section UNKNOWN

Chunk `778a1b3ae78a37939b5437512688576e298b4b0d61696a39ac377ef501adc048`; source `arxiv:2104.08663`; faiss_cosine rank 1 similarity 0.8077787756919861 rerank None; metadata_filtered_cosine rank 1 similarity 0.8077787756919861 rerank None; paper_aggregation rank 1 similarity 0.8077787756919861 rerank None; mmr_diversity rank 1 similarity 0.8077787756919861 rerank 0.5654451429843902

> This setting hinders for investigation of model generalization
> across diverse set of domains and task types. MultiReQA [19] consists of eight Question-Answering
> (QA) datasets and evaluates sentence-level answer retrieval given a question. It only tests a single
> task and five out of eight datasets are from Wikipedia. Further, MultiReQA evaluates retrieval over
> rather small corpora: six out of eight tasks have less than 100k candidate sentences, which benefits
> dense retrieval over lexical as previously shown [54]. KILT [50] consists of five knowledge-intensive
> 2

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 4, section UNKNOWN

Chunk `c21efe82bce97071b34b10d82c9ae3ab8cd56f4544deb625edb27bdd769d1a2b`; source `arxiv:2104.08663`; faiss_cosine rank 2 similarity 0.8063359260559082 rerank None; metadata_filtered_cosine rank 2 similarity 0.8063359260559082 rerank None; mmr_diversity rank 2 similarity 0.8063359260559082 rerank 0.2644351482391356

> Binary
> —-
> —-
> 1,406
> 8,674
> 1.0
> 192.98
> 166.80
> Retrieval
> Misc. Touché-2020 [6]

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 18, section UNKNOWN

Chunk `b70a47037c6a027260219719b86bea803e00d8f60804cf3b760813c7ab1fffa0`; source `arxiv:2104.08663`; faiss_cosine rank 3 similarity 0.8060715198516846 rerank None; metadata_filtered_cosine rank 3 similarity 0.8060715198516846 rerank None; mmr_diversity rank 3 similarity 0.8060715198516846 rerank 0.2642500638961791

> by T and test queries for evaluation denoted by Q. We additionally provide dataset website links in
> Table 5 and intuitive examples in Table 8. We now describe each task and dataset included in the
> BEIR benchmark below:
> D.1
> Bio-Medical Information Retrieval
> Bio-medical information retrieval is the task of searching relevant scientific documents such as
> research papers or blogs for a given scientific query in the biomedical domain [28]. We consider a
> scientific query as input and retrieve bio-medical documents as output. TREC-COVID [65] is an ad-hoc search challenge based on the CORD-19 dataset containing scientific articles related to the COVID-19 pandemic [69]. We include the July 16, 2020 version of
> CORD-19 dataset as corpus T and use the final cumulative judgements with query descriptions from
> the original task as queries Q. NFCorpus [7] contains natural language queries harvested from NutritionFacts (NF). We use the
> original splits provided alongside all content sources from NF (videos, blogs, and Q&A posts) as
> queries Q and annotated medical documents from PubMed as corpus T. BioASQ [61] Task 8b is a biomedical semantic question answering challenge. We use the original
> train and test splits provided in Task 8b as queries Q and collect around 15M articles from PubMed
> provided in Task 8a as our corpus T. D.2
> Open-domain Question Answering (QA)
> Retrieval in open domain question answering [8] is the task of retrieving the correct answer for a
> question, without a predefined location for the answer. In open-domain tasks, model must retrieve
> over an entire knowledge source (such as Wikipedia). We consider the question as input and the
> passage containing the answer as output. Natural Questions [34] contains Google search queries and documents with paragraphs and answer
> spans within Wikipedia articles. We did not use the NQ version from ReQA [1] as it focused on
> queries having a short answer. As a result, we parsed the HTML of the original NQ dataset and
> include more complex development queries that often require a longer passage as answer compared to
> ReQA. We filtered out queries without an answer, or having a table as an answer, or with conflicting
> Wikipedia pages. We retain 2,681,468 passages as our corpus T and 3452 test queries Q from the
> original dataset. HotpotQA [76] contains multi-hop like questions which require reasoning over multiple paragraphs
> to find the correct answer.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 4, section UNKNOWN

Chunk `3e1cf5025f84e7c3585f6eafba1ffd803b1521d2b088f430cd538ca51b33123e`; source `arxiv:2104.08663`; faiss_cosine rank 4 similarity 0.8051598072052002 rerank None; metadata_filtered_cosine rank 4 similarity 0.8051598072052002 rerank None; mmr_diversity rank 4 similarity 0.8051598072052002 rerank 0.2636118650436401

> Split (→)
> Train
> Dev
> Test
> Avg. Word Lengths
> Task (↓)
> Domain (↓)
> Dataset (↓)
> Title
> Relevancy
> #Pairs
> #Query
> #Query
> #Corpus
> Avg. D / Q
> Query
> Document
> Passage-Retrieval
> Misc. MS MARCO [45]

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 15, section UNKNOWN

Chunk `c39a9f867d984f69a45a9c1e7aea058b53765513592ac6fbe76020489628d3a0`; source `arxiv:2104.08663`; faiss_cosine rank 5 similarity 0.8044604063034058 rerank None; metadata_filtered_cosine rank 5 similarity 0.8044604063034058 rerank None; mmr_diversity rank 5 similarity 0.8044604063034058 rerank 0.26312228441238394

> [75] Yinfei Yang, Daniel Cer, Amin Ahmad, Mandy Guo, Jax Law, Noah Constant, Gustavo Hernandez Abrego, Steve Yuan, Chris Tar, Yun-hsuan Sung, et al. 2020. Multilingual Universal
> Sentence Encoder for Semantic Retrieval. In Proceedings of the 58th Annual Meeting of the
> Association for Computational Linguistics: System Demonstrations, pages 87–94. 4
> [76] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov,
> and Christopher D. Manning. 2018. HotpotQA: A Dataset for Diverse, Explainable Multi-hop
> Question Answering. In Proceedings of the 2018 Conference on Empirical Methods in Natural
> Language Processing, pages 2369–2380, Brussels, Belgium. Association for Computational
> Linguistics. 4, 18
> [77] Xinyu Zhang, Xueguang Ma, Peng Shi, and Jimmy Lin. 2021. mr. TyDi: A Multi-lingual
> Benchmark for Dense Retrieval. 17
> [78] Yun Zhang, David Lo, Xin Xia, and Jian-Ling Sun. 2015. Multi-factor duplicate question
> detection in stack overflow. Journal of Computer Science and Technology, 30(5):981–997. 1
> [79] Tiancheng Zhao, Xiaopeng Lu, and Kyusong Lee. 2021. SPARTA: Efficient Open-Domain
> Question Answering via Sparse Transformer Matching Retrieval. In Proceedings of the 2021
> Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 565–575, Online. Association for Computational
> Linguistics. 3, 6
> 15

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 16, section UNKNOWN

Chunk `e80ca938a59925c5c9d0fd5edffdfef57f2b272bc831688594a748b56fc38c28`; source `arxiv:2104.08663`; faiss_cosine rank 6 similarity 0.8042533993721008 rerank None; metadata_filtered_cosine rank 6 similarity 0.8042533993721008 rerank None; mmr_diversity rank 6 similarity 0.8042533993721008 rerank 0.2629773795604705

> (d) Did you discuss whether and how consent was obtained from people whose data you’re
> using/curating? [N/A] Used datasets provide a specific dataset license, which we
> follow. (e) Did you discuss whether the data you are using/curating contains personally identifiable
> information or offensive content? [No] We re-use existing datasets, which most are
> freely available. Most datasets are from less sensitive sources, like Wikipedia or scientific publications, where don’t expect personally identifiable information. Checking for
> offensive content in more than 50 million documents is difficult and removing it would
> alter the underlying dataset. 5. If you used crowdsourcing or conducted research with human subjects... (a) Did you include the full text of instructions given to participants and screenshots, if
> applicable? [N/A] We ourselves performed annotation on the TREC-COVID dataset,
> where we followed the instructions from the original task website. (b) Did you describe any potential participant risks, with links to Institutional Review
> Board (IRB) approvals, if applicable? [N/A]
> (c) Did you include the estimated hourly wage paid to participants and the total amount
> spent on participant compensation? [N/A] Annotations were done by the authors of the
> paper. 16

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 4, section UNKNOWN

Chunk `030176541265bc3885afb8894e0f405e7490c2ae66337ccd2155691f030bfc2d`; source `arxiv:2104.08663`; faiss_cosine rank 7 similarity 0.8024219870567322 rerank None; metadata_filtered_cosine rank 7 similarity 0.8024219870567322 rerank None; mmr_diversity rank 7 similarity 0.8024219870567322 rerank 0.2616953909397124

> 5-level
> —-
> —-
> 57
> 594,977
> 19.6
> 11.14
> 634.79
> Retrieval
> News
> Robust04 [64]

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 20, section UNKNOWN

Chunk `6181d5caea057ff3b39f1408d174ba63493eef78cd16815a8711426dd2562b2a`; source `arxiv:2104.08663`; faiss_cosine rank 8 similarity 0.8020424246788025 rerank None; metadata_filtered_cosine rank 8 similarity 0.8020424246788025 rerank None; mmr_diversity rank 8 similarity 0.8020424246788025 rerank 0.26142969727516163

> G
> Capped Recall@k Score
> Recall at k is calculated as the fraction of the relevant documents that are successfully retrieved
> within the top k extracted documents. More formally, the R@k score is calculated as:
> R@k =
> 1
> |Q|
> |Q|
> X
> i=1
> | maxk(Ai) ∩A⋆
> i |
> |A⋆
> i |
> where Q is the set of queries, A⋆
> i is the set of relevant documents for the ith query, and Ai is a scored
> list of documents provided by the model, from which top k are extracted. However measuring recall can be counterintuitive, if a high number of relevant documents (> k) are
> present within a dataset. For example, consider a hypothetical dataset with 500 relevant documents
> for a query. Retrieving all relevant documents would produce a maximum R@100 score = 0.2, which
> 20

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 12, section UNKNOWN

Chunk `e6789f8ecd111b73768cdbeffb7bfc9a463c87584a6a5a75b96fea576d4ecf8d`; source `arxiv:2104.08663`; faiss_cosine rank 9 similarity 0.8019718527793884 rerank None; metadata_filtered_cosine rank 9 similarity 0.8019718527793884 rerank None; mmr_diversity rank 9 similarity 0.8019718527793884 rerank 0.26138029694557186

> Association for Computing Machinery. 9
> [39] Aldo Lipani. 2019. On Biases in Information retrieval models and evaluation. Ph.D. thesis,
> Technische Universität Wien. 8
> [40] Aldo Lipani, Mihai Lupu, and Allan Hanbury. 2016. The Curious Incidence of Bias Corrections
> in the Pool. In European Conference on Information Retrieval, pages 267–279. Springer. 9
> [41] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike
> Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. RoBERTa: A Robustly Optimized BERT
> Pretraining Approach. 6
> [42] Yi Luan, Jacob Eisenstein, Kristina Toutanova, and Michael Collins. 2021. Sparse, Dense, and
> Attentional Representations for Text Retrieval. 3
> [43] Ji Ma, Ivan Korotkov, Yinfei Yang, Keith Hall, and Ryan McDonald. 2021. Zero-shot Neural
> Passage Retrieval via Domain-targeted Synthetic Question Generation. 3
> [44] Macedo Maia, Siegfried Handschuh, André Freitas, Brian Davis, Ross McDermott, Manel
> Zarrouk, and Alexandra Balahur. 2018. WWW’18 Open Challenge: Financial Opinion Mining
> and Question Answering. In Companion Proceedings of the The Web Conference 2018, WWW
> ’18, page 1941–1942, Republic and Canton of Geneva, CHE. International World Wide Web
> Conferences Steering Committee. 4, 18
> 12

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 10, section References

Chunk `746d4c2368892d73f909fa023ab5768851fbea932da4001ebf58544c8de28a6a`; source `arxiv:2104.08663`; faiss_cosine rank 10 similarity 0.8014787435531616 rerank None; metadata_filtered_cosine rank 10 similarity 0.8014787435531616 rerank None; mmr_diversity rank 10 similarity 0.8014787435531616 rerank 0.261035120487213

> References
> [1] Amin Ahmad, Noah Constant, Yinfei Yang, and Daniel Cer. 2019. ReQA: An Evaluation for
> End-to-End Answer Retrieval Models. In Proceedings of the 2nd Workshop on Machine Reading
> for Question Answering, pages 137–146, Hong Kong, China. Association for Computational
> Linguistics. 18
> [2] Akari Asai, Jungo Kasai, Jonathan Clark, Kenton Lee, Eunsol Choi, and Hannaneh Hajishirzi. 2021. XOR QA: Cross-lingual Open-Retrieval Question Answering. In Proceedings of the
> 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 547–564, Online. Association for Computational
> Linguistics. 17
> [3] Petr Baudiš and Jan Šediv`y. 2015. Modeling of the question answering task in the yodaqa
> system. In International Conference of the Cross-Language Evaluation Forum for European
> Languages, pages 222–228. Springer. 6
> [4] Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. 2013. Semantic Parsing on
> Freebase from Question-Answer Pairs. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, pages 1533–1544, Seattle, Washington, USA. Association for Computational Linguistics. 6
> [5] Adam Berger, Rich Caruana, David Cohn, Dayne Freitag, and Vibhu Mittal. 2000. Bridging
> the lexical chasm: statistical approaches to answer-finding. In Proceedings of the 23rd annual
> international ACM SIGIR conference on Research and development in information retrieval,
> pages 192–199. 1, 3
> [6] Alexander Bondarenko, Maik Fröbe, Meriem Beloucif, Lukas Gienapp, Yamen Ajjour, Alexander Panchenko, Chris Biemann, Benno Stein, Henning Wachsmuth, Martin Potthast, and
> Matthias Hagen. 2020. Overview of Touché 2020: Argument Retrieval. In Working Notes
> Papers of the CLEF 2020 Evaluation Labs, volume 2696 of CEUR Workshop Proceedings. 4,
> 19, 22
> [7] Vera Boteva, Demian Gholipour, Artem Sokolov, and Stefan Riezler. 2016. A full-text learning to
> rank dataset for medical information retrieval. In Proceedings of the 38th European Conference
> on Information Retrieval (ECIR 2016), pages 716–722. 4, 18
> [8] Danqi Chen, Adam Fisch, Jason Weston, and Antoine Bordes. 2017. Reading Wikipedia to
> Answer Open-Domain Questions. In Proceedings of the 55th Annual Meeting of the Association
> for Computational Linguistics (Volume 1: Long Papers), pages 1870–1879, Vancouver, Canada. Association for Computational Linguistics. 1, 18
> [9] Arman Cohan, Sergey Feldman, Iz Beltagy, Doug Downey, and Daniel Weld. 2020. SPECTER:
> Document-level Representation Learning using Citation-informed Transformers. In Proceedings
> of the 58th Annual Meeting of the Association for Computational Linguistics, pages 2270–2282,
> Online. Association for Computational Linguistics. 4, 19
> [10] Davind Corney, Dyaa Albakour, Miguel Martinez, and Samir Moussa. 2016. What do a Million
> News Articles Look like?

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 14, section UNKNOWN

Chunk `f7f46d59ca966b0002a03869ab70bd6b3a2a74387ed5f895f57768ad7347463b`; source `arxiv:2005.11401`; paper_aggregation rank 2 similarity 0.7622647881507874 rerank None

> How much knowledge can you pack into
> the parameters of a language model? arXiv e-prints, 2020. URL https://arxiv.org/abs/
> 2002.08910. [53] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: Bm25 and
> beyond. Found. Trends Inf. Retr., 3(4):333–389, April 2009. ISSN 1554-0669. doi: 10.1561/
> 1500000019. URL https://doi.org/10.1561/1500000019. [54] Irene Solaiman, Miles Brundage, Jack Clark, Amanda Askell, Ariel Herbert-Voss, Jeff Wu, Alec
> Radford, and Jian-Bing Wang. Release strategies and the social impacts of language models. ArXiv, abs/1908.09203, 2019. [55] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors, Advances
> in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates, Inc., 2015. URL http://papers.nips.cc/paper/5846-end-to-end-memory-networks.pdf. 14

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 6, section UNKNOWN

Chunk `c3b0b77b442fab2d4b6cf646866065bc13d71028bba59c5d18649c60b4323788`; source `arxiv:2004.04906`; paper_aggregation rank 3 similarity 0.756056010723114 rerank None

> 65.8
> 78.0
> 84.9
> Table 3: Comparison of different training schemes,
> measured as top-k retrieval accuracy on Natural Questions (development set). #N: number of negative
> examples, IB: in-batch training. g.+BM25(1) and
> g.+BM25(2) denote in-batch training with 1 or 2 additional BM25 negatives, which serve as negative passages for all questions in the batch. Our experiments on Natural Questions show that
> switching to distantly-supervised passages (using
> the highest-ranked BM25 passage that contains the
> answer), has only a small impact: 1 point lower
> top-k accuracy for retrieval. Appendix A contains
> more details. Similarity and loss
> Besides dot product, cosine
> and Euclidean L2 distance are also commonly used
> as decomposable similarity functions. We test these
> alternatives and find that L2 performs comparable to dot product, and both of them are superior
> to cosine. Similarly, in addition to negative loglikelihood, a popular option for ranking is triplet
> loss, which compares a positive passage and a negative one directly with respect to a question (Burges
> et al., 2005). Our experiments show that using
> triplet loss does not affect the results much. More
> details can be found in Appendix B. Cross-dataset generalization
> One interesting
> question regarding DPR’s discriminative training
> is how much performance degradation it may suffer from a non-iid setting. In other words, can
> it still generalize well when directly applied to
> a different dataset without additional fine-tuning? To test the cross-dataset generalization, we train
> DPR on Natural Questions only and test it directly
> on the smaller WebQuestions and CuratedTREC
> datasets. We find that DPR generalizes well, with
> 3-5 points loss from the best performing fine-tuned
> model in top-20 retrieval accuracy (69.9/86.3 vs.
> 75.0/89.1 for WebQuestions and TREC, respectively), while still greatly outperforming the BM25
> baseline (55.0/70.9).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 11, section UNKNOWN

Chunk `2c479e9ca7c0278f1d1a4e5f083d8b2bc2e7d3ab4e4af1b4c41504297f97f5ed`; source `arxiv:1706.03762`; paper_aggregation rank 4 similarity 0.745858371257782 rerank None

> [5] Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, Fethi Bougares, Holger Schwenk,
> and Yoshua Bengio. Learning phrase representations using rnn encoder-decoder for statistical
> machine translation. CoRR, abs/1406.1078, 2014. [6] Francois Chollet. Xception: Deep learning with depthwise separable convolutions. arXiv
> preprint arXiv:1610.02357, 2016. [7] Junyoung Chung, Çaglar Gülçehre, Kyunghyun Cho, and Yoshua Bengio. Empirical evaluation
> of gated recurrent neural networks on sequence modeling. CoRR, abs/1412.3555, 2014. [8] Chris Dyer, Adhiguna Kuncoro, Miguel Ballesteros, and Noah A. Smith. Recurrent neural
> network grammars. In Proc. of NAACL, 2016. [9] Jonas Gehring, Michael Auli, David Grangier, Denis Yarats, and Yann N. Dauphin. Convolutional sequence to sequence learning. arXiv preprint arXiv:1705.03122v2, 2017. [10] Alex Graves. Generating sequences with recurrent neural networks. arXiv preprint
> arXiv:1308.0850, 2013. [11] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In Proceedings of the IEEE Conference on Computer Vision and Pattern
> Recognition, pages 770–778, 2016. [12] Sepp Hochreiter, Yoshua Bengio, Paolo Frasconi, and Jürgen Schmidhuber. Gradient flow in
> recurrent nets: the difficulty of learning long-term dependencies, 2001. [13] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural computation,
> 9(8):1735–1780, 1997. [14] Zhongqiang Huang and Mary Harper. Self-training PCFG grammars with latent annotations
> across languages. In Proceedings of the 2009 Conference on Empirical Methods in Natural
> Language Processing, pages 832–841. ACL, August 2009. [15] Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu. Exploring
> the limits of language modeling. arXiv preprint arXiv:1602.02410, 2016. [16] Łukasz Kaiser and Samy Bengio. Can active memory replace attention? In Advances in Neural
> Information Processing Systems, (NIPS), 2016. [17] Łukasz Kaiser and Ilya Sutskever. Neural GPUs learn algorithms. In International Conference
> on Learning Representations (ICLR), 2016. [18] Nal Kalchbrenner, Lasse Espeholt, Karen Simonyan, Aaron van den Oord, Alex Graves, and Koray Kavukcuoglu. Neural machine translation in linear time. arXiv preprint arXiv:1610.10099v2,
> 2017. [19] Yoon Kim, Carl Denton, Luong Hoang, and Alexander M. Rush. Structured attention networks. In International Conference on Learning Representations, 2017. [20] Diederik Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In ICLR, 2015. [21] Oleksii Kuchaiev and Boris Ginsburg. Factorization tricks for LSTM networks. arXiv preprint
> arXiv:1703.10722, 2017. [22] Zhouhan Lin, Minwei Feng, Cicero Nogueira dos Santos, Mo Yu, Bing Xiang, Bowen
> Zhou, and Yoshua Bengio. A structured self-attentive sentence embedding. arXiv preprint
> arXiv:1703.03130, 2017. [23] Minh-Thang Luong, Quoc V. Le, Ilya Sutskever, Oriol Vinyals, and Lukasz Kaiser. Multi-task
> sequence to sequence learning.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 3, section UNKNOWN

Chunk `2ece33288a1f2d2161a27f5b52b15e43ebecc0b98d088e36eb387c1757a2c0e9`; source `arxiv:1710.10903`; paper_aggregation rank 5 similarity 0.7396112084388733 rerank None

> P
> k∈Ni exp

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 4, section UNKNOWN

Chunk `88c0b4ab21070dd8600e466ddcb4dc4a784ad46113f0a69e6a97a45ab845fb4b`; source `arxiv:1903.10676`; paper_aggregation rank 6 similarity 0.7374803423881531 rerank None

> Field
> Task
> Dataset
> SOTA
> BERT-Base
> SCIBERT
> Frozen
> Finetune
> Frozen
> Finetune
> Bio
> NER
> BC5CDR (Li et al., 2016)
> 88.857
> 85.08
> 86.72
> 88.73
> 90.01
> JNLPBA (Collier and Kim, 2004)
> 78.58
> 74.05
> 76.09
> 75.77
> 77.28
> NCBI-disease (Dogan et al., 2014)
> 89.36
> 84.06
> 86.88
> 86.39
> 88.57
> PICO
> EBM-NLP (Nye et al., 2018)
> 66.30
> 61.44
> 71.53
> 68.30
> 72.28
> DEP
> GENIA (Kim et al., 2003) - LAS
> 91.92
> 90.22
> 90.33
> 90.36
> 90.43
> GENIA (Kim et al., 2003) - UAS
> 92.84
> 91.84
> 91.89
> 92.00
> 91.99
> REL
> ChemProt (Kringelum et al., 2016)
> 76.68
> 68.21
> 79.14
> 75.03
> 83.64
> CS
> NER
> SciERC (Luan et al., 2018)
> 64.20
> 63.58
> 65.24
> 65.77
> 67.57
> REL
> SciERC (Luan et al., 2018)
> n/a
> 72.74
> 78.71
> 75.25
> 79.97
> CLS
> ACL-ARC (Jurgens et al., 2018)
> 67.9
> 62.04
> 63.91
> 60.74
> 70.98
> Multi
> CLS
> Paper Field
> n/a
> 63.64
> 65.37
> 64.38
> 65.71
> SciCite (Cohan et al., 2019)
> 84.0
> 84.31
> 84.85
> 85.42
> 85.49
> Average
> 73.58
> 77.16
> 76.01
> 79.27
> Table 1: Test performances of all BERT variants on all tasks and datasets. Bold indicates the SOTA result (multiple
> results bolded if difference within 95% bootstrap confidence interval). Keeping with past work, we report macro
> F1 scores for NER (span-level), macro F1 scores for REL and CLS (sentence-level), and macro F1 for PICO
> (token-level), and micro F1 for ChemProt specifically. For DEP, we report labeled (LAS) and unlabeled (UAS)
> attachment scores (excluding punctuation) for the same model with hyperparameters tuned for LAS. All results
> are the average of multiple runs with different random seeds. Task
> Dataset
> BIOBERT
> SCIBERT
> NER
> BC5CDR
> 88.85
> 90.01
> JNLPBA
> 77.59
> 77.28
> NCBI-disease
> 89.36
> 88.57
> REL
> ChemProt
> 76.68
> 83.64
> Table 2:
> Comparing SCIBERT with the reported
> BIOBERT results on biomedical datasets. BC5CDR and ChemProt, and performs similarly
> on JNLPBA despite being trained on a substantially smaller biomedical corpus. 4.2
> Computer Science Domain
> We observe that SCIBERT outperforms BERTBase on computer science tasks (+3.55 F1 with
> finetuning and +1.13 F1 without). In addition,
> SCIBERT achieves new SOTA results on ACLARC (Cohan et al., 2019), and the NER part of
> SciERC (Luan et al., 2018). For relations in SciERC, our results are not comparable with those in
> Luan et al. (2018) because we are performing relation classification given gold entities, while they
> perform joint entity and relation extraction. 4.3
> Multiple Domains
> We observe that SCIBERT outperforms BERTBase on the multidomain tasks (+0.49 F1 with
> finetuning and +0.93 F1 without). In addition, SCIBERT outperforms the SOTA on SciCite (Cohan et al., 2019).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 6, section UNKNOWN

Chunk `d238aa05d00c9b881574d747613e25cf072abc1eee257872ead9c6d9f3711765`; source `arxiv:1512.03385`; paper_aggregation rank 7 similarity 0.7352151870727539 rerank None

> model
> top-1 err. top-5 err. VGG-16 [41]
> 28.07
> 9.33
> GoogLeNet [44]
> -
> 9.15
> PReLU-net [13]
> 24.27
> 7.38
> plain-34
> 28.54
> 10.02
> ResNet-34 A
> 25.03
> 7.76
> ResNet-34 B
> 24.52
> 7.46
> ResNet-34 C
> 24.19
> 7.40
> ResNet-50
> 22.85
> 6.71
> ResNet-101
> 21.75
> 6.05
> ResNet-152
> 21.43
> 5.71
> Table 3. Error rates (%, 10-crop testing) on ImageNet validation. VGG-16 is based on our test. ResNet-50/101/152 are of option B
> that only uses projections for increasing dimensions. method
> top-1 err. top-5 err. VGG [41] (ILSVRC’14)
> -
> 8.43†
> GoogLeNet [44] (ILSVRC’14)
> -
> 7.89
> VGG [41] (v5)
> 24.4
> 7.1
> PReLU-net [13]
> 21.59
> 5.71
> BN-inception [16]
> 21.99
> 5.81
> ResNet-34 B
> 21.84
> 5.71
> ResNet-34 C
> 21.53
> 5.60
> ResNet-50
> 20.74
> 5.25
> ResNet-101
> 19.87
> 4.60
> ResNet-152
> 19.38
> 4.49
> Table 4. Error rates (%) of single-model results on the ImageNet
> validation set (except † reported on the test set). method
> top-5 err. (test)
> VGG [41] (ILSVRC’14)
> 7.32
> GoogLeNet [44] (ILSVRC’14)
> 6.66
> VGG [41] (v5)
> 6.8
> PReLU-net [13]
> 4.94
> BN-inception [16]
> 4.82
> ResNet (ILSVRC’15)
> 3.57
> Table 5. Error rates (%) of ensembles. The top-5 error is on the
> test set of ImageNet and reported by the test server. ResNet reduces the top-1 error by 3.5% (Table 2), resulting
> from the successfully reduced training error (fig. 4 right vs.
> left). This comparison verifies the effectiveness of residual
> learning on extremely deep systems. Last, we also note that the 18-layer plain/residual nets
> are comparably accurate (Table 2), but the 18-layer ResNet
> converges faster (fig. 4 right vs. left). When the net is “not
> overly deep” (18 layers here), the current SGD solver is still
> able to find good solutions to the plain net. In this case, the
> ResNet eases the optimization by providing faster convergence at the early stage. Identity vs. Projection Shortcuts. We have shown that
> 3x3, 64
> 1x1, 64
> relu
> 1x1, 256
> relu
> relu
> 3x3, 64
> 3x3, 64
> relu
> relu
> 64-d
> 256-d
> Figure 5. A deeper residual function F for ImageNet. Left: a
> building block (on 56×56 feature maps) as in fig. 3 for ResNet34. Right: a “bottleneck” building block for ResNet-50/101/152. parameter-free, identity shortcuts help with training. Next
> we investigate projection shortcuts (Eqn.(2)). In Table 3 we
> compare three options: (A) zero-padding shortcuts are used
> for increasing dimensions, and all shortcuts are parameterfree (the same as Table 2 and fig. 4 right); (B) projection shortcuts are used for increasing dimensions, and other
> shortcuts are identity; and (C) all shortcuts are projections.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 3, section UNKNOWN

Chunk `5e503ef1d99a78cd350e19c5a8899dcceccd7e3955ca5a7dcd6950444ee1ad58`; source `arxiv:1609.02907`; paper_aggregation rank 8 similarity 0.7280056476593018 rerank None

> ˆA ReLU

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 2, section UNKNOWN

Chunk `bd7fdd808fe36233187d46c17a839a69994ecf4f0d7b9d89962381a8dc01e51f`; source `arxiv:2004.12832`; paper_aggregation rank 9 similarity 0.7271326184272766 rerank None

> Query
> Document
> MaxSim
> ∑
> MaxSim
> MaxSim
> s
> Query
> CNN / Match Kernels
> CNN / Match Kernels / MLP
> MLP
> s
> Document
> (c) All-to-all Interaction
> (e.g., BERT)
> (b) Query-Document Interaction
> (e.g., DRMM, KNRM, Conv-KNRM)
> (d) Late Interaction
> (i.e., the proposed ColBERT)
> (a) Representation-based Similarity
> (e.g., DSSM, SNRM)
> Query
> Document
> s
> Query
> Document
> s
> Figure 2: Schematic diagrams illustrating query–document matching paradigms in neural IR. Te figure contrasts existing
> approaches (sub-figures (a), (b), and (c)) with the proposed late interaction paradigm (sub-figure (d)). Other methods, including ColBERT (full retrieval), directly retrieve
> the top-1000 results from the entire collection. As the figure shows, BERT considerably improves search precision, raising MRR@10 by almost 7% against the best previous methods; simultaneously, it increases latency by up to tens of thousands
> of milliseconds even with a high-end GPU. Tis poses a challenging
> tradeoffsince raising query response times by as litle as 100ms is
> known to impact user experience and even measurably diminish
> revenue [17]. To tackle this problem, recent work has started exploring using Natural Language Understanding (NLU) techniques
> to augment traditional retrieval models like BM25 [32]. For example, Nogueira et al. [26, 28] expand documents with NLU-generated
> queries before indexing with BM25 scores and Dai & Callan [2] replace BM25’s term frequency with NLU-estimated term importance. Despite successfully reducing latency, these approaches generally
> reduce precision substantially relative to BERT. To reconcile efficiency and contextualization in IR, we propose
> ColBERT, a ranking model based on contextualized late interaction over BERT. As the name suggests, ColBERT proposes a novel
> late interaction paradigm for estimating relevance between a query
> q and a document d. Under late interaction, q and d are separately
> encoded into two sets of contextual embeddings, and relevance is
> evaluated using cheap and pruning-friendly computations between
> both sets—that is, fast computations that enable ranking without
> exhaustively evaluating every possible candidate. Figure 2 contrasts our proposed late interaction approach with
> existing neural matching paradigms. On the lef, Figure 2 (a) illustrates representation-focused rankers, which independently compute
> an embedding for q and another for d and estimate relevance as
> a single similarity score between two vectors [12, 41]. Moving to
> the right, Figure 2 (b) visualizes typical interaction-focused rankers. Instead of summarizing q and d into individual embeddings, these
> rankers model word- and phrase-level relationships across q and d
> and match them using a deep neural network (e.g., with CNNs/MLPs
> [22] or kernels [36]).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 12, section UNKNOWN

Chunk `a8f6c60b445c4eb467a1f720a489928caa1ffb1e7092756fbc9aa6601a6609cd`; source `arxiv:1810.04805`; paper_aggregation rank 10 similarity 0.7151699662208557 rerank None

> for natural language understanding. In Proceedings
> of the 2018 EMNLP Workshop BlackboxNLP: Analyzing and Interpreting Neural Networks for NLP,
> pages 353–355. Wei Wang, Ming Yan, and Chen Wu. 2018b. Multigranularity hierarchical attention fusion networks
> for reading comprehension and question answering. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1:
> Long Papers). Association for Computational Linguistics. Alex Warstadt, Amanpreet Singh, and Samuel R Bowman. 2018. Neural network acceptability judgments. arXiv preprint arXiv:1805.12471. Adina Williams, Nikita Nangia, and Samuel R Bowman. 2018. A broad-coverage challenge corpus
> for sentence understanding through inference. In
> NAACL. Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V
> Le,
> Mohammad Norouzi,
> Wolfgang Macherey,
> Maxim Krikun,
> Yuan Cao,
> Qin Gao,
> Klaus
> Macherey, et al. 2016. Google’s neural machine translation system: Bridging the gap between
> human and machine translation. arXiv preprint
> arXiv:1609.08144. Jason Yosinski, Jeff Clune, Yoshua Bengio, and Hod
> Lipson. 2014. How transferable are features in deep
> neural networks? In Advances in neural information
> processing systems, pages 3320–3328. Adams Wei Yu, David Dohan, Minh-Thang Luong, Rui
> Zhao, Kai Chen, Mohammad Norouzi, and Quoc V
> Le. 2018. QANet: Combining local convolution
> with global self-attention for reading comprehension. In ICLR. Rowan Zellers, Yonatan Bisk, Roy Schwartz, and Yejin
> Choi. 2018. Swag: A large-scale adversarial dataset
> for grounded commonsense inference. In Proceedings of the 2018 Conference on Empirical Methods
> in Natural Language Processing (EMNLP). Yukun Zhu, Ryan Kiros, Rich Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Torralba, and Sanja
> Fidler. 2015. Aligning books and movies: Towards
> story-like visual explanations by watching movies
> and reading books. In Proceedings of the IEEE
> international conference on computer vision, pages
> 19–27. Appendix for “BERT: Pre-training of
> Deep Bidirectional Transformers for
> Language Understanding”
> We organize the appendix into three sections:
> • Additional implementation details for BERT
> are presented in Appendix A;
> • Additional details for our experiments are
> presented in Appendix B; and
> • Additional ablation studies are presented in
> Appendix C. We present additional ablation studies for
> BERT including:
> – Effect of Number of Training Steps; and
> – Ablation for Different Masking Procedures. A
> Additional Details for BERT
> A.1
> Illustration of the Pre-training Tasks
> We provide examples of the pre-training tasks in
> the following.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### nlp-rag-07

How can retrieved documents provide non-parametric knowledge to language generation models?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 14, section UNKNOWN

Chunk `f7f46d59ca966b0002a03869ab70bd6b3a2a74387ed5f895f57768ad7347463b`; source `arxiv:2005.11401`; faiss_cosine rank 1 similarity 0.8200380206108093 rerank None; metadata_filtered_cosine rank 1 similarity 0.8200380206108093 rerank None; paper_aggregation rank 1 similarity 0.8200380206108093 rerank None; mmr_diversity rank 1 similarity 0.8200380206108093 rerank 0.5740266144275665

> How much knowledge can you pack into
> the parameters of a language model? arXiv e-prints, 2020. URL https://arxiv.org/abs/
> 2002.08910. [53] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: Bm25 and
> beyond. Found. Trends Inf. Retr., 3(4):333–389, April 2009. ISSN 1554-0669. doi: 10.1561/
> 1500000019. URL https://doi.org/10.1561/1500000019. [54] Irene Solaiman, Miles Brundage, Jack Clark, Amanda Askell, Ariel Herbert-Voss, Jeff Wu, Alec
> Radford, and Jian-Bing Wang. Release strategies and the social impacts of language models. ArXiv, abs/1908.09203, 2019. [55] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors, Advances
> in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates, Inc., 2015. URL http://papers.nips.cc/paper/5846-end-to-end-memory-networks.pdf. 14

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 2, section UNKNOWN

Chunk `c51719df323668c7f3c31dd7ea9a4f7b679f2b167f0353eecc1a7c7e8a196d5a`; source `arxiv:2005.11401`; faiss_cosine rank 2 similarity 0.8109079003334045 rerank None; metadata_filtered_cosine rank 2 similarity 0.8109079003334045 rerank None; mmr_diversity rank 4 similarity 0.8109079003334045 rerank 0.26763553023338305

> In contrast, we explore a setting where both
> parametric and non-parametric memory components are pre-trained and pre-loaded with extensive
> knowledge. Crucially, by using pre-trained access mechanisms, the ability to access knowledge is
> present without additional training. Our results highlight the benefits of combining parametric and non-parametric memory with generation for knowledge-intensive tasks—tasks that humans could not reasonably be expected to perform
> without access to an external knowledge source. Our RAG models achieve state-of-the-art results
> on open Natural Questions [29], WebQuestions [3] and CuratedTrec [2] and strongly outperform
> recent approaches that use specialised pre-training objectives on TriviaQA [24]. Despite these being
> extractive tasks, we find that unconstrained generation outperforms previous extractive approaches. For knowledge-intensive generation, we experiment with MS-MARCO [1] and Jeopardy question
> generation, and we find that our models generate responses that are more factual, specific, and
> diverse than a BART baseline. For FEVER [56] fact verification, we achieve results within 4.3% of
> state-of-the-art pipeline models which use strong retrieval supervision. Finally, we demonstrate that
> the non-parametric memory can be replaced to update the models’ knowledge as the world changes.1
> 2
> Methods
> We explore RAG models, which use the input sequence x to retrieve text documents z and use them
> as additional context when generating the target sequence y. As shown in Figure 1, our models
> leverage two components: (i) a retriever pη(z|x) with parameters η that returns (top-K truncated)
> distributions over text passages given a query x and (ii) a generator pθ(yi|x, z, y1:i−1) parametrized
> 1Code to run experiments with RAG has been open-sourced as part of the HuggingFace Transformers Library [66] and can be found at https://github.com/huggingface/transformers/blob/master/
> examples/rag/. An interactive demo of RAG models can be found at https://huggingface.co/rag/
> 2

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 9, section UNKNOWN

Chunk `54434aa40441c8944ed6772c69c8265a119a189ce54acd1fd10acc584550d48d`; source `arxiv:2005.11401`; faiss_cosine rank 3 similarity 0.8079560399055481 rerank None; metadata_filtered_cosine rank 3 similarity 0.8079560399055481 rerank None; mmr_diversity rank 5 similarity 0.8079560399055481 rerank 0.2655692279338836

> Retrieve-and-Edit approaches
> Our method shares some similarities with retrieve-and-edit style
> approaches, where a similar training input-output pair is retrieved for a given input, and then edited
> to provide a final output. These approaches have proved successful in a number of domains including
> Machine Translation [18, 22] and Semantic Parsing [21]. Our approach does have several differences,
> including less of emphasis on lightly editing a retrieved item, but on aggregating content from several
> pieces of retrieved content, as well as learning latent retrieval, and retrieving evidence documents
> rather than related training pairs. This said, RAG techniques may work well in these settings, and
> could represent promising future work. 6
> Discussion
> In this work, we presented hybrid generation models with access to parametric and non-parametric
> memory. We showed that our RAG models obtain state of the art results on open-domain QA. We
> found that people prefer RAG’s generation over purely parametric BART, finding RAG more factual
> and specific. We conducted an thorough investigation of the learned retrieval component, validating
> its effectiveness, and we illustrated how the retrieval index can be hot-swapped to update the model
> without requiring any retraining. In future work, it may be fruitful to investigate if the two components
> can be jointly pre-trained from scratch, either with a denoising objective similar to BART or some
> another objective. Our work opens up new research directions on how parametric and non-parametric
> memories interact and how to most effectively combine them, showing promise in being applied to a
> wide variety of NLP tasks. 9

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 19, section UNKNOWN

Chunk `0751e99035f7bad788f2a842be9f7930b1ce6a0c0753382ddd9d78b492ad9834`; source `arxiv:2005.11401`; faiss_cosine rank 4 similarity 0.8055962920188904 rerank None; metadata_filtered_cosine rank 4 similarity 0.8055962920188904 rerank None; mmr_diversity rank 6 similarity 0.8055962920188904 rerank 0.2639174044132232

> Table 7: Number of instances in the datasets used. *A hidden subset of this data is used for evaluation
> Task
> Train
> Development
> Test
> Natural Questions
> 79169
> 8758
> 3611
> TriviaQA
> 78786
> 8838
> 11314
> WebQuestions
> 3418
> 362
> 2033
> CuratedTrec
> 635
> 134
> 635
> Jeopardy Question Generation
> 97392
> 13714
> 26849
> MS-MARCO
> 153726
> 12468
> 101093*
> FEVER-3-way
> 145450
> 10000
> 10000
> FEVER-2-way
> 96966
> 6666
> 6666
> parameters. The best performing "closed-book" (parametric only) open-domain QA model is T5-11B
> with 11 Billion trainable parameters. The T5 model with the closest number of parameters to our
> models is T5-large (770M parameters), which achieves a score of 28.9 EM on Natural Questions [52],
> substantially below the 44.5 that RAG-Sequence achieves, indicating that hybrid parametric/nonparametric models require far fewer trainable parameters for strong open-domain QA performance. The non-parametric memory index does not consist of trainable parameters, but does consists of 21M
> 728 dimensional vectors, consisting of 15.3B values. These can be easily be stored at 8-bit floating
> point precision to manage memory and disk footprints. H
> Retrieval Collapse
> In preliminary experiments, we observed that for some tasks such as story generation [11], the
> retrieval component would “collapse” and learn to retrieve the same documents regardless of the
> input. In these cases, once retrieval had collapsed, the generator would learn to ignore the documents,
> and the RAG model would perform equivalently to BART. The collapse could be due to a less-explicit
> requirement for factual knowledge in some tasks, or the longer target sequences, which could result
> in less informative gradients for the retriever. Perez et al. [46] also found spurious retrieval results
> when optimizing a retrieval component in order to improve performance on downstream tasks. I
> Number of instances per dataset
> The number of training, development and test datapoints in each of our datasets is shown in Table 7. 19

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 1, section UNKNOWN

Chunk `21661f4c6b1930ac3b2c91eaa606a95f601ed929bfc72e8ea4eb42eff5c11140`; source `arxiv:2005.11401`; faiss_cosine rank 5 similarity 0.8044525384902954 rerank None; metadata_filtered_cosine rank 5 similarity 0.8044525384902954 rerank None; mmr_diversity rank 7 similarity 0.8044525384902954 rerank 0.2631167769432067

> Retrieval-Augmented Generation for
> Knowledge-Intensive NLP Tasks
> Patrick Lewis†‡, Ethan Perez⋆,
> Aleksandra Piktus†, Fabio Petroni†, Vladimir Karpukhin†, Naman Goyal†, Heinrich Küttler†,
> Mike Lewis†, Wen-tau Yih†, Tim Rocktäschel†‡, Sebastian Riedel†‡, Douwe Kiela†
> †Facebook AI Research; ‡University College London; ⋆New York University;
> plewis@fb.com
> Abstract
> Large pre-trained language models have been shown to store factual knowledge
> in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance
> lags behind task-specific architectures. Additionally, providing provenance for their
> decisions and updating their world knowledge remain open research problems. Pretrained models with a differentiable access mechanism to explicit non-parametric
> memory have so far been only investigated for extractive downstream tasks. We
> explore a general-purpose fine-tuning recipe for retrieval-augmented generation
> (RAG) — models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric
> memory is a pre-trained seq2seq model and the non-parametric memory is a dense
> vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages
> across the whole generated sequence, and another which can use different passages
> per token. We fine-tune and evaluate our models on a wide range of knowledgeintensive NLP tasks and set the state of the art on three open domain QA tasks,
> outperforming parametric seq2seq models and task-specific retrieve-and-extract
> architectures. For language generation tasks, we find that RAG models generate
> more specific, diverse and factual language than a state-of-the-art parametric-only
> seq2seq baseline. 1
> Introduction
> Pre-trained neural language models have been shown to learn a substantial amount of in-depth knowledge from data [47]. They can do so without any access to an external memory, as a parameterized
> implicit knowledge base [51, 52]. While this development is exciting, such models do have downsides: They cannot easily expand or revise their memory, can’t straightforwardly provide insight into
> their predictions, and may produce “hallucinations” [38]. Hybrid models that combine parametric
> memory with non-parametric (i.e., retrieval-based) memories [20, 26, 48] can address some of these
> issues because knowledge can be directly revised and expanded, and accessed knowledge can be
> inspected and interpreted. REALM [20] and ORQA [31], two recently introduced models that
> combine masked language models [8] with a differentiable retriever, have shown promising results,
> arXiv:2005.11401v4 [cs.CL] 12 Apr 2021

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 7, section UNKNOWN

Chunk `eba89e765cee21dbeb540999d12d41a5757e9e0304935aad98a563cd0f0ca8c7`; source `arxiv:2005.11401`; faiss_cosine rank 6 similarity 0.8030462861061096 rerank None; metadata_filtered_cosine rank 6 similarity 0.8030462861061096 rerank None; mmr_diversity rank 8 similarity 0.8030462861061096 rerank 0.26213240027427664

> Document 1: his works are considered classics of American
> literature ... His wartime experiences formed the basis for his novel
> ”A Farewell to Arms” (1929) ... Document 2: ... artists of the 1920s ”Lost Generation” expatriate
> community. His debut novel, ”The Sun Also Rises”, was published
> in 1926. BOS ”
> The
> Sun
> Also
> R
> ises
> ”
> is
> a
> novel
> by
> this
> authorof
> ”
> A
> Fare
> well
> to
> Arms”
> Doc 1
> Doc 2
> Doc 3
> Doc 4
> Doc 5
> Figure 2: RAG-Token document posterior p(zi|x, yi, y−i) for each generated token for input “Hemingway" for Jeopardy generation with 5 retrieved documents. The posterior for document 1 is high
> when generating “A Farewell to Arms" and for document 2 when generating “The Sun Also Rises". Table 3: Examples from generation tasks. RAG models generate more specific and factually accurate
> responses. ‘?’ indicates factually incorrect responses, * indicates partially correct responses. Task
> Input
> Model
> Generation
> MSMARCO
> define middle
> ear
> BART
> ?The middle ear is the part of the ear between the middle ear and the nose. RAG-T The middle ear is the portion of the ear internal to the eardrum. RAG-S The middle ear includes the tympanic cavity and the three ossicles. what currency
> needed in
> scotland
> BART
> The currency needed in Scotland is Pound sterling. RAG-T Pound is the currency needed in Scotland. RAG-S The currency needed in Scotland is the pound sterling. Jeopardy
> Question
> Gener
> -ation
> Washington
> BART
> ?This state has the largest number of counties in the U.S. RAG-T It’s the only U.S. state named for a U.S. president
> RAG-S It’s the state where you’ll find Mount Rainier National Park
> The Divine
> Comedy
> BART
> *This epic poem by Dante is divided into 3 parts: the Inferno, the Purgatorio & the Purgatorio
> RAG-T Dante’s "Inferno" is the first part of this epic poem
> RAG-S This 14th century work is divided into 3 sections: "Inferno", "Purgatorio" & "Paradiso"
> For 2-way classification, we compare against Thorne and Vlachos [57], who train RoBERTa [35]
> to classify the claim as true or false given the gold evidence sentence. RAG achieves an accuracy
> within 2.7% of this model, despite being supplied with only the claim and retrieving its own evidence. We also analyze whether documents retrieved by RAG correspond to documents annotated as gold
> evidence in FEVER. We calculate the overlap in article titles between the top k documents retrieved
> by RAG and gold evidence annotations.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 8, section UNKNOWN

Chunk `435bb08116556c16f91527e3507c5d07c70e488a965d5a835f8d834fb0a5eaf2`; source `arxiv:2005.11401`; faiss_cosine rank 7 similarity 0.802947461605072 rerank None; metadata_filtered_cosine rank 7 similarity 0.802947461605072 rerank None; mmr_diversity rank 9 similarity 0.802947461605072 rerank 0.26206322312355035

> Table 4: Human assessments for the Jeopardy
> Question Generation Task. Factuality
> Specificity
> BART better
> 7.1%
> 16.8%
> RAG better
> 42.7%
> 37.4%
> Both good
> 11.7%
> 11.8%
> Both poor
> 17.7%
> 6.9%
> No majority
> 20.8%
> 20.1%
> Table 5: Ratio of distinct to total tri-grams for
> generation tasks. MSMARCO
> Jeopardy QGen
> Gold
> 89.6%
> 90.0%
> BART
> 70.7%
> 32.4%
> RAG-Token
> 77.8%
> 46.8%
> RAG-Seq. 83.5%
> 53.8%
> Table 6: Ablations on the dev set. As FEVER is a classification task, both RAG models are equivalent. Model
> NQ
> TQA
> WQ
> CT
> Jeopardy-QGen
> MSMarco
> FVR-3
> FVR-2
> Exact Match
> B-1
> QB-1
> R-L
> B-1
> Label Accuracy
> RAG-Token-BM25
> 29.7
> 41.5
> 32.1
> 33.1
> 17.5
> 22.3
> 55.5
> 48.4
> 75.1
> 91.6
> RAG-Sequence-BM25
> 31.8
> 44.1
> 36.6
> 33.8
> 11.1
> 19.5
> 56.5
> 46.9
> RAG-Token-Frozen
> 37.8
> 50.1
> 37.1
> 51.1
> 16.7
> 21.7
> 55.9
> 49.4
> 72.9
> 89.4
> RAG-Sequence-Frozen
> 41.2
> 52.1
> 41.8
> 52.6
> 11.8
> 19.6
> 56.7
> 47.3
> RAG-Token
> 43.5
> 54.8
> 46.5
> 51.9
> 17.9
> 22.6
> 56.2
> 49.4
> 74.5
> 90.6
> RAG-Sequence
> 44.0
> 55.8
> 44.9
> 53.4
> 15.3
> 21.5
> 57.2
> 47.5
> between these dates and use a template “Who is {position}?” (e.g. “Who is the President of Peru?”)
> to query our NQ RAG model with each index. RAG answers 70% correctly using the 2016 index for
> 2016 world leaders and 68% using the 2018 index for 2018 world leaders. Accuracy with mismatched
> indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders). This shows we can update RAG’s world knowledge by simply replacing its non-parametric memory. Effect of Retrieving more documents
> Models are trained with either 5 or 10 retrieved latent
> documents, and we do not observe significant differences in performance between them. We have the
> flexibility to adjust the number of retrieved documents at test time, which can affect performance and
> runtime. Figure 3 (left) shows that retrieving more documents at test time monotonically improves
> Open-domain QA results for RAG-Sequence, but performance peaks for RAG-Token at 10 retrieved
> documents. Figure 3 (right) shows that retrieving more documents leads to higher Rouge-L for
> RAG-Token at the expense of Bleu-1, but the effect is less pronounced for RAG-Sequence.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 18, section UNKNOWN

Chunk `853bc9c8710afb6e12a5ed0762b9ed84de2e2f0b68b7b65c5fdc9be033ab3098`; source `arxiv:2005.11401`; faiss_cosine rank 8 similarity 0.8018666505813599 rerank None; metadata_filtered_cosine rank 8 similarity 0.8018666505813599 rerank None; mmr_diversity rank 10 similarity 0.8018666505813599 rerank 0.26130665540695186

> We find that our performance is much higher using the official Wiki test set, rather than the more
> conventional open-domain test set, which we attribute to the official Wiki test set questions being
> simpler to answer from Wikipedia. E
> Further Details on FEVER
> For FEVER classification, we follow the practice from [32], and first re-generate the claim, and
> then classify using the representation of the final hidden state, before finally marginalizing across
> documents to obtain the class probabilities. The FEVER task traditionally has two sub-tasks. The
> first is to classify the claim as either "Supported", "Refuted" or "Not Enough Info", which is the task
> we explore in the main paper. FEVER’s other sub-task involves extracting sentences from Wikipedia
> as evidence supporting the classification prediction. As FEVER uses a different Wikipedia dump to
> us, directly tackling this task is not straightforward. We hope to address this in future work. F
> Null Document Probabilities
> We experimented with adding "Null document" mechanism to RAG, similar to REALM [20] in order
> to model cases where no useful information could be retrieved for a given input. Here, if k documents
> were retrieved, we would additionally "retrieve" an empty document and predict a logit for the null
> document, before marginalizing over k + 1 predictions. We explored modelling this null document
> logit by learning (i) a document embedding for the null document, (ii) a static learnt bias term, or
> (iii) a neural network to predict the logit. We did not find that these improved performance, so in
> the interests of simplicity, we omit them. For Open MS-MARCO, where useful retrieved documents
> cannot always be retrieved, we observe that the model learns to always retrieve a particular set of
> documents for questions that are less likely to benefit from retrieval, suggesting that null document
> mechanisms may not be necessary for RAG. G
> Parameters
> Our RAG models contain the trainable parameters for the BERT-base query and document encoder of
> DPR, with 110M parameters each (although we do not train the document encoder ourselves) and
> 406M trainable parameters from BART-large, 406M parameters, making a total of 626M trainable
> 18

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 7, section UNKNOWN

Chunk `045b24cf04ff1f2f566c322f68ed5175534a80a37bdd67df18e3c81b56692ffb`; source `arxiv:2005.11401`; faiss_cosine rank 9 similarity 0.8000943660736084 rerank None; metadata_filtered_cosine rank 9 similarity 0.8000943660736084 rerank None

> We also analyze whether documents retrieved by RAG correspond to documents annotated as gold
> evidence in FEVER. We calculate the overlap in article titles between the top k documents retrieved
> by RAG and gold evidence annotations. We find that the top retrieved document is from a gold article
> in 71% of cases, and a gold article is present in the top 10 retrieved articles in 90% of cases. 4.5
> Additional Results
> Generation Diversity
> Section 4.3 shows that RAG models are more factual and specific than
> BART for Jeopardy question generation. Following recent work on diversity-promoting decoding
> [33, 59, 39], we also investigate generation diversity by calculating the ratio of distinct ngrams to
> total ngrams generated by different models. Table 5 shows that RAG-Sequence’s generations are
> more diverse than RAG-Token’s, and both are significantly more diverse than BART without needing
> any diversity-promoting decoding. Retrieval Ablations
> A key feature of RAG is learning to retrieve relevant information for the task. To assess the effectiveness of the retrieval mechanism, we run ablations where we freeze the retriever
> during training. As shown in Table 6, learned retrieval improves results for all tasks. We compare RAG’s dense retriever to a word overlap-based BM25 retriever [53]. Here, we replace
> RAG’s retriever with a fixed BM25 system, and use BM25 retrieval scores as logits when calculating
> p(z|x). Table 6 shows the results. For FEVER, BM25 performs best, perhaps since FEVER claims are
> heavily entity-centric and thus well-suited for word overlap-based retrieval. Differentiable retrieval
> improves results on all other tasks, especially for Open-Domain QA, where it is crucial. Index hot-swapping
> An advantage of non-parametric memory models like RAG is that knowledge
> can be easily updated at test time. Parametric-only models like T5 or BART need further training to
> update their behavior as the world changes. To demonstrate, we build an index using the DrQA [5]
> Wikipedia dump from December 2016 and compare outputs from RAG using this index to the newer
> index from our main results (December 2018). We prepare a list of 82 world leaders who had changed
> 7

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 12, section UNKNOWN

Chunk `9f3ef2ab28ab0769c05d21d20d08ab08b7dda2099307cc78bf55613f84cc2e07`; source `arxiv:2005.11401`; faiss_cosine rank 10 similarity 0.7996149063110352 rerank None; metadata_filtered_cosine rank 10 similarity 0.7996149063110352 rerank None

> Toutanova, Llion Jones, Ming-Wei Chang, Andrew Dai, Jakob
> Uszkoreit, Quoc Le, and Slav Petrov. Natural Questions:
> a Benchmark for Question Answering Research. Transactions of the Association of Computational Linguistics, 2019. URL https://tomkwiat.users.x20web.corp.google.com/papers/
> natural-questions/main-1455-kwiatkowski.pdf. [30] Guillaume Lample, Alexandre Sablayrolles, Marc’ Aurelio Ranzato, Ludovic Denoyer, and
> Herve Jegou. Large memory layers with product keys. In H. Wallach, H. Larochelle,
> A. Beygelzimer, F. d’ Alché-Buc, e. Fox, and R. Garnett, editors, Advances in Neural Information Processing Systems 32, pages 8548–8559. Curran Associates, Inc., 2019. URL http:
> //papers.nips.cc/paper/9061-large-memory-layers-with-product-keys.pdf. [31] Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. Latent retrieval for weakly supervised
> open domain question answering. In Proceedings of the 57th Annual Meeting of the Association
> 12

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 6, section UNKNOWN

Chunk `6177659bb17cd663b66e47f4788a257482a3ffed5895fb6f6206826c70778e3c`; source `arxiv:2004.04906`; paper_aggregation rank 2 similarity 0.7675896883010864 rerank None; mmr_diversity rank 2 similarity 0.7675896883010864 rerank 0.2600030541419982

> 42.6
> 63.1
> 78.3
> Gold
> 7

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 2, section UNKNOWN

Chunk `0b001009879392c9654a9ae956a8dc6d82bcdba4d3845b9309439f7ef1ae6b3a`; source `arxiv:2104.08663`; paper_aggregation rank 3 similarity 0.7636582851409912 rerank None; mmr_diversity rank 3 similarity 0.7636582851409912 rerank 0.25618376731872555

> Fact Checking
> Citation-Prediction
> Wiki
> FEVER
> QUERY
> DOCS
> Natural Claim
> Wikipedia Articles
> Wiki
> Climate-FEVER
> QUERY
> DOCS
> Climate-based Claim
> Wikipedia Articles
> SciFact
> QUERY
> DOCS
> Scientific claim
> PubMed Articles
> Scientific
> SCIDOCS
> QUERY
> DOCS
> Article Title
> PubMed Articles
> Scientific
> Dup. Question Retrieval
> Quora
> Quora
> QUERY
> DOCS
> StackEx. CQADupStack
> QUERY
> DOCS
> Argument Retrieval
> Misc. QUERY
> DOCS
> Misc. ArguAna
> QUERY
> DOCS
> Tóuche-2020
> Query Title
> Query Title + Body
> Query Title
> Quora Questions
> Argument
> Idebate Arguments
> Args.me Arguments
> News Retrieval
> TREC-NEWS
> QUERY
> DOCS
> News Articles
> News
> Tweet Retrieval
> Signal-1M
> QUERY
> DOCS
> News Headline
> Twitter Tweets
> Twitter
> Question-Answering
> Wiki
> NQ
> QUERY
> DOCS
> Wiki
> HotpotQA
> QUERY
> DOCS
> FiQA-2018
> QUERY
> DOCS
> Finance
> Bio-Medical IR
> QUERY
> DOCS
> Scientific
> BioASQ
> QUERY
> DOCS
> NFCorpus
> QUERY
> DOCS
> Scientific
> Entity Retrieval
> DBPedia
> QUERY
> DOCS
> Entity-based Query
> DBPedia Articles
> Wiki
> TREC-COVID
> Scientific
> Wikipedia Articles
> Wikipedia Articles
> Natural Query
> Multi-Hop Query
> CORD-19 Articles
> PubMed Articles
> PubMed Articles
> COVID-19 Query
> Nutrition Facts
> Bio-Medical Query
> Financial Query
> Investment Articles
> Controversial Query
> 9 Tasks
> 18 Datasets
> News Headline
> Robust04
> QUERY
> DOCS
> News
> News Articles
> News Query
> Figure 1: An overview of the diverse tasks and datasets in BEIR benchmark. So far, it is unclear how well existing trained neural models will perform for other text domains or
> textual retrieval tasks. Even more important, it is unclear how well different approaches, like sparse
> embeddings vs. dense embeddings, generalize to out-of-distribution data. In this work, we present a novel robust and heterogeneous benchmark called BEIR (Benchmarking
> IR), comprising of 18 retrieval datasets for comparison and evaluation of model generalization. Prior
> retrieval benchmarks [19, 50] have issues of a comparatively narrow evaluation focusing either only
> on a single task, like question-answering, or on a certain domain. In BEIR, we focus on Diversity, we
> include nine different retrieval tasks: Fact checking, citation prediction, duplicate question retrieval,
> argument retrieval, news retrieval, question answering, tweet retrieval, bio-medical IR, and entity
> retrieval. Further, we include datasets from diverse text domains, datasets that cover broad topics (like
> Wikipedia) and specialized topics (like COVID-19 publications), different text types (news articles vs.
> Tweets), datasets of various sizes (3.6k - 15M documents), and datasets with different query lengths
> (average query length between 3 and 192 words) and document lengths (average document length
> between 11 and 635 words). We use BEIR to evaluate ten diverse retrieval methods from five broad architectures: lexical, sparse,
> dense, late interaction, and re-ranking.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 11, section UNKNOWN

Chunk `2c479e9ca7c0278f1d1a4e5f083d8b2bc2e7d3ab4e4af1b4c41504297f97f5ed`; source `arxiv:1706.03762`; paper_aggregation rank 4 similarity 0.7571728229522705 rerank None

> [5] Kyunghyun Cho, Bart van Merrienboer, Caglar Gulcehre, Fethi Bougares, Holger Schwenk,
> and Yoshua Bengio. Learning phrase representations using rnn encoder-decoder for statistical
> machine translation. CoRR, abs/1406.1078, 2014. [6] Francois Chollet. Xception: Deep learning with depthwise separable convolutions. arXiv
> preprint arXiv:1610.02357, 2016. [7] Junyoung Chung, Çaglar Gülçehre, Kyunghyun Cho, and Yoshua Bengio. Empirical evaluation
> of gated recurrent neural networks on sequence modeling. CoRR, abs/1412.3555, 2014. [8] Chris Dyer, Adhiguna Kuncoro, Miguel Ballesteros, and Noah A. Smith. Recurrent neural
> network grammars. In Proc. of NAACL, 2016. [9] Jonas Gehring, Michael Auli, David Grangier, Denis Yarats, and Yann N. Dauphin. Convolutional sequence to sequence learning. arXiv preprint arXiv:1705.03122v2, 2017. [10] Alex Graves. Generating sequences with recurrent neural networks. arXiv preprint
> arXiv:1308.0850, 2013. [11] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In Proceedings of the IEEE Conference on Computer Vision and Pattern
> Recognition, pages 770–778, 2016. [12] Sepp Hochreiter, Yoshua Bengio, Paolo Frasconi, and Jürgen Schmidhuber. Gradient flow in
> recurrent nets: the difficulty of learning long-term dependencies, 2001. [13] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural computation,
> 9(8):1735–1780, 1997. [14] Zhongqiang Huang and Mary Harper. Self-training PCFG grammars with latent annotations
> across languages. In Proceedings of the 2009 Conference on Empirical Methods in Natural
> Language Processing, pages 832–841. ACL, August 2009. [15] Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu. Exploring
> the limits of language modeling. arXiv preprint arXiv:1602.02410, 2016. [16] Łukasz Kaiser and Samy Bengio. Can active memory replace attention? In Advances in Neural
> Information Processing Systems, (NIPS), 2016. [17] Łukasz Kaiser and Ilya Sutskever. Neural GPUs learn algorithms. In International Conference
> on Learning Representations (ICLR), 2016. [18] Nal Kalchbrenner, Lasse Espeholt, Karen Simonyan, Aaron van den Oord, Alex Graves, and Koray Kavukcuoglu. Neural machine translation in linear time. arXiv preprint arXiv:1610.10099v2,
> 2017. [19] Yoon Kim, Carl Denton, Luong Hoang, and Alexander M. Rush. Structured attention networks. In International Conference on Learning Representations, 2017. [20] Diederik Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In ICLR, 2015. [21] Oleksii Kuchaiev and Boris Ginsburg. Factorization tricks for LSTM networks. arXiv preprint
> arXiv:1703.10722, 2017. [22] Zhouhan Lin, Minwei Feng, Cicero Nogueira dos Santos, Mo Yu, Bing Xiang, Bowen
> Zhou, and Yoshua Bengio. A structured self-attentive sentence embedding. arXiv preprint
> arXiv:1703.03130, 2017. [23] Minh-Thang Luong, Quoc V. Le, Ilya Sutskever, Oriol Vinyals, and Lukasz Kaiser. Multi-task
> sequence to sequence learning.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 4, section UNKNOWN

Chunk `88c0b4ab21070dd8600e466ddcb4dc4a784ad46113f0a69e6a97a45ab845fb4b`; source `arxiv:1903.10676`; paper_aggregation rank 5 similarity 0.7498911023139954 rerank None

> Field
> Task
> Dataset
> SOTA
> BERT-Base
> SCIBERT
> Frozen
> Finetune
> Frozen
> Finetune
> Bio
> NER
> BC5CDR (Li et al., 2016)
> 88.857
> 85.08
> 86.72
> 88.73
> 90.01
> JNLPBA (Collier and Kim, 2004)
> 78.58
> 74.05
> 76.09
> 75.77
> 77.28
> NCBI-disease (Dogan et al., 2014)
> 89.36
> 84.06
> 86.88
> 86.39
> 88.57
> PICO
> EBM-NLP (Nye et al., 2018)
> 66.30
> 61.44
> 71.53
> 68.30
> 72.28
> DEP
> GENIA (Kim et al., 2003) - LAS
> 91.92
> 90.22
> 90.33
> 90.36
> 90.43
> GENIA (Kim et al., 2003) - UAS
> 92.84
> 91.84
> 91.89
> 92.00
> 91.99
> REL
> ChemProt (Kringelum et al., 2016)
> 76.68
> 68.21
> 79.14
> 75.03
> 83.64
> CS
> NER
> SciERC (Luan et al., 2018)
> 64.20
> 63.58
> 65.24
> 65.77
> 67.57
> REL
> SciERC (Luan et al., 2018)
> n/a
> 72.74
> 78.71
> 75.25
> 79.97
> CLS
> ACL-ARC (Jurgens et al., 2018)
> 67.9
> 62.04
> 63.91
> 60.74
> 70.98
> Multi
> CLS
> Paper Field
> n/a
> 63.64
> 65.37
> 64.38
> 65.71
> SciCite (Cohan et al., 2019)
> 84.0
> 84.31
> 84.85
> 85.42
> 85.49
> Average
> 73.58
> 77.16
> 76.01
> 79.27
> Table 1: Test performances of all BERT variants on all tasks and datasets. Bold indicates the SOTA result (multiple
> results bolded if difference within 95% bootstrap confidence interval). Keeping with past work, we report macro
> F1 scores for NER (span-level), macro F1 scores for REL and CLS (sentence-level), and macro F1 for PICO
> (token-level), and micro F1 for ChemProt specifically. For DEP, we report labeled (LAS) and unlabeled (UAS)
> attachment scores (excluding punctuation) for the same model with hyperparameters tuned for LAS. All results
> are the average of multiple runs with different random seeds. Task
> Dataset
> BIOBERT
> SCIBERT
> NER
> BC5CDR
> 88.85
> 90.01
> JNLPBA
> 77.59
> 77.28
> NCBI-disease
> 89.36
> 88.57
> REL
> ChemProt
> 76.68
> 83.64
> Table 2:
> Comparing SCIBERT with the reported
> BIOBERT results on biomedical datasets. BC5CDR and ChemProt, and performs similarly
> on JNLPBA despite being trained on a substantially smaller biomedical corpus. 4.2
> Computer Science Domain
> We observe that SCIBERT outperforms BERTBase on computer science tasks (+3.55 F1 with
> finetuning and +1.13 F1 without). In addition,
> SCIBERT achieves new SOTA results on ACLARC (Cohan et al., 2019), and the NER part of
> SciERC (Luan et al., 2018). For relations in SciERC, our results are not comparable with those in
> Luan et al. (2018) because we are performing relation classification given gold entities, while they
> perform joint entity and relation extraction. 4.3
> Multiple Domains
> We observe that SCIBERT outperforms BERTBase on the multidomain tasks (+0.49 F1 with
> finetuning and +0.93 F1 without). In addition, SCIBERT outperforms the SOTA on SciCite (Cohan et al., 2019).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 2, section UNKNOWN

Chunk `bd7fdd808fe36233187d46c17a839a69994ecf4f0d7b9d89962381a8dc01e51f`; source `arxiv:2004.12832`; paper_aggregation rank 6 similarity 0.7407162189483643 rerank None

> Query
> Document
> MaxSim
> ∑
> MaxSim
> MaxSim
> s
> Query
> CNN / Match Kernels
> CNN / Match Kernels / MLP
> MLP
> s
> Document
> (c) All-to-all Interaction
> (e.g., BERT)
> (b) Query-Document Interaction
> (e.g., DRMM, KNRM, Conv-KNRM)
> (d) Late Interaction
> (i.e., the proposed ColBERT)
> (a) Representation-based Similarity
> (e.g., DSSM, SNRM)
> Query
> Document
> s
> Query
> Document
> s
> Figure 2: Schematic diagrams illustrating query–document matching paradigms in neural IR. Te figure contrasts existing
> approaches (sub-figures (a), (b), and (c)) with the proposed late interaction paradigm (sub-figure (d)). Other methods, including ColBERT (full retrieval), directly retrieve
> the top-1000 results from the entire collection. As the figure shows, BERT considerably improves search precision, raising MRR@10 by almost 7% against the best previous methods; simultaneously, it increases latency by up to tens of thousands
> of milliseconds even with a high-end GPU. Tis poses a challenging
> tradeoffsince raising query response times by as litle as 100ms is
> known to impact user experience and even measurably diminish
> revenue [17]. To tackle this problem, recent work has started exploring using Natural Language Understanding (NLU) techniques
> to augment traditional retrieval models like BM25 [32]. For example, Nogueira et al. [26, 28] expand documents with NLU-generated
> queries before indexing with BM25 scores and Dai & Callan [2] replace BM25’s term frequency with NLU-estimated term importance. Despite successfully reducing latency, these approaches generally
> reduce precision substantially relative to BERT. To reconcile efficiency and contextualization in IR, we propose
> ColBERT, a ranking model based on contextualized late interaction over BERT. As the name suggests, ColBERT proposes a novel
> late interaction paradigm for estimating relevance between a query
> q and a document d. Under late interaction, q and d are separately
> encoded into two sets of contextual embeddings, and relevance is
> evaluated using cheap and pruning-friendly computations between
> both sets—that is, fast computations that enable ranking without
> exhaustively evaluating every possible candidate. Figure 2 contrasts our proposed late interaction approach with
> existing neural matching paradigms. On the lef, Figure 2 (a) illustrates representation-focused rankers, which independently compute
> an embedding for q and another for d and estimate relevance as
> a single similarity score between two vectors [12, 41]. Moving to
> the right, Figure 2 (b) visualizes typical interaction-focused rankers. Instead of summarizing q and d into individual embeddings, these
> rankers model word- and phrase-level relationships across q and d
> and match them using a deep neural network (e.g., with CNNs/MLPs
> [22] or kernels [36]).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 3, section UNKNOWN

Chunk `fa699eb3c5cddedd61a30dd13c1d093b7e0803f121ac1f670c7ef5dd4bb2b5d4`; source `arxiv:1810.04805`; paper_aggregation rank 7 similarity 0.7333930730819702 rerank None

> BERT
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Question
> Paragraph
> Start/End Span
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Masked Sentence A
> Masked Sentence B
> Pre-training
> Fine-Tuning
> NSP
> Mask LM
> Mask LM
> Unlabeled Sentence A and B Pair 
> SQuAD
> Question Answer Pair
> NER
> MNLI
> Figure 1: Overall pre-training and fine-tuning procedures for BERT. Apart from output layers, the same architectures are used in both pre-training and fine-tuning. The same pre-trained model parameters are used to initialize
> models for different down-stream tasks. During fine-tuning, all parameters are fine-tuned. [CLS] is a special
> symbol added in front of every input example, and [SEP] is a special separator token (e.g. separating questions/answers). ing and auto-encoder objectives have been used
> for pre-training such models (Howard and Ruder,
> 2018; Radford et al., 2018; Dai and Le, 2015). 2.3
> Transfer Learning from Supervised Data
> There has also been work showing effective transfer from supervised tasks with large datasets, such
> as natural language inference (Conneau et al.,
> 2017) and machine translation (McCann et al.,
> 2017). Computer vision research has also demonstrated the importance of transfer learning from
> large pre-trained models, where an effective recipe
> is to fine-tune models pre-trained with ImageNet (Deng et al., 2009; Yosinski et al., 2014). 3
> BERT
> We introduce BERT and its detailed implementation in this section. There are two steps in our
> framework: pre-training and fine-tuning. During pre-training, the model is trained on unlabeled
> data over different pre-training tasks. For finetuning, the BERT model is first initialized with
> the pre-trained parameters, and all of the parameters are fine-tuned using labeled data from the
> downstream tasks. Each downstream task has separate fine-tuned models, even though they are initialized with the same pre-trained parameters. The
> question-answering example in Figure 1 will serve
> as a running example for this section. A distinctive feature of BERT is its unified architecture across different tasks. There is minimal difference between the pre-trained architecture and the final downstream architecture.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 6, section UNKNOWN

Chunk `bcd9418b179cf36e8cb914d1a339d305a3d1eba19445abb72a8a688c942fc541`; source `arxiv:1710.10903`; paper_aggregation rank 8 similarity 0.7299998998641968 rerank None

> Published as a conference paper at ICLR 2018
> Table 1: Summary of the datasets used in our experiments. Cora
> Citeseer
> Pubmed
> PPI
> Task
> Transductive
> Transductive
> Transductive
> Inductive
> # Nodes
> 2708 (1 graph)
> 3327 (1 graph)
> 19717 (1 graph)
> 56944 (24 graphs)
> # Edges
> 5429
> 4732
> 44338
> 818716
> # Features/Node
> 1433
> 3703
> 500
> 50
> # Classes
> 7
> 6
> 3
> 121 (multilabel)
> # Training Nodes
> 140
> 120
> 60
> 44906 (20 graphs)
> # Validation Nodes
> 500
> 500
> 500
> 6514 (2 graphs)
> # Test Nodes
> 1000
> 1000
> 1000
> 5524 (2 graphs)
> well as inductive), achieving or matching state-of-the-art performance across all of them. This section summarizes our experimental setup, results, and a brief qualitative analysis of a GAT model’s
> extracted feature representations. 3.1
> DATASETS
> Transductive learning
> We utilize three standard citation network benchmark datasets—Cora,
> Citeseer and Pubmed (Sen et al., 2008)—and closely follow the transductive experimental setup of
> Yang et al. (2016). In all of these datasets, nodes correspond to documents and edges to (undirected)
> citations. Node features correspond to elements of a bag-of-words representation of a document. Each node has a class label. We allow for only 20 nodes per class to be used for training—however,
> honoring the transductive setup, the training algorithm has access to all of the nodes’ feature vectors. The predictive power of the trained models is evaluated on 1000 test nodes, and we use 500
> additional nodes for validation purposes (the same ones as used by Kipf & Welling (2017)). The
> Cora dataset contains 2708 nodes, 5429 edges, 7 classes and 1433 features per node. The Citeseer
> dataset contains 3327 nodes, 4732 edges, 6 classes and 3703 features per node. The Pubmed dataset
> contains 19717 nodes, 44338 edges, 3 classes and 500 features per node. Inductive learning
> We make use of a protein-protein interaction (PPI) dataset that consists of
> graphs corresponding to different human tissues (Zitnik & Leskovec, 2017). The dataset contains
> 20 graphs for training, 2 for validation and 2 for testing. Critically, testing graphs remain completely unobserved during training. To construct the graphs, we used the preprocessed data provided
> by Hamilton et al. (2017). The average number of nodes per graph is 2372. Each node has 50
> features that are composed of positional gene sets, motif gene sets and immunological signatures.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 3, section UNKNOWN

Chunk `5e503ef1d99a78cd350e19c5a8899dcceccd7e3955ca5a7dcd6950444ee1ad58`; source `arxiv:1609.02907`; paper_aggregation rank 9 similarity 0.7232446670532227 rerank None

> ˆA ReLU

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 4, section UNKNOWN

Chunk `4358e1cb657d28d446d0eab305cda0c18d76e58391c27db18d885c42702ce0a5`; source `arxiv:1512.03385`; paper_aggregation rank 10 similarity 0.7034565806388855 rerank None

> 7x7 conv, 64, /2
> pool, /2
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 128, /2
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 256, /2
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 512, /2
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> avg pool
> fc 1000
> image
> 3x3 conv, 512
> 3x3 conv, 64
> 3x3 conv, 64
> pool, /2
> 3x3 conv, 128
> 3x3 conv, 128
> pool, /2
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> pool, /2
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> pool, /2
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> pool, /2
> fc 4096
> fc 4096
> fc 1000
> image
> output 
> size: 112
> output 
> size: 224
> output 
> size: 56
> output 
> size: 28
> output 
> size: 14
> output 
> size: 7
> output 
> size: 1
> VGG-19
> 34-layer plain
> 7x7 conv, 64, /2
> pool, /2
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 64
> 3x3 conv, 128, /2
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 128
> 3x3 conv, 256, /2
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 256
> 3x3 conv, 512, /2
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> 3x3 conv, 512
> avg pool
> fc 1000
> image
> 34-layer residual
> Figure 3. Example network architectures for ImageNet. Left: the
> VGG-19 model [41] (19.6 billion FLOPs) as a reference. Middle: a plain network with 34 parameter layers (3.6 billion FLOPs). Right: a residual network with 34 parameter layers (3.6 billion
> FLOPs). The dotted shortcuts increase dimensions. Table 1 shows
> more details and other variants. Residual Network. Based on the above plain network, we
> insert shortcut connections (fig. 3, right) which turn the
> network into its counterpart residual version.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### gnn-gcn-08

How can graph convolution propagate neighborhood information for semi-supervised node classification?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 3, section UNKNOWN

Chunk `65137ae0ad466e6c5d2e2a6f20dc16291f8e7456a078c9b287dd54ed4738d08f`; source `arxiv:1609.02907`; faiss_cosine rank 1 similarity 0.8227717876434326 rerank None; metadata_filtered_cosine rank 1 similarity 0.8227717876434326 rerank None; paper_aggregation rank 1 similarity 0.8227717876434326 rerank None; mmr_diversity rank 1 similarity 0.8227717876434326 rerank 0.5759402513504028

> x ,
> (7)
> with a single parameter θ = θ′
> 0 = −θ′
> 1. Note that IN + D−1
> 2 AD−1
> 2 now has eigenvalues in
> the range [0, 2]. Repeated application of this operator can therefore lead to numerical instabilities
> and exploding/vanishing gradients when used in a deep neural network model. To alleviate this
> problem, we introduce the following renormalization trick: IN +D−1
> 2 AD−1
> 2 → ̃D−1
> 2 ̃A ̃D−1
> 2 , with
>  ̃A = A + IN and ̃Dii = P
> j ̃Aij. We can generalize this definition to a signal X ∈RN×C with C input channels (i.e. a C-dimensional
> feature vector for every node) and F filters or feature maps as follows:
> Z = ̃D−1
> 2 ̃A ̃D−1
> 2 XΘ ,
> (8)
> where Θ ∈RC×F is now a matrix of filter parameters and Z ∈RN×F is the convolved signal
> matrix. This filtering operation has complexity O(|E|FC), as ̃AX can be efficiently implemented
> as a product of a sparse matrix with a dense matrix. 3
> SEMI-SUPERVISED NODE CLASSIFICATION
> Having introduced a simple, yet flexible model f(X, A) for efficient information propagation on
> graphs, we can return to the problem of semi-supervised node classification. As outlined in the introduction, we can relax certain assumptions typically made in graph-based semi-supervised learning by conditioning our model f(X, A) both on the data X and on the adjacency matrix A of the
> underlying graph structure. We expect this setting to be especially powerful in scenarios where the
> adjacency matrix contains information not present in the data X, such as citation links between documents in a citation network or relations in a knowledge graph. The overall model, a multi-layer
> GCN for semi-supervised learning, is schematically depicted in Figure 1. 3.1
> EXAMPLE
> In the following, we consider a two-layer GCN for semi-supervised node classification on a graph
> with a symmetric adjacency matrix A (binary or weighted). We first calculate ˆA = ̃D−1
> 2 ̃A ̃D−1
> 2 in
> a pre-processing step. Our forward model then takes the simple form:
> Z = f(X, A) = softmax

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 3, section UNKNOWN

Chunk `e7bd3150c9ee6ea76ade30fd26e9b8f8d57bd0517a464c3f36aa5f5bdf588c49`; source `arxiv:1609.02907`; faiss_cosine rank 2 similarity 0.8197122812271118 rerank None; metadata_filtered_cosine rank 2 similarity 0.8197122812271118 rerank None; mmr_diversity rank 3 similarity 0.8197122812271118 rerank 0.2737985968589782

> Published as a conference paper at ICLR 2017
> In this way, we can still recover a rich class of convolutional filter functions by stacking multiple
> such layers, but we are not limited to the explicit parameterization given by, e.g., the Chebyshev
> polynomials. We intuitively expect that such a model can alleviate the problem of overfitting on
> local neighborhood structures for graphs with very wide node degree distributions, such as social
> networks, citation networks, knowledge graphs and many other real-world graph datasets. Additionally, for a fixed computational budget, this layer-wise linear formulation allows us to build deeper
> models, a practice that is known to improve modeling capacity on a number of domains (He et al.,
> 2016). In this linear formulation of a GCN we further approximate λmax ≈2, as we can expect that neural
> network parameters will adapt to this change in scale during training. Under these approximations
> eq. 5 simplifies to:
> gθ′ ⋆x ≈θ′
> 0x + θ′
> 1 (L −IN) x = θ′
> 0x −θ′
> 1D−1
> 2 AD−1
> 2 x ,
> (6)
> with two free parameters θ′
> 0 and θ′
> 1. The filter parameters can be shared over the whole graph. Successive application of filters of this form then effectively convolve the kth-order neighborhood of
> a node, where k is the number of successive filtering operations or convolutional layers in the neural
> network model. In practice, it can be beneficial to constrain the number of parameters further to address overfitting
> and to minimize the number of operations (such as matrix multiplications) per layer. This leaves us
> with the following expression:
> gθ ⋆x ≈θ

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 1, section UNKNOWN

Chunk `5e26d1b055aa111dfbfd77c0c481f8b4ba96ba0e9137d12ef13310768fb57ca1`; source `arxiv:1609.02907`; faiss_cosine rank 3 similarity 0.818448543548584 rerank None; metadata_filtered_cosine rank 3 similarity 0.818448543548584 rerank None; mmr_diversity rank 4 similarity 0.818448543548584 rerank 0.2729139804840087

> In this work, we encode the graph structure directly using a neural network model f(X, A) and
> train on a supervised target L0 for all nodes with labels, thereby avoiding explicit graph-based
> regularization in the loss function. Conditioning f(·) on the adjacency matrix of the graph will
> allow the model to distribute gradient information from the supervised loss L0 and will enable it to
> learn representations of nodes both with and without labels. Our contributions are two-fold. Firstly, we introduce a simple and well-behaved layer-wise propagation rule for neural network models which operate directly on graphs and show how it can be
> motivated from a first-order approximation of spectral graph convolutions (Hammond et al., 2011). Secondly, we demonstrate how this form of a graph-based neural network model can be used for
> fast and scalable semi-supervised classification of nodes in a graph. Experiments on a number of
> datasets demonstrate that our model compares favorably both in classification accuracy and efficiency (measured in wall-clock time) against state-of-the-art methods for semi-supervised learning. 1
> arXiv:1609.02907v4 [cs.LG] 22 Feb 2017

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 1, section UNKNOWN

Chunk `ac4857da7e0b8bac79fde74bc7075b92db3983c30c09051cdfc2a495f294afcb`; source `arxiv:1609.02907`; faiss_cosine rank 4 similarity 0.815761148929596 rerank None; metadata_filtered_cosine rank 4 similarity 0.815761148929596 rerank None; mmr_diversity rank 5 similarity 0.815761148929596 rerank 0.2710328042507171

> Published as a conference paper at ICLR 2017
> SEMI-SUPERVISED CLASSIFICATION WITH
> GRAPH CONVOLUTIONAL NETWORKS
> Thomas N. Kipf
> University of Amsterdam
> T.N.Kipf@uva.nl
> Max Welling
> University of Amsterdam
> Canadian Institute for Advanced Research (CIFAR)
> M.Welling@uva.nl
> ABSTRACT
> We present a scalable approach for semi-supervised learning on graph-structured
> data that is based on an efficient variant of convolutional neural networks which
> operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer
> representations that encode both local graph structure and features of nodes. In
> a number of experiments on citation networks and on a knowledge graph dataset
> we demonstrate that our approach outperforms related methods by a significant
> margin. 1
> INTRODUCTION
> We consider the problem of classifying nodes (such as documents) in a graph (such as a citation
> network), where labels are only available for a small subset of nodes. This problem can be framed
> as graph-based semi-supervised learning, where label information is smoothed over the graph via
> some form of explicit graph-based regularization (Zhu et al., 2003; Zhou et al., 2004; Belkin et al.,
> 2006; Weston et al., 2012), e.g. by using a graph Laplacian regularization term in the loss function:
> L = L0 + λLreg ,
> with
> Lreg =
> X
> i,j
> Aij∥f(Xi) −f(Xj)∥2 = f(X)⊤∆f(X) . (1)
> Here, L0 denotes the supervised loss w.r.t. the labeled part of the graph, f(·) can be a neural networklike differentiable function, λ is a weighing factor and X is a matrix of node feature vectors Xi. ∆= D −A denotes the unnormalized graph Laplacian of an undirected graph G = (V, E) with
> N nodes vi ∈V, edges (vi, vj) ∈E, an adjacency matrix A ∈RN×N (binary or weighted) and
> a degree matrix Dii = P
> j Aij. The formulation of eq. 1 relies on the assumption that connected
> nodes in the graph are likely to share the same label. This assumption, however, might restrict
> modeling capacity, as graph edges need not necessarily encode node similarity, but could contain
> additional information. In this work, we encode the graph structure directly using a neural network model f(X, A) and
> train on a supervised target L0 for all nodes with labels, thereby avoiding explicit graph-based
> regularization in the loss function.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 8, section UNKNOWN

Chunk `0d8529708c430036b219049fb78b67f59184e036cafbf254aaac40d98c9d41c4`; source `arxiv:1609.02907`; faiss_cosine rank 5 similarity 0.8140131235122681 rerank None; metadata_filtered_cosine rank 5 similarity 0.8140131235122681 rerank None; mmr_diversity rank 6 similarity 0.8140131235122681 rerank 0.26980918645858754

> We have shown that for large graphs that do not fit in GPU
> memory, training on CPU can still be a viable option. Mini-batch stochastic gradient descent can
> alleviate this issue. The procedure of generating mini-batches, however, should take into account the
> number of layers in the GCN model, as the Kth-order neighborhood for a GCN with K layers has to
> be stored in memory for an exact procedure. For very large and densely connected graph datasets,
> further approximations might be necessary. Directed edges and edge features
> Our framework currently does not naturally support edge features and is limited to undirected graphs (weighted or unweighted). Results on NELL however
> show that it is possible to handle both directed edges and edge features by representing the original
> directed graph as an undirected bipartite graph with additional nodes that represent edges in the
> original graph (see Section 5.1 for details). Limiting assumptions
> Through the approximations introduced in Section 2, we implicitly assume
> locality (dependence on the Kth-order neighborhood for a GCN with K layers) and equal importance of self-connections vs. edges to neighboring nodes. For some datasets, however, it might be
> beneficial to introduce a trade-off parameter λ in the definition of ̃A:
>  ̃A = A + λIN . (11)
> 4Hardware used: 16-core Intel R⃝Xeon R⃝CPU E5-2640 v3 @ 2.60GHz, GeForce R⃝GTX TITAN X
> 8

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 8, section UNKNOWN

Chunk `ba7beebc5592f367fc048cdeb4629d2e28c4713135b6b29bc946ee4ac680d22c`; source `arxiv:1609.02907`; faiss_cosine rank 6 similarity 0.8137871623039246 rerank None; metadata_filtered_cosine rank 6 similarity 0.8137871623039246 rerank None; mmr_diversity rank 7 similarity 0.8137871623039246 rerank 0.2696510136127471

> Published as a conference paper at ICLR 2017
> 6.3
> TRAINING TIME PER EPOCH
> 1k
> 10k
> 100k
> 1M
> 10M
> # Edges
> 10-3
> 10-2
> 10-1
> 100
> 101
> Sec./epoch
> *
> GPU
> CPU
> Figure 2: Wall-clock time per epoch for random
> graphs. (*) indicates out-of-memory error. Here, we report results for the mean training
> time per epoch (forward pass, cross-entropy
> calculation, backward pass) for 100 epochs on
> simulated random graphs, measured in seconds
> wall-clock time. See Section 5.1 for a detailed
> description of the random graph dataset used
> in these experiments. We compare results on
> a GPU and on a CPU-only implementation4 in
> TensorFlow (Abadi et al., 2015). Figure 2 summarizes the results. 7
> DISCUSSION
> 7.1
> SEMI-SUPERVISED MODEL
> In the experiments demonstrated here, our method for semi-supervised node classification outperforms recent related methods by a significant margin. Methods based on graph-Laplacian regularization (Zhu et al., 2003; Belkin et al., 2006; Weston et al., 2012) are most likely limited due to their
> assumption that edges encode mere similarity of nodes. Skip-gram based methods on the other hand
> are limited by the fact that they are based on a multi-step pipeline which is difficult to optimize. Our proposed model can overcome both limitations, while still comparing favorably in terms of efficiency (measured in wall-clock time) to related methods. Propagation of feature information from
> neighboring nodes in every layer improves classification performance in comparison to methods like
> ICA (Lu & Getoor, 2003), where only label information is aggregated. We have further demonstrated that the proposed renormalized propagation model (eq. 8) offers both
> improved efficiency (fewer parameters and operations, such as multiplication or addition) and better
> predictive performance on a number of datasets compared to a na ̈ıve 1st-order model (eq. 6) or
> higher-order graph convolutional models using Chebyshev polynomials (eq. 5). 7.2
> LIMITATIONS AND FUTURE WORK
> Here, we describe several limitations of our current model and outline how these might be overcome
> in future work. Memory requirement
> In the current setup with full-batch gradient descent, memory requirement
> grows linearly in the size of the dataset. We have shown that for large graphs that do not fit in GPU
> memory, training on CPU can still be a viable option. Mini-batch stochastic gradient descent can
> alleviate this issue.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 9, section UNKNOWN

Chunk `e357b75d3ab59b0c905ca9161147055027d265495365555e5702feeef5a82827`; source `arxiv:1609.02907`; faiss_cosine rank 7 similarity 0.8131273984909058 rerank None; metadata_filtered_cosine rank 7 similarity 0.8131273984909058 rerank None; mmr_diversity rank 8 similarity 0.8131273984909058 rerank 0.2691891789436339

> Published as a conference paper at ICLR 2017
> This parameter now plays a similar role as the trade-off parameter between supervised and unsupervised loss in the typical semi-supervised setting (see eq. 1). Here, however, it can be learned via
> gradient descent. 8
> CONCLUSION
> We have introduced a novel approach for semi-supervised classification on graph-structured data. Our GCN model uses an efficient layer-wise propagation rule that is based on a first-order approximation of spectral convolutions on graphs. Experiments on a number of network datasets suggest
> that the proposed GCN model is capable of encoding both graph structure and node features in a
> way useful for semi-supervised classification. In this setting, our model outperforms several recently
> proposed methods by a significant margin, while being computationally efficient. ACKNOWLEDGMENTS
> We would like to thank Christos Louizos, Taco Cohen, Joan Bruna, Zhilin Yang, Dave Herman,
> Pramod Sinha and Abdul-Saboor Sheikh for helpful discussions. This research was funded by SAP. REFERENCES
> Mart ́ın Abadi et al. TensorFlow: Large-scale machine learning on heterogeneous systems, 2015. James Atwood and Don Towsley. Diffusion-convolutional neural networks. In Advances in neural
> information processing systems (NIPS), 2016. Mikhail Belkin, Partha Niyogi, and Vikas Sindhwani. Manifold regularization: A geometric framework for learning from labeled and unlabeled examples. Journal of machine learning research
> (JMLR), 7(Nov):2399–2434, 2006. Ulrik Brandes, Daniel Delling, Marco Gaertler, Robert Gorke, Martin Hoefer, Zoran Nikoloski,
> and Dorothea Wagner. On modularity clustering. IEEE Transactions on Knowledge and Data
> Engineering, 20(2):172–188, 2008. Joan Bruna, Wojciech Zaremba, Arthur Szlam, and Yann LeCun. Spectral networks and locally
> connected networks on graphs. In International Conference on Learning Representations (ICLR),
> 2014. Andrew Carlson, Justin Betteridge, Bryan Kisiel, Burr Settles, Estevam R. Hruschka Jr, and Tom M. Mitchell. Toward an architecture for never-ending language learning. In AAAI, volume 5, pp. 3,
> 2010. Micha ̈el Defferrard, Xavier Bresson, and Pierre Vandergheynst. Convolutional neural networks on
> graphs with fast localized spectral filtering. In Advances in neural information processing systems
> (NIPS), 2016. Brendan L. Douglas. The Weisfeiler-Lehman method and graph isomorphism testing. arXiv preprint
> arXiv:1101.5211, 2011. David K. Duvenaud, Dougal Maclaurin, Jorge Iparraguirre, Rafael Bombarell, Timothy Hirzel, Al ́an
> Aspuru-Guzik, and Ryan P. Adams. Convolutional networks on graphs for learning molecular
> fingerprints. In Advances in neural information processing systems (NIPS), pp. 2224–2232, 2015. Xavier Glorot and Yoshua Bengio. Understanding the difficulty of training deep feedforward neural
> networks. In AISTATS, volume 9, pp. 249–256, 2010. Marco Gori, Gabriele Monfardini, and Franco Scarselli.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 5, section UNKNOWN

Chunk `35528922de4d34893c1ac4b7d60d30c77e64d25f111142be5c7cd599e67b1f4d`; source `arxiv:1609.02907`; faiss_cosine rank 8 similarity 0.8112154603004456 rerank None; metadata_filtered_cosine rank 8 similarity 0.8112154603004456 rerank None; mmr_diversity rank 9 similarity 0.8112154603004456 rerank 0.26785082221031176

> Published as a conference paper at ICLR 2017
> Recently, attention has shifted to models that learn graph embeddings with methods inspired by
> the skip-gram model (Mikolov et al., 2013). DeepWalk (Perozzi et al., 2014) learns embeddings
> via the prediction of the local neighborhood of nodes, sampled from random walks on the graph. LINE (Tang et al., 2015) and node2vec (Grover & Leskovec, 2016) extend DeepWalk with more
> sophisticated random walk or breadth-first search schemes. For all these methods, however, a multistep pipeline including random walk generation and semi-supervised training is required where each
> step has to be optimized separately. Planetoid (Yang et al., 2016) alleviates this by injecting label
> information in the process of learning embeddings. 4.2
> NEURAL NETWORKS ON GRAPHS
> Neural networks that operate on graphs have previously been introduced in Gori et al. (2005);
> Scarselli et al. (2009) as a form of recurrent neural network. Their framework requires the repeated
> application of contraction maps as propagation functions until node representations reach a stable
> fixed point. This restriction was later alleviated in Li et al. (2016) by introducing modern practices
> for recurrent neural network training to the original graph neural network framework. Duvenaud
> et al. (2015) introduced a convolution-like propagation rule on graphs and methods for graph-level
> classification. Their approach requires to learn node degree-specific weight matrices which does not
> scale to large graphs with wide node degree distributions. Our model instead uses a single weight
> matrix per layer and deals with varying node degrees through an appropriate normalization of the
> adjacency matrix (see Section 3.1). A related approach to node classification with a graph-based neural network was recently introduced
> in Atwood & Towsley (2016). They report O(N 2) complexity, limiting the range of possible applications. In a different yet related model, Niepert et al. (2016) convert graphs locally into sequences
> that are fed into a conventional 1D convolutional neural network, which requires the definition of a
> node ordering in a pre-processing step. Our method is based on spectral graph convolutional neural networks, introduced in Bruna et al.
> (2014) and later extended by Defferrard et al. (2016) with fast localized convolutions. In contrast
> to these works, we consider here the task of transductive node classification within networks of
> significantly larger scale.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 5, section UNKNOWN

Chunk `dcad8c65fc188a446b2a56a49c2b68ac9f9408656ee578f8c5e973b59ae24289`; source `arxiv:1609.02907`; faiss_cosine rank 9 similarity 0.811034083366394 rerank None; metadata_filtered_cosine rank 9 similarity 0.811034083366394 rerank None; mmr_diversity rank 10 similarity 0.811034083366394 rerank 0.2677238583564757

> Our method is based on spectral graph convolutional neural networks, introduced in Bruna et al.
> (2014) and later extended by Defferrard et al. (2016) with fast localized convolutions. In contrast
> to these works, we consider here the task of transductive node classification within networks of
> significantly larger scale. We show that in this setting, a number of simplifications (see Section 2.2)
> can be introduced to the original frameworks of Bruna et al. (2014) and Defferrard et al. (2016) that
> improve scalability and classification performance in large-scale networks. 5
> EXPERIMENTS
> We test our model in a number of experiments: semi-supervised document classification in citation networks, semi-supervised entity classification in a bipartite graph extracted from a knowledge
> graph, an evaluation of various graph propagation models and a run-time analysis on random graphs. 5.1
> DATASETS
> We closely follow the experimental setup in Yang et al. (2016). Dataset statistics are summarized
> in Table 1. In the citation network datasets—Citeseer, Cora and Pubmed (Sen et al., 2008)—nodes
> are documents and edges are citation links. Label rate denotes the number of labeled nodes that are
> used for training divided by the total number of nodes in each dataset. NELL (Carlson et al., 2010;
> Yang et al., 2016) is a bipartite graph dataset extracted from a knowledge graph with 55,864 relation
> nodes and 9,891 entity nodes. Table 1: Dataset statistics, as reported in Yang et al. (2016). Dataset
> Type
> Nodes
> Edges
> Classes
> Features
> Label rate
> Citeseer
> Citation network
> 3,327
> 4,732
> 6
> 3,703
> 0.036
> Cora
> Citation network
> 2,708
> 5,429
> 7
> 1,433
> 0.052
> Pubmed
> Citation network
> 19,717
> 44,338
> 3
> 500
> 0.003
> NELL
> Knowledge graph
> 65,755
> 266,144
> 210
> 5,414
> 0.001
> 5

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 7, section UNKNOWN

Chunk `23bea2e74c1dd0e85a9e7f3f08bc637c52b9e665af1afe35558f88662c45628f`; source `arxiv:1609.02907`; faiss_cosine rank 10 similarity 0.8109776377677917 rerank None; metadata_filtered_cosine rank 10 similarity 0.8109776377677917 rerank None

> Published as a conference paper at ICLR 2017
> 6
> RESULTS
> 6.1
> SEMI-SUPERVISED NODE CLASSIFICATION
> Results are summarized in Table 2. Reported numbers denote classification accuracy in percent. For
> ICA, we report the mean accuracy of 100 runs with random node orderings. Results for all other
> baseline methods are taken from the Planetoid paper (Yang et al., 2016). Planetoid* denotes the best
> model for the respective dataset out of the variants presented in their paper. Table 2: Summary of results in terms of classification accuracy (in percent). Method
> Citeseer
> Cora
> Pubmed
> NELL
> ManiReg [3]
> 60.1
> 59.5
> 70.7
> 21.8
> SemiEmb [28]
> 59.6
> 59.0
> 71.1
> 26.7
> LP [32]
> 45.3
> 68.0
> 63.0
> 26.5
> DeepWalk [22]
> 43.2
> 67.2
> 65.3
> 58.1
> ICA [18]
> 69.1
> 75.1
> 73.9
> 23.1
> Planetoid* [29]
> 64.7 (26s)
> 75.7 (13s)
> 77.2 (25s)
> 61.9 (185s)
> GCN (this paper)
> 70.3 (7s)
> 81.5 (4s)
> 79.0 (38s)
> 66.0 (48s)
> GCN (rand. splits)
> 67.9 ± 0.5
> 80.1 ± 0.5
> 78.9 ± 0.7
> 58.4 ± 1.7
> We further report wall-clock training time in seconds until convergence (in brackets) for our method
> (incl. evaluation of validation error) and for Planetoid. For the latter, we used an implementation provided by the authors3 and trained on the same hardware (with GPU) as our GCN model. We trained
> and tested our model on the same dataset splits as in Yang et al. (2016) and report mean accuracy
> of 100 runs with random weight initializations. We used the following sets of hyperparameters for
> Citeseer, Cora and Pubmed: 0.5 (dropout rate), 5 · 10−4 (L2 regularization) and 16 (number of hidden units); and for NELL: 0.1 (dropout rate), 1 · 10−5 (L2 regularization) and 64 (number of hidden
> units). In addition, we report performance of our model on 10 randomly drawn dataset splits of the same
> size as in Yang et al. (2016), denoted by GCN (rand. splits). Here, we report mean and standard
> error of prediction accuracy on the test set split in percent. 6.2
> EVALUATION OF PROPAGATION MODEL
> We compare different variants of our proposed per-layer propagation model on the citation network
> datasets. We follow the experimental set-up described in the previous section. Results are summarized in Table 3. The propagation model of our original GCN model is denoted by renormalization
> trick (in bold). In all other cases, the propagation model of both neural network layers is replaced
> with the model specified under propagation model.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 6, section UNKNOWN

Chunk `80af267b3541aa12b6fe3a700558acd19a2191a57b850a1dc937dcc2086ea789`; source `arxiv:1710.10903`; paper_aggregation rank 2 similarity 0.7829773426055908 rerank None; mmr_diversity rank 2 similarity 0.7829773426055908 rerank 0.26593003869056697

> Critically, testing graphs remain completely unobserved during training. To construct the graphs, we used the preprocessed data provided
> by Hamilton et al. (2017). The average number of nodes per graph is 2372. Each node has 50
> features that are composed of positional gene sets, motif gene sets and immunological signatures. There are 121 labels for each node set from gene ontology, collected from the Molecular Signatures
> Database (Subramanian et al., 2005), and a node can possess several labels simultaneously. An overview of the interesting characteristics of the datasets is given in Table 1. 3.2
> STATE-OF-THE-ART METHODS
> Transductive learning
> For transductive learning tasks, we compare against the same strong baselines and state-of-the-art approaches as specified in Kipf & Welling (2017). This includes label
> propagation (LP) (Zhu et al., 2003), semi-supervised embedding (SemiEmb) (Weston et al., 2012),
> manifold regularization (ManiReg) (Belkin et al., 2006), skip-gram based graph embeddings (DeepWalk) (Perozzi et al., 2014), the iterative classification algorithm (ICA) (Lu & Getoor, 2003) and
> Planetoid (Yang et al., 2016). We also directly compare our model against GCNs (Kipf & Welling,
> 2017), as well as graph convolutional models utilising higher-order Chebyshev filters (Defferrard
> et al., 2016), and the MoNet model presented in Monti et al. (2016). Inductive learning
> For the inductive learning task, we compare against the four different supervised GraphSAGE inductive methods presented in Hamilton et al. (2017). These provide a variety
> of approaches to aggregating features within a sampled neighborhood: GraphSAGE-GCN (which
> extends a graph convolution-style operation to the inductive setting), GraphSAGE-mean (taking
> 6

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 9, section References

Chunk `2170cd38792c4eb9d975ed72e2557b60f386e8f939af667bbb048215a94e2a65`; source `arxiv:1512.03385`; paper_aggregation rank 3 similarity 0.7541738748550415 rerank None

> Fitnets: Hints for thin deep nets. In ICLR, 2015. [36] O. Russakovsky, J. Deng, H. Su, J. Krause, S. Satheesh, S. Ma,
> Z. Huang, A. Karpathy, A. Khosla, M. Bernstein, et al. Imagenet
> large scale visual recognition challenge. arXiv:1409.0575, 2014. [37] A. M. Saxe, J. L. McClelland, and S. Ganguli. Exact solutions to
> the nonlinear dynamics of learning in deep linear neural networks. arXiv:1312.6120, 2013. [38] N. N. Schraudolph. Accelerated gradient descent by factor-centering
> decomposition. Technical report, 1998. [39] N. N. Schraudolph. Centering neural network gradient factors. In
> Neural Networks: Tricks of the Trade, pages 207–226. Springer,
> 1998. [40] P. Sermanet, D. Eigen, X. Zhang, M. Mathieu, R. Fergus, and Y. LeCun. Overfeat: Integrated recognition, localization and detection
> using convolutional networks. In ICLR, 2014. [41] K. Simonyan and A. Zisserman. Very deep convolutional networks
> for large-scale image recognition. In ICLR, 2015. [42] R. K. Srivastava, K. Greff, and J. Schmidhuber. Highway networks. arXiv:1505.00387, 2015. [43] R. K. Srivastava, K. Greff, and J. Schmidhuber. Training very deep
> networks. 1507.06228, 2015. [44] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov, D. Erhan, V. Vanhoucke, and A. Rabinovich. Going deeper with convolutions. In CVPR, 2015. [45] R. Szeliski. Fast surface interpolation using hierarchical basis functions. TPAMI, 1990. [46] R. Szeliski. Locally adapted hierarchical basis preconditioning. In
> SIGGRAPH, 2006. [47] T. Vatanen, T. Raiko, H. Valpola, and Y. LeCun. Pushing stochastic gradient towards second-order methods–backpropagation learning with transformations in nonlinearities. In Neural Information
> Processing, 2013. [48] A. Vedaldi and B. Fulkerson. VLFeat: An open and portable library
> of computer vision algorithms, 2008. [49] W. Venables and B. Ripley. Modern applied statistics with s-plus. 1999. [50] M. D. Zeiler and R. Fergus. Visualizing and understanding convolutional neural networks. In ECCV, 2014. 9

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 10, section References

Chunk `ad8807c67a3567046428dedc1e1300aa50602b8357b1e4012abfabd7da61b8d4`; source `arxiv:1810.04805`; paper_aggregation rank 4 similarity 0.7425034046173096 rerank None

> 2017. Supervised
> learning of universal sentence representations from
> natural language inference data. In Proceedings of
> the 2017 Conference on Empirical Methods in Natural Language Processing, pages 670–680, Copenhagen, Denmark. Association for Computational
> Linguistics. Andrew M Dai and Quoc V Le. 2015. Semi-supervised
> sequence learning. In Advances in neural information processing systems, pages 3079–3087. J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. FeiFei. 2009. ImageNet: A Large-Scale Hierarchical
> Image Database. In CVPR09. William B Dolan and Chris Brockett. 2005. Automatically constructing a corpus of sentential paraphrases. In Proceedings of the Third International Workshop
> on Paraphrasing (IWP2005). William Fedus, Ian Goodfellow, and Andrew M Dai. 2018. Maskgan: Better text generation via filling in
> the . arXiv preprint arXiv:1801.07736. Dan Hendrycks and Kevin Gimpel. 2016. Bridging
> nonlinearities and stochastic regularizers with gaussian error linear units. CoRR, abs/1606.08415. Felix Hill, Kyunghyun Cho, and Anna Korhonen. 2016. Learning distributed representations of sentences
> from unlabelled data. In Proceedings of the 2016
> Conference of the North American Chapter of the
> Association for Computational Linguistics: Human
> Language Technologies. Association for Computational Linguistics. Jeremy Howard and Sebastian Ruder. 2018. Universal
> language model fine-tuning for text classification. In
> ACL. Association for Computational Linguistics. Minghao Hu, Yuxing Peng, Zhen Huang, Xipeng Qiu,
> Furu Wei, and Ming Zhou. 2018. Reinforced
> mnemonic reader for machine reading comprehension. In IJCAI. Yacine Jernite, Samuel R. Bowman, and David Sontag. 2017. Discourse-based objectives for fast unsupervised sentence representation learning. CoRR,
> abs/1705.00557.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 9, section UNKNOWN

Chunk `e4c664d8069367afd383cc4603c5d4c66ade54d601249970eb6671b4e0946b6f`; source `arxiv:1706.03762`; paper_aggregation rank 5 similarity 0.7400736212730408 rerank None

> This task presents specific challenges: the output is subject to strong structural
> constraints and is significantly longer than the input. Furthermore, RNN sequence-to-sequence
> models have not been able to attain state-of-the-art results in small-data regimes [37]. We trained a 4-layer transformer with dmodel = 1024 on the Wall Street Journal (WSJ) portion of the
> Penn Treebank [25], about 40K training sentences. We also trained it in a semi-supervised setting,
> using the larger high-confidence and BerkleyParser corpora from with approximately 17M sentences
> [37]. We used a vocabulary of 16K tokens for the WSJ only setting and a vocabulary of 32K tokens
> for the semi-supervised setting. We performed only a small number of experiments to select the dropout, both attention and residual
> (section 5.4), learning rates and beam size on the Section 22 development set, all other parameters
> remained unchanged from the English-to-German base translation model. During inference, we
> 9

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 9, section UNKNOWN

Chunk `26ee961215b1f62c02b4dfb81a11495e97e5fd88ed16966eb0c83a1905df704a`; source `arxiv:1506.01497`; paper_aggregation rank 6 similarity 0.734288215637207 rerank None

> 9
> Table 6: Results on PASCAL VOC 2007 test set with Fast R-CNN detectors and VGG-16. For RPN, the train-time
> proposals for Fast R-CNN are 2000. RPN∗denotes the unsharing feature version. method
> # box
> data
> mAP
> areo
> bike
> bird
> boat
> bottle
> bus
> car
> cat
> chair
> cow
> table
> dog
> horse
> mbike person plant
> sheep
> sofa
> train
> tv
> SS
> 2000
> 07
> 66.9
> 74.5
> 78.3
> 69.2
> 53.2
> 36.6
> 77.3
> 78.2
> 82.0
> 40.7
> 72.7
> 67.9
> 79.6
> 79.2
> 73.0
> 69.0
> 30.1
> 65.4
> 70.2
> 75.8
> 65.8
> SS
> 2000
> 07+12
> 70.0
> 77.0
> 78.1
> 69.3
> 59.4
> 38.3
> 81.6
> 78.6
> 86.7
> 42.8
> 78.8
> 68.9
> 84.7
> 82.0
> 76.6
> 69.9
> 31.8
> 70.1
> 74.8
> 80.4
> 70.4
> RPN∗
> 300
> 07
> 68.5
> 74.1
> 77.2
> 67.7
> 53.9
> 51.0
> 75.1
> 79.2
> 78.9
> 50.7
> 78.0
> 61.1
> 79.1
> 81.9
> 72.2
> 75.9
> 37.2
> 71.4
> 62.5
> 77.4
> 66.4
> RPN
> 300
> 07
> 69.9
> 70.0
> 80.6
> 70.1
> 57.3
> 49.9
> 78.2
> 80.4
> 82.0
> 52.2
> 75.3
> 67.2
> 80.3
> 79.8
> 75.0
> 76.3
> 39.1
> 68.3
> 67.3
> 81.1
> 67.6
> RPN
> 300
> 07+12
> 73.2
> 76.5
> 79.0
> 70.9
> 65.5
> 52.1
> 83.1
> 84.7
> 86.4
> 52.0
> 81.9
> 65.7
> 84.8
> 84.6
> 77.5
> 76.7
> 38.8
> 73.6
> 73.9
> 83.0
> 72.6
> RPN
> 300
> COCO+07+12
> 78.8
> 84.3
> 82.0
> 77.7
> 68.9
> 65.7
> 88.1
> 88.4
> 88.9
> 63.6
> 86.3
> 70.8
> 85.9
> 87.6
> 80.1
> 82.3
> 53.6
> 80.4
> 75.8
> 86.6
> 78.9
> Table 7: Results on PASCAL VOC 2012 test set with Fast R-CNN detectors and VGG-16. For RPN, the train-time
> proposals for Fast R-CNN are 2000. method
> # box
> data
> mAP
> areo
> bike
> bird
> boat
> bottle
> bus
> car
> cat
> chair
> cow
> table
> dog
> horse
> mbike person plant
> sheep
> sofa
> train
> tv
> SS
> 2000
> 12
> 65.7
> 80.3
> 74.7
> 66.9
> 46.9
> 37.7
> 73.9
> 68.6
> 87.7
> 41.7
> 71.1
> 51.1
> 86.0
> 77.8
> 79.8
> 69.8
> 32.1
> 65.5
> 63.8
> 76.4
> 61.7
> SS
> 2000
> 07++12
> 68.4
> 82.3
> 78.4
> 70.8
> 52.3
> 38.7
> 77.8
> 71.6
> 89.3
> 44.2
> 73.0
> 55.0
> 87.5
> 80.5
> 80.8
> 72.0
> 35.1
> 68.3
> 65.7
> 80.4
> 64.2
> RPN
> 300
> 12
> 67.0
> 82.3
> 76.4
> 71.0
> 48.4
> 45.2
> 72.1
> 72.3
> 87.3
> 42.2
> 73.7
> 50.0
> 86.8
> 78.7
> 78.4
> 77.4
> 34.5
> 70.1
> 57.1
> 77.1
> 58.9
> RPN
> 300
> 07++12
> 70.4
> 84.9
> 79.8
> 74.3
> 53.9
> 49.8
> 77.5
> 75.9
> 88.5
> 45.6
> 77.1
> 55.3
> 86.9
> 81.7
> 80.9
> 79.6
> 40.1
> 72.6
> 60.9
> 81.2
> 61.5
> RPN
> 300
> COCO+07++12
> 75.9
> 87.4
> 83.6
> 76.8
> 62.9
> 59.6
> 81.9
> 82.0
> 91.3
> 54.9
> 82.6
> 59.0
> 89.0
> 85.5
> 84.7
> 84.1
> 52.2
> 78.9
> 65.5
> 85.4
> 70.2
> Table 8: Detection results of Faster R-CNN on PASCAL VOC 2007 test set using different settings of
> anchors. The network is VGG-16. The training data
> is VOC 2007 trainval.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 4, section UNKNOWN

Chunk `88c0b4ab21070dd8600e466ddcb4dc4a784ad46113f0a69e6a97a45ab845fb4b`; source `arxiv:1903.10676`; paper_aggregation rank 7 similarity 0.7323951721191406 rerank None

> Field
> Task
> Dataset
> SOTA
> BERT-Base
> SCIBERT
> Frozen
> Finetune
> Frozen
> Finetune
> Bio
> NER
> BC5CDR (Li et al., 2016)
> 88.857
> 85.08
> 86.72
> 88.73
> 90.01
> JNLPBA (Collier and Kim, 2004)
> 78.58
> 74.05
> 76.09
> 75.77
> 77.28
> NCBI-disease (Dogan et al., 2014)
> 89.36
> 84.06
> 86.88
> 86.39
> 88.57
> PICO
> EBM-NLP (Nye et al., 2018)
> 66.30
> 61.44
> 71.53
> 68.30
> 72.28
> DEP
> GENIA (Kim et al., 2003) - LAS
> 91.92
> 90.22
> 90.33
> 90.36
> 90.43
> GENIA (Kim et al., 2003) - UAS
> 92.84
> 91.84
> 91.89
> 92.00
> 91.99
> REL
> ChemProt (Kringelum et al., 2016)
> 76.68
> 68.21
> 79.14
> 75.03
> 83.64
> CS
> NER
> SciERC (Luan et al., 2018)
> 64.20
> 63.58
> 65.24
> 65.77
> 67.57
> REL
> SciERC (Luan et al., 2018)
> n/a
> 72.74
> 78.71
> 75.25
> 79.97
> CLS
> ACL-ARC (Jurgens et al., 2018)
> 67.9
> 62.04
> 63.91
> 60.74
> 70.98
> Multi
> CLS
> Paper Field
> n/a
> 63.64
> 65.37
> 64.38
> 65.71
> SciCite (Cohan et al., 2019)
> 84.0
> 84.31
> 84.85
> 85.42
> 85.49
> Average
> 73.58
> 77.16
> 76.01
> 79.27
> Table 1: Test performances of all BERT variants on all tasks and datasets. Bold indicates the SOTA result (multiple
> results bolded if difference within 95% bootstrap confidence interval). Keeping with past work, we report macro
> F1 scores for NER (span-level), macro F1 scores for REL and CLS (sentence-level), and macro F1 for PICO
> (token-level), and micro F1 for ChemProt specifically. For DEP, we report labeled (LAS) and unlabeled (UAS)
> attachment scores (excluding punctuation) for the same model with hyperparameters tuned for LAS. All results
> are the average of multiple runs with different random seeds. Task
> Dataset
> BIOBERT
> SCIBERT
> NER
> BC5CDR
> 88.85
> 90.01
> JNLPBA
> 77.59
> 77.28
> NCBI-disease
> 89.36
> 88.57
> REL
> ChemProt
> 76.68
> 83.64
> Table 2:
> Comparing SCIBERT with the reported
> BIOBERT results on biomedical datasets. BC5CDR and ChemProt, and performs similarly
> on JNLPBA despite being trained on a substantially smaller biomedical corpus. 4.2
> Computer Science Domain
> We observe that SCIBERT outperforms BERTBase on computer science tasks (+3.55 F1 with
> finetuning and +1.13 F1 without). In addition,
> SCIBERT achieves new SOTA results on ACLARC (Cohan et al., 2019), and the NER part of
> SciERC (Luan et al., 2018). For relations in SciERC, our results are not comparable with those in
> Luan et al. (2018) because we are performing relation classification given gold entities, while they
> perform joint entity and relation extraction. 4.3
> Multiple Domains
> We observe that SCIBERT outperforms BERTBase on the multidomain tasks (+0.49 F1 with
> finetuning and +0.93 F1 without). In addition, SCIBERT outperforms the SOTA on SciCite (Cohan et al., 2019).

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 8, section UNKNOWN

Chunk `62b1c885ab5d06106c283c7211d19aea8407a974251174545d521b415c3a8900`; source `arxiv:1505.04597`; paper_aggregation rank 8 similarity 0.730519711971283 rerank None

> 8
> mations, it only needs very few annotated images and has a very reasonable
> training time of only 10 hours on a NVidia Titan GPU (6 GB). We provide the
> full Caffe[6]-based implementation and the trained networks4. We are sure that
> the u-net architecture can be applied easily to many more tasks. Acknowlegements
> This study was supported by the Excellence Initiative of the German Federal
> and State governments (EXC 294) and by the BMBF (Fkz 0316185B). References
> 1. Ciresan, D.C., Gambardella, L.M., Giusti, A., Schmidhuber, J.: Deep neural networks segment neuronal membranes in electron microscopy images. In: NIPS. pp. 2852–2860 (2012)
> 2. Dosovitskiy, A., Springenberg, J.T., Riedmiller, M., Brox, T.: Discriminative unsupervised feature learning with convolutional neural networks. In: NIPS (2014)
> 3. Girshick, R., Donahue, J., Darrell, T., Malik, J.: Rich feature hierarchies for accurate object detection and semantic segmentation. In: Proceedings of the IEEE
> Conference on Computer Vision and Pattern Recognition (CVPR) (2014)
> 4. Hariharan, B., Arbelez, P., Girshick, R., Malik, J.: Hypercolumns for object segmentation and fine-grained localization (2014), arXiv:1411.5752 [cs.CV]
> 5. He, K., Zhang, X., Ren, S., Sun, J.: Delving deep into rectifiers: Surpassing humanlevel performance on imagenet classification (2015), arXiv:1502.01852 [cs.CV]
> 6. Jia, Y., Shelhamer, e., Donahue, J., Karayev, S., Long, J., Girshick, R., Guadarrama, S., Darrell, T.: Caffe: Convolutional architecture for fast feature embedding
> (2014), arXiv:1408.5093 [cs.CV]
> 7. Krizhevsky, A., Sutskever, i., Hinton, g.e.: Imagenet classification with deep convolutional neural networks. In: NIPS. pp. 1106–1114 (2012)
> 8. LeCun, Y., Boser, B., Denker, J.S., Henderson, D., Howard, R.e., Hubbard, W.,
> Jackel, L.D.: Backpropagation applied to handwritten zip code recognition. Neural
> Computation 1(4), 541–551 (1989)
> 9. Long, J., Shelhamer, e., Darrell, T.: Fully convolutional networks for semantic
> segmentation (2014), arXiv:1411.4038 [cs.CV]
> 10. Maska, M., (...), de Solorzano, C.O.: A benchmark for comparison of cell tracking
> algorithms. Bioinformatics 30, 1609–1617 (2014)
> 11. Seyedhosseini, M., Sajjadi, M., Tasdizen, T.: Image segmentation with cascaded
> hierarchical models and logistic disjunctive normal networks. In: Computer Vision
> (ICCV), 2013 IEEE International Conference on. pp. 2168–2175 (2013)
> 12. Simonyan, K., Zisserman, A.: Very deep convolutional networks for large-scale
> image recognition (2014), arXiv:1409.1556 [cs.CV]
> 13. WWW: Web page of the cell tracking challenge, http://www.codesolorzano.com/
> celltrackingchallenge/Cell_Tracking_Challenge/Welcome.html
> 14. WWW: Web page of the em segmentation challenge, http://brainiac2.mit.edu/
> isbi_challenge/
> 4 U-net implementation, trained networks and supplementary material available at
> http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 14, section UNKNOWN

Chunk `f7f46d59ca966b0002a03869ab70bd6b3a2a74387ed5f895f57768ad7347463b`; source `arxiv:2005.11401`; paper_aggregation rank 9 similarity 0.7242364287376404 rerank None

> How much knowledge can you pack into
> the parameters of a language model? arXiv e-prints, 2020. URL https://arxiv.org/abs/
> 2002.08910. [53] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: Bm25 and
> beyond. Found. Trends Inf. Retr., 3(4):333–389, April 2009. ISSN 1554-0669. doi: 10.1561/
> 1500000019. URL https://doi.org/10.1561/1500000019. [54] Irene Solaiman, Miles Brundage, Jack Clark, Amanda Askell, Ariel Herbert-Voss, Jeff Wu, Alec
> Radford, and Jian-Bing Wang. Release strategies and the social impacts of language models. ArXiv, abs/1908.09203, 2019. [55] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors, Advances
> in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates, Inc., 2015. URL http://papers.nips.cc/paper/5846-end-to-end-memory-networks.pdf. 14

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 11, section UNKNOWN

Chunk `10581b2ea9ed1e7381096291bba0ceeadb84192718cac4ef45e1db5ff4b98550`; source `arxiv:2004.04906`; paper_aggregation rank 10 similarity 0.7085292935371399 rerank None

> In Advances in Neural Information Processing Systems (NIPS), pages 2321–
> 2329. Ellen M Voorhees. 1999. The TREC-8 question answering track report. In TREC, volume 99, pages
> 77–82. Shuohang Wang, Mo Yu, Xiaoxiao Guo, Zhiguo Wang,
> Tim Klinger, Wei Zhang, Shiyu Chang, Gerry
> Tesauro, Bowen Zhou, and Jing Jiang. 2018. Rˆ3:
> Reinforced ranker-reader for open-domain question
> answering. In Conference on Artificial Intelligence
> (AAAI). Zhiguo Wang, Patrick Ng, Xiaofei Ma, Ramesh Nallapati, and Bing Xiang. 2019. Multi-passage BERT:
> A globally normalized bert model for open-domain
> question answering. In Empirical Methods in Natural Language Processing (EMNLP). Tomer Wolfson, Mor Geva, Ankit Gupta, Matt Gardner, Yoav Goldberg, Daniel Deutch, and Jonathan
> Berant. 2020. Break it down: A question understanding benchmark. Transactions of the Association of Computational Linguistics (TACL). Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang,
> Jialin Liu, Paul Bennett, Junaid Ahmed, and Arnold
> Overwijk. 2020a. Approximate nearest neighbor
> negative contrastive learning for dense text retrieval. ArXiv, abs/2007.00808. Wenhan Xiong, Hankang Wang, and William Yang
> Wang. 2020b. Progressively pretrained dense corpus
> index for open-domain question answering. ArXiv,
> abs/2005.00038. Wei Yang, Yuqing Xie, Aileen Lin, Xingyu Li, Luchen
> Tan, Kun Xiong, Ming Li, and Jimmy Lin. 2019a. End-to-end open-domain question answering with
> bertserini. In North American Association for Computational Linguistics (NAACL), pages 72–77. Wei Yang, Yuqing Xie, Luchen Tan, Kun Xiong, Ming
> Li, and Jimmy Lin. 2019b. Data augmentation for
> bert fine-tuning in open-domain question answering. ArXiv, abs/1904.06652. Wen-tau Yih, Kristina Toutanova, John C Platt, and
> Christopher Meek. 2011. Learning discriminative
> projections for text similarity measures. In Computational Natural Language Learning (CoNLL),
> pages 247–256.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### gnn-attention-09

How can attention assign different importance to neighboring nodes in graph neural networks?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 4, section UNKNOWN

Chunk `609a59affb186feef0345ebc1b4e2e8b2df11fb52b48e352fc745c6866c40540`; source `arxiv:1710.10903`; faiss_cosine rank 1 similarity 0.813741147518158 rerank None; metadata_filtered_cosine rank 1 similarity 0.813741147518158 rerank None; paper_aggregation rank 1 similarity 0.813741147518158 rerank None; mmr_diversity rank 1 similarity 0.813741147518158 rerank 0.5696188032627105

> X
> j∈Ni
> αijW⃗hj

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 4, section UNKNOWN

Chunk `11af379cd5ac768941c1c3428c50923e7a84c737eb652e41a34b9ffb929959ea`; source `arxiv:1710.10903`; faiss_cosine rank 2 similarity 0.810969352722168 rerank None; metadata_filtered_cosine rank 2 similarity 0.810969352722168 rerank None; mmr_diversity rank 4 similarity 0.810969352722168 rerank 0.2676785469055175

> X
> j∈Ni
> αk
> ijWk⃗hj

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 4, section UNKNOWN

Chunk `973d8009e7b8ea1b503b48b8994639d93db49904352ad0355f0c78708d9e2115`; source `arxiv:1710.10903`; faiss_cosine rank 3 similarity 0.8085325360298157 rerank None; metadata_filtered_cosine rank 3 similarity 0.8085325360298157 rerank None; mmr_diversity rank 5 similarity 0.8085325360298157 rerank 0.2659727752208709

> 1
> K
> K
> X
> k=1
> X
> j∈Ni
> αk
> ijWk⃗hj

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 3, section UNKNOWN

Chunk `e9bf2e70e2ae00f242b7937e265aa95f0e373e67a99dd0f4ee8e610d3bac9cdb`; source `arxiv:1710.10903`; faiss_cosine rank 4 similarity 0.8077970147132874 rerank None; metadata_filtered_cosine rank 4 similarity 0.8077970147132874 rerank None; mmr_diversity rank 6 similarity 0.8077970147132874 rerank 0.2654579102993011

> (3)
> where ·T represents transposition and ∥is the concatenation operation. Once obtained, the normalized attention coefficients are used to compute a linear combination of the
> features corresponding to them, to serve as the final output features for every node (after potentially
> 3

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 4, section UNKNOWN

Chunk `c84540ef7300a30ebc9066dc700e0fa11fcae705df471d932d69944385d884fe`; source `arxiv:1710.10903`; faiss_cosine rank 5 similarity 0.8077138662338257 rerank None; metadata_filtered_cosine rank 5 similarity 0.8077138662338257 rerank None; mmr_diversity rank 7 similarity 0.8077138662338257 rerank 0.26539970636367793

> (5)
> where ∥represents concatenation, αk
> ij are normalized attention coefficients computed by the k-th
> attention mechanism (ak), and Wk is the corresponding input linear transformation’s weight matrix. Note that, in this setting, the final returned output, h′, will consist of KF ′ features (rather than F ′)
> for each node. Specially, if we perform multi-head attention on the final (prediction) layer of the network, concatenation is no longer sensible—instead, we employ averaging, and delay applying the final nonlinearity (usually a softmax or logistic sigmoid for classification problems) until then:⃗
> h′
> i = σ

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 1, section UNKNOWN

Chunk `790cad77a52aae536fc01bd5f25815cd26dcd38d88aea43d30f50d2ad2ed046c`; source `arxiv:1710.10903`; faiss_cosine rank 6 similarity 0.8073104023933411 rerank None; metadata_filtered_cosine rank 6 similarity 0.8073104023933411 rerank None; mmr_diversity rank 8 similarity 0.8073104023933411 rerank 0.26511728167533866

> There have been several attempts in the literature to extend neural networks to deal with arbitrarily
> structured graphs. Early work used recursive neural networks to process data represented in graph
> domains as directed acyclic graphs (Frasconi et al., 1998; Sperduti & Starita, 1997). Graph Neural
> Networks (GNNs) were introduced in Gori et al. (2005) and Scarselli et al. (2009) as a generalization
> of recursive neural networks that can directly deal with a more general class of graphs, e.g. cyclic,
> directed and undirected graphs. GNNs consist of an iterative process, which propagates the node
> states until equilibrium; followed by a neural network, which produces an output for each node
> ∗Work performed while the author was at the Montr ́eal Institute of Learning Algorithms. 1
> arXiv:1710.10903v3 [stat.ML] 4 Feb 2018

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 3, section UNKNOWN

Chunk `2ece33288a1f2d2161a27f5b52b15e43ebecc0b98d088e36eb387c1757a2c0e9`; source `arxiv:1710.10903`; faiss_cosine rank 7 similarity 0.8036714792251587 rerank None; metadata_filtered_cosine rank 7 similarity 0.8036714792251587 rerank None; mmr_diversity rank 9 similarity 0.8036714792251587 rerank 0.26257003545761104

> P
> k∈Ni exp

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 4, section UNKNOWN

Chunk `4b3764a067d3290d31f007d612ffd8abe1ec00aeaaa31e6cd4391b6350b80f66`; source `arxiv:1710.10903`; faiss_cosine rank 8 similarity 0.8032049536705017 rerank None; metadata_filtered_cosine rank 8 similarity 0.8032049536705017 rerank None; mmr_diversity rank 10 similarity 0.8032049536705017 rerank 0.26224346756935113

> Published as a conference paper at ICLR 2018
> αij⃗
> a
> softmaxj
> W⃗hi
> W⃗hj⃗
> h1⃗
> h2⃗
> h3⃗
> h4⃗
> h5⃗
> h6⃗
> α16⃗
> α11⃗
> α12⃗
> α13⃗
> α14⃗
> α15⃗
> h′
> 1
> concat/avg
> Figure 1: Left: The attention mechanism a(W⃗hi, W⃗hj) employed by our model, parametrized
> by a weight vector⃗a ∈R2F ′, applying a LeakyReLU activation. Right: An illustration of multihead attention (with K = 3 heads) by node 1 on its neighborhood. Different arrow styles and
> colors denote independent attention computations. The aggregated features from each head are
> concatenated or averaged to obtain⃗h′
> 1. applying a nonlinearity, σ):⃗
> h′
> i = σ

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 4, section UNKNOWN

Chunk `995bb224ce8542e08d7c899ef427867f1fdc77ab2235b272244db45fc864a658`; source `arxiv:1710.10903`; faiss_cosine rank 9 similarity 0.8028320074081421 rerank None; metadata_filtered_cosine rank 9 similarity 0.8028320074081421 rerank None

> . (4)
> To stabilize the learning process of self-attention, we have found extending our mechanism to employ multi-head attention to be beneficial, similarly to Vaswani et al. (2017). Specifically, K independent attention mechanisms execute the transformation of Equation 4, and then their features are
> concatenated, resulting in the following output feature representation:⃗
> h′
> i =
> K
> ∥
> k=1
> σ

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 3, section UNKNOWN

Chunk `916aaacae058b8058a3dc75036725437e03f22eb967efdb92c1110055c0a5a0f`; source `arxiv:1710.10903`; faiss_cosine rank 10 similarity 0.8026596307754517 rerank None; metadata_filtered_cosine rank 10 similarity 0.8026596307754517 rerank None

> LeakyReLU
> ⃗
> aT [W⃗hi∥W⃗hj]

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 12, section UNKNOWN

Chunk `031f9cd08bc2ad3612c947978c2bd7c316d55ca755b3fc81719a2df5b72353a1`; source `arxiv:1706.03762`; paper_aggregation rank 2 similarity 0.771404504776001 rerank None; mmr_diversity rank 2 similarity 0.771404504776001 rerank 0.2631504654884338

> [25] Mitchell P Marcus, Mary Ann Marcinkiewicz, and Beatrice Santorini. Building a large annotated
> corpus of english: The penn treebank. Computational linguistics, 19(2):313–330, 1993. [26] David McClosky, Eugene Charniak, and Mark Johnson. Effective self-training for parsing. In
> Proceedings of the Human Language Technology Conference of the NAACL, Main Conference,
> pages 152–159. ACL, June 2006. [27] Ankur Parikh, Oscar Täckström, Dipanjan Das, and Jakob Uszkoreit. A decomposable attention
> model. In Empirical Methods in Natural Language Processing, 2016. [28] Romain Paulus, Caiming Xiong, and Richard Socher. A deep reinforced model for abstractive
> summarization. arXiv preprint arXiv:1705.04304, 2017. [29] Slav Petrov, Leon Barrett, Romain Thibaux, and Dan Klein. Learning accurate, compact,
> and interpretable tree annotation. In Proceedings of the 21st International Conference on
> Computational Linguistics and 44th Annual Meeting of the ACL, pages 433–440. ACL, July
> 2006. [30] Ofir Press and Lior Wolf. Using the output embedding to improve language models. arXiv
> preprint arXiv:1608.05859, 2016. [31] Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words
> with subword units. arXiv preprint arXiv:1508.07909, 2015. [32] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton,
> and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts
> layer. arXiv preprint arXiv:1701.06538, 2017. [33] Nitish Srivastava, Geoffrey E Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov. Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine
> Learning Research, 15(1):1929–1958, 2014. [34] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory
> networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors,
> Advances in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates,
> Inc., 2015. [35] Ilya Sutskever, Oriol Vinyals, and Quoc VV Le. Sequence to sequence learning with neural
> networks. In Advances in Neural Information Processing Systems, pages 3104–3112, 2014. [36] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. CoRR, abs/1512.00567, 2015. [37] Vinyals & Kaiser, Koo, Petrov, Sutskever, and Hinton. Grammar as a foreign language. In
> Advances in Neural Information Processing Systems, 2015. [38] Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le, Mohammad Norouzi, Wolfgang
> Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al. Google’s neural machine
> translation system: Bridging the gap between human and machine translation. arXiv preprint
> arXiv:1609.08144, 2016. [39] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 3, section UNKNOWN

Chunk `e7bd3150c9ee6ea76ade30fd26e9b8f8d57bd0517a464c3f36aa5f5bdf588c49`; source `arxiv:1609.02907`; paper_aggregation rank 3 similarity 0.7621128559112549 rerank None; mmr_diversity rank 3 similarity 0.7621128559112549 rerank 0.2554338991641997

> Published as a conference paper at ICLR 2017
> In this way, we can still recover a rich class of convolutional filter functions by stacking multiple
> such layers, but we are not limited to the explicit parameterization given by, e.g., the Chebyshev
> polynomials. We intuitively expect that such a model can alleviate the problem of overfitting on
> local neighborhood structures for graphs with very wide node degree distributions, such as social
> networks, citation networks, knowledge graphs and many other real-world graph datasets. Additionally, for a fixed computational budget, this layer-wise linear formulation allows us to build deeper
> models, a practice that is known to improve modeling capacity on a number of domains (He et al.,
> 2016). In this linear formulation of a GCN we further approximate λmax ≈2, as we can expect that neural
> network parameters will adapt to this change in scale during training. Under these approximations
> eq. 5 simplifies to:
> gθ′ ⋆x ≈θ′
> 0x + θ′
> 1 (L −IN) x = θ′
> 0x −θ′
> 1D−1
> 2 AD−1
> 2 x ,
> (6)
> with two free parameters θ′
> 0 and θ′
> 1. The filter parameters can be shared over the whole graph. Successive application of filters of this form then effectively convolve the kth-order neighborhood of
> a node, where k is the number of successive filtering operations or convolutional layers in the neural
> network model. In practice, it can be beneficial to constrain the number of parameters further to address overfitting
> and to minimize the number of operations (such as matrix multiplications) per layer. This leaves us
> with the following expression:
> gθ ⋆x ≈θ

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 9, section References

Chunk `0b7ef6a77c23d10f9fc41f9cb59b2e038144dfc147f829f8ae5cc68d75767d1f`; source `arxiv:1512.03385`; paper_aggregation rank 4 similarity 0.7305300235748291 rerank None

> References
> [1] Y. Bengio, P. Simard, and P. Frasconi. Learning long-term dependencies with gradient descent is difficult. IEEE Transactions on Neural
> Networks, 5(2):157–166, 1994. [2] C. M. Bishop. Neural networks for pattern recognition. Oxford
> university press, 1995. [3] W. L. Briggs, S. F. McCormick, et al. A Multigrid Tutorial. Siam,
> 2000. [4] K. Chatfield, V. Lempitsky, A. Vedaldi, and A. Zisserman. The devil
> is in the details: an evaluation of recent feature encoding methods. In BMVC, 2011. [5] M. Everingham, L. Van Gool, C. K. Williams, J. Winn, and A. Zisserman. The Pascal Visual Object Classes (VOC) Challenge. IJCV,
> pages 303–338, 2010. [6] S. Gidaris and N. Komodakis. Object detection via a multi-region &
> semantic segmentation-aware cnn model. In ICCV, 2015. [7] R. Girshick. Fast R-CNN. In ICCV, 2015. [8] R. Girshick, J. Donahue, T. Darrell, and J. Malik. Rich feature hierarchies for accurate object detection and semantic segmentation. In
> CVPR, 2014. [9] X. Glorot and Y. Bengio. Understanding the difficulty of training
> deep feedforward neural networks. In AISTATS, 2010. [10] i. J. Goodfellow, D. Warde-Farley, M. Mirza, A. Courville, and
> Y. Bengio. Maxout networks. arXiv:1302.4389, 2013. [11] K. He and J. Sun. Convolutional neural networks at constrained time
> cost. In CVPR, 2015. [12] K. He, X. Zhang, S. Ren, and J. Sun. Spatial pyramid pooling in deep
> convolutional networks for visual recognition. In ECCV, 2014. [13] K. He, X. Zhang, S. Ren, and J. Sun. Delving deep into rectifiers:
> Surpassing human-level performance on imagenet classification. In
> ICCV, 2015. [14] g. e. Hinton, N. Srivastava, A. Krizhevsky, i. Sutskever, and
> R. R. Salakhutdinov. Improving neural networks by preventing coadaptation of feature detectors. arXiv:1207.0580, 2012. [15] S. Hochreiter and J. Schmidhuber. Long short-term memory. Neural
> computation, 9(8):1735–1780, 1997. [16] S. Ioffe and C. Szegedy. Batch normalization: Accelerating deep
> network training by reducing internal covariate shift. In ICML, 2015. [17] H. Jegou, M. Douze, and C. Schmid. Product quantization for nearest
> neighbor search. TPAMI, 33, 2011. [18] H. Jegou, F. Perronnin, M. Douze, J. Sanchez, P. Perez, and
> C. Schmid. Aggregating local image descriptors into compact codes. TPAMI, 2012. [19] Y. Jia, e. Shelhamer, J. Donahue, S. Karayev, J. Long, R. Girshick,
> S. Guadarrama, and T. Darrell. Caffe: Convolutional architecture for
> fast feature embedding. arXiv:1408.5093, 2014. [20] A. Krizhevsky. Learning multiple layers of features from tiny images. Tech Report, 2009. [21] A. Krizhevsky, i. Sutskever, and g. Hinton.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 7, section UNKNOWN

Chunk `c9ca9684f6f4d5b798fdff26297910f82af73222ce57345a19b1fa08f6bea058`; source `arxiv:2004.04906`; paper_aggregation rank 5 similarity 0.7173391580581665 rerank None

> t,
> (4)
> Pselected(i)
> =
> softmax
> ˆP⊺wselected

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 8, section UNKNOWN

Chunk `62b1c885ab5d06106c283c7211d19aea8407a974251174545d521b415c3a8900`; source `arxiv:1505.04597`; paper_aggregation rank 6 similarity 0.7159454822540283 rerank None

> 8
> mations, it only needs very few annotated images and has a very reasonable
> training time of only 10 hours on a NVidia Titan GPU (6 GB). We provide the
> full Caffe[6]-based implementation and the trained networks4. We are sure that
> the u-net architecture can be applied easily to many more tasks. Acknowlegements
> This study was supported by the Excellence Initiative of the German Federal
> and State governments (EXC 294) and by the BMBF (Fkz 0316185B). References
> 1. Ciresan, D.C., Gambardella, L.M., Giusti, A., Schmidhuber, J.: Deep neural networks segment neuronal membranes in electron microscopy images. In: NIPS. pp. 2852–2860 (2012)
> 2. Dosovitskiy, A., Springenberg, J.T., Riedmiller, M., Brox, T.: Discriminative unsupervised feature learning with convolutional neural networks. In: NIPS (2014)
> 3. Girshick, R., Donahue, J., Darrell, T., Malik, J.: Rich feature hierarchies for accurate object detection and semantic segmentation. In: Proceedings of the IEEE
> Conference on Computer Vision and Pattern Recognition (CVPR) (2014)
> 4. Hariharan, B., Arbelez, P., Girshick, R., Malik, J.: Hypercolumns for object segmentation and fine-grained localization (2014), arXiv:1411.5752 [cs.CV]
> 5. He, K., Zhang, X., Ren, S., Sun, J.: Delving deep into rectifiers: Surpassing humanlevel performance on imagenet classification (2015), arXiv:1502.01852 [cs.CV]
> 6. Jia, Y., Shelhamer, e., Donahue, J., Karayev, S., Long, J., Girshick, R., Guadarrama, S., Darrell, T.: Caffe: Convolutional architecture for fast feature embedding
> (2014), arXiv:1408.5093 [cs.CV]
> 7. Krizhevsky, A., Sutskever, i., Hinton, g.e.: Imagenet classification with deep convolutional neural networks. In: NIPS. pp. 1106–1114 (2012)
> 8. LeCun, Y., Boser, B., Denker, J.S., Henderson, D., Howard, R.e., Hubbard, W.,
> Jackel, L.D.: Backpropagation applied to handwritten zip code recognition. Neural
> Computation 1(4), 541–551 (1989)
> 9. Long, J., Shelhamer, e., Darrell, T.: Fully convolutional networks for semantic
> segmentation (2014), arXiv:1411.4038 [cs.CV]
> 10. Maska, M., (...), de Solorzano, C.O.: A benchmark for comparison of cell tracking
> algorithms. Bioinformatics 30, 1609–1617 (2014)
> 11. Seyedhosseini, M., Sajjadi, M., Tasdizen, T.: Image segmentation with cascaded
> hierarchical models and logistic disjunctive normal networks. In: Computer Vision
> (ICCV), 2013 IEEE International Conference on. pp. 2168–2175 (2013)
> 12. Simonyan, K., Zisserman, A.: Very deep convolutional networks for large-scale
> image recognition (2014), arXiv:1409.1556 [cs.CV]
> 13. WWW: Web page of the cell tracking challenge, http://www.codesolorzano.com/
> celltrackingchallenge/Cell_Tracking_Challenge/Welcome.html
> 14. WWW: Web page of the em segmentation challenge, http://brainiac2.mit.edu/
> isbi_challenge/
> 4 U-net implementation, trained networks and supplementary material available at
> http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 13, section UNKNOWN

Chunk `b723d6afde45a0af14ab72be16571c7886e9b7f3f9c2ddc9fbc7cf873494ee9a`; source `arxiv:1506.01497`; paper_aggregation rank 7 similarity 0.7107303738594055 rerank None

> 13
> cup : 0.807
> bowl : 0.847
> bowl : 0.816
> bowl : 0.744
> bowl : 0.710
> chair : 0.772
> dining table : 0.618
> oven : 0.969
> refrigerator : 0.631
> cup : 0.990
> pizza : 0.919
> dining table : 0.888
> person : 0.984
> person
> person
> car : 0.816
> pizza : 0.965
> clock : 0.988
> person : 0.998
> kite : 0.934
> toothbrush : 0.668
> teddy bear : 0.999
> teddy bear : 0.890
> teddy bear : 0.802
> teddy bear : 0.738
> bowl : 0.602
> potted plant : 0.769
> toilet : 0.921
> sink : 0.969
> sink : 0.994
> sink : 0.992
> sink : 0.976sink : 0.938
> person : 0.970
> : 0.970
> erson
> person : 0.869
> bus : 0.999
> bottle : 0.768
> cup : 0.720
> chair : 0.644
> tv : 0.964
> tv : 0.959
> laptop : 0.986
> mouse : 0.871
> mouse : 0.677
> m
> keyboard : 0.956
> book : 0.611
> person : 0.986
> boat : 0.758
> boat : 0.746
> boat : 0.613
> bench : 0.971
> train : 0.965
> traffic light : 0.869
> traffic light : 0.713
> chair : 0.631
> couch : 0.991
> couch : 0.719
> couch : 0.627
> dining table : 0.637
> dog : 0.966
> frisbee : 0.998
> bird : 0.987
> bird : 0.968
> bird : 0.894
> person : 0.723
> cup : 0.986
> cup : 0.931
> bowl : 0.958
> sandwich : 0.629
> dining table : 0.941
> zebra : 0.996
> zebra : 0.993
> zebra : 0.970
> 970
> zebra : 0.848
> person : 0.917
> person : 0.792
> : 0.792
> 0 792
> tv : 0.711
> laptop : 0.973
> mouse : 0.981
> keyboard : 0.638
> keyboard : 0.615
> person : 0.999
> person : 0.999
> person : 0.999
> perso
> perso
> tennis racket : 0.960
> bird : 0.956
> bird : 0.906
> bird : 0.746
> horse : 0.990
> person : 0.993
> bottle : 0.982
> oven : 0.655
> refrigerator : 0.699
> clock : 0.982
> bed : 0.999
> person : 0.808
> bottle : 0.627
> pizza : 0.995
> pizza : 0.985
> pizza : 0.982
> pizza : 0.938
> dining table : 0.956
> person : 0.998
> skis : 0.919
> bowl : 0.759
> broccoli : 0.953
> person : 0.999
> person : 0.934
> surfboard : 0.979
> person : 0.940
> person : 0.927
> person : 0.864
> 0.940
> person : 0.854
> person : 0.825person : 0.813
> person : 0.716
> person : 0.692
> p
> person : 0.691
> 927
> 927
> person : 0.665
> person : 0.618
> boat : 0.992
> umbrella : 0.885
> giraffe : 0.993
> giraffe : 0.989
> giraffe : 0.988
> person : 0.867
> airplane : 0.997
> person : 0.970
> person : 0.950
> person : 0.931
> p
> person : 0.916
> person : 0.897
> person : 0.842
> person : 0.841
> person : 0.84
> person : 0.772
> bicycle : 0.891
> bicycle : 0.639
> car : 0.957
> motorcycle : 0.827
> motorcycle : 0.713
> traffic light : 0.802
> umbrella : 0.824
> person : 0.800
> clock : 0.986
> clock : 0.981
> person : 0.996
> person : 0.976
> person : 0.975
> rson : 0.975
> rson
> son : 0
> on
> person : 0.958
> person : 0.950
> person : 0.941
> 0.976
> 0 976
> person : 0.939
> pe
> pe
> person : 0.928
> 958
> 958
> 0 975
> n : 0.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 14, section UNKNOWN

Chunk `f7f46d59ca966b0002a03869ab70bd6b3a2a74387ed5f895f57768ad7347463b`; source `arxiv:2005.11401`; paper_aggregation rank 8 similarity 0.7100379467010498 rerank None

> How much knowledge can you pack into
> the parameters of a language model? arXiv e-prints, 2020. URL https://arxiv.org/abs/
> 2002.08910. [53] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: Bm25 and
> beyond. Found. Trends Inf. Retr., 3(4):333–389, April 2009. ISSN 1554-0669. doi: 10.1561/
> 1500000019. URL https://doi.org/10.1561/1500000019. [54] Irene Solaiman, Miles Brundage, Jack Clark, Amanda Askell, Ariel Herbert-Voss, Jeff Wu, Alec
> Radford, and Jian-Bing Wang. Release strategies and the social impacts of language models. ArXiv, abs/1908.09203, 2019. [55] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors, Advances
> in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates, Inc., 2015. URL http://papers.nips.cc/paper/5846-end-to-end-memory-networks.pdf. 14

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 11, section UNKNOWN

Chunk `c64091b9f2ac650bd1caf6c837de194e183193f5d6d81efd10e08f2906d3541b`; source `arxiv:2104.08663`; paper_aggregation rank 9 similarity 0.707601010799408 rerank None

> 2021. Efficiently Teaching an Effective Dense Retriever with Balanced Topic Aware Sampling. In Proc. of SIGIR. 6
> [24] Sebastian Hofstätter, Sophia Althammer, Michael Schröder, Mete Sertkan, and Allan Hanbury. 2021. Improving Efficient Neural Ranking Models with Cross-Architecture Knowledge
> Distillation. 6, 21
> [25] Doris Hoogeveen, Karin M Verspoor, and Timothy Baldwin. 2015. CQADupStack: A benchmark data set for community question-answering research. In Proceedings of the 20th Australasian document computing symposium, pages 1–8. 4, 19
> [26] Sergey Ioffe. 2010. Improved consistent sampling, weighted minhash and l1 sketching. In 2010
> IEEE International Conference on Data Mining, pages 246–255. IEEE. 4, 20
> [27] Ming Ji, Yizhou Sun, Marina Danilevsky, Jiawei Han, and Jing Gao. 2010. Graph Regularized
> Transductive Classification on Heterogeneous Information Networks. In Machine Learning
> and Knowledge Discovery in Databases, pages 570–586, Berlin, Heidelberg. Springer Berlin
> Heidelberg. 19
> [28] Jing Jiang and ChengXiang Zhai. 2007. An empirical study of tokenization strategies for
> biomedical information retrieval. Information Retrieval, 10(4-5):341–363. 18
> 11

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 3, section UNKNOWN

Chunk `3d97b3becfaeaca7639b5e5ea5a24a93be8c61aff2f2fda5d97294f9efb72ca6`; source `arxiv:1810.04805`; paper_aggregation rank 10 similarity 0.6993507146835327 rerank None

> The
> question-answering example in Figure 1 will serve
> as a running example for this section. A distinctive feature of BERT is its unified architecture across different tasks. There is minimal difference between the pre-trained architecture and the final downstream architecture. Model Architecture
> BERT’s model architecture is a multi-layer bidirectional Transformer encoder based on the original implementation described in Vaswani et al. (2017) and released in
> the tensor2tensor library.1 Because the use
> of Transformers has become common and our implementation is almost identical to the original,
> we will omit an exhaustive background description of the model architecture and refer readers to
> Vaswani et al. (2017) as well as excellent guides
> such as “The Annotated Transformer.”2
> In this work, we denote the number of layers
> (i.e., Transformer blocks) as L, the hidden size as
> H, and the number of self-attention heads as A.3
> We primarily report results on two model sizes:
> BERTBASE (L=12, H=768, A=12, Total Parameters=110M) and BERTLARGE (L=24, H=1024,
> A=16, Total Parameters=340M). BERTBASE was chosen to have the same model
> size as OpenAI GPT for comparison purposes. Critically, however, the BERT Transformer uses
> bidirectional self-attention, while the GPT Transformer uses constrained self-attention where every
> token can only attend to context to its left.4
> 1https://github.com/tensorflow/tensor2tensor
> 2http://nlp.seas.harvard.edu/2018/04/03/attention.html
> 3In all cases we set the feed-forward/filter size to be 4H,
> i.e., 3072 for the H = 768 and 4096 for the H = 1024. 4We note that in the literature the bidirectional Trans-

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### cv-residual-10

How do residual connections enable training of deeper convolutional image recognition networks?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 7, section UNKNOWN

Chunk `1869c59ea2d0d7dc271a684c00164828e67ae3e7b97941e0123a54a108c63ac5`; source `arxiv:1512.03385`; faiss_cosine rank 1 similarity 0.803420901298523 rerank None; metadata_filtered_cosine rank 1 similarity 0.803420901298523 rerank None; paper_aggregation rank 1 similarity 0.803420901298523 rerank None; mmr_diversity rank 1 similarity 0.803420901298523 rerank 0.562394630908966

> The deep plain nets suffer from increased depth,
> and exhibit higher training error when going deeper. This
> phenomenon is similar to that on ImageNet (fig. 4, left) and
> on MNIST (see [42]), suggesting that such an optimization
> difficulty is a fundamental problem. fig. 6 (middle) shows the behaviors of ResNets. Also
> similar to the ImageNet cases (fig. 4, right), our ResNets
> manage to overcome the optimization difficulty and demonstrate accuracy gains when the depth increases. We further explore n = 18 that leads to a 110-layer
> ResNet. In this case, we find that the initial learning rate
> of 0.1 is slightly too large to start converging5. So we use
> 0.01 to warm up the training until the training error is below
> 80% (about 400 iterations), and then go back to 0.1 and continue training. The rest of the learning schedule is as done
> previously. This 110-layer network converges well (fig. 6,
> middle). It has fewer parameters than other deep and thin
> 5With an initial learning rate of 0.1, it starts converging (<90% error)
> after several epochs, but still reaches similar accuracy. 7

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 1, section UNKNOWN

Chunk `ab668d284bc3b11841905e0f6ba63638c4f5a245d43d24e44fd75c1d2689c63f`; source `arxiv:1512.03385`; faiss_cosine rank 2 similarity 0.8028454780578613 rerank None; metadata_filtered_cosine rank 2 similarity 0.8028454780578613 rerank None; mmr_diversity rank 2 similarity 0.8028454780578613 rerank 0.2619918346405028

> 56-layer
> 20-layer
> 56-layer
> 20-layer
> Figure 1. Training error (left) and test error (right) on CIFAR-10
> with 20-layer and 56-layer “plain” networks. The deeper network
> has higher training error, and thus test error. Similar phenomena
> on ImageNet is presented in fig. 4. greatly benefited from very deep models. Driven by the significance of depth, a question arises: Is
> learning better networks as easy as stacking more layers? An obstacle to answering this question was the notorious
> problem of vanishing/exploding gradients [1, 9], which
> hamper convergence from the beginning. This problem,
> however, has been largely addressed by normalized initialization [23, 9, 37, 13] and intermediate normalization layers
> [16], which enable networks with tens of layers to start converging for stochastic gradient descent (SGD) with backpropagation [22]. When deeper networks are able to start converging, a
> degradation problem has been exposed: with the network
> depth increasing, accuracy gets saturated (which might be
> unsurprising) and then degrades rapidly. Unexpectedly,
> such degradation is not caused by overfitting, and adding
> more layers to a suitably deep model leads to higher training error, as reported in [11, 42] and thoroughly verified by
> our experiments. fig. 1 shows a typical example. The degradation (of training accuracy) indicates that not
> all systems are similarly easy to optimize. Let us consider a
> shallower architecture and its deeper counterpart that adds
> more layers onto it. There exists a solution by construction
> to the deeper model: the added layers are identity mapping,
> and the other layers are copied from the learned shallower
> model. The existence of this constructed solution indicates
> that a deeper model should produce no higher training error
> than its shallower counterpart. But experiments show that
> our current solvers on hand are unable to find solutions that
> 1
> arXiv:1512.03385v1 [cs.CV] 10 Dec 2015

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 8, section UNKNOWN

Chunk `b48e386737a8807636608f1e9c0f64706a5fea59698ea4f756d50b7f96e3be47`; source `arxiv:1512.03385`; faiss_cosine rank 3 similarity 0.7965937852859497 rerank None; metadata_filtered_cosine rank 3 similarity 0.7965937852859497 rerank None; mmr_diversity rank 3 similarity 0.7965937852859497 rerank 0.2576156497001647

> residual-110
> residual-1202
> Figure 6. Training on CIFAR-10. Dashed lines denote training error, and bold lines denote testing error. Left: plain networks. The error
> of plain-110 is higher than 60% and not displayed. Middle: ResNets. Right: ResNets with 110 and 1202 layers. 0
> 20
> 40
> 60
> 80
> 100
> 1
> 2
> 3
> layer index (sorted by magnitude)
> std

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 3, section UNKNOWN

Chunk `40bfc2ecd67deed2ab6457842a3fad3c17f1b067a873e3402fffd66403a44b99`; source `arxiv:1512.03385`; faiss_cosine rank 4 similarity 0.7956429719924927 rerank None; metadata_filtered_cosine rank 4 similarity 0.7956429719924927 rerank None; mmr_diversity rank 4 similarity 0.7956429719924927 rerank 0.25695008039474476

> 3.3. Network Architectures
> We have tested various plain/residual nets, and have observed consistent phenomena. To provide instances for discussion, we describe two models for ImageNet as follows. Plain Network. Our plain baselines (fig. 3, middle) are
> mainly inspired by the philosophy of VGG nets [41] (fig. 3,
> left). The convolutional layers mostly have 3×3 filters and
> follow two simple design rules: (i) for the same output
> feature map size, the layers have the same number of filters; and (ii) if the feature map size is halved, the number of filters is doubled so as to preserve the time complexity per layer. We perform downsampling directly by
> convolutional layers that have a stride of 2. The network
> ends with a global average pooling layer and a 1000-way
> fully-connected layer with softmax. The total number of
> weighted layers is 34 in fig. 3 (middle). It is worth noticing that our model has fewer filters and
> lower complexity than VGG nets [41] (fig. 3, left). Our 34layer baseline has 3.6 billion FLOPs (multiply-adds), which
> is only 18% of VGG-19 (19.6 billion FLOPs). 3

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 5, section UNKNOWN

Chunk `6b28e52d3377c346aa217e53902ec285c144634dd338a2f63e09da8bf8ad891e`; source `arxiv:1512.03385`; faiss_cosine rank 5 similarity 0.7954057455062866 rerank None; metadata_filtered_cosine rank 5 similarity 0.7954057455062866 rerank None; mmr_diversity rank 5 similarity 0.7954057455062866 rerank 0.2567840218544005

> More importantly, the 34-layer ResNet exhibits
> considerably lower training error and is generalizable to the
> validation data. This indicates that the degradation problem
> is well addressed in this setting and we manage to obtain
> accuracy gains from increased depth. Second, compared to its plain counterpart, the 34-layer
> 3We have experimented with more training iterations (3×) and still observed the degradation problem, suggesting that this problem cannot be
> feasibly addressed by simply using more iterations. 5

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 1, section UNKNOWN

Chunk `340d13415178da085e6a14c88aa653559bf6057dbb772334af9f0ff9cc30cd00`; source `arxiv:1512.03385`; faiss_cosine rank 6 similarity 0.7949886322021484 rerank None; metadata_filtered_cosine rank 6 similarity 0.7949886322021484 rerank None; mmr_diversity rank 6 similarity 0.7949886322021484 rerank 0.2564920425415038

> Deep Residual Learning for Image Recognition
> Kaiming He
> Xiangyu Zhang
> Shaoqing Ren
> Jian Sun
> Microsoft Research
> {kahe, v-xiangz, v-shren, jiansun}@microsoft.com
> Abstract
> Deeper neural networks are more difficult to train. We
> present a residual learning framework to ease the training
> of networks that are substantially deeper than those used
> previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual
> networks are easier to optimize, and can gain accuracy from
> considerably increased depth. On the ImageNet dataset we
> evaluate residual nets with a depth of up to 152 layers—8×
> deeper than VGG nets [41] but still having lower complexity. An ensemble of these residual nets achieves 3.57% error
> on the ImageNet test set. This result won the 1st place on the
> ILSVRC 2015 classification task. We also present analysis
> on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance
> for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep
> residual nets are foundations of our submissions to ILSVRC
> & COCO 2015 competitions1, where we also won the 1st
> places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation. 1. Introduction
> Deep convolutional neural networks [22, 21] have led
> to a series of breakthroughs for image classification [21,
> 50, 40]. Deep networks naturally integrate low/mid/highlevel features [50] and classifiers in an end-to-end multilayer fashion, and the “levels” of features can be enriched
> by the number of stacked layers (depth). Recent evidence
> [41, 44] reveals that network depth is of crucial importance,
> and the leading results [41, 44, 13, 16] on the challenging
> ImageNet dataset [36] all exploit “very deep” [41] models,
> with a depth of sixteen [41] to thirty [16]. Many other nontrivial visual recognition tasks [8, 12, 7, 32, 27] have also
> 1http://image-net.org/challenges/LSVRC/2015/
> and
> http://mscoco.org/dataset/#detections-challenge2015. 0
> 1
> 2
> 3
> 4
> 5
> 6
> 0 
> 10
> 20
> iter. (1e4)
> training error (%)

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 7, section UNKNOWN

Chunk `6a36434bbf2202180d3fb2c2e61156a3d698bcf89e0726af8575418637970040`; source `arxiv:1512.03385`; faiss_cosine rank 7 similarity 0.794219970703125 rerank None; metadata_filtered_cosine rank 7 similarity 0.794219970703125 rerank None; mmr_diversity rank 7 similarity 0.794219970703125 rerank 0.25595397949218746

> The numbers of
> filters are {16, 32, 64} respectively. The subsampling is performed by convolutions with a stride of 2. The network ends
> with a global average pooling, a 10-way fully-connected
> layer, and softmax. There are totally 6n+2 stacked weighted
> layers. The following table summarizes the architecture:
> output map size
> 32×32
> 16×16
> 8×8
> # layers
> 1+2n
> 2n
> 2n
> # filters
> 16
> 32
> 64
> When shortcut connections are used, they are connected
> to the pairs of 3×3 layers (totally 3n shortcuts). On this
> dataset we use identity shortcuts in all cases (i.e., option A),
> method
> error (%)
> Maxout [10]
> 9.38
> NIN [25]
> 8.81
> DSN [24]
> 8.22
> # layers
> # params
> FitNet [35]
> 19
> 2.5M
> 8.39
> Highway [42, 43]
> 19
> 2.3M
> 7.54 (7.72±0.16)
> Highway [42, 43]
> 32
> 1.25M
> 8.80
> ResNet
> 20
> 0.27M
> 8.75
> ResNet
> 32
> 0.46M
> 7.51
> ResNet
> 44
> 0.66M
> 7.17
> ResNet
> 56
> 0.85M
> 6.97
> ResNet
> 110
> 1.7M
> 6.43 (6.61±0.16)
> ResNet
> 1202
> 19.4M
> 7.93
> Table 6. Classification error on the CIFAR-10 test set. All methods are with data augmentation. For ResNet-110, we run it 5 times
> and show “best (mean±std)” as in [43]. so our residual models have exactly the same depth, width,
> and number of parameters as the plain counterparts. We use a weight decay of 0.0001 and momentum of 0.9,
> and adopt the weight initialization in [13] and BN [16] but
> with no dropout. These models are trained with a minibatch size of 128 on two GPUs. We start with a learning
> rate of 0.1, divide it by 10 at 32k and 48k iterations, and
> terminate training at 64k iterations, which is determined on
> a 45k/5k train/val split. We follow the simple data augmentation in [24] for training: 4 pixels are padded on each side,
> and a 32×32 crop is randomly sampled from the padded
> image or its horizontal flip. For testing, we only evaluate
> the single view of the original 32×32 image. We compare n = {3, 5, 7, 9}, leading to 20, 32, 44, and
> 56-layer networks. fig. 6 (left) shows the behaviors of the
> plain nets. The deep plain nets suffer from increased depth,
> and exhibit higher training error when going deeper. This
> phenomenon is similar to that on ImageNet (fig. 4, left) and
> on MNIST (see [42]), suggesting that such an optimization
> difficulty is a fundamental problem. fig. 6 (middle) shows the behaviors of ResNets.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 7, section UNKNOWN

Chunk `423c76019c479f351ab52a4a2a052f2fd6aaac4b9e9919a498292c2d5f3c6d61`; source `arxiv:1512.03385`; faiss_cosine rank 8 similarity 0.7920120358467102 rerank None; metadata_filtered_cosine rank 8 similarity 0.7920120358467102 rerank None; mmr_diversity rank 8 similarity 0.7920120358467102 rerank 0.254408425092697

> 34-layer net with this 3-layer bottleneck block, resulting in
> a 50-layer ResNet (Table 1). We use option B for increasing
> dimensions. This model has 3.8 billion FLOPs. 101-layer and 152-layer ResNets: We construct 101layer and 152-layer ResNets by using more 3-layer blocks
> (Table 1). Remarkably, although the depth is significantly
> increased, the 152-layer ResNet (11.3 billion FLOPs) still
> has lower complexity than VGG-16/19 nets (15.3/19.6 billion FLOPs). The 50/101/152-layer ResNets are more accurate than
> the 34-layer ones by considerable margins (Table 3 and 4). We do not observe the degradation problem and thus enjoy significant accuracy gains from considerably increased
> depth. The benefits of depth are witnessed for all evaluation
> metrics (Table 3 and 4). Comparisons with State-of-the-art Methods. In Table 4
> we compare with the previous best single-model results. Our baseline 34-layer ResNets have achieved very competitive accuracy. Our 152-layer ResNet has a single-model
> top-5 validation error of 4.49%. This single-model result
> outperforms all previous ensemble results (Table 5). We
> combine six models of different depth to form an ensemble
> (only with two 152-layer ones at the time of submitting). This leads to 3.57% top-5 error on the test set (Table 5). This entry won the 1st place in ILSVRC 2015. 4.2. CIFAR-10 and Analysis
> We conducted more studies on the CIFAR-10 dataset
> [20], which consists of 50k training images and 10k testing images in 10 classes. We present experiments trained
> on the training set and evaluated on the test set. Our focus
> is on the behaviors of extremely deep networks, but not on
> pushing the state-of-the-art results, so we intentionally use
> simple architectures as follows. The plain/residual architectures follow the form in fig. 3
> (middle/right). The network inputs are 32×32 images, with
> the per-pixel mean subtracted. The first layer is 3×3 convolutions. Then we use a stack of 6n layers with 3×3 convolutions on the feature maps of sizes {32, 16, 8} respectively,
> with 2n layers for each feature map size. The numbers of
> filters are {16, 32, 64} respectively. The subsampling is performed by convolutions with a stride of 2. The network ends
> with a global average pooling, a 10-way fully-connected
> layer, and softmax. There are totally 6n+2 stacked weighted
> layers.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 6, section UNKNOWN

Chunk `bb2aa1a054a6db96ef659077b87eac5cd4b63f99a8832168406f4bb0ad009b80`; source `arxiv:1512.03385`; faiss_cosine rank 9 similarity 0.7899971008300781 rerank None; metadata_filtered_cosine rank 9 similarity 0.7899971008300781 rerank None; mmr_diversity rank 9 similarity 0.7899971008300781 rerank 0.25299797058105455

> In Table 3 we
> compare three options: (A) zero-padding shortcuts are used
> for increasing dimensions, and all shortcuts are parameterfree (the same as Table 2 and fig. 4 right); (B) projection shortcuts are used for increasing dimensions, and other
> shortcuts are identity; and (C) all shortcuts are projections. Table 3 shows that all three options are considerably better than the plain counterpart. B is slightly better than A. We
> argue that this is because the zero-padded dimensions in A
> indeed have no residual learning. C is marginally better than
> B, and we attribute this to the extra parameters introduced
> by many (thirteen) projection shortcuts. But the small differences among A/B/C indicate that projection shortcuts are
> not essential for addressing the degradation problem. So we
> do not use option C in the rest of this paper, to reduce memory/time complexity and model sizes. Identity shortcuts are
> particularly important for not increasing the complexity of
> the bottleneck architectures that are introduced below. Deeper Bottleneck Architectures. Next we describe our
> deeper nets for ImageNet. Because of concerns on the training time that we can afford, we modify the building block
> as a bottleneck design4. For each residual function F, we
> use a stack of 3 layers instead of 2 (fig. 5). The three layers
> are 1×1, 3×3, and 1×1 convolutions, where the 1×1 layers
> are responsible for reducing and then increasing (restoring)
> dimensions, leaving the 3×3 layer a bottleneck with smaller
> input/output dimensions. fig. 5 shows an example, where
> both designs have similar time complexity. The parameter-free identity shortcuts are particularly important for the bottleneck architectures. If the identity shortcut in fig. 5 (right) is replaced with projection, one can
> show that the time complexity and model size are doubled,
> as the shortcut is connected to the two high-dimensional
> ends. So identity shortcuts lead to more efficient models
> for the bottleneck designs. 50-layer ResNet: We replace each 2-layer block in the
> 4Deeper non-bottleneck ResNets (e.g., fig. 5 left) also gain accuracy
> from increased depth (as shown on CIFAR-10), but are not as economical
> as the bottleneck ResNets. So the usage of bottleneck designs is mainly due
> to practical considerations. We further note that the degradation problem
> of plain nets is also witnessed for the bottleneck designs. 6

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 6, section UNKNOWN

Chunk `d238aa05d00c9b881574d747613e25cf072abc1eee257872ead9c6d9f3711765`; source `arxiv:1512.03385`; faiss_cosine rank 10 similarity 0.7861875295639038 rerank None; metadata_filtered_cosine rank 10 similarity 0.7861875295639038 rerank None; mmr_diversity rank 10 similarity 0.7861875295639038 rerank 0.2503312706947326

> model
> top-1 err. top-5 err. VGG-16 [41]
> 28.07
> 9.33
> GoogLeNet [44]
> -
> 9.15
> PReLU-net [13]
> 24.27
> 7.38
> plain-34
> 28.54
> 10.02
> ResNet-34 A
> 25.03
> 7.76
> ResNet-34 B
> 24.52
> 7.46
> ResNet-34 C
> 24.19
> 7.40
> ResNet-50
> 22.85
> 6.71
> ResNet-101
> 21.75
> 6.05
> ResNet-152
> 21.43
> 5.71
> Table 3. Error rates (%, 10-crop testing) on ImageNet validation. VGG-16 is based on our test. ResNet-50/101/152 are of option B
> that only uses projections for increasing dimensions. method
> top-1 err. top-5 err. VGG [41] (ILSVRC’14)
> -
> 8.43†
> GoogLeNet [44] (ILSVRC’14)
> -
> 7.89
> VGG [41] (v5)
> 24.4
> 7.1
> PReLU-net [13]
> 21.59
> 5.71
> BN-inception [16]
> 21.99
> 5.81
> ResNet-34 B
> 21.84
> 5.71
> ResNet-34 C
> 21.53
> 5.60
> ResNet-50
> 20.74
> 5.25
> ResNet-101
> 19.87
> 4.60
> ResNet-152
> 19.38
> 4.49
> Table 4. Error rates (%) of single-model results on the ImageNet
> validation set (except † reported on the test set). method
> top-5 err. (test)
> VGG [41] (ILSVRC’14)
> 7.32
> GoogLeNet [44] (ILSVRC’14)
> 6.66
> VGG [41] (v5)
> 6.8
> PReLU-net [13]
> 4.94
> BN-inception [16]
> 4.82
> ResNet (ILSVRC’15)
> 3.57
> Table 5. Error rates (%) of ensembles. The top-5 error is on the
> test set of ImageNet and reported by the test server. ResNet reduces the top-1 error by 3.5% (Table 2), resulting
> from the successfully reduced training error (fig. 4 right vs.
> left). This comparison verifies the effectiveness of residual
> learning on extremely deep systems. Last, we also note that the 18-layer plain/residual nets
> are comparably accurate (Table 2), but the 18-layer ResNet
> converges faster (fig. 4 right vs. left). When the net is “not
> overly deep” (18 layers here), the current SGD solver is still
> able to find good solutions to the plain net. In this case, the
> ResNet eases the optimization by providing faster convergence at the early stage. Identity vs. Projection Shortcuts. We have shown that
> 3x3, 64
> 1x1, 64
> relu
> 1x1, 256
> relu
> relu
> 3x3, 64
> 3x3, 64
> relu
> relu
> 64-d
> 256-d
> Figure 5. A deeper residual function F for ImageNet. Left: a
> building block (on 56×56 feature maps) as in fig. 3 for ResNet34. Right: a “bottleneck” building block for ResNet-50/101/152. parameter-free, identity shortcuts help with training. Next
> we investigate projection shortcuts (Eqn.(2)). In Table 3 we
> compare three options: (A) zero-padding shortcuts are used
> for increasing dimensions, and all shortcuts are parameterfree (the same as Table 2 and fig. 4 right); (B) projection shortcuts are used for increasing dimensions, and other
> shortcuts are identity; and (C) all shortcuts are projections.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 14, section UNKNOWN

Chunk `0839505d3b7de68977b30ae94ac4219a860f639d6082aaeee8639c6cd346c6db`; source `arxiv:1609.02907`; paper_aggregation rank 2 similarity 0.7577685117721558 rerank None

> Published as a conference paper at ICLR 2017
> B
> EXPERIMENTS ON MODEL DEPTH
> In these experiments, we investigate the influence of model depth (number of layers) on classification
> performance. We report results on a 5-fold cross-validation experiment on the Cora, Citeseer and
> Pubmed datasets (Sen et al., 2008) using all labels. In addition to the standard GCN model (eq. 2),
> we report results on a model variant where we use residual connections (He et al., 2016) between
> hidden layers to facilitate training of deeper models by enabling the model to carry over information
> from the previous layer’s input:
> H(l+1) = σ

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 2, section UNKNOWN

Chunk `f08b9157e6e528fb2b32c5aceb0226d7a638fd1f4ef4e3c2626c2d9298ee254f`; source `arxiv:1706.03762`; paper_aggregation rank 3 similarity 0.7536789774894714 rerank None

> 1
> Introduction
> Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks
> in particular, have been firmly established as state of the art approaches in sequence modeling and
> transduction problems such as language modeling and machine translation [35, 2, 5]. Numerous
> efforts have since continued to push the boundaries of recurrent language models and encoder-decoder
> architectures [38, 24, 15]. Recurrent models typically factor computation along the symbol positions of the input and output
> sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden
> states ht, as a function of the previous hidden state ht−1 and the input for position t. This inherently
> sequential nature precludes parallelization within training examples, which becomes critical at longer
> sequence lengths, as memory constraints limit batching across examples. Recent work has achieved
> significant improvements in computational efficiency through factorization tricks [21] and conditional
> computation [32], while also improving model performance in case of the latter. The fundamental
> constraint of sequential computation, however, remains. Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in
> the input or output sequences [2, 19]. In all but a few cases [27], however, such attention mechanisms
> are used in conjunction with a recurrent network. In this work we propose the Transformer, a model architecture eschewing recurrence and instead
> relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in
> translation quality after being trained for as little as twelve hours on eight P100 GPUs. 2
> Background
> The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU
> [16], ByteNet [18] and ConvS2S [9], all of which use convolutional neural networks as basic building
> block, computing hidden representations in parallel for all input and output positions. In these models,
> the number of operations required to relate signals from two arbitrary input or output positions grows
> in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet. This makes
> it more difficult to learn dependencies between distant positions [12].

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 3, section UNKNOWN

Chunk `916aaacae058b8058a3dc75036725437e03f22eb967efdb92c1110055c0a5a0f`; source `arxiv:1710.10903`; paper_aggregation rank 4 similarity 0.7493507862091064 rerank None

> LeakyReLU
> ⃗
> aT [W⃗hi∥W⃗hj]

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 2, section UNKNOWN

Chunk `92b7219b4d847d6bba2b852cdc83a6f7d59943d6845aae54413843ef42854574`; source `arxiv:1505.04597`; paper_aggregation rank 5 similarity 0.7362827062606812 rerank None

> 2
> copy and crop
> input
> image
> tile
> output 
> segmentation 
> map
> 64
> 1
> 128
> 256
> 512
> 1024
> max pool 2x2
> up-conv 2x2
> conv 3x3, ReLU
> 572 x 572
> 2842
> 64
> 128
> 256
> 512
> 570 x 570
> 568 x 568
> 2822
> 2802
> 1402
> 1382
> 1362
> 682
> 662
> 642
> 322
> 282
> 562
> 542
> 522
> 512
> 1042
> 1022
> 1002
> 2002
> 302
> 1982
> 1962
> 392 x 392
> 390 x 390
> 388 x 388
> 388 x 388
> 1024
> 512
> 256
> 256 128
> 64
> 128
> 64
> 2
> conv 1x1
> fig. 1. U-net architecture (example for 32x32 pixels in the lowest resolution). Each blue
> box corresponds to a multi-channel feature map. The number of channels is denoted
> on top of the box. The x-y-size is provided at the lower left edge of the box. White
> boxes represent copied feature maps. The arrows denote the different operations. as input. First, this network can localize. Secondly, the training data in terms
> of patches is much larger than the number of training images. The resulting
> network won the EM segmentation challenge at ISBI 2012 by a large margin. Obviously, the strategy in Ciresan et al. [1] has two drawbacks. First, it
> is quite slow because the network must be run separately for each patch, and
> there is a lot of redundancy due to overlapping patches. Secondly, there is a
> trade-offbetween localization accuracy and the use of context. Larger patches
> require more max-pooling layers that reduce the localization accuracy, while
> small patches allow the network to see only little context. More recent approaches
> [11,4] proposed a classifier output that takes into account the features from
> multiple layers. Good localization and the use of context are possible at the
> same time. In this paper, we build upon a more elegant architecture, the so-called “fully
> convolutional network” [9]. We modify and extend this architecture such that it
> works with very few training images and yields more precise segmentations; see
> Figure 1. The main idea in [9] is to supplement a usual contracting network by
> successive layers, where pooling operators are replaced by upsampling operators. Hence, these layers increase the resolution of the output. In order to localize, high
> resolution features from the contracting path are combined with the upsampled

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 9, section UNKNOWN

Chunk `26ee961215b1f62c02b4dfb81a11495e97e5fd88ed16966eb0c83a1905df704a`; source `arxiv:1506.01497`; paper_aggregation rank 6 similarity 0.7337234020233154 rerank None

> 9
> Table 6: Results on PASCAL VOC 2007 test set with Fast R-CNN detectors and VGG-16. For RPN, the train-time
> proposals for Fast R-CNN are 2000. RPN∗denotes the unsharing feature version. method
> # box
> data
> mAP
> areo
> bike
> bird
> boat
> bottle
> bus
> car
> cat
> chair
> cow
> table
> dog
> horse
> mbike person plant
> sheep
> sofa
> train
> tv
> SS
> 2000
> 07
> 66.9
> 74.5
> 78.3
> 69.2
> 53.2
> 36.6
> 77.3
> 78.2
> 82.0
> 40.7
> 72.7
> 67.9
> 79.6
> 79.2
> 73.0
> 69.0
> 30.1
> 65.4
> 70.2
> 75.8
> 65.8
> SS
> 2000
> 07+12
> 70.0
> 77.0
> 78.1
> 69.3
> 59.4
> 38.3
> 81.6
> 78.6
> 86.7
> 42.8
> 78.8
> 68.9
> 84.7
> 82.0
> 76.6
> 69.9
> 31.8
> 70.1
> 74.8
> 80.4
> 70.4
> RPN∗
> 300
> 07
> 68.5
> 74.1
> 77.2
> 67.7
> 53.9
> 51.0
> 75.1
> 79.2
> 78.9
> 50.7
> 78.0
> 61.1
> 79.1
> 81.9
> 72.2
> 75.9
> 37.2
> 71.4
> 62.5
> 77.4
> 66.4
> RPN
> 300
> 07
> 69.9
> 70.0
> 80.6
> 70.1
> 57.3
> 49.9
> 78.2
> 80.4
> 82.0
> 52.2
> 75.3
> 67.2
> 80.3
> 79.8
> 75.0
> 76.3
> 39.1
> 68.3
> 67.3
> 81.1
> 67.6
> RPN
> 300
> 07+12
> 73.2
> 76.5
> 79.0
> 70.9
> 65.5
> 52.1
> 83.1
> 84.7
> 86.4
> 52.0
> 81.9
> 65.7
> 84.8
> 84.6
> 77.5
> 76.7
> 38.8
> 73.6
> 73.9
> 83.0
> 72.6
> RPN
> 300
> COCO+07+12
> 78.8
> 84.3
> 82.0
> 77.7
> 68.9
> 65.7
> 88.1
> 88.4
> 88.9
> 63.6
> 86.3
> 70.8
> 85.9
> 87.6
> 80.1
> 82.3
> 53.6
> 80.4
> 75.8
> 86.6
> 78.9
> Table 7: Results on PASCAL VOC 2012 test set with Fast R-CNN detectors and VGG-16. For RPN, the train-time
> proposals for Fast R-CNN are 2000. method
> # box
> data
> mAP
> areo
> bike
> bird
> boat
> bottle
> bus
> car
> cat
> chair
> cow
> table
> dog
> horse
> mbike person plant
> sheep
> sofa
> train
> tv
> SS
> 2000
> 12
> 65.7
> 80.3
> 74.7
> 66.9
> 46.9
> 37.7
> 73.9
> 68.6
> 87.7
> 41.7
> 71.1
> 51.1
> 86.0
> 77.8
> 79.8
> 69.8
> 32.1
> 65.5
> 63.8
> 76.4
> 61.7
> SS
> 2000
> 07++12
> 68.4
> 82.3
> 78.4
> 70.8
> 52.3
> 38.7
> 77.8
> 71.6
> 89.3
> 44.2
> 73.0
> 55.0
> 87.5
> 80.5
> 80.8
> 72.0
> 35.1
> 68.3
> 65.7
> 80.4
> 64.2
> RPN
> 300
> 12
> 67.0
> 82.3
> 76.4
> 71.0
> 48.4
> 45.2
> 72.1
> 72.3
> 87.3
> 42.2
> 73.7
> 50.0
> 86.8
> 78.7
> 78.4
> 77.4
> 34.5
> 70.1
> 57.1
> 77.1
> 58.9
> RPN
> 300
> 07++12
> 70.4
> 84.9
> 79.8
> 74.3
> 53.9
> 49.8
> 77.5
> 75.9
> 88.5
> 45.6
> 77.1
> 55.3
> 86.9
> 81.7
> 80.9
> 79.6
> 40.1
> 72.6
> 60.9
> 81.2
> 61.5
> RPN
> 300
> COCO+07++12
> 75.9
> 87.4
> 83.6
> 76.8
> 62.9
> 59.6
> 81.9
> 82.0
> 91.3
> 54.9
> 82.6
> 59.0
> 89.0
> 85.5
> 84.7
> 84.1
> 52.2
> 78.9
> 65.5
> 85.4
> 70.2
> Table 8: Detection results of Faster R-CNN on PASCAL VOC 2007 test set using different settings of
> anchors. The network is VGG-16. The training data
> is VOC 2007 trainval.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 3, section UNKNOWN

Chunk `fa699eb3c5cddedd61a30dd13c1d093b7e0803f121ac1f670c7ef5dd4bb2b5d4`; source `arxiv:1810.04805`; paper_aggregation rank 7 similarity 0.7230801582336426 rerank None

> BERT
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Question
> Paragraph
> Start/End Span
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Masked Sentence A
> Masked Sentence B
> Pre-training
> Fine-Tuning
> NSP
> Mask LM
> Mask LM
> Unlabeled Sentence A and B Pair 
> SQuAD
> Question Answer Pair
> NER
> MNLI
> Figure 1: Overall pre-training and fine-tuning procedures for BERT. Apart from output layers, the same architectures are used in both pre-training and fine-tuning. The same pre-trained model parameters are used to initialize
> models for different down-stream tasks. During fine-tuning, all parameters are fine-tuned. [CLS] is a special
> symbol added in front of every input example, and [SEP] is a special separator token (e.g. separating questions/answers). ing and auto-encoder objectives have been used
> for pre-training such models (Howard and Ruder,
> 2018; Radford et al., 2018; Dai and Le, 2015). 2.3
> Transfer Learning from Supervised Data
> There has also been work showing effective transfer from supervised tasks with large datasets, such
> as natural language inference (Conneau et al.,
> 2017) and machine translation (McCann et al.,
> 2017). Computer vision research has also demonstrated the importance of transfer learning from
> large pre-trained models, where an effective recipe
> is to fine-tune models pre-trained with ImageNet (Deng et al., 2009; Yosinski et al., 2014). 3
> BERT
> We introduce BERT and its detailed implementation in this section. There are two steps in our
> framework: pre-training and fine-tuning. During pre-training, the model is trained on unlabeled
> data over different pre-training tasks. For finetuning, the BERT model is first initialized with
> the pre-trained parameters, and all of the parameters are fine-tuned using labeled data from the
> downstream tasks. Each downstream task has separate fine-tuned models, even though they are initialized with the same pre-trained parameters. The
> question-answering example in Figure 1 will serve
> as a running example for this section. A distinctive feature of BERT is its unified architecture across different tasks. There is minimal difference between the pre-trained architecture and the final downstream architecture.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 12, section UNKNOWN

Chunk `9f3ef2ab28ab0769c05d21d20d08ab08b7dda2099307cc78bf55613f84cc2e07`; source `arxiv:2005.11401`; paper_aggregation rank 8 similarity 0.714580774307251 rerank None

> Toutanova, Llion Jones, Ming-Wei Chang, Andrew Dai, Jakob
> Uszkoreit, Quoc Le, and Slav Petrov. Natural Questions:
> a Benchmark for Question Answering Research. Transactions of the Association of Computational Linguistics, 2019. URL https://tomkwiat.users.x20web.corp.google.com/papers/
> natural-questions/main-1455-kwiatkowski.pdf. [30] Guillaume Lample, Alexandre Sablayrolles, Marc’ Aurelio Ranzato, Ludovic Denoyer, and
> Herve Jegou. Large memory layers with product keys. In H. Wallach, H. Larochelle,
> A. Beygelzimer, F. d’ Alché-Buc, e. Fox, and R. Garnett, editors, Advances in Neural Information Processing Systems 32, pages 8548–8559. Curran Associates, Inc., 2019. URL http:
> //papers.nips.cc/paper/9061-large-memory-layers-with-product-keys.pdf. [31] Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. Latent retrieval for weakly supervised
> open domain question answering. In Proceedings of the 57th Annual Meeting of the Association
> 12

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)** — arXiv:2004.04906, page 9, section UNKNOWN

Chunk `b0a4393b46edfaa665fc64fc19ce6a0d3d6f786c5b296a14be218badec60438f`; source `arxiv:2004.04906`; paper_aggregation rank 9 similarity 0.6946197748184204 rerank None

> In contrast, our model provides a simple and yet
> effective solution that shows stronger empirical performance, without relying on additional pretraining
> or complex joint training schemes. DPR has also been used as an important module in very recent work. For instance, extending
> the idea of leveraging hard negatives, Xiong et al.
> (2020a) use the retrieval model trained in the previous iteration to discover new negatives and construct a different set of examples in each training
> iteration. Starting from our trained DPR model,
> they show that the retrieval performance can be
> further improved. Recent work (Izacard and Grave,
> 2020; Lewis et al., 2020b) have also shown that
> DPR can be combined with generation models
> such as BART (Lewis et al., 2020a) and T5 (Raffel et al., 2019), achieving good performance on
> open-domain QA and other knowledge-intensive
> tasks. 8
> Conclusion
> In this work, we demonstrated that dense retrieval
> can outperform and potentially replace the traditional sparse retrieval component in open-domain
> question answering. While a simple dual-encoder
> approach can be made to work surprisingly well,
> we showed that there are some critical ingredients
> to training a dense retriever successfully. Moreover,
> our empirical analysis and ablation studies indicate
> that more complex model frameworks or similarity
> functions do not necessarily provide additional values. As a result of improved retrieval performance,
> we obtained new state-of-the-art results on multiple
> open-domain question answering benchmarks. Acknowledgments
> We thank the anonymous reviewers for their helpful
> comments and suggestions. References
> Akari Asai, Kazuma Hashimoto, Hannaneh Hajishirzi,
> Richard Socher, and Caiming Xiong. 2020. Learning to retrieve reasoning paths over Wikipedia graph
> for question answering. In International Conference
> on Learning Representations (ICLR). Petr Baudiˇs and Jan ˇSediv`y. 2015. Modeling of the
> question answering task in the yodaqa system. In International Conference of the Cross-Language Evaluation Forum for European Languages, pages 222–
> 228. Springer. Jonathan Berant, Andrew Chou, Roy Frostig, and Percy
> Liang. 2013. Semantic parsing on Freebase from

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 4, section UNKNOWN

Chunk `542f67896add4417df24665a10ebc2d6030f04028398609993b4976acc0feb48`; source `arxiv:2004.12832`; paper_aggregation rank 10 similarity 0.6895363330841064 rerank None

> Even though ColBERT’s late-interaction framework can be applied to a wide variety of architectures (e.g., CNNs, RNNs, transformers, etc.), we choose to focus this work on bi-directional transformerbased encoders (i.e., BERT) owing to their state-of-the-art effectiveness yet very high computational cost. 3.1
> Architecture
> Figure 3 depicts the general architecture of ColBERT, which comprises: (a) a query encoder fQ, (b) a document encoder fD, and (c)
> the late interaction mechanism. Given a query q and document d,
> fQ encodes q into a bag of fixed-size embeddings Eq while fD encodes d into another bag Ed. Crucially, each embeddings in Eq and
> Ed is contextualized based on the other terms in q or d, respectively. We describe our BERT-based encoders in §3.2. Using Eq and Ed, ColBERT computes the relevance score between q and d via late interaction, which we define as a summation
> of maximum similarity (MaxSim) operators. In particular, we find
> the maximum cosine similarity of each v ∈Eq with vectors in Ed,
> and combine the outputs via summation. Besides cosine, we also
> evaluate squared L2 distance as a measure of vector similarity. Intuitively, this interaction mechanism sofly searches for each query
> term tq—in a manner that reflects its context in the query—against
> the document’s embeddings, quantifying the strength of the “match”
> via the largest similarity score between tq and a document term td. Given these term scores, it then estimates the document relevance
> by summing the matching evidence across all query terms. While more sophisticated matching is possible with other choices
> such as deep convolution and atention layers (i.e., as in typical
> interaction-focused models), a summation of maximum similarity
> computations has two distinctive characteristics. First, it stands
> out as a particularly cheap interaction mechanism, as we examine
> its FLOPs in §4.2. Second, and more importantly, it is amenable
> to highly-efficient pruning for top-k retrieval, as we evaluate in
> §4.3. Tis enables using vector-similarity algorithms for skipping
> documents without materializing the full interaction matrix or even
> considering each document in isolation. Other cheap choices (e.g.,
> a summation of average similarity scores, instead of maximum) are
> possible; however, many are less amenable to pruning. In §4.4, we
> conduct an extensive ablation study that empirically verifies the advantage of our MaxSim-based late interaction against alternatives. 3.2
> Qery & Document Encoders
> Prior to late interaction, ColBERT encodes each query or document
> into a bag of embeddings, employing BERT-based encoders.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### cv-detection-11

How do region proposal networks improve object detection speed and accuracy?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 10, section UNKNOWN

Chunk `cc2f3bddbb8a801daa71e3280093cf30bcabfb7e96fd4a2ae7158109d68aeb1d`; source `arxiv:1506.01497`; faiss_cosine rank 1 similarity 0.8345438838005066 rerank None; metadata_filtered_cosine rank 1 similarity 0.8345438838005066 rerank None; paper_aggregation rank 1 similarity 0.8345438838005066 rerank None; mmr_diversity rank 1 similarity 0.8345438838005066 rerank 0.5841807186603546

> 10

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 12, section UNKNOWN

Chunk `4f6ada0767ced573936449050f455410820cb4194b086c6ff19cd2fb9583f647`; source `arxiv:1506.01497`; faiss_cosine rank 2 similarity 0.8298682570457458 rerank None; metadata_filtered_cosine rank 2 similarity 0.8298682570457458 rerank None; mmr_diversity rank 3 similarity 0.8298682570457458 rerank 0.280907779932022

> The model is VGG-16 and the training data is 07+12 trainval (73.2% mAP on the 2007 test
> set). Our method detects objects of a wide range of scales and aspect ratios. Each output box is associated
> with a category label and a softmax score in [0, 1]. A score threshold of 0.6 is used to display these images. The running time for obtaining these results is 198ms per image, including all steps. features with the down-stream detection network, the
> region proposal step is nearly cost-free. Our method
> enables a unified, deep-learning-based object detection system to run at near real-time frame rates. The
> learned RPN also improves region proposal quality
> and thus the overall object detection accuracy. REFERENCES
> [1]
> K. He, X. Zhang, S. Ren, and J. Sun, “Spatial pyramid pooling
> in deep convolutional networks for visual recognition,” in
> European Conference on Computer Vision (ECCV), 2014. [2]
> R. Girshick, “Fast R-CNN,” in IEEE International Conference on
> Computer Vision (ICCV), 2015. [3]
> K. Simonyan and A. Zisserman, “Very deep convolutional

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 1, section UNKNOWN

Chunk `3b684f1e382dcfef7294fff686aa73e958610737b726e79eb0dbb694c002bc5f`; source `arxiv:1506.01497`; faiss_cosine rank 3 similarity 0.8273165225982666 rerank None; metadata_filtered_cosine rank 3 similarity 0.8273165225982666 rerank None; mmr_diversity rank 4 similarity 0.8273165225982666 rerank 0.27912156581878655

> 1
> Faster R-CNN: Towards Real-Time Object
> Detection with Region Proposal Networks
> Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun
> Abstract—State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet [1] and Fast R-CNN [2] have reduced the running time of these detection networks, exposing region
> proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image
> convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional
> network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to
> generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN
> into a single network by sharing their convolutional features—using the recently popular terminology of neural networks with
> “attention” mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model [3],
> our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection
> accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO
> 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been
> made publicly available. Index Terms—Object Detection, Region Proposal, Convolutional Neural Network. ! 1
> INTRODUCTION
> Recent advances in object detection are driven by
> the success of region proposal methods (e.g., [4])
> and region-based convolutional neural networks (RCNNs) [5]. Although region-based CNNs were computationally expensive as originally developed in [5],
> their cost has been drastically reduced thanks to sharing convolutions across proposals [1], [2]. The latest
> incarnation, Fast R-CNN [2], achieves near real-time
> rates using very deep networks [3], when ignoring the
> time spent on region proposals. Now, proposals are the
> test-time computational bottleneck in state-of-the-art
> detection systems. Region proposal methods typically rely on inexpensive features and economical inference schemes. Selective Search [4], one of the most popular methods, greedily merges superpixels based on engineered
> low-level features. Yet when compared to efficient
> detection networks [2], Selective Search is an order of
> magnitude slower, at 2 seconds per image in a CPU
> implementation. EdgeBoxes [6] currently provides the
> best tradeoff between proposal quality and speed,
> at 0.2 seconds per image.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 2, section UNKNOWN

Chunk `f1678ad1881ffa6f4f6a365fd7fa5b8480eb94ad93b99e41b585a6b40373467e`; source `arxiv:1506.01497`; faiss_cosine rank 4 similarity 0.8233081102371216 rerank None; metadata_filtered_cosine rank 4 similarity 0.8233081102371216 rerank None; mmr_diversity rank 5 similarity 0.8233081102371216 rerank 0.27631567716598504

> Since then, the frameworks of
> RPN and Faster R-CNN have been adopted and generalized to other methods, such as 3D object detection
> [13], part-based detection [14], instance segmentation
> [15], and image captioning [16]. Our fast and effective
> object detection system has also been built in com1. Since the publication of the conference version of this paper
> [10], we have also found that RPNs can be trained jointly with Fast
> R-CNN networks leading to less training time. mercial systems such as at Pinterests [17], with user
> engagement improvements reported. In ILSVRC and COCO 2015 competitions, Faster
> R-CNN and RPN are the basis of several 1st-place
> entries [18] in the tracks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation. RPNs completely learn to propose regions
> from data, and thus can easily benefit from deeper
> and more expressive features (such as the 101-layer
> residual nets adopted in [18]). Faster R-CNN and RPN
> are also used by several other leading entries in these
> competitions2. These results suggest that our method
> is not only a cost-efficient solution for practical usage,
> but also an effective way of improving object detection accuracy. 2
> RELATED WORK
> Object Proposals. There is a large literature on object
> proposal methods. Comprehensive surveys and comparisons of object proposal methods can be found in
> [19], [20], [21]. Widely used object proposal methods
> include those based on grouping super-pixels (e.g.,
> Selective Search [4], CPMC [22], MCG [23]) and those
> based on sliding windows (e.g., objectness in windows
> [24], EdgeBoxes [6]). Object proposal methods were
> adopted as external modules independent of the detectors (e.g., Selective Search [4] object detectors, RCNN [5], and Fast R-CNN [2]). Deep Networks for Object Detection. The R-CNN
> method [5] trains CNNs end-to-end to classify the
> proposal regions into object categories or background. R-CNN mainly plays as a classifier, and it does not
> predict object bounds (except for refining by bounding
> box regression). Its accuracy depends on the performance of the region proposal module (see comparisons in [20]). Several papers have proposed ways of
> using deep networks for predicting object bounding
> boxes [25], [9], [26], [27]. In the OverFeat method [9],
> a fully-connected layer is trained to predict the box
> coordinates for the localization task that assumes a
> single object. The fully-connected layer is then turned
> 2. http://image-net.org/challenges/LSVRC/2015/results

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 14, section UNKNOWN

Chunk `02a518fd6abcd19eafcfe8670a8c5c9a083b4d71107d6c985695040447cce509`; source `arxiv:1506.01497`; faiss_cosine rank 5 similarity 0.8222972750663757 rerank None; metadata_filtered_cosine rank 5 similarity 0.8222972750663757 rerank None; mmr_diversity rank 6 similarity 0.8222972750663757 rerank 0.2756080925464629

> [26] D. Erhan, C. Szegedy, A. Toshev, and D. Anguelov, “Scalable
> object detection using deep neural networks,” in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2014. [27] C. Szegedy, S. Reed, D. Erhan, and D. Anguelov, “Scalable,
> high-quality object detection,” arXiv:1412.1441 (v1), 2015. [28] P. O. Pinheiro, R. Collobert, and P. Dollar, “Learning to
> segment object candidates,” in Neural Information Processing
> Systems (NIPS), 2015. [29] J. Dai, K. He, and J. Sun, “Convolutional feature masking
> for joint object and stuff segmentation,” in IEEE Conference on
> Computer Vision and Pattern Recognition (CVPR), 2015. [30] S. Ren, K. He, R. Girshick, X. Zhang, and J. Sun, “Object detection networks on convolutional feature maps,”
> arXiv:1504.06066, 2015. [31] J. K. Chorowski, D. Bahdanau, D. Serdyuk, K. Cho, and
> Y. Bengio, “Attention-based models for speech recognition,”
> in Neural Information Processing Systems (NIPS), 2015. [32] M. D. Zeiler and R. Fergus, “Visualizing and understanding
> convolutional neural networks,” in European Conference on
> Computer Vision (ECCV), 2014. [33] V. Nair and g. e. Hinton, “Rectified linear units improve
> restricted boltzmann machines,” in International Conference on
> Machine Learning (ICML), 2010. [34] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov,
> D. Erhan, and A. Rabinovich, “Going deeper with convolutions,” in IEEE Conference on Computer Vision and Pattern
> Recognition (CVPR), 2015. [35] Y. LeCun, B. Boser, J. S. Denker, D. Henderson, R. e. Howard,
> W. Hubbard, and L. D. Jackel, “Backpropagation applied to
> handwritten zip code recognition,” Neural computation, 1989. [36] O. Russakovsky, J. Deng, H. Su, J. Krause, S. Satheesh, S. Ma,
> Z. Huang, A. Karpathy, A. Khosla, M. Bernstein, A. C. Berg,
> and L. Fei-Fei, “ImageNet Large Scale Visual Recognition
> Challenge,” in International Journal of Computer Vision (IJCV),
> 2015. [37] A. Krizhevsky, i. Sutskever, and g. Hinton, “Imagenet classification with deep convolutional neural networks,” in Neural
> Information Processing Systems (NIPS), 2012. [38] Y. Jia, e. Shelhamer, J. Donahue, S. Karayev, J. Long, R. Girshick, S. Guadarrama, and T. Darrell, “Caffe: Convolutional
> architecture for fast feature embedding,” arXiv:1408.5093, 2014. [39] K. Lenc and A. Vedaldi, “R-CNN minus R,” in British Machine
> Vision Conference (BMVC), 2015.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 1, section UNKNOWN

Chunk `90905cfd4fee5f5bec53a74f8f3a50e76416b2718d890bd318b641415b49035a`; source `arxiv:1506.01497`; faiss_cosine rank 6 similarity 0.8221530914306641 rerank None; metadata_filtered_cosine rank 6 similarity 0.8221530914306641 rerank None; mmr_diversity rank 7 similarity 0.8221530914306641 rerank 0.2755071640014648

> Yet when compared to efficient
> detection networks [2], Selective Search is an order of
> magnitude slower, at 2 seconds per image in a CPU
> implementation. EdgeBoxes [6] currently provides the
> best tradeoff between proposal quality and speed,
> at 0.2 seconds per image. Nevertheless, the region
> proposal step still consumes as much running time
> as the detection network. • S. Ren is with University of Science and Technology of China, Hefei,
> China. This work was done when S. Ren was an intern at Microsoft
> Research. Email: sqren@mail.ustc.edu.cn
> • K. He and J. Sun are with Visual Computing Group, Microsoft
> Research. E-mail: {kahe,jiansun}@microsoft.com
> • R. Girshick is with Facebook AI Research. The majority of this work
> was done when R. Girshick was with Microsoft Research. E-mail:
> rbg@fb.com
> One may note that fast region-based CNNs take
> advantage of GPUs, while the region proposal methods used in research are implemented on the CPU,
> making such runtime comparisons inequitable. An obvious way to accelerate proposal computation is to reimplement it for the GPU. This may be an effective engineering solution, but re-implementation ignores the
> down-stream detection network and therefore misses
> important opportunities for sharing computation. In this paper, we show that an algorithmic change—
> computing proposals with a deep convolutional neural network—leads to an elegant and effective solution
> where proposal computation is nearly cost-free given
> the detection network’s computation. To this end, we
> introduce novel Region Proposal Networks (RPNs) that
> share convolutional layers with state-of-the-art object
> detection networks [1], [2]. By sharing convolutions at
> test-time, the marginal cost for computing proposals
> is small (e.g., 10ms per image). Our observation is that the convolutional feature
> maps used by region-based detectors, like Fast RCNN, can also be used for generating region proposals. On top of these convolutional features, we
> construct an RPN by adding a few additional convolutional layers that simultaneously regress region
> bounds and objectness scores at each location on a
> regular grid. The RPN is thus a kind of fully convolutional network (FCN) [7] and can be trained end-toend specifically for the task for generating detection
> proposals. RPNs are designed to efficiently predict region proposals with a wide range of scales and aspect ratios. In
> contrast to prevalent methods [8], [9], [1], [2] that use
> arXiv:1506.01497v3 [cs.CV] 6 Jan 2016

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 9, section UNKNOWN

Chunk `3143ca30c8ba751064ecff5820fa439d4de8e18e32f2d4b5f11b6d8d9103e404`; source `arxiv:1506.01497`; faiss_cosine rank 7 similarity 0.8219385743141174 rerank None; metadata_filtered_cosine rank 7 similarity 0.8219385743141174 rerank None; mmr_diversity rank 8 similarity 0.8219385743141174 rerank 0.2753570020198821

> But we still adopt these two
> dimensions in our designs to keep our system flexible. In Table 9 we compare different values of λ in Equation (1). By default we use λ = 10 which makes the
> two terms in Equation (1) roughly equally weighted
> after normalization. Table 9 shows that our result is
> impacted just marginally (by ∼1%) when λ is within
> a scale of about two orders of magnitude (1 to 100). This demonstrates that the result is insensitive to λ in
> a wide range. Analysis of Recall-to-IoU. Next we compute the
> recall of proposals at different IoU ratios with groundtruth boxes. It is noteworthy that the Recall-to-IoU
> metric is just loosely [19], [20], [21] related to the
> ultimate detection accuracy. It is more appropriate to
> use this metric to diagnose the proposal method than
> to evaluate it. In Figure 4, we show the results of using 300, 1000,
> and 2000 proposals. We compare with SS and EB, and
> the N proposals are the top-N ranked ones based on
> the confidence generated by these methods. The plots
> show that the RPN method behaves gracefully when
> the number of proposals drops from 2000 to 300. This
> explains why the RPN has a good ultimate detection
> mAP when using as few as 300 proposals. As we
> analyzed before, this property is mainly attributed to
> the cls term of the RPN. The recall of SS and EB drops
> more quickly than RPN when the proposals are fewer.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 4, section UNKNOWN

Chunk `bfb8a8a583c4aff49179368eac67bbc8673786b75edec29a8880b31f00ad0a79`; source `arxiv:1506.01497`; faiss_cosine rank 8 similarity 0.8216978311538696 rerank None; metadata_filtered_cosine rank 8 similarity 0.8216978311538696 rerank None; mmr_diversity rank 9 similarity 0.8216978311538696 rerank 0.2751884818077086

> 4
> car : 1.000
> dog : 0.997
> person : 0.992
> person : 0.979
> horse : 0.993
> conv feature map
> intermediate layer
> 256-d
> 2k scores
> 4k coordinates
> sliding window
> reg layer
> cls layer
> k anchor boxes
> bus : 0.996
> person : 0.736
> boat : 0.970
> person : 0.989
> person : 0.983 person : 0.983
> person : 0.925
> cat : 0.982
> dog : 0.994
> Figure 3: Left: Region Proposal Network (RPN). Right: Example detections using RPN proposals on PASCAL
> VOC 2007 test. Our method detects objects in a wide range of scales and aspect ratios. anchors. An anchor is centered at the sliding window
> in question, and is associated with a scale and aspect
> ratio (Figure 3, left). By default we use 3 scales and
> 3 aspect ratios, yielding k = 9 anchors at each sliding
> position. For a convolutional feature map of a size
> W × H (typically ∼2,400), there are WHk anchors in
> total. Translation-Invariant Anchors
> An important property of our approach is that it
> is translation invariant, both in terms of the anchors
> and the functions that compute proposals relative to
> the anchors. If one translates an object in an image,
> the proposal should translate and the same function
> should be able to predict the proposal in either location. This translation-invariant property is guaranteed by our method5. As a comparison, the MultiBox
> method [27] uses k-means to generate 800 anchors,
> which are not translation invariant. So MultiBox does
> not guarantee that the same proposal is generated if
> an object is translated. The translation-invariant property also reduces the
> model size. MultiBox has a (4 + 1) × 800-dimensional
> fully-connected output layer, whereas our method has
> a (4 + 2) × 9-dimensional convolutional output layer
> in the case of k = 9 anchors. As a result, our output
> layer has 2.8 × 104 parameters (512 × (4 + 2) × 9
> for VGG-16), two orders of magnitude fewer than
> MultiBox’s output layer that has 6.1 × 106 parameters
> (1536 × (4 + 1) × 800 for GoogleNet [34] in MultiBox
> [27]). If considering the feature projection layers, our
> proposal layers still have an order of magnitude fewer
> parameters than MultiBox6. We expect our method
> to have less risk of overfitting on small datasets, like
> PASCAL VOC. 5. As is the case of FCNs [7], our network is translation invariant
> up to the network’s total stride. 6.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 13, section UNKNOWN

Chunk `c0f1a5c616393fe35a429f1b1d8aa7c0c082b827dc674f8eb2829dda169e9f86`; source `arxiv:1506.01497`; faiss_cosine rank 9 similarity 0.8215556144714355 rerank None; metadata_filtered_cosine rank 9 similarity 0.8215556144714355 rerank None; mmr_diversity rank 10 similarity 0.8215556144714355 rerank 0.2750889301300048

> n : 0. 0.975
> 0.975
> 0. person : 0.823
> on : 0.950
> 0 50
> person : 0.805
> person : 0.766
> person : 0.759
> .941
> 4
> person : 0.673
> dog : 0.996
> dog : 0.691
> 0 939
> p
> backpack : 0.756
> handbag : 0.848
> Figure 6: Selected examples of object detection results on the MS COCO test-dev set using the Faster R-CNN
> system. The model is VGG-16 and the training data is COCO trainval (42.7% mAP@0.5 on the test-dev set). Each output box is associated with a category label and a softmax score in [0, 1]. A score threshold of 0.6 is
> used to display these images. For each image, one color represents one object category in that image. networks for large-scale image recognition,” in International
> Conference on Learning Representations (ICLR), 2015. [4]
> J. R. Uijlings, K. e. van de Sande, T. Gevers, and A. W. Smeulders, “Selective search for object recognition,” International
> Journal of Computer Vision (IJCV), 2013. [5]
> R. Girshick, J. Donahue, T. Darrell, and J. Malik, “Rich feature
> hierarchies for accurate object detection and semantic segmentation,” in IEEE Conference on Computer Vision and Pattern
> Recognition (CVPR), 2014. [6]
> C. L. Zitnick and P. Doll ́ar, “Edge boxes: Locating object
> proposals from edges,” in European Conference on Computer
> Vision (ECCV), 2014. [7]
> J. Long, e. Shelhamer, and T. Darrell, “Fully convolutional
> networks for semantic segmentation,” in IEEE Conference on
> Computer Vision and Pattern Recognition (CVPR), 2015. [8]
> P. F. Felzenszwalb, R. B. Girshick, D. McAllester, and D. Ramanan, “Object detection with discriminatively trained partbased models,” IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2010. [9]
> P. Sermanet, D. Eigen, X. Zhang, M. Mathieu, R. Fergus,
> and Y. LeCun, “Overfeat: Integrated recognition, localization
> and detection using convolutional networks,” in International
> Conference on Learning Representations (ICLR), 2014. [10] S. Ren, K. He, R. Girshick, and J. Sun, “Faster R-CNN: Towards

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 6, section UNKNOWN

Chunk `bb9c3800f329b4de56d73db603e4a6296c7313a965a2d32a0a9eeb8ddcc01e62`; source `arxiv:1506.01497`; faiss_cosine rank 10 similarity 0.8207887411117554 rerank None; metadata_filtered_cosine rank 10 similarity 0.8207887411117554 rerank None

> Figure 3 (right)
> shows the capability of our method for a wide range
> of scales and aspect ratios. Table 1 shows the learned
> average proposal size for each anchor using the ZF
> net. We note that our algorithm allows predictions
> that are larger than the underlying receptive field. Such predictions are not impossible—one may still
> roughly infer the extent of an object if only the middle
> of the object is visible. The anchor boxes that cross image boundaries need
> to be handled with care. During training, we ignore
> all cross-boundary anchors so they do not contribute
> to the loss. For a typical 1000 × 600 image, there
> will be roughly 20000 (≈60 × 40 × 9) anchors in
> total. With the cross-boundary anchors ignored, there
> are about 6000 anchors per image for training. If the
> boundary-crossing outliers are not ignored in training,
> they introduce large, difficult to correct error terms in
> the objective, and training does not converge. During
> testing, however, we still apply the fully convolutional
> RPN to the entire image. This may generate crossboundary proposal boxes, which we clip to the image
> boundary.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 11, section UNKNOWN

Chunk `f2f62b78d840fe39da52d6ee669b2a06d8fd231cc8189f696bb62101523eff84`; source `arxiv:1512.03385`; paper_aggregation rank 2 similarity 0.7816970348358154 rerank None; mmr_diversity rank 2 similarity 0.7816970348358154 rerank 0.263394671678543

> training data
> COCO train
> COCO trainval
> test data
> COCO val
> COCO test-dev
> mAP
> @.5
> @[.5, .95]
> @.5
> @[.5, .95]
> baseline Faster R-CNN (VGG-16)
> 41.5
> 21.2
> baseline Faster R-CNN (ResNet-101)
> 48.4
> 27.2
> +box refinement
> 49.9
> 29.9
> +context
> 51.1
> 30.0
> 53.3
> 32.2
> +multi-scale testing
> 53.8
> 32.5
> 55.7
> 34.9
> ensemble
> 59.0
> 37.4
> Table 9. Object detection improvements on MS COCO using Faster R-CNN and ResNet-101. system
> net
> data
> mAP
> areo
> bike
> bird
> boat
> bottle
> bus
> car
> cat
> chair
> cow
> table
> dog
> horse
> mbike person
> plant
> sheep
> sofa
> train
> tv
> baseline
> VGG-16
> 07+12
> 73.2
> 76.5 79.0 70.9 65.5 52.1 83.1 84.7 86.4 52.0 81.9 65.7 84.8 84.6 77.5 76.7 38.8 73.6 73.9 83.0 72.6
> baseline
> ResNet-101
> 07+12
> 76.4
> 79.8 80.7 76.2 68.3 55.9 85.1 85.3 89.8 56.7 87.8 69.4 88.3 88.9 80.9 78.4 41.7 78.6 79.8 85.3 72.0
> baseline+++ ResNet-101
> COCO+07+12
> 85.6
> 90.0 89.6 87.8 80.8 76.1 89.9 89.9 89.6 75.5 90.0 80.7 89.6 90.3 89.1 88.7 65.4 88.1 85.6 89.0 86.8
> Table 10. Detection results on the PASCAL VOC 2007 test set. The baseline is the Faster R-CNN system. The system “baseline+++”
> include box refinement, context, and multi-scale testing in Table 9. system
> net
> data
> mAP
> areo
> bike
> bird
> boat
> bottle
> bus
> car
> cat
> chair
> cow
> table
> dog
> horse
> mbike person
> plant
> sheep
> sofa
> train
> tv
> baseline
> VGG-16
> 07++12
> 70.4
> 84.9 79.8 74.3 53.9 49.8 77.5 75.9 88.5 45.6 77.1 55.3 86.9 81.7 80.9 79.6 40.1 72.6 60.9 81.2 61.5
> baseline
> ResNet-101
> 07++12
> 73.8
> 86.5 81.6 77.2 58.0 51.0 78.6 76.6 93.2 48.6 80.4 59.0 92.1 85.3 84.8 80.7 48.1 77.3 66.5 84.7 65.6
> baseline+++ ResNet-101 COCO+07++12
> 83.8
> 92.1 88.4 84.8 75.9 71.4 86.3 87.8 94.2 66.8 89.4 69.2 93.9 91.9 90.9 89.6 67.9 88.2 76.8 90.3 80.0
> Table 11. Detection results on the PASCAL VOC 2012 test set (http://host.robots.ox.ac.uk:8080/leaderboard/
> displaylb.php?challengeid=11&compid=4). The baseline is the Faster R-CNN system. The system “baseline+++” include
> box refinement, context, and multi-scale testing in Table 9. We select two adjacent scales from the pyramid following
> [33]. RoI pooling and subsequent layers are performed on
> the feature maps of these two scales [33], which are merged
> by maxout as in [33]. Multi-scale testing improves the mAP
> by over 2 points (Table 9). Using validation data. Next we use the 80k+40k trainval set
> for training and the 20k test-dev set for evaluation. The testdev set has no publicly available ground truth and the result
> is reported by the evaluation server.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 2, section UNKNOWN

Chunk `fbd20e002d597122773d49a6f552306c4fcdb02aab870a794ea25f7bf63ddaa9`; source `arxiv:1609.02907`; paper_aggregation rank 3 similarity 0.747177004814148 rerank None

> Published as a conference paper at ICLR 2017
> 2
> FAST APPROXIMATE CONVOLUTIONS ON GRAPHS
> In this section, we provide theoretical motivation for a specific graph-based neural network model
> f(X, A) that we will use in the rest of this paper. We consider a multi-layer Graph Convolutional
> Network (GCN) with the following layer-wise propagation rule:
> H(l+1) = σ

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 12, section UNKNOWN

Chunk `117db82f92e284317641eb2c073a226438b7b540fd982528bac8f02d0b9aa1dc`; source `arxiv:1706.03762`; paper_aggregation rank 4 similarity 0.744791567325592 rerank None

> arXiv preprint
> arXiv:1609.08144, 2016. [39] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu. Deep recurrent models with
> fast-forward connections for neural machine translation. CoRR, abs/1606.04199, 2016. [40] Muhua Zhu, Yue Zhang, Wenliang Chen, Min Zhang, and Jingbo Zhu. Fast and accurate
> shift-reduce constituent parsing. In Proceedings of the 51st Annual Meeting of the ACL (Volume
> 1: Long Papers), pages 434–443. ACL, August 2013. 12

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 3, section UNKNOWN

Chunk `9781b558b298bc8204f2edaf446b1e19f26ae2f1d597f7cf0751467b257c2828`; source `arxiv:1710.10903`; paper_aggregation rank 5 similarity 0.7447810173034668 rerank None

> LeakyReLU
> ⃗
> aT [W⃗hi∥W⃗hk]

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 1, section UNKNOWN

Chunk `ef0308da96f996c02fe3e0a0ccf430f3c05d02e5dfbf09e144698acc2b902fe6`; source `arxiv:1505.04597`; paper_aggregation rank 6 similarity 0.7384428381919861 rerank None

> U-Net: Convolutional Networks for Biomedical
> Image Segmentation
> Olaf Ronneberger, Philipp Fischer, and Thomas Brox
> Computer Science Department and BIOSS Centre for Biological Signalling Studies,
> University of Freiburg, Germany
> ronneber@informatik.uni-freiburg.de,
> WWW home page: http://lmb.informatik.uni-freiburg.de/
> Abstract. There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong
> use of data augmentation to use the available annotated samples more
> efficiently. The architecture consists of a contracting path to capture
> context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very
> few images and outperforms the prior best method (a sliding-window
> convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast
> and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation
> of a 512x512 image takes less than a second on a recent GPU. The full
> implementation (based on Caffe) and the trained networks are available
> at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net. 1
> Introduction
> In the last two years, deep convolutional networks have outperformed the state of
> the art in many visual recognition tasks, e.g. [7,3]. While convolutional networks
> have already existed for a long time [8], their success was limited due to the
> size of the available training sets and the size of the considered networks. The
> breakthrough by Krizhevsky et al. [7] was due to supervised training of a large
> network with 8 layers and millions of parameters on the ImageNet dataset with
> 1 million training images. Since then, even larger and deeper networks have been
> trained [12]. The typical use of convolutional networks is on classification tasks, where
> the output to an image is a single class label. However, in many visual tasks,
> especially in biomedical image processing, the desired output should include
> localization, i.e., a class label is supposed to be assigned to each pixel. Moreover, thousands of training images are usually beyond reach in biomedical tasks. Hence, Ciresan et al. [1] trained a network in a sliding-window setup to predict
> the class label of each pixel by providing a local region (patch) around that pixel
> arXiv:1505.04597v1 [cs.CV] 18 May 2015

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 14, section UNKNOWN

Chunk `f7f46d59ca966b0002a03869ab70bd6b3a2a74387ed5f895f57768ad7347463b`; source `arxiv:2005.11401`; paper_aggregation rank 7 similarity 0.7106202840805054 rerank None

> How much knowledge can you pack into
> the parameters of a language model? arXiv e-prints, 2020. URL https://arxiv.org/abs/
> 2002.08910. [53] Stephen Robertson and Hugo Zaragoza. The probabilistic relevance framework: Bm25 and
> beyond. Found. Trends Inf. Retr., 3(4):333–389, April 2009. ISSN 1554-0669. doi: 10.1561/
> 1500000019. URL https://doi.org/10.1561/1500000019. [54] Irene Solaiman, Miles Brundage, Jack Clark, Amanda Askell, Ariel Herbert-Voss, Jeff Wu, Alec
> Radford, and Jian-Bing Wang. Release strategies and the social impacts of language models. ArXiv, abs/1908.09203, 2019. [55] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors, Advances
> in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates, Inc., 2015. URL http://papers.nips.cc/paper/5846-end-to-end-memory-networks.pdf. 14

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT](https://arxiv.org/abs/2004.12832)** — arXiv:2004.12832, page 7, section UNKNOWN

Chunk `4d21e231d9f96454c79e53894266a6429b9782bb0ac00f6ffd883dc225af4a7c`; source `arxiv:2004.12832`; paper_aggregation rank 8 similarity 0.7044649124145508 rerank None

> Method
> MRR@10 (Dev)
> MRR@10 (Eval)
> Re-ranking Latency (ms)
> FLOPs/query
> BM25 (official)
> 16.7
> 16.5
> -
> -
> KNRM
> 19.8
> 19.8
> 3
> 592M (0.085×)
> Duet
> 24.3
> 24.5
> 22
> 159B (23×)
> fastText+ConvKNRM
> 29.0
> 27.7
> 28
> 78B (11×)
> BERTbase [25]
> 34.7
> -
> 10,700
> 97T (13,900×)
> BERTbase (our training)
> 36.0
> -
> 10,700
> 97T (13,900×)
> BERTlarge [25]
> 36.5
> 35.9
> 32,900
> 340T (48,600×)
> ColBERT (over BERTbase)
> 34.9
> 34.9
> 61
> 7B (1×)
> Table 1: “Re-ranking” results on MS MARCO. Each neural model re-ranks the official top-1000 results produced by BM25. Latency is reported for re-ranking only. To obtain the end-to-end latency in Figure 1, we add the BM25 latency from Table 2. Method
> MRR@10 (Dev)
> MRR@10 (Local Eval)
> Latency (ms)
> Recall@50
> Recall@200
> Recall@1000
> BM25 (official)
> 16.7
> -
> -
> -
> -
> 81.4
> BM25 (Anserini)
> 18.7
> 19.5
> 62
> 59.2
> 73.8
> 85.7
> doc2query
> 21.5
> 22.8
> 85
> 64.4
> 77.9
> 89.1
> DeepCT
> 24.3
> -
> 62 (est.)
> 69 [2]
> 82 [2]
> 91 [2]
> docTTTTTquery
> 27.7
> 28.4
> 87
> 75.6
> 86.9
> 94.7
> ColBERTL2 (re-rank)
> 34.8
> 36.4
> -
> 75.3
> 80.5
> 81.4
> ColBERTL2 (end-to-end)
> 36.0
> 36.7
> 458
> 82.9
> 92.3
> 96.8
> Table 2: End-to-end retrieval results on MS MARCO. Each model retrieves the top-1000 documents per query directly from the
> entire 8.8M document collection. retrieval (i.e., for methods with neural computations) but we use
> up to all four GPUs during indexing. 4.2
> Qality–Cost Tradeoff: Top-k Re-ranking
> In this section, we examine ColBERT’s efficiency and effectiveness
> at re-ranking the top-k results extracted by a bag-of-words retrieval
> model, which is the most typical seting for testing and deploying
> neural ranking models. We begin with the MS MARCO dataset. We
> compare against KNRM, Duet, and fastText+ConvKNRM, a representative set of neural matching models that have been previously
> tested on MS MARCO. In addition, we compare against the natural adaptation of BERT for ranking by Nogueira and Cho [25],
> in particular, BERTbase and its deeper counterpart BERTlarge. We
> also report results for “BERTbase (our training)”, which is based on
> Nogueira and Cho’s base model (including hyperparameters) but
> is trained with the same loss function as ColBERT (§3.3) for 200k
> iterations, allowing for a more direct comparison of the results. We report the competition’s official metric, namely MRR@10,
> on the validation set (Dev) and the evaluation set (Eval). We also
> report the re-ranking latency, which we measure using a single
> Tesla V100 GPU, and the FLOPs per query for each neural ranking
> model.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 2, section UNKNOWN

Chunk `0b001009879392c9654a9ae956a8dc6d82bcdba4d3845b9309439f7ef1ae6b3a`; source `arxiv:2104.08663`; paper_aggregation rank 9 similarity 0.6946675777435303 rerank None

> Fact Checking
> Citation-Prediction
> Wiki
> FEVER
> QUERY
> DOCS
> Natural Claim
> Wikipedia Articles
> Wiki
> Climate-FEVER
> QUERY
> DOCS
> Climate-based Claim
> Wikipedia Articles
> SciFact
> QUERY
> DOCS
> Scientific claim
> PubMed Articles
> Scientific
> SCIDOCS
> QUERY
> DOCS
> Article Title
> PubMed Articles
> Scientific
> Dup. Question Retrieval
> Quora
> Quora
> QUERY
> DOCS
> StackEx. CQADupStack
> QUERY
> DOCS
> Argument Retrieval
> Misc. QUERY
> DOCS
> Misc. ArguAna
> QUERY
> DOCS
> Tóuche-2020
> Query Title
> Query Title + Body
> Query Title
> Quora Questions
> Argument
> Idebate Arguments
> Args.me Arguments
> News Retrieval
> TREC-NEWS
> QUERY
> DOCS
> News Articles
> News
> Tweet Retrieval
> Signal-1M
> QUERY
> DOCS
> News Headline
> Twitter Tweets
> Twitter
> Question-Answering
> Wiki
> NQ
> QUERY
> DOCS
> Wiki
> HotpotQA
> QUERY
> DOCS
> FiQA-2018
> QUERY
> DOCS
> Finance
> Bio-Medical IR
> QUERY
> DOCS
> Scientific
> BioASQ
> QUERY
> DOCS
> NFCorpus
> QUERY
> DOCS
> Scientific
> Entity Retrieval
> DBPedia
> QUERY
> DOCS
> Entity-based Query
> DBPedia Articles
> Wiki
> TREC-COVID
> Scientific
> Wikipedia Articles
> Wikipedia Articles
> Natural Query
> Multi-Hop Query
> CORD-19 Articles
> PubMed Articles
> PubMed Articles
> COVID-19 Query
> Nutrition Facts
> Bio-Medical Query
> Financial Query
> Investment Articles
> Controversial Query
> 9 Tasks
> 18 Datasets
> News Headline
> Robust04
> QUERY
> DOCS
> News
> News Articles
> News Query
> Figure 1: An overview of the diverse tasks and datasets in BEIR benchmark. So far, it is unclear how well existing trained neural models will perform for other text domains or
> textual retrieval tasks. Even more important, it is unclear how well different approaches, like sparse
> embeddings vs. dense embeddings, generalize to out-of-distribution data. In this work, we present a novel robust and heterogeneous benchmark called BEIR (Benchmarking
> IR), comprising of 18 retrieval datasets for comparison and evaluation of model generalization. Prior
> retrieval benchmarks [19, 50] have issues of a comparatively narrow evaluation focusing either only
> on a single task, like question-answering, or on a certain domain. In BEIR, we focus on Diversity, we
> include nine different retrieval tasks: Fact checking, citation prediction, duplicate question retrieval,
> argument retrieval, news retrieval, question answering, tweet retrieval, bio-medical IR, and entity
> retrieval. Further, we include datasets from diverse text domains, datasets that cover broad topics (like
> Wikipedia) and specialized topics (like COVID-19 publications), different text types (news articles vs.
> Tweets), datasets of various sizes (3.6k - 15M documents), and datasets with different query lengths
> (average query length between 3 and 192 words) and document lengths (average document length
> between 11 and 635 words). We use BEIR to evaluate ten diverse retrieval methods from five broad architectures: lexical, sparse,
> dense, late interaction, and re-ranking.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 3, section UNKNOWN

Chunk `fa699eb3c5cddedd61a30dd13c1d093b7e0803f121ac1f670c7ef5dd4bb2b5d4`; source `arxiv:1810.04805`; paper_aggregation rank 10 similarity 0.6897255182266235 rerank None

> BERT
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Question
> Paragraph
> Start/End Span
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Masked Sentence A
> Masked Sentence B
> Pre-training
> Fine-Tuning
> NSP
> Mask LM
> Mask LM
> Unlabeled Sentence A and B Pair 
> SQuAD
> Question Answer Pair
> NER
> MNLI
> Figure 1: Overall pre-training and fine-tuning procedures for BERT. Apart from output layers, the same architectures are used in both pre-training and fine-tuning. The same pre-trained model parameters are used to initialize
> models for different down-stream tasks. During fine-tuning, all parameters are fine-tuned. [CLS] is a special
> symbol added in front of every input example, and [SEP] is a special separator token (e.g. separating questions/answers). ing and auto-encoder objectives have been used
> for pre-training such models (Howard and Ruder,
> 2018; Radford et al., 2018; Dai and Le, 2015). 2.3
> Transfer Learning from Supervised Data
> There has also been work showing effective transfer from supervised tasks with large datasets, such
> as natural language inference (Conneau et al.,
> 2017) and machine translation (McCann et al.,
> 2017). Computer vision research has also demonstrated the importance of transfer learning from
> large pre-trained models, where an effective recipe
> is to fine-tune models pre-trained with ImageNet (Deng et al., 2009; Yosinski et al., 2014). 3
> BERT
> We introduce BERT and its detailed implementation in this section. There are two steps in our
> framework: pre-training and fine-tuning. During pre-training, the model is trained on unlabeled
> data over different pre-training tasks. For finetuning, the BERT model is first initialized with
> the pre-trained parameters, and all of the parameters are fine-tuned using labeled data from the
> downstream tasks. Each downstream task has separate fine-tuned models, even though they are initialized with the same pre-trained parameters. The
> question-answering example in Figure 1 will serve
> as a running example for this section. A distinctive feature of BERT is its unified architecture across different tasks. There is minimal difference between the pre-trained architecture and the final downstream architecture.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---

### cv-segmentation-12

How can encoder-decoder convolutional networks perform biomedical image segmentation with limited training data?

#### Paper-level judgments (all corpus papers)

| Benchmark paper ID | arXiv ID | Title | Source | Judgment (relevant/not_relevant) | Optional grade 0-3 | Reviewer notes |
|---:|---|---|---|---|---:|---|
| 58905439630608566 | 1706.03762 | Attention Is All You Need | [arXiv](https://arxiv.org/abs/1706.03762) |  |  |  |

**Abstract — Attention Is All You Need**

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

| 12418753514679917 | 1810.04805 | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | [arXiv](https://arxiv.org/abs/1810.04805) |  |  |  |

**Abstract — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**

We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

| 34616904588166131 | 1903.10676 | SciBERT: A Pretrained Language Model for Scientific Text | [arXiv](https://arxiv.org/abs/1903.10676) |  |  |  |

**Abstract — SciBERT: A Pretrained Language Model for Scientific Text**

Obtaining large-scale annotated data for NLP tasks in the scientific domain is challenging and expensive. We release SciBERT, a pretrained language model based on BERT (Devlin et al., 2018) to address the lack of high-quality, large-scale labeled scientific data. SciBERT leverages unsupervised pretraining on a large multi-domain corpus of scientific publications to improve performance on downstream scientific NLP tasks. We evaluate on a suite of tasks including sequence tagging, sentence classification and dependency parsing, with datasets from a variety of scientific domains. We demonstrate statistically significant improvements over BERT and achieve new state-of-the-art results on several of these tasks. The code and pretrained models are available at https://github.com/allenai/scibert/.

| 53209105594986581 | 2004.12832 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT | [arXiv](https://arxiv.org/abs/2004.12832) |  |  |  |

**Abstract — ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT**

Recent progress in Natural Language Understanding (NLU) is driving fast-paced advances in Information Retrieval (IR), largely owed to fine-tuning deep language models (LMs) for document ranking. While remarkably effective, the ranking models based on these LMs increase computational cost by orders of magnitude over prior approaches, particularly as they must feed each query-document pair through a massive neural network to compute a single relevance score. To tackle this, we present ColBERT, a novel ranking model that adapts deep LMs (in particular, BERT) for efficient retrieval. ColBERT introduces a late interaction architecture that independently encodes the query and the document using BERT and then employs a cheap yet powerful interaction step that models their fine-grained similarity. By delaying and yet retaining this fine-granular interaction, ColBERT can leverage the expressiveness of deep LMs while simultaneously gaining the ability to pre-compute document representations offline, considerably speeding up query processing. Beyond reducing the cost of re-ranking the documents retrieved by a traditional model, ColBERT's pruning-friendly interaction mechanism enables leveraging vector-similarity indexes for end-to-end retrieval directly from a large document collection. We extensively evaluate ColBERT using two recent passage search datasets. Results show that ColBERT's effectiveness is competitive with existing BERT-based models (and outperforms every non-BERT baseline), while executing two orders-of-magnitude faster and requiring four orders-of-magnitude fewer FLOPs per query.

| 11982946698762241 | 2004.04906 | Dense Passage Retrieval for Open-Domain Question Answering | [arXiv](https://arxiv.org/abs/2004.04906) |  |  |  |

**Abstract — Dense Passage Retrieval for Open-Domain Question Answering**

Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

| 38507081297810974 | 2104.08663 | BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models | [arXiv](https://arxiv.org/abs/2104.08663) |  |  |  |

**Abstract — BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models**

Existing neural information retrieval (IR) models have often been studied in homogeneous and narrow settings, which has considerably limited insights into their out-of-distribution (OOD) generalization capabilities. To address this, and to facilitate researchers to broadly evaluate the effectiveness of their models, we introduce Benchmarking-IR (BEIR), a robust and heterogeneous evaluation benchmark for information retrieval. We leverage a careful selection of 18 publicly available datasets from diverse text retrieval tasks and domains and evaluate 10 state-of-the-art retrieval systems including lexical, sparse, dense, late-interaction and re-ranking architectures on the BEIR benchmark. Our results show BM25 is a robust baseline and re-ranking and late-interaction-based models on average achieve the best zero-shot performances, however, at high computational costs. In contrast, dense and sparse-retrieval models are computationally more efficient but often underperform other approaches, highlighting the considerable room for improvement in their generalization capabilities. We hope this framework allows us to better evaluate and understand existing retrieval systems, and contributes to accelerating progress towards better robust and generalizable systems in the future. BEIR is publicly available at https://github.com/UKPLab/beir.

| 50966763783952365 | 2005.11401 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | [arXiv](https://arxiv.org/abs/2005.11401) |  |  |  |

**Abstract — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**

Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

| 65784579707493984 | 1609.02907 | Semi-Supervised Classification with Graph Convolutional Networks | [arXiv](https://arxiv.org/abs/1609.02907) |  |  |  |

**Abstract — Semi-Supervised Classification with Graph Convolutional Networks**

We present a scalable approach for semi-supervised learning on graph-structured data that is based on an efficient variant of convolutional neural networks which operate directly on graphs. We motivate the choice of our convolutional architecture via a localized first-order approximation of spectral graph convolutions. Our model scales linearly in the number of graph edges and learns hidden layer representations that encode both local graph structure and features of nodes. In a number of experiments on citation networks and on a knowledge graph dataset we demonstrate that our approach outperforms related methods by a significant margin.

| 27355577948731638 | 1710.10903 | Graph Attention Networks | [arXiv](https://arxiv.org/abs/1710.10903) |  |  |  |

**Abstract — Graph Attention Networks**

We present graph attention networks (GATs), novel neural network architectures that operate on graph-structured data, leveraging masked self-attentional layers to address the shortcomings of prior methods based on graph convolutions or their approximations. By stacking layers in which nodes are able to attend over their neighborhoods' features, we enable (implicitly) specifying different weights to different nodes in a neighborhood, without requiring any kind of costly matrix operation (such as inversion) or depending on knowing the graph structure upfront. In this way, we address several key challenges of spectral-based graph neural networks simultaneously, and make our model readily applicable to inductive as well as transductive problems. Our GAT models have achieved or matched state-of-the-art results across four established transductive and inductive graph benchmarks: the Cora, Citeseer and Pubmed citation network datasets, as well as a protein-protein interaction dataset (wherein test graphs remain unseen during training).

| 11712364253894094 | 1512.03385 | Deep Residual Learning for Image Recognition | [arXiv](https://arxiv.org/abs/1512.03385) |  |  |  |

**Abstract — Deep Residual Learning for Image Recognition**

Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions with reference to the layer inputs, instead of learning unreferenced functions. We provide comprehensive empirical evidence showing that these residual networks are easier to optimize, and can gain accuracy from considerably increased depth. On the ImageNet dataset we evaluate residual nets with a depth of up to 152 layers---8x deeper than VGG nets but still having lower complexity. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set. This result won the 1st place on the ILSVRC 2015 classification task. We also present analysis on CIFAR-10 with 100 and 1000 layers. The depth of representations is of central importance for many visual recognition tasks. Solely due to our extremely deep representations, we obtain a 28% relative improvement on the COCO object detection dataset. Deep residual nets are foundations of our submissions to ILSVRC & COCO 2015 competitions, where we also won the 1st places on the tasks of ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation.

| 34506080824068468 | 1506.01497 | Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks | [arXiv](https://arxiv.org/abs/1506.01497) |  |  |  |

**Abstract — Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks**

State-of-the-art object detection networks depend on region proposal algorithms to hypothesize object locations. Advances like SPPnet and Fast R-CNN have reduced the running time of these detection networks, exposing region proposal computation as a bottleneck. In this work, we introduce a Region Proposal Network (RPN) that shares full-image convolutional features with the detection network, thus enabling nearly cost-free region proposals. An RPN is a fully convolutional network that simultaneously predicts object bounds and objectness scores at each position. The RPN is trained end-to-end to generate high-quality region proposals, which are used by Fast R-CNN for detection. We further merge RPN and Fast R-CNN into a single network by sharing their convolutional features---using the recently popular terminology of neural networks with 'attention' mechanisms, the RPN component tells the unified network where to look. For the very deep VGG-16 model, our detection system has a frame rate of 5fps (including all steps) on a GPU, while achieving state-of-the-art object detection accuracy on PASCAL VOC 2007, 2012, and MS COCO datasets with only 300 proposals per image. In ILSVRC and COCO 2015 competitions, Faster R-CNN and RPN are the foundations of the 1st-place winning entries in several tracks. Code has been made publicly available.

| 26454626075950155 | 1505.04597 | U-Net: Convolutional Networks for Biomedical Image Segmentation | [arXiv](https://arxiv.org/abs/1505.04597) |  |  |  |

**Abstract — U-Net: Convolutional Networks for Biomedical Image Segmentation**

There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong use of data augmentation to use the available annotated samples more efficiently. The architecture consists of a contracting path to capture context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation of a 512x512 image takes less than a second on a recent GPU. The full implementation (based on Caffe) and the trained networks are available at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net .

#### Retrieved passages

Scores/ranks below are for review context only. Each unique passage is shown once; its occurrences across strategies are listed.

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 8, section UNKNOWN

Chunk `62b1c885ab5d06106c283c7211d19aea8407a974251174545d521b415c3a8900`; source `arxiv:1505.04597`; faiss_cosine rank 1 similarity 0.7988296747207642 rerank None; metadata_filtered_cosine rank 1 similarity 0.7988296747207642 rerank None; paper_aggregation rank 1 similarity 0.7988296747207642 rerank None; mmr_diversity rank 1 similarity 0.7988296747207642 rerank 0.5591807723045349

> 8
> mations, it only needs very few annotated images and has a very reasonable
> training time of only 10 hours on a NVidia Titan GPU (6 GB). We provide the
> full Caffe[6]-based implementation and the trained networks4. We are sure that
> the u-net architecture can be applied easily to many more tasks. Acknowlegements
> This study was supported by the Excellence Initiative of the German Federal
> and State governments (EXC 294) and by the BMBF (Fkz 0316185B). References
> 1. Ciresan, D.C., Gambardella, L.M., Giusti, A., Schmidhuber, J.: Deep neural networks segment neuronal membranes in electron microscopy images. In: NIPS. pp. 2852–2860 (2012)
> 2. Dosovitskiy, A., Springenberg, J.T., Riedmiller, M., Brox, T.: Discriminative unsupervised feature learning with convolutional neural networks. In: NIPS (2014)
> 3. Girshick, R., Donahue, J., Darrell, T., Malik, J.: Rich feature hierarchies for accurate object detection and semantic segmentation. In: Proceedings of the IEEE
> Conference on Computer Vision and Pattern Recognition (CVPR) (2014)
> 4. Hariharan, B., Arbelez, P., Girshick, R., Malik, J.: Hypercolumns for object segmentation and fine-grained localization (2014), arXiv:1411.5752 [cs.CV]
> 5. He, K., Zhang, X., Ren, S., Sun, J.: Delving deep into rectifiers: Surpassing humanlevel performance on imagenet classification (2015), arXiv:1502.01852 [cs.CV]
> 6. Jia, Y., Shelhamer, e., Donahue, J., Karayev, S., Long, J., Girshick, R., Guadarrama, S., Darrell, T.: Caffe: Convolutional architecture for fast feature embedding
> (2014), arXiv:1408.5093 [cs.CV]
> 7. Krizhevsky, A., Sutskever, i., Hinton, g.e.: Imagenet classification with deep convolutional neural networks. In: NIPS. pp. 1106–1114 (2012)
> 8. LeCun, Y., Boser, B., Denker, J.S., Henderson, D., Howard, R.e., Hubbard, W.,
> Jackel, L.D.: Backpropagation applied to handwritten zip code recognition. Neural
> Computation 1(4), 541–551 (1989)
> 9. Long, J., Shelhamer, e., Darrell, T.: Fully convolutional networks for semantic
> segmentation (2014), arXiv:1411.4038 [cs.CV]
> 10. Maska, M., (...), de Solorzano, C.O.: A benchmark for comparison of cell tracking
> algorithms. Bioinformatics 30, 1609–1617 (2014)
> 11. Seyedhosseini, M., Sajjadi, M., Tasdizen, T.: Image segmentation with cascaded
> hierarchical models and logistic disjunctive normal networks. In: Computer Vision
> (ICCV), 2013 IEEE International Conference on. pp. 2168–2175 (2013)
> 12. Simonyan, K., Zisserman, A.: Very deep convolutional networks for large-scale
> image recognition (2014), arXiv:1409.1556 [cs.CV]
> 13. WWW: Web page of the cell tracking challenge, http://www.codesolorzano.com/
> celltrackingchallenge/Cell_Tracking_Challenge/Welcome.html
> 14. WWW: Web page of the em segmentation challenge, http://brainiac2.mit.edu/
> isbi_challenge/
> 4 U-net implementation, trained networks and supplementary material available at
> http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 2, section UNKNOWN

Chunk `92b7219b4d847d6bba2b852cdc83a6f7d59943d6845aae54413843ef42854574`; source `arxiv:1505.04597`; faiss_cosine rank 2 similarity 0.7839155197143555 rerank None; metadata_filtered_cosine rank 2 similarity 0.7839155197143555 rerank None; mmr_diversity rank 6 similarity 0.7839155197143555 rerank 0.24874086380004878

> 2
> copy and crop
> input
> image
> tile
> output 
> segmentation 
> map
> 64
> 1
> 128
> 256
> 512
> 1024
> max pool 2x2
> up-conv 2x2
> conv 3x3, ReLU
> 572 x 572
> 2842
> 64
> 128
> 256
> 512
> 570 x 570
> 568 x 568
> 2822
> 2802
> 1402
> 1382
> 1362
> 682
> 662
> 642
> 322
> 282
> 562
> 542
> 522
> 512
> 1042
> 1022
> 1002
> 2002
> 302
> 1982
> 1962
> 392 x 392
> 390 x 390
> 388 x 388
> 388 x 388
> 1024
> 512
> 256
> 256 128
> 64
> 128
> 64
> 2
> conv 1x1
> fig. 1. U-net architecture (example for 32x32 pixels in the lowest resolution). Each blue
> box corresponds to a multi-channel feature map. The number of channels is denoted
> on top of the box. The x-y-size is provided at the lower left edge of the box. White
> boxes represent copied feature maps. The arrows denote the different operations. as input. First, this network can localize. Secondly, the training data in terms
> of patches is much larger than the number of training images. The resulting
> network won the EM segmentation challenge at ISBI 2012 by a large margin. Obviously, the strategy in Ciresan et al. [1] has two drawbacks. First, it
> is quite slow because the network must be run separately for each patch, and
> there is a lot of redundancy due to overlapping patches. Secondly, there is a
> trade-offbetween localization accuracy and the use of context. Larger patches
> require more max-pooling layers that reduce the localization accuracy, while
> small patches allow the network to see only little context. More recent approaches
> [11,4] proposed a classifier output that takes into account the features from
> multiple layers. Good localization and the use of context are possible at the
> same time. In this paper, we build upon a more elegant architecture, the so-called “fully
> convolutional network” [9]. We modify and extend this architecture such that it
> works with very few training images and yields more precise segmentations; see
> Figure 1. The main idea in [9] is to supplement a usual contracting network by
> successive layers, where pooling operators are replaced by upsampling operators. Hence, these layers increase the resolution of the output. In order to localize, high
> resolution features from the contracting path are combined with the upsampled

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 1, section UNKNOWN

Chunk `ef0308da96f996c02fe3e0a0ccf430f3c05d02e5dfbf09e144698acc2b902fe6`; source `arxiv:1505.04597`; faiss_cosine rank 3 similarity 0.7833541631698608 rerank None; metadata_filtered_cosine rank 3 similarity 0.7833541631698608 rerank None; mmr_diversity rank 7 similarity 0.7833541631698608 rerank 0.24834791421890245

> U-Net: Convolutional Networks for Biomedical
> Image Segmentation
> Olaf Ronneberger, Philipp Fischer, and Thomas Brox
> Computer Science Department and BIOSS Centre for Biological Signalling Studies,
> University of Freiburg, Germany
> ronneber@informatik.uni-freiburg.de,
> WWW home page: http://lmb.informatik.uni-freiburg.de/
> Abstract. There is large consent that successful training of deep networks requires many thousand annotated training samples. In this paper, we present a network and training strategy that relies on the strong
> use of data augmentation to use the available annotated samples more
> efficiently. The architecture consists of a contracting path to capture
> context and a symmetric expanding path that enables precise localization. We show that such a network can be trained end-to-end from very
> few images and outperforms the prior best method (a sliding-window
> convolutional network) on the ISBI challenge for segmentation of neuronal structures in electron microscopic stacks. Using the same network trained on transmitted light microscopy images (phase contrast
> and DIC) we won the ISBI cell tracking challenge 2015 in these categories by a large margin. Moreover, the network is fast. Segmentation
> of a 512x512 image takes less than a second on a recent GPU. The full
> implementation (based on Caffe) and the trained networks are available
> at http://lmb.informatik.uni-freiburg.de/people/ronneber/u-net. 1
> Introduction
> In the last two years, deep convolutional networks have outperformed the state of
> the art in many visual recognition tasks, e.g. [7,3]. While convolutional networks
> have already existed for a long time [8], their success was limited due to the
> size of the available training sets and the size of the considered networks. The
> breakthrough by Krizhevsky et al. [7] was due to supervised training of a large
> network with 8 layers and millions of parameters on the ImageNet dataset with
> 1 million training images. Since then, even larger and deeper networks have been
> trained [12]. The typical use of convolutional networks is on classification tasks, where
> the output to an image is a single class label. However, in many visual tasks,
> especially in biomedical image processing, the desired output should include
> localization, i.e., a class label is supposed to be assigned to each pixel. Moreover, thousands of training images are usually beyond reach in biomedical tasks. Hence, Ciresan et al. [1] trained a network in a sliding-window setup to predict
> the class label of each pixel by providing a local region (patch) around that pixel
> arXiv:1505.04597v1 [cs.CV] 18 May 2015

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 4, section UNKNOWN

Chunk `f19d0644b9397fe0b7112d8c758024d2a8b20909ed4047fa73465564ab8e9324`; source `arxiv:1505.04597`; faiss_cosine rank 4 similarity 0.7738637328147888 rerank None; metadata_filtered_cosine rank 4 similarity 0.7738637328147888 rerank None; mmr_diversity rank 8 similarity 0.7738637328147888 rerank 0.24170461297035206

> 4
> performed the network of Ciresan et al. [1]. Furthermore, we show results for
> cell segmentation in light microscopy images from the ISBI cell tracking challenge 2015. Here we won with a large margin on the two most challenging 2D
> transmitted light datasets. 2
> Network Architecture
> The network architecture is illustrated in Figure 1. It consists of a contracting
> path (left side) and an expansive path (right side). The contracting path follows
> the typical architecture of a convolutional network. It consists of the repeated
> application of two 3x3 convolutions (unpadded convolutions), each followed by
> a rectified linear unit (ReLU) and a 2x2 max pooling operation with stride 2
> for downsampling. At each downsampling step we double the number of feature
> channels. Every step in the expansive path consists of an upsampling of the
> feature map followed by a 2x2 convolution (“up-convolution”) that halves the
> number of feature channels, a concatenation with the correspondingly cropped
> feature map from the contracting path, and two 3x3 convolutions, each followed by a ReLU. The cropping is necessary due to the loss of border pixels in
> every convolution. At the final layer a 1x1 convolution is used to map each 64component feature vector to the desired number of classes. In total the network
> has 23 convolutional layers. To allow a seamless tiling of the output segmentation map (see Figure 2), it
> is important to select the input tile size such that all 2x2 max-pooling operations
> are applied to a layer with an even x- and y-size. 3
> Training
> The input images and their corresponding segmentation maps are used to train
> the network with the stochastic gradient descent implementation of Caffe [6]. Due to the unpadded convolutions, the output image is smaller than the input
> by a constant border width. To minimize the overhead and make maximum use
> of the GPU memory, we favor large input tiles over a large batch size and hence
> reduce the batch to a single image. Accordingly we use a high momentum (0.99)
> such that a large number of the previously seen training samples determine the
> update in the current optimization step. The energy function is computed by a pixel-wise soft-max over the final
> feature map combined with the cross entropy loss function. The soft-max is
> defined as pk(x) = exp(ak(x))/
> PK
> k′=1 exp(ak′(x))

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 3, section UNKNOWN

Chunk `44a2f69d8066e8ccb22b3addac85bdb00886a53823c45ecce210e2f2377b1c3a`; source `arxiv:1505.04597`; faiss_cosine rank 5 similarity 0.7736750841140747 rerank None; metadata_filtered_cosine rank 5 similarity 0.7736750841140747 rerank None; mmr_diversity rank 9 similarity 0.7736750841140747 rerank 0.24157255887985218

> 3
> fig. 2. Overlap-tile strategy for seamless segmentation of arbitrary large images (here
> segmentation of neuronal structures in EM stacks). Prediction of the segmentation in
> the yellow area, requires image data within the blue area as input. Missing input data
> is extrapolated by mirroring
> output. A successive convolution layer can then learn to assemble a more precise
> output based on this information. One important modification in our architecture is that in the upsampling
> part we have also a large number of feature channels, which allow the network
> to propagate context information to higher resolution layers. As a consequence,
> the expansive path is more or less symmetric to the contracting path, and yields
> a u-shaped architecture. The network does not have any fully connected layers
> and only uses the valid part of each convolution, i.e., the segmentation map only
> contains the pixels, for which the full context is available in the input image. This strategy allows the seamless segmentation of arbitrarily large images by an
> overlap-tile strategy (see Figure 2). To predict the pixels in the border region
> of the image, the missing context is extrapolated by mirroring the input image. This tiling strategy is important to apply the network to large images, since
> otherwise the resolution would be limited by the GPU memory. As for our tasks there is very little training data available, we use excessive
> data augmentation by applying elastic deformations to the available training images. This allows the network to learn invariance to such deformations, without
> the need to see these transformations in the annotated image corpus. This is
> particularly important in biomedical segmentation, since deformation used to
> be the most common variation in tissue and realistic deformations can be simulated efficiently. The value of data augmentation for learning invariance has been
> shown in Dosovitskiy et al. [2] in the scope of unsupervised feature learning. Another challenge in many cell segmentation tasks is the separation of touching objects of the same class; see Figure 3. To this end, we propose the use of
> a weighted loss, where the separating background labels between touching cells
> obtain a large weight in the loss function. The resulting network is applicable to various biomedical segmentation problems. In this paper, we show results on the segmentation of neuronal structures
> in EM stacks (an ongoing competition started at ISBI 2012), where we out-

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 5, section UNKNOWN

Chunk `0d6e6990d2dee05bb1e02b1e1a143e3646b3124e90aefb3f5ac15a7aa8d9728a`; source `arxiv:1505.04597`; faiss_cosine rank 6 similarity 0.7720290422439575 rerank None; metadata_filtered_cosine rank 6 similarity 0.7720290422439575 rerank None; mmr_diversity rank 10 similarity 0.7720290422439575 rerank 0.2404203295707702

> 5
> a
> b
> c
> d
> fig. 3. HeLa cells on glass recorded with DIC (differential interference contrast) microscopy. (a) raw image. (b) overlay with ground truth segmentation. Different colors
> indicate different instances of the HeLa cells. (c) generated segmentation mask (white:
> foreground, black: background). (d) map with a pixel-wise loss weight to force the
> network to learn the border pixels. where l: Ω→{1, . . . , K} is the true label of each pixel and w : Ω→R is
> a weight map that we introduced to give some pixels more importance in the
> training. We pre-compute the weight map for each ground truth segmentation to compensate the different frequency of pixels from a certain class in the training
> data set, and to force the network to learn the small separation borders that we
> introduce between touching cells (See Figure 3c and d). The separation border is computed using morphological operations. The
> weight map is then computed as
> w(x) = wc(x) + w0 · exp

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 6, section UNKNOWN

Chunk `01db7b93caba46def91e2df206199aee8fcd08bec137bad16479ba905687393d`; source `arxiv:1505.04597`; faiss_cosine rank 7 similarity 0.7692052125930786 rerank None; metadata_filtered_cosine rank 7 similarity 0.7692052125930786 rerank None

> 6
> microscopical images we primarily need shift and rotation invariance as well as
> robustness to deformations and gray value variations. Especially random elastic deformations of the training samples seem to be the key concept to train
> a segmentation network with very few annotated images. We generate smooth
> deformations using random displacement vectors on a coarse 3 by 3 grid. The
> displacements are sampled from a Gaussian distribution with 10 pixels standard
> deviation. Per-pixel displacements are then computed using bicubic interpolation. Drop-out layers at the end of the contracting path perform further implicit
> data augmentation. 4
> Experiments
> We demonstrate the application of the u-net to three different segmentation
> tasks. The first task is the segmentation of neuronal structures in electron microscopic recordings. An example of the data set and our obtained segmentation
> is displayed in Figure 2. We provide the full result as Supplementary Material. The data set is provided by the EM segmentation challenge [14] that was started
> at ISBI 2012 and is still open for new contributions. The training data is a set of
> 30 images (512x512 pixels) from serial section transmission electron microscopy
> of the Drosophila first instar larva ventral nerve cord (VNC). Each image comes
> with a corresponding fully annotated ground truth segmentation map for cells
> (white) and membranes (black). The test set is publicly available, but its segmentation maps are kept secret. An evaluation can be obtained by sending the
> predicted membrane probability map to the organizers. The evaluation is done
> by thresholding the map at 10 different levels and computation of the “warping
> error”, the “Rand error” and the “pixel error” [14]. The u-net (averaged over 7 rotated versions of the input data) achieves without any further pre- or postprocessing a warping error of 0.0003529 (the new
> best score, see Table 1) and a rand-error of 0.0382. This is significantly better than the sliding-window convolutional network
> result by Ciresan et al. [1], whose best submission had a warping error of 0.000420
> and a rand error of 0.0504. In terms of rand error the only better performing
> Table 1. Ranking on the EM segmentation challenge [14] (march 6th, 2015), sorted
> by warping error. Rank
> Group name
> Warping Error
> Rand Error
> Pixel Error
> ** human values **
> 0.000005
> 0.0021
> 0.0010
> 1. u-net
> 0.000353
> 0.0382
> 0.0611
> 2. DIVE-SCI
> 0.000355
> 0.0305
> 0.0584
> 3. IDSIA [1]
> 0.000420
> 0.0504
> 0.0613
> 4. DIVE
> 0.000430
> 0.0545
> 0.0582
> ... 10. IDSIA-SCI
> 0.000653
> 0.0189
> 0.1027

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 7, section UNKNOWN

Chunk `b163da4ec3a37bd97e6974d3303f7dde2a119785127f8baf066c239b17829d1c`; source `arxiv:1505.04597`; faiss_cosine rank 8 similarity 0.7676153779029846 rerank None; metadata_filtered_cosine rank 8 similarity 0.7676153779029846 rerank None

> 7
> a
> b
> c
> d
> fig. 4. Result on the ISBI cell tracking challenge. (a) part of an input image of the
> “PhC-U373” data set. (b) Segmentation result (cyan mask) with manual ground truth
> (yellow border) (c) input image of the “DIC-HeLa” data set. (d) Segmentation result
> (random colored masks) with manual ground truth (yellow border). Table 2. Segmentation results (IOU) on the ISBI cell tracking challenge 2015. Name
> PhC-U373
> DIC-HeLa
> IMCB-SG (2014)
> 0.2669
> 0.2935
> KTH-SE (2014)
> 0.7953
> 0.4607
> HOUS-US (2014)
> 0.5323
> -
> second-best 2015
> 0.83
> 0.46
> u-net (2015)
> 0.9203
> 0.7756
> algorithms on this data set use highly data set specific post-processing methods1
> applied to the probability map of Ciresan et al. [1]. We also applied the u-net to a cell segmentation task in light microscopic images. This segmenation task is part of the ISBI cell tracking challenge 2014 and
> 2015 [10,13]. The first data set “PhC-U373”2 contains Glioblastoma-astrocytoma
> U373 cells on a polyacrylimide substrate recorded by phase contrast microscopy
> (see Figure 4a,b and Supp. Material). It contains 35 partially annotated training images. Here we achieve an average IOU (“intersection over union”) of 92%,
> which is significantly better than the second best algorithm with 83% (see Table 2). The second data set “DIC-HeLa”3 are HeLa cells on a flat glass recorded
> by differential interference contrast (DIC) microscopy (see Figure 3, Figure 4c,d
> and Supp. Material). It contains 20 partially annotated training images. Here we
> achieve an average IOU of 77.5% which is significantly better than the second
> best algorithm with 46%. 5
> Conclusion
> The u-net architecture achieves very good performance on very different biomedical segmentation applications. Thanks to data augmentation with elastic defor1 The authors of this algorithm have submitted 78 different solutions to achieve this
> result. 2 Data set provided by dr. Sanjay Kumar. Department of Bioengineering University
> of California at Berkeley. Berkeley CA (USA)
> 3 Data set provided by dr. Gert van Cappellen Erasmus Medical Center. Rotterdam. The Netherlands

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 4, section UNKNOWN

Chunk `9a744158f4112533da8d5c0c96239c03aa3f1224bcabc8e909b3713301e7e1ce`; source `arxiv:1505.04597`; faiss_cosine rank 9 similarity 0.7654784321784973 rerank None; metadata_filtered_cosine rank 9 similarity 0.7654784321784973 rerank None

> where ak(x) denotes the
> activation in feature channel k at the pixel position x ∈Ωwith Ω⊂Z2. K
> is the number of classes and pk(x) is the approximated maximum-function. i.e.
> pk(x) ≈1 for the k that has the maximum activation ak(x) and pk(x) ≈0 for
> all other k. The cross entropy then penalizes at each position the deviation of
> pl(x)(x) from 1 using
> E =
> X
> x∈Ω
> w(x) log(pl(x)(x))
> (1)

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)** — arXiv:1505.04597, page 5, section UNKNOWN

Chunk `06d7fe8bb8301853a739bf8b2d6783623dde0217f499c1fefa363d1bc46f3558`; source `arxiv:1505.04597`; faiss_cosine rank 10 similarity 0.7629326581954956 rerank None; metadata_filtered_cosine rank 10 similarity 0.7629326581954956 rerank None

> −(d1(x) + d2(x))2
> 2σ2
> ! (2)
> where wc : Ω→R is the weight map to balance the class frequencies, d1 : Ω→R
> denotes the distance to the border of the nearest cell and d2 : Ω→R the distance
> to the border of the second nearest cell. In our experiments we set w0 = 10 and
> σ ≈5 pixels. In deep networks with many convolutional layers and different paths through
> the network, a good initialization of the weights is extremely important. Otherwise, parts of the network might give excessive activations, while other parts
> never contribute. Ideally the initial weights should be adapted such that each
> feature map in the network has approximately unit variance. For a network with
> our architecture (alternating convolution and ReLU layers) this can be achieved
> by drawing the initial weights from a Gaussian distribution with a standard
> deviation of
> p
> 2/N, where N denotes the number of incoming nodes of one neuron [5]. e.g. for a 3x3 convolution and 64 feature channels in the previous layer
> N = 9 · 64 = 576. 3.1
> Data Augmentation
> Data augmentation is essential to teach the network the desired invariance and
> robustness properties, when only few training samples are available. In case of

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 9, section References

Chunk `0b7ef6a77c23d10f9fc41f9cb59b2e038144dfc147f829f8ae5cc68d75767d1f`; source `arxiv:1512.03385`; paper_aggregation rank 2 similarity 0.7368345260620117 rerank None

> References
> [1] Y. Bengio, P. Simard, and P. Frasconi. Learning long-term dependencies with gradient descent is difficult. IEEE Transactions on Neural
> Networks, 5(2):157–166, 1994. [2] C. M. Bishop. Neural networks for pattern recognition. Oxford
> university press, 1995. [3] W. L. Briggs, S. F. McCormick, et al. A Multigrid Tutorial. Siam,
> 2000. [4] K. Chatfield, V. Lempitsky, A. Vedaldi, and A. Zisserman. The devil
> is in the details: an evaluation of recent feature encoding methods. In BMVC, 2011. [5] M. Everingham, L. Van Gool, C. K. Williams, J. Winn, and A. Zisserman. The Pascal Visual Object Classes (VOC) Challenge. IJCV,
> pages 303–338, 2010. [6] S. Gidaris and N. Komodakis. Object detection via a multi-region &
> semantic segmentation-aware cnn model. In ICCV, 2015. [7] R. Girshick. Fast R-CNN. In ICCV, 2015. [8] R. Girshick, J. Donahue, T. Darrell, and J. Malik. Rich feature hierarchies for accurate object detection and semantic segmentation. In
> CVPR, 2014. [9] X. Glorot and Y. Bengio. Understanding the difficulty of training
> deep feedforward neural networks. In AISTATS, 2010. [10] i. J. Goodfellow, D. Warde-Farley, M. Mirza, A. Courville, and
> Y. Bengio. Maxout networks. arXiv:1302.4389, 2013. [11] K. He and J. Sun. Convolutional neural networks at constrained time
> cost. In CVPR, 2015. [12] K. He, X. Zhang, S. Ren, and J. Sun. Spatial pyramid pooling in deep
> convolutional networks for visual recognition. In ECCV, 2014. [13] K. He, X. Zhang, S. Ren, and J. Sun. Delving deep into rectifiers:
> Surpassing human-level performance on imagenet classification. In
> ICCV, 2015. [14] g. e. Hinton, N. Srivastava, A. Krizhevsky, i. Sutskever, and
> R. R. Salakhutdinov. Improving neural networks by preventing coadaptation of feature detectors. arXiv:1207.0580, 2012. [15] S. Hochreiter and J. Schmidhuber. Long short-term memory. Neural
> computation, 9(8):1735–1780, 1997. [16] S. Ioffe and C. Szegedy. Batch normalization: Accelerating deep
> network training by reducing internal covariate shift. In ICML, 2015. [17] H. Jegou, M. Douze, and C. Schmid. Product quantization for nearest
> neighbor search. TPAMI, 33, 2011. [18] H. Jegou, F. Perronnin, M. Douze, J. Sanchez, P. Perez, and
> C. Schmid. Aggregating local image descriptors into compact codes. TPAMI, 2012. [19] Y. Jia, e. Shelhamer, J. Donahue, S. Karayev, J. Long, R. Girshick,
> S. Guadarrama, and T. Darrell. Caffe: Convolutional architecture for
> fast feature embedding. arXiv:1408.5093, 2014. [20] A. Krizhevsky. Learning multiple layers of features from tiny images. Tech Report, 2009. [21] A. Krizhevsky, i. Sutskever, and g. Hinton.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907)** — arXiv:1609.02907, page 11, section UNKNOWN

Chunk `1564785c05e0d036919533a696ff0cdcb1b015902e4adee64cf2f642cb111d41`; source `arxiv:1609.02907`; paper_aggregation rank 3 similarity 0.7365154027938843 rerank None; mmr_diversity rank 4 similarity 0.7365154027938843 rerank 0.2467033922672271

> X
> j∈Ni
> 1
> cij
> h(l)
> j W (l)

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762)** — arXiv:1706.03762, page 12, section UNKNOWN

Chunk `031f9cd08bc2ad3612c947978c2bd7c316d55ca755b3fc81719a2df5b72353a1`; source `arxiv:1706.03762`; paper_aggregation rank 4 similarity 0.730786919593811 rerank None; mmr_diversity rank 3 similarity 0.730786919593811 rerank 0.25125198960304257

> [25] Mitchell P Marcus, Mary Ann Marcinkiewicz, and Beatrice Santorini. Building a large annotated
> corpus of english: The penn treebank. Computational linguistics, 19(2):313–330, 1993. [26] David McClosky, Eugene Charniak, and Mark Johnson. Effective self-training for parsing. In
> Proceedings of the Human Language Technology Conference of the NAACL, Main Conference,
> pages 152–159. ACL, June 2006. [27] Ankur Parikh, Oscar Täckström, Dipanjan Das, and Jakob Uszkoreit. A decomposable attention
> model. In Empirical Methods in Natural Language Processing, 2016. [28] Romain Paulus, Caiming Xiong, and Richard Socher. A deep reinforced model for abstractive
> summarization. arXiv preprint arXiv:1705.04304, 2017. [29] Slav Petrov, Leon Barrett, Romain Thibaux, and Dan Klein. Learning accurate, compact,
> and interpretable tree annotation. In Proceedings of the 21st International Conference on
> Computational Linguistics and 44th Annual Meeting of the ACL, pages 433–440. ACL, July
> 2006. [30] Ofir Press and Lior Wolf. Using the output embedding to improve language models. arXiv
> preprint arXiv:1608.05859, 2016. [31] Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words
> with subword units. arXiv preprint arXiv:1508.07909, 2015. [32] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton,
> and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts
> layer. arXiv preprint arXiv:1701.06538, 2017. [33] Nitish Srivastava, Geoffrey E Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov. Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine
> Learning Research, 15(1):1929–1958, 2014. [34] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory
> networks. In C. Cortes, N. D. Lawrence, D. D. Lee, M. Sugiyama, and R. Garnett, editors,
> Advances in Neural Information Processing Systems 28, pages 2440–2448. Curran Associates,
> Inc., 2015. [35] Ilya Sutskever, Oriol Vinyals, and Quoc VV Le. Sequence to sequence learning with neural
> networks. In Advances in Neural Information Processing Systems, pages 3104–3112, 2014. [36] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. CoRR, abs/1512.00567, 2015. [37] Vinyals & Kaiser, Koo, Petrov, Sutskever, and Hinton. Grammar as a foreign language. In
> Advances in Neural Information Processing Systems, 2015. [38] Yonghui Wu, Mike Schuster, Zhifeng Chen, Quoc V Le, Mohammad Norouzi, Wolfgang
> Macherey, Maxim Krikun, Yuan Cao, Qin Gao, Klaus Macherey, et al. Google’s neural machine
> translation system: Bridging the gap between human and machine translation. arXiv preprint
> arXiv:1609.08144, 2016. [39] Jie Zhou, Ying Cao, Xuguang Wang, Peng Li, and Wei Xu.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[SciBERT: A Pretrained Language Model for Scientific Text](https://arxiv.org/abs/1903.10676)** — arXiv:1903.10676, page 5, section UNKNOWN

Chunk `da8f408fc72cbfc67233d77f126bad748dacb4637e21261e9f0ce0a1137d9b4b`; source `arxiv:1903.10676`; paper_aggregation rank 5 similarity 0.7250841856002808 rerank None; mmr_diversity rank 2 similarity 0.7250841856002808 rerank 0.254685878753662

> main, we observe +0.76 F1 for biomedical tasks,
> +0.61 F1 for computer science tasks, and +0.11 F1
> for multidomain tasks. Given the disjoint vocabularies (Section 2) and
> the magnitude of improvement over BERT-Base
> (Section 4), we suspect that while an in-domain
> vocabulary is helpful, SCIBERT benefits most
> from the scientific corpus pretraining. 6
> Related Work
> Recent work on domain adaptation of BERT includes BIOBERT (Lee et al., 2019) and CLINICALBERT (Alsentzer et al., 2019; Huang et al.,
> 2019). BIOBERT is trained on PubMed abstracts and PMC full text articles, and CLINICALBERT is trained on clinical text from the
> MIMIC-III database (Johnson et al., 2016). In
> contrast, SCIBERT is trained on the full text of
> 1.14M biomedical and computer science papers
> from the Semantic Scholar corpus (Ammar et al.,
> 2018). Furthermore, SCIBERT uses an in-domain
> vocabulary (SCIVOCAB) while the other abovementioned models use the original BERT vocabulary (BASEVOCAB). 7
> Conclusion and Future Work
> We released SCIBERT, a pretrained language
> model for scientific text based on BERT. We evaluated SCIBERT on a suite of tasks and datasets from
> scientific domains. SCIBERT significantly outperformed BERT-Base and achieves new SOTA results on several of these tasks, even compared to
> some reported BIOBERT (Lee et al., 2019) results
> on biomedical tasks. For future work, we will release a version of
> SCIBERT analogous to BERT-Large, as well as experiment with different proportions of papers from
> each domain. Because these language models are
> costly to train, we aim to build a single resource
> that’s useful across multiple domains. Acknowledgment
> We thank the anonymous reviewers for their comments and suggestions. We also thank Waleed
> Ammar, Noah Smith, Yoav Goldberg, Daniel
> King, Doug Downey, and Dan Weld for their helpful discussions and feedback. All experiments
> were performed on beaker.org and supported
> in part by credits from Google Cloud. References
> Emily Alsentzer, John R. Murphy, Willie Boag, WeiHung Weng, Di Jin, Tristan Naumann, and Matthew
> B. A. McDermott. 2019. Publicly available clinical bert embeddings. In ClinicalNLP workshop at
> NAACL. Waleed Ammar, Dirk Groeneveld, Chandra Bhagavatula, Iz Beltagy, Miles Crawford, Doug Downey, Jason Dunkelberger, Ahmed Elgohary, Sergey Feldman, Vu Ha, Rodney Kinney, Sebastian Kohlmeier,
> Kyle Lo, Tyler Murray, Hsu-Han Ooi, Matthew Peters, Joanna Power, Sam Skjonsberg, Lucy Lu Wang,
> Chris Wilhelm, Zheng Yuan, Madeleine van Zuylen,
> and Oren Etzioni. 2018. Construction of the literature graph in semantic scholar. In NAACL. Arman
> Cohan,
> Waleed
> Ammar,
> Madeleine
> van
> Zuylen,
> and
> Field
> Cady. 2019.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Graph Attention Networks](https://arxiv.org/abs/1710.10903)** — arXiv:1710.10903, page 10, section UNKNOWN

Chunk `fcea54931b05092e1a0163f59962b65e5c07f16c3f329520bdf035a8660a7fe4`; source `arxiv:1710.10903`; paper_aggregation rank 6 similarity 0.711514949798584 rerank None

> Learning phrase representations using rnn encoder-decoder
> for statistical machine translation. arXiv preprint arXiv:1406.1078, 2014. Djork-Arn ́e Clevert, Thomas Unterthiner, and Sepp Hochreiter. Fast and accurate deep network
> learning by exponential linear units (elus). International Conference on Learning Representations
> (ICLR), 2016. Micha ̈el Defferrard, Xavier Bresson, and Pierre Vandergheynst. Convolutional neural networks
> on graphs with fast localized spectral filtering. In Advances in Neural Information Processing
> Systems, pp. 3844–3852, 2016. Misha Denil, Sergio G ́omez Colmenarejo, Serkan Cabi, David Saxton, and Nando de Freitas. Programmable agents. arXiv preprint arXiv:1706.06383, 2017. Yan Duan, Marcin Andrychowicz, Bradly Stadie, Jonathan Ho, Jonas Schneider, Ilya Sutskever,
> Pieter Abbeel, and Wojciech Zaremba. One-shot imitation learning. arXiv preprint
> arXiv:1703.07326, 2017. David K Duvenaud, Dougal Maclaurin, Jorge Iparraguirre, Rafael Bombarell, Timothy Hirzel, Al ́an
> Aspuru-Guzik, and Ryan P Adams. Convolutional networks on graphs for learning molecular
> fingerprints. In Advances in neural information processing systems, pp. 2224–2232, 2015. 10

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)** — arXiv:1810.04805, page 3, section UNKNOWN

Chunk `fa699eb3c5cddedd61a30dd13c1d093b7e0803f121ac1f670c7ef5dd4bb2b5d4`; source `arxiv:1810.04805`; paper_aggregation rank 7 similarity 0.7087681293487549 rerank None

> BERT
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Question
> Paragraph
> Start/End Span
> BERT
> E[CLS]
> E1
>  E[SEP]
> ... EN
> E1’
> ... EM’
> C
> T1
> T[SEP]
> ... TN
> T1’
> ... TM’
> [CLS]
> Tok 1
>  [SEP]
> ... Tok N
> Tok 1
> ... TokM
> Masked Sentence A
> Masked Sentence B
> Pre-training
> Fine-Tuning
> NSP
> Mask LM
> Mask LM
> Unlabeled Sentence A and B Pair 
> SQuAD
> Question Answer Pair
> NER
> MNLI
> Figure 1: Overall pre-training and fine-tuning procedures for BERT. Apart from output layers, the same architectures are used in both pre-training and fine-tuning. The same pre-trained model parameters are used to initialize
> models for different down-stream tasks. During fine-tuning, all parameters are fine-tuned. [CLS] is a special
> symbol added in front of every input example, and [SEP] is a special separator token (e.g. separating questions/answers). ing and auto-encoder objectives have been used
> for pre-training such models (Howard and Ruder,
> 2018; Radford et al., 2018; Dai and Le, 2015). 2.3
> Transfer Learning from Supervised Data
> There has also been work showing effective transfer from supervised tasks with large datasets, such
> as natural language inference (Conneau et al.,
> 2017) and machine translation (McCann et al.,
> 2017). Computer vision research has also demonstrated the importance of transfer learning from
> large pre-trained models, where an effective recipe
> is to fine-tune models pre-trained with ImageNet (Deng et al., 2009; Yosinski et al., 2014). 3
> BERT
> We introduce BERT and its detailed implementation in this section. There are two steps in our
> framework: pre-training and fine-tuning. During pre-training, the model is trained on unlabeled
> data over different pre-training tasks. For finetuning, the BERT model is first initialized with
> the pre-trained parameters, and all of the parameters are fine-tuned using labeled data from the
> downstream tasks. Each downstream task has separate fine-tuned models, even though they are initialized with the same pre-trained parameters. The
> question-answering example in Figure 1 will serve
> as a running example for this section. A distinctive feature of BERT is its unified architecture across different tasks. There is minimal difference between the pre-trained architecture and the final downstream architecture.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](https://arxiv.org/abs/1506.01497)** — arXiv:1506.01497, page 14, section UNKNOWN

Chunk `02a518fd6abcd19eafcfe8670a8c5c9a083b4d71107d6c985695040447cce509`; source `arxiv:1506.01497`; paper_aggregation rank 8 similarity 0.7055658102035522 rerank None

> [26] D. Erhan, C. Szegedy, A. Toshev, and D. Anguelov, “Scalable
> object detection using deep neural networks,” in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2014. [27] C. Szegedy, S. Reed, D. Erhan, and D. Anguelov, “Scalable,
> high-quality object detection,” arXiv:1412.1441 (v1), 2015. [28] P. O. Pinheiro, R. Collobert, and P. Dollar, “Learning to
> segment object candidates,” in Neural Information Processing
> Systems (NIPS), 2015. [29] J. Dai, K. He, and J. Sun, “Convolutional feature masking
> for joint object and stuff segmentation,” in IEEE Conference on
> Computer Vision and Pattern Recognition (CVPR), 2015. [30] S. Ren, K. He, R. Girshick, X. Zhang, and J. Sun, “Object detection networks on convolutional feature maps,”
> arXiv:1504.06066, 2015. [31] J. K. Chorowski, D. Bahdanau, D. Serdyuk, K. Cho, and
> Y. Bengio, “Attention-based models for speech recognition,”
> in Neural Information Processing Systems (NIPS), 2015. [32] M. D. Zeiler and R. Fergus, “Visualizing and understanding
> convolutional neural networks,” in European Conference on
> Computer Vision (ECCV), 2014. [33] V. Nair and g. e. Hinton, “Rectified linear units improve
> restricted boltzmann machines,” in International Conference on
> Machine Learning (ICML), 2010. [34] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. Reed, D. Anguelov,
> D. Erhan, and A. Rabinovich, “Going deeper with convolutions,” in IEEE Conference on Computer Vision and Pattern
> Recognition (CVPR), 2015. [35] Y. LeCun, B. Boser, J. S. Denker, D. Henderson, R. e. Howard,
> W. Hubbard, and L. D. Jackel, “Backpropagation applied to
> handwritten zip code recognition,” Neural computation, 1989. [36] O. Russakovsky, J. Deng, H. Su, J. Krause, S. Satheesh, S. Ma,
> Z. Huang, A. Karpathy, A. Khosla, M. Bernstein, A. C. Berg,
> and L. Fei-Fei, “ImageNet Large Scale Visual Recognition
> Challenge,” in International Journal of Computer Vision (IJCV),
> 2015. [37] A. Krizhevsky, i. Sutskever, and g. Hinton, “Imagenet classification with deep convolutional neural networks,” in Neural
> Information Processing Systems (NIPS), 2012. [38] Y. Jia, e. Shelhamer, J. Donahue, S. Karayev, J. Long, R. Girshick, S. Guadarrama, and T. Darrell, “Caffe: Convolutional
> architecture for fast feature embedding,” arXiv:1408.5093, 2014. [39] K. Lenc and A. Vedaldi, “R-CNN minus R,” in British Machine
> Vision Conference (BMVC), 2015.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)** — arXiv:2005.11401, page 12, section UNKNOWN

Chunk `d28074865837340f79552b04ec4048a5ec1d94c4f59c99df54220cc0ab8ae4f5`; source `arxiv:2005.11401`; paper_aggregation rank 9 similarity 0.7028299570083618 rerank None

> [20] Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Ming-Wei Chang. REALM:
> Retrieval-augmented language model pre-training. ArXiv, abs/2002.08909, 2020. URL https:
> //arxiv.org/abs/2002.08909. [21] Tatsunori B Hashimoto,
> Kelvin Guu,
> Yonatan Oren,
> and Percy S Liang. A
> retrieve-and-edit
> framework
> for
> predicting
> structured
> outputs. In
> S. Bengio,
> H. Wallach,
> H. Larochelle,
> K. Grauman,
> N. Cesa-Bianchi,
> and R. Garnett,
> editors,
> Advances
> in
> Neural
> Information
> Processing
> Systems
> 31,
> pages
> 10052–
> 10062. Curran
> Associates,
> Inc.,
> 2018. URL
> http://papers.nips.cc/paper/
> 8209-a-retrieve-and-edit-framework-for-predicting-structured-outputs. pdf. [22] Nabil Hossain, Marjan Ghazvininejad, and Luke Zettlemoyer. Simple and effective retrieveedit-rerank text generation. In Proceedings of the 58th Annual Meeting of the Association for
> Computational Linguistics, pages 2532–2538, Online, July 2020. Association for Computational Linguistics. doi: 10.18653/v1/2020.acl-main.228. URL https://www.aclweb.org/
> anthology/2020.acl-main.228. [23] Jeff Johnson, Matthijs Douze, and Hervé Jégou. Billion-scale similarity search with gpus. arXiv
> preprint arXiv:1702.08734, 2017. URL https://arxiv.org/abs/1702.08734. [24] Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer. TriviaQA: A Large Scale
> Distantly Supervised Challenge Dataset for Reading Comprehension. In Proceedings of the
> 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
> pages 1601–1611, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1147. URL https://www.aclweb.org/anthology/P17-1147. [25] Armand Joulin and Tomas Mikolov. Inferring algorithmic patterns with stackaugmented recurrent nets. In Proceedings of the 28th International Conference on
> Neural Information Processing Systems - Volume 1, NIPS’15, page 190–198, Cambridge,
> MA, USA, 2015. MIT Press. URL https://papers.nips.cc/paper/
> 5857-inferring-algorithmic-patterns-with-stack-augmented-recurrent-nets. [26] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Ledell Wu, Sergey Edunov, Danqi Chen, and
> Wen-tau Yih. Dense passage retrieval for open-domain question answering. arXiv preprint
> arXiv:2004.04906, 2020. URL https://arxiv.org/abs/2004.04906. [27] Urvashi Khandelwal, Omer Levy, Dan Jurafsky, Luke Zettlemoyer, and Mike Lewis. Generalization through memorization: Nearest neighbor language models. In International Conference on
> Learning Representations, 2020. URL https://openreview.net/forum?id=HklBjCEKvH. [28] Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In Yoshua
> Bengio and Yann LeCun, editors, 3rd International Conference on Learning Representations,
> ICLR 2015, San Diego, CA, USA, May 7-9, 2015, Conference Track Proceedings, 2015. URL
> http://arxiv.org/abs/1412.6980. [29] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh,
> Chris Alberti, Danielle Epstein, Illia Polosukhin, Matthew Kelcey, Jacob Devlin, Kenton Lee, Kristina N. Toutanova, Llion Jones, Ming-Wei Chang, Andrew Dai, Jakob
> Uszkoreit, Quoc Le, and Slav Petrov. Natural Questions:
> a Benchmark for Question Answering Research. Transactions of the Association of Computational Linguistics, 2019. URL https://tomkwiat.users.x20web.corp.google.com/papers/
> natural-questions/main-1455-kwiatkowski.pdf. [30] Guillaume Lample, Alexandre Sablayrolles, Marc’ Aurelio Ranzato, Ludovic Denoyer, and
> Herve Jegou.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663)** — arXiv:2104.08663, page 18, section UNKNOWN

Chunk `b70a47037c6a027260219719b86bea803e00d8f60804cf3b760813c7ab1fffa0`; source `arxiv:2104.08663`; paper_aggregation rank 10 similarity 0.7024025321006775 rerank None

> by T and test queries for evaluation denoted by Q. We additionally provide dataset website links in
> Table 5 and intuitive examples in Table 8. We now describe each task and dataset included in the
> BEIR benchmark below:
> D.1
> Bio-Medical Information Retrieval
> Bio-medical information retrieval is the task of searching relevant scientific documents such as
> research papers or blogs for a given scientific query in the biomedical domain [28]. We consider a
> scientific query as input and retrieve bio-medical documents as output. TREC-COVID [65] is an ad-hoc search challenge based on the CORD-19 dataset containing scientific articles related to the COVID-19 pandemic [69]. We include the July 16, 2020 version of
> CORD-19 dataset as corpus T and use the final cumulative judgements with query descriptions from
> the original task as queries Q. NFCorpus [7] contains natural language queries harvested from NutritionFacts (NF). We use the
> original splits provided alongside all content sources from NF (videos, blogs, and Q&A posts) as
> queries Q and annotated medical documents from PubMed as corpus T. BioASQ [61] Task 8b is a biomedical semantic question answering challenge. We use the original
> train and test splits provided in Task 8b as queries Q and collect around 15M articles from PubMed
> provided in Task 8a as our corpus T. D.2
> Open-domain Question Answering (QA)
> Retrieval in open domain question answering [8] is the task of retrieving the correct answer for a
> question, without a predefined location for the answer. In open-domain tasks, model must retrieve
> over an entire knowledge source (such as Wikipedia). We consider the question as input and the
> passage containing the answer as output. Natural Questions [34] contains Google search queries and documents with paragraphs and answer
> spans within Wikipedia articles. We did not use the NQ version from ReQA [1] as it focused on
> queries having a short answer. As a result, we parsed the HTML of the original NQ dataset and
> include more complex development queries that often require a longer passage as answer compared to
> ReQA. We filtered out queries without an answer, or having a table as an answer, or with conflicting
> Wikipedia pages. We retain 2,681,468 passages as our corpus T and 3452 test queries Q from the
> original dataset. HotpotQA [76] contains multi-hop like questions which require reasoning over multiple paragraphs
> to find the correct answer.

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

**[Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)** — arXiv:1512.03385, page 1, section UNKNOWN

Chunk `ab668d284bc3b11841905e0f6ba63638c4f5a245d43d24e44fd75c1d2689c63f`; source `arxiv:1512.03385`; mmr_diversity rank 5 similarity 0.7293094396591187 rerank 0.2434404194355011

> 56-layer
> 20-layer
> 56-layer
> 20-layer
> Figure 1. Training error (left) and test error (right) on CIFAR-10
> with 20-layer and 56-layer “plain” networks. The deeper network
> has higher training error, and thus test error. Similar phenomena
> on ImageNet is presented in fig. 4. greatly benefited from very deep models. Driven by the significance of depth, a question arises: Is
> learning better networks as easy as stacking more layers? An obstacle to answering this question was the notorious
> problem of vanishing/exploding gradients [1, 9], which
> hamper convergence from the beginning. This problem,
> however, has been largely addressed by normalized initialization [23, 9, 37, 13] and intermediate normalization layers
> [16], which enable networks with tens of layers to start converging for stochastic gradient descent (SGD) with backpropagation [22]. When deeper networks are able to start converging, a
> degradation problem has been exposed: with the network
> depth increasing, accuracy gets saturated (which might be
> unsurprising) and then degrades rapidly. Unexpectedly,
> such degradation is not caused by overfitting, and adding
> more layers to a suitably deep model leads to higher training error, as reported in [11, 42] and thoroughly verified by
> our experiments. fig. 1 shows a typical example. The degradation (of training accuracy) indicates that not
> all systems are similarly easy to optimize. Let us consider a
> shallower architecture and its deeper counterpart that adds
> more layers onto it. There exists a solution by construction
> to the deeper model: the added layers are identity mapping,
> and the other layers are copied from the learned shallower
> model. The existence of this constructed solution indicates
> that a deeper model should produce no higher training error
> than its shallower counterpart. But experiments show that
> our current solvers on hand are unable to find solutions that
> 1
> arXiv:1512.03385v1 [cs.CV] 10 Dec 2015

Judgment: ______  Grade (0–3, optional): ______  Reviewer notes: ____________________

---
