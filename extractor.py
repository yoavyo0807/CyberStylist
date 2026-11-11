from collections import Counter
import numpy as np
import spacy

# Spacy model upload
nlp = spacy.load("en_core_web_sm")

# Function word list
FUNCTION_WORDS = set([
    "the", "a", "an", "in", "on", "at", "by", "for", "with", "about", "against", 
    "between", "into", "through", "during", "before", "after", "above", "below",
    "to", "from", "up", "upon", "down", "out", "off", "over", "under", "and",
    "but", "or", "nor", "so", "yet", "both", "either", "neither", "not", "only",
    "that", "which", "who", "whom", "this", "these", "it", "its", "they", "them", "their"
])

class AdvancedStylometricExtractor:
    def __init__(self, text: str):
        self.text = text
        self.doc = nlp(text)
    
    def extract_l1_linguistic_markers(self) -> dict:
        '''
        Function that extract native language features from English text to identify native language
        '''
        words = [token.text.lower() for token in self.doc if token.is_alpha]
        total_words = len(words) if words else 1
        
        # Determiners omission rater (Typical for Russian/Slavic native speaker)
        articles_count = sum(1 for w in words if w in ["a", "an", "the"])
        article_ratio = articles_count / total_words
        
        "Over-coordination rater (Typical with Farsi native speakers)"
        coord_conj_count = sum(1 for token in self.doc if token.dep_ == "cc" or token.text.lower() in ["and", "that"])
        coordination_ratio = coord_conj_count / total_words
        
        # Pronoun redundancy (Typical with Farsi native speakers)
        pronoun_redundancy = 0
        tokens = list(self.doc)
        for i in range(len(tokens) - 1):
            if tokens[i].pos_ == "NOUN" and tokens[i+1].pos_ == "PRON":
                pronoun_redundancy += 1
        pronoun_redundancy_ratio = pronoun_redundancy / total_words
        
        return {
            "article_ratio": article_ratio,                 # Low rate identify Russian/Slavic speaker
            "coordination_ratio": coordination_ratio,       # High rate identify Farsi speaker
            "pronoun_redundancy": pronoun_redundancy_ratio  # High rate identify Farsi speaker
        }        
        
    def extract_structural_metrics(self) -> dict:
        sentences = list(self.doc.sents)
        words = [token for token in self.doc if token.is_alpha]
        avg_sent_len = np.mean([len(s) for s in sentences]) if sentences else 0
        avg_word_len = np.mean([len(w.text) for w in words]) if words else 0
        punct_count = sum(1 for token in self.doc if token.is_punct)
        punct_ratio = punct_count / (len(self.doc) if len(self.doc) else 1)
        
        return {
            "avg_sent_len": avg_sent_len,
            "avg_word_len": avg_word_len,
            "punct_ratio": punct_ratio
        }
    
    def get_profile(self) -> dict:
        profile = {}
        profile.update(self.extract_l1_linguistic_markers())
        profile.update(self.extract_structural_metrics())
        return profile