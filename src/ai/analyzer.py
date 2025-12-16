"""
AI-powered analysis engine for analyzing complaints and responses.
Uses LLM to extract key information, identify patterns, and recommend strategies.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.core.models import Complaint, Document, AIAnalysis, DocumentType
from config.settings import settings
import structlog

logger = structlog.get_logger(__name__)


class ComplaintAnalyzer:
    """AI-powered complaint analyzer."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the complaint analyzer.
        
        Args:
            api_key: OpenAI API key. If not provided, uses key from settings.
            model: Model to use. If not provided, uses model from settings.
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        
        if not self.api_key or self.api_key == "your-openai-api-key-here":
            raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY in your .env file.")
        
        self.llm = ChatOpenAI(
            model_name=self.model,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            openai_api_key=self.api_key
        )
    
    def analyze_complaint(
        self,
        complaint: Complaint,
        complaint_documents: List[Document],
        response_documents: List[Document]
    ) -> AIAnalysis:
        """
        Analyze a complaint and its associated documents.
        
        Args:
            complaint: The complaint to analyze
            complaint_documents: Documents related to the complaint
            response_documents: Response documents from licensee
            
        Returns:
            AIAnalysis object with findings and recommendations
        """
        logger.info("Starting AI analysis", complaint_id=complaint.id)
        
        # Prepare document summaries (in production, would extract text from documents)
        complaint_text = self._prepare_complaint_text(complaint, complaint_documents)
        response_text = self._prepare_response_text(response_documents)
        
        # Create analysis prompt
        analysis_prompt = self._create_analysis_prompt(complaint_text, response_text)
        
        # Get AI analysis
        response = self.llm.invoke(analysis_prompt)
        analysis_result = self._parse_analysis_response(response.content)
        
        # Create AIAnalysis object
        ai_analysis = AIAnalysis(
            complaint_id=complaint.id or "",
            analysis_date=datetime.utcnow(),
            key_findings=analysis_result.get("key_findings", []),
            recommended_strategies=analysis_result.get("recommended_strategies", []),
            risk_assessment=analysis_result.get("risk_assessment", {}),
            compliance_notes=analysis_result.get("compliance_notes", []),
            confidence_score=analysis_result.get("confidence_score", 0.0),
            model_version=self.model
        )
        
        logger.info("AI analysis complete", complaint_id=complaint.id)
        return ai_analysis
    
    def _prepare_complaint_text(
        self,
        complaint: Complaint,
        documents: List[Document]
    ) -> str:
        """Prepare complaint text for analysis."""
        text_parts = [
            f"Complaint Number: {complaint.complaint_number}",
            f"Received Date: {complaint.received_date}",
            f"Licensee: {complaint.licensee_name} (License: {complaint.licensee_license_number})",
            f"Description: {complaint.complaint_description}",
        ]
        
        if documents:
            text_parts.append(f"\nAssociated Documents: {len(documents)} document(s)")
            for doc in documents:
                text_parts.append(f"  - {doc.filename} ({doc.document_type})")
        
        return "\n".join(text_parts)
    
    def _prepare_response_text(self, documents: List[Document]) -> str:
        """Prepare response text for analysis."""
        if not documents:
            return "No response documents available."
        
        text_parts = [f"Response Documents: {len(documents)} document(s)"]
        for doc in documents:
            text_parts.append(f"  - {doc.filename} ({doc.document_type})")
            # In production, would extract and include actual document text
        
        return "\n".join(text_parts)
    
    def _create_analysis_prompt(self, complaint_text: str, response_text: str) -> List:
        """Create the analysis prompt for the LLM."""
        system_prompt = SystemMessage(content="""You are an expert investigator analyzing complaints against licensed professionals. 
Your role is to:
1. Identify key facts and allegations in the complaint
2. Analyze responses and evidence provided
3. Identify gaps in information
4. Recommend investigation strategies
5. Assess compliance risks
6. Note any HIPAA, 42 CFR Part 2, or state law considerations

Provide your analysis in a structured format with:
- Key findings (list of important facts and observations)
- Recommended information-gathering strategies (specific actions to take)
- Risk assessment (level of risk and factors)
- Compliance notes (regulatory considerations)

Be thorough, objective, and focus on actionable recommendations.""")
        
        human_prompt = HumanMessage(content=f"""Please analyze the following complaint investigation:

COMPLAINT INFORMATION:
{complaint_text}

RESPONSE INFORMATION:
{response_text}

Provide a comprehensive analysis in JSON format with the following structure:
{{
    "key_findings": ["finding1", "finding2", ...],
    "recommended_strategies": ["strategy1", "strategy2", ...],
    "risk_assessment": {{
        "level": "low|medium|high|critical",
        "factors": ["factor1", "factor2", ...],
        "urgency": "low|medium|high"
    }},
    "compliance_notes": ["note1", "note2", ...],
    "confidence_score": 0.0-1.0
}}""")
        
        return [system_prompt, human_prompt]
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response into structured data."""
        try:
            # Try to extract JSON from response
            # LLM responses may include markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                json_text = response_text.strip()
            
            # Remove leading/trailing whitespace and parse
            json_text = json_text.strip()
            if json_text.startswith("{"):
                return json.loads(json_text)
            else:
                # Fallback: try to find JSON object in text
                start = json_text.find("{")
                end = json_text.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(json_text[start:end])
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse JSON response", error=str(e))
        
        # Fallback: return structured default response
        return {
            "key_findings": ["Analysis completed. Review required."],
            "recommended_strategies": ["Conduct thorough investigation"],
            "risk_assessment": {
                "level": "medium",
                "factors": ["Requires manual review"],
                "urgency": "medium"
            },
            "compliance_notes": ["Ensure HIPAA compliance in investigation"],
            "confidence_score": 0.5
        }
    
    def recommend_investigation_strategies(
        self,
        complaint: Complaint,
        current_findings: List[str],
        available_evidence: List[Document]
    ) -> List[str]:
        """
        Recommend specific information-gathering strategies based on complaint analysis.
        
        Args:
            complaint: The complaint
            current_findings: Current findings from analysis
            available_evidence: Currently available evidence documents
            
        Returns:
            List of recommended investigation strategies
        """
        logger.info("Generating investigation strategies", complaint_id=complaint.id)
        
        prompt = f"""Based on the following complaint and current findings, recommend specific information-gathering strategies:

Complaint: {complaint.complaint_description}
Current Findings: {', '.join(current_findings)}
Available Evidence: {len(available_evidence)} document(s)

Provide a list of specific, actionable investigation strategies. Consider:
- What additional information is needed
- Who should be interviewed
- What documents should be requested
- What expert opinions might be needed
- Compliance and legal considerations

Return as a JSON array of strategy strings."""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            strategies_text = response.content
            if "```json" in strategies_text:
                json_start = strategies_text.find("```json") + 7
                json_end = strategies_text.find("```", json_start)
                strategies_text = strategies_text[json_start:json_end].strip()
            elif strategies_text.startswith("["):
                strategies_text = strategies_text.strip()
            
            strategies = json.loads(strategies_text)
            if isinstance(strategies, list):
                return strategies
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning("Failed to parse strategies", error=str(e))
        
        return ["Review all available documentation", "Conduct interviews with relevant parties"]

