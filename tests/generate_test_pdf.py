import fitz
from pathlib import Path

def create_sample_pdf(dest_path: str):
    """
    Programmatically creates a mock academic PDF file using PyMuPDF for testing purposes.
    """
    doc = fitz.open()
    
    # Page 1: Title, Abstract, Introduction
    page1 = doc.new_page()
    page1.insert_text((50, 50), "Attention Is All You Need", fontsize=20)
    page1.insert_text((50, 80), "Ashish Vaswani, Noam Shazeer, Niki Parmar", fontsize=12)
    
    abstract_text = (
        "Abstract\n"
        "The dominant sequence transduction models are based on complex recurrent or convolutional neural "
        "networks in an encoder-decoder configuration. We propose a new simple network architecture, the "
        "Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. "
        "Experiments on two translation tasks show these models to be superior in quality while being more parallelizable "
        "and requiring significantly less time to train. Our model achieves 28.4 BLEU on English-to-German translation."
    )
    page1.insert_textbox(fitz.Rect(50, 110, 550, 250), abstract_text, fontsize=10)
    
    intro_text = (
        "Introduction\n"
        "Recurrent neural networks, long short-term memory (LSTM) and gated recurrent neural networks "
        "have been firmly established as state-of-the-art approaches in sequence modeling and transduction "
        "problems. However, sequential computation precludes parallelization within training examples, which "
        "becomes critical at longer sequence lengths, as memory constraints limit batching across examples."
    )
    page1.insert_textbox(fitz.Rect(50, 270, 550, 420), intro_text, fontsize=10)
    
    # Page 2: Methodology, Results, References
    page2 = doc.new_page()
    method_text = (
        "Methodology\n"
        "Most competitive neural sequence transduction models have an encoder-decoder structure. Here, the "
        "encoder maps an input sequence of symbol representations to a sequence of continuous representations. "
        "Given the encoder representations, the decoder then generates an output sequence of symbols one element at a time. "
        "The Transformer follows this overall architecture using stacked self-attention and point-wise, fully "
        "connected layers for both the encoder and decoder."
    )
    page2.insert_textbox(fitz.Rect(50, 50, 550, 200), method_text, fontsize=10)
    
    results_text = (
        "Results\n"
        "On the WMT 2014 English-to-German translation task, the big transformer model outperforms the best "
        "previously reported models (including ensembles) by more than 2.0 BLEU, establishing a new "
        "state-of-the-art BLEU score of 28.4. Our model achieves 41.8 BLEU on English-to-French translation."
    )
    page2.insert_textbox(fitz.Rect(50, 220, 550, 350), results_text, fontsize=10)
    
    ref_text = (
        "References\n"
        "[1] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In CVPR, 2016.\n"
        "[2] Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In ICLR, 2015.\n"
        "[3] Ashish Vaswani et al. Attention is all you need. In NeurIPS, 2017."
    )
    page2.insert_textbox(fitz.Rect(50, 370, 550, 550), ref_text, fontsize=10)
    
    doc.save(dest_path)
    doc.close()
    print(f"Sample PDF created at {dest_path}")

if __name__ == "__main__":
    dest = Path(__file__).parent.parent / "data" / "sample_paper.pdf"
    dest.parent.mkdir(exist_ok=True, parents=True)
    create_sample_pdf(str(dest))
