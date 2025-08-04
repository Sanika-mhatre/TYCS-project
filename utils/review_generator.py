import random
from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime


class ReviewGenerator:
    """Generates comprehensive academic paper reviews."""
    
    def __init__(self):
        # Review templates for different styles
        self.review_templates = {
            'Academic Conference': {
                'intro': "This paper presents {subject} and proposes {contribution}. The review evaluates the work based on conference standards for novelty, technical quality, and clarity.",
                'structure': "conference paper format",
                'criteria_weights': {'novelty': 0.3, 'methodology': 0.25, 'clarity': 0.25, 'significance': 0.2}
            },
            'Journal Review': {
                'intro': "This manuscript investigates {subject} and contributes {contribution}. The review assesses the work according to journal standards for originality, rigor, and impact.",
                'structure': "journal article format",
                'criteria_weights': {'novelty': 0.25, 'methodology': 0.3, 'clarity': 0.2, 'significance': 0.25}
            },
            'Thesis Defense': {
                'intro': "This thesis explores {subject} and demonstrates {contribution}. The evaluation focuses on the depth of research, methodological rigor, and contribution to the field.",
                'structure': "thesis format",
                'criteria_weights': {'novelty': 0.2, 'methodology': 0.4, 'clarity': 0.2, 'significance': 0.2}
            },
            'Peer Review': {
                'intro': "This work addresses {subject} and claims {contribution}. The peer review examines the validity, clarity, and relevance of the research.",
                'structure': "research paper format",
                'criteria_weights': {'novelty': 0.25, 'methodology': 0.3, 'clarity': 0.25, 'significance': 0.2}
            }
        }
        
        # Strength and weakness templates
        self.strength_patterns = {
            'high_novelty': [
                "The paper presents a novel approach to {topic}",
                "The research addresses an important gap in {field}",
                "The proposed method is innovative and well-motivated",
                "The work introduces original concepts that advance the field"
            ],
            'strong_methodology': [
                "The methodology is rigorous and well-designed",
                "The experimental setup is comprehensive and appropriate",
                "The authors employ sound research methods",
                "The approach is methodologically robust"
            ],
            'clear_presentation': [
                "The paper is well-written and clearly structured",
                "The presentation is clear and easy to follow",
                "The writing quality is high with good organization",
                "The paper effectively communicates its contributions"
            ],
            'significant_impact': [
                "The work has clear practical implications",
                "The results demonstrate significant improvements",
                "The findings contribute meaningfully to the field",
                "The research addresses an important problem"
            ]
        }
        
        self.weakness_patterns = {
            'low_novelty': [
                "The novelty of the approach is limited",
                "The contribution appears incremental",
                "Similar approaches have been explored previously",
                "The innovation over existing work is unclear"
            ],
            'weak_methodology': [
                "The methodology lacks sufficient detail",
                "The experimental design has notable limitations",
                "The evaluation could be more comprehensive",
                "The validation is insufficient for the claims made"
            ],
            'unclear_presentation': [
                "The presentation could be clearer in several areas",
                "Some sections are difficult to follow",
                "The writing quality needs improvement",
                "The organization could be better structured"
            ],
            'limited_significance': [
                "The practical impact is not clearly demonstrated",
                "The significance of the results is unclear",
                "The broader implications need better articulation",
                "The relevance to the field could be stronger"
            ]
        }
    
    def generate_review(self, paper_text: str, criteria: Dict[str, int], 
                       review_type: str, analysis_results: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive review of the paper.
        
        Args:
            paper_text: Full text of the paper
            criteria: Dictionary with criterion weights (1-10 scale)
            review_type: Type of review to generate
            analysis_results: Results from text analysis
            
        Returns:
            Dictionary containing the complete review
        """
        # Extract key information
        paper_info = self._extract_paper_info(paper_text)
        
        # Calculate scores
        scores = self._calculate_scores(paper_text, criteria, analysis_results)
        
        # Generate overall assessment
        overall_score = self._calculate_overall_score(scores, criteria)
        recommendation = self._get_recommendation(overall_score)
        
        # Generate review content
        strengths = self._generate_strengths(scores, analysis_results)
        weaknesses = self._generate_weaknesses(scores, analysis_results)
        suggestions = self._generate_suggestions(scores, analysis_results)
        detailed_comments = self._generate_detailed_comments(paper_text, analysis_results, review_type)
        
        return {
            'overall_score': overall_score,
            'recommendation': recommendation,
            'detailed_scores': scores,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions,
            'detailed_comments': detailed_comments,
            'review_type': review_type,
            'review_date': datetime.now().strftime("%Y-%m-%d"),
            'summary': self._generate_summary(paper_info, overall_score, recommendation)
        }
    
    def _extract_paper_info(self, text: str) -> Dict[str, str]:
        """Extract basic information about the paper."""
        # Simple heuristics to extract paper information
        lines = text.split('\n')
        
        # Try to find title (usually in first few lines)
        title = "Research Paper"
        for line in lines[:10]:
            if len(line.split()) > 3 and len(line) < 200:
                title = line.strip()
                break
        
        # Estimate subject and contribution
        subject = "the research topic"
        contribution = "novel insights"
        
        # Look for common academic patterns
        if "machine learning" in text.lower() or "artificial intelligence" in text.lower():
            subject = "machine learning and AI applications"
        elif "deep learning" in text.lower() or "neural network" in text.lower():
            subject = "deep learning methodologies"
        elif "natural language" in text.lower() or "nlp" in text.lower():
            subject = "natural language processing"
        elif "computer vision" in text.lower() or "image" in text.lower():
            subject = "computer vision techniques"
        
        if "novel" in text.lower() or "new" in text.lower():
            contribution = "novel methodological contributions"
        elif "improve" in text.lower() or "better" in text.lower():
            contribution = "performance improvements"
        elif "framework" in text.lower() or "system" in text.lower():
            contribution = "systematic framework development"
        
        return {
            'title': title,
            'subject': subject,
            'contribution': contribution
        }
    
    def _calculate_scores(self, text: str, criteria: Dict[str, int], 
                         analysis_results: Optional[Dict] = None) -> Dict[str, float]:
        """Calculate scores for each review criterion."""
        scores = {}
        
        # Base scores from criteria weights (convert from 1-10 to 0-10 scale)
        base_scores = {k: v for k, v in criteria.items()}
        
        # Adjust based on analysis results if available
        if analysis_results:
            # Adjust novelty based on keyword analysis
            if 'keywords' in analysis_results:
                novelty_score = base_scores.get('novelty', 7)
                keyword_coverage = analysis_results['keywords'].get('academic_keyword_coverage', 0)
                novelty_adjustment = (keyword_coverage / 5.0) * 2  # Max 2 point adjustment
                scores['novelty'] = min(10, max(1, novelty_score + novelty_adjustment - 1))
            
            # Adjust methodology based on structure
            if 'structure' in analysis_results:
                methodology_score = base_scores.get('methodology', 7)
                structure = analysis_results['structure']
                method_adjustment = 0
                if structure.get('has_methodology', False):
                    method_adjustment += 1
                if structure.get('has_results', False):
                    method_adjustment += 1
                scores['methodology'] = min(10, max(1, methodology_score + method_adjustment - 1))
            
            # Adjust clarity based on readability
            if 'readability' in analysis_results:
                clarity_score = base_scores.get('clarity', 7)
                flesch_score = analysis_results['readability'].get('flesch_score', 50)
                # Convert Flesch score to adjustment (-2 to +2)
                if flesch_score >= 60:
                    clarity_adjustment = (flesch_score - 60) / 20  # 0 to 2
                else:
                    clarity_adjustment = (flesch_score - 60) / 30  # -2 to 0
                scores['clarity'] = min(10, max(1, clarity_score + clarity_adjustment))
            
            # Adjust significance based on citations and academic quality
            if 'citations' in analysis_results and 'academic_quality' in analysis_results:
                significance_score = base_scores.get('significance', 7)
                citation_density = analysis_results['citations'].get('citation_density', 0.5)
                quality_scores = analysis_results['academic_quality']
                significance_adjustment = (citation_density - 0.5) * 2  # Baseline adjustment
                significance_adjustment += np.mean(list(quality_scores.values())) * 2  # Quality adjustment
                scores['significance'] = min(10, max(1, significance_score + significance_adjustment - 1))
        
        # Fill in any missing scores with base values
        for criterion in ['novelty', 'methodology', 'clarity', 'significance']:
            if criterion not in scores:
                scores[criterion] = base_scores.get(criterion, 7.0)
        
        return scores
    
    def _calculate_overall_score(self, scores: Dict[str, float], criteria: Dict[str, int]) -> float:
        """Calculate the overall weighted score."""
        total_weight = sum(criteria.values())
        weighted_sum = sum(scores[k] * criteria[k] for k in scores.keys() if k in criteria)
        return weighted_sum / total_weight if total_weight > 0 else 7.0
    
    def _get_recommendation(self, overall_score: float) -> str:
        """Determine recommendation based on overall score."""
        if overall_score >= 8.5:
            return "Accept"
        elif overall_score >= 7.0:
            return "Minor Revision"
        elif overall_score >= 5.5:
            return "Major Revision"
        else:
            return "Reject"
    
    def _generate_strengths(self, scores: Dict[str, float], 
                          analysis_results: Optional[Dict] = None) -> List[str]:
        """Generate list of paper strengths."""
        strengths = []
        
        # Add strengths based on high scores
        for criterion, score in scores.items():
            if score >= 8.0:
                if criterion == 'novelty':
                    strengths.append(random.choice(self.strength_patterns['high_novelty']).format(
                        topic="the research area", field="the field"
                    ))
                elif criterion == 'methodology':
                    strengths.append(random.choice(self.strength_patterns['strong_methodology']))
                elif criterion == 'clarity':
                    strengths.append(random.choice(self.strength_patterns['clear_presentation']))
                elif criterion == 'significance':
                    strengths.append(random.choice(self.strength_patterns['significant_impact']))
        
        # Add strengths based on analysis results
        if analysis_results:
            if 'readability' in analysis_results:
                flesch_score = analysis_results['readability'].get('flesch_score', 50)
                if flesch_score >= 70:
                    strengths.append("The paper demonstrates excellent readability and accessibility")
            
            if 'structure' in analysis_results:
                structure = analysis_results['structure']
                if structure.get('balance_score', 0) >= 0.8:
                    strengths.append("The paper is well-structured with balanced sections")
            
            if 'citations' in analysis_results:
                citation_density = analysis_results['citations'].get('citation_density', 0)
                if citation_density >= 1.0:
                    strengths.append("The work demonstrates comprehensive literature coverage")
        
        # Ensure at least 2 strengths
        if len(strengths) < 2:
            strengths.extend([
                "The research addresses a relevant problem in the field",
                "The paper makes a meaningful contribution to the literature"
            ])
        
        return strengths[:5]  # Limit to 5 strengths
    
    def _generate_weaknesses(self, scores: Dict[str, float], 
                           analysis_results: Optional[Dict] = None) -> List[str]:
        """Generate list of paper weaknesses."""
        weaknesses = []
        
        # Add weaknesses based on low scores
        for criterion, score in scores.items():
            if score <= 6.0:
                if criterion == 'novelty':
                    weaknesses.append(random.choice(self.weakness_patterns['low_novelty']))
                elif criterion == 'methodology':
                    weaknesses.append(random.choice(self.weakness_patterns['weak_methodology']))
                elif criterion == 'clarity':
                    weaknesses.append(random.choice(self.weakness_patterns['unclear_presentation']))
                elif criterion == 'significance':
                    weaknesses.append(random.choice(self.weakness_patterns['limited_significance']))
        
        # Add weaknesses based on analysis results
        if analysis_results:
            if 'readability' in analysis_results:
                flesch_score = analysis_results['readability'].get('flesch_score', 50)
                if flesch_score < 40:
                    weaknesses.append("The text complexity may hinder accessibility to broader audiences")
            
            if 'structure' in analysis_results:
                structure = analysis_results['structure']
                if not structure.get('has_methodology', True):
                    weaknesses.append("The methodology section needs strengthening or clarification")
                if structure.get('abstract_quality', 1.0) < 0.5:
                    weaknesses.append("The abstract could be more comprehensive and informative")
            
            if 'citations' in analysis_results:
                citation_density = analysis_results['citations'].get('citation_density', 1.0)
                if citation_density < 0.3:
                    weaknesses.append("The literature review could be more comprehensive")
        
        # Ensure at least 1 weakness for constructive feedback
        if len(weaknesses) == 0:
            weaknesses.append("Minor improvements in presentation could enhance the paper's impact")
        
        return weaknesses[:4]  # Limit to 4 weaknesses
    
    def _generate_suggestions(self, scores: Dict[str, float], 
                            analysis_results: Optional[Dict] = None) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        # Suggestions based on scores
        for criterion, score in scores.items():
            if score <= 7.0:
                if criterion == 'novelty':
                    suggestions.extend([
                        "Consider highlighting the novel aspects more prominently",
                        "Provide clearer differentiation from existing work"
                    ])
                elif criterion == 'methodology':
                    suggestions.extend([
                        "Expand the methodology section with more implementation details",
                        "Include additional validation or comparison studies"
                    ])
                elif criterion == 'clarity':
                    suggestions.extend([
                        "Improve the organization and flow of the paper",
                        "Add more explanatory text for complex concepts"
                    ])
                elif criterion == 'significance':
                    suggestions.extend([
                        "Better articulate the practical implications of the work",
                        "Discuss broader impact and future applications"
                    ])
        
        # Analysis-based suggestions
        if analysis_results:
            if 'readability' in analysis_results:
                avg_sentence_length = analysis_results['readability'].get('avg_sentence_length', 20)
                if avg_sentence_length > 25:
                    suggestions.append("Consider breaking down long sentences for improved readability")
            
            if 'keywords' in analysis_results:
                keyword_coverage = analysis_results['keywords'].get('academic_keyword_coverage', 5)
                if keyword_coverage < 3:
                    suggestions.append("Strengthen the use of domain-specific terminology")
        
        # General suggestions
        suggestions.extend([
            "Consider adding more visual aids (figures, tables) to support the narrative",
            "Strengthen the conclusion with clearer implications and future work directions"
        ])
        
        return list(set(suggestions))[:6]  # Remove duplicates and limit
    
    def _generate_detailed_comments(self, text: str, analysis_results: Optional[Dict], 
                                  review_type: str) -> str:
        """Generate detailed review comments."""
        paper_info = self._extract_paper_info(text)
        template = self.review_templates.get(review_type, self.review_templates['Peer Review'])
        
        intro = template['intro'].format(
            subject=paper_info['subject'],
            contribution=paper_info['contribution']
        )
        
        comments = [intro]
        
        # Structure comments
        comments.append(f"\n**Structure and Organization:**")
        if analysis_results and 'structure' in analysis_results:
            structure = analysis_results['structure']
            comments.append(f"The paper follows a {template['structure']} with {structure.get('total_sections', 'several')} main sections.")
            
            if structure.get('abstract_quality', 0.5) >= 0.7:
                comments.append("The abstract effectively summarizes the work.")
            else:
                comments.append("The abstract could benefit from better summarization of key contributions.")
        
        # Content comments
        comments.append(f"\n**Technical Content:**")
        if analysis_results:
            if 'academic_quality' in analysis_results:
                quality = analysis_results['academic_quality']
                if quality.get('methodology_rigor', 0.5) >= 0.6:
                    comments.append("The methodology demonstrates good rigor and systematic approach.")
                if quality.get('evidence_strength', 0.5) >= 0.6:
                    comments.append("The evidence presented supports the claims made.")
        
        # Presentation comments
        comments.append(f"\n**Presentation Quality:**")
        if analysis_results and 'readability' in analysis_results:
            readability = analysis_results['readability']
            grade_level = readability.get('grade_level', 'Graduate')
            comments.append(f"The writing is at {grade_level} level, which is appropriate for the target audience.")
        
        return '\n'.join(comments)
    
    def _generate_summary(self, paper_info: Dict[str, str], overall_score: float, 
                         recommendation: str) -> str:
        """Generate a brief review summary."""
        return f"This paper on {paper_info['subject']} receives an overall score of {overall_score:.1f}/10 " \
               f"with a recommendation of '{recommendation}'. The work shows {paper_info['contribution']} " \
               f"and demonstrates {'strong' if overall_score >= 7.5 else 'adequate' if overall_score >= 6.0 else 'limited'} " \
               f"quality across the evaluation criteria."