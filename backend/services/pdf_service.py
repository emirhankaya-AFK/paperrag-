import re
import fitz  # PyMuPDF
from typing import Dict, List, Any, Tuple
from pathlib import Path

class PDFService:
    @staticmethod
    def extract_structured_text(pdf_path: str) -> Dict[str, Any]:
        """
        Extracts text from a PDF, detects multi-column layout, reconstructs sections,
        and extracts references from the bibliography.
        """
        doc = fitz.open(pdf_path)
        full_text = []
        pages_content = []
        
        for page_num, page in enumerate(doc):
            # Extract text blocks: (x0, y0, x1, y1, "text", block_no, block_type)
            blocks = page.get_text("blocks")
            
            # Sort blocks: first by column (left/right split if multi-column), then by y coordinate
            # Usually multi-column papers have standard margins. We check if blocks cluster in 2 columns.
            page_width = page.rect.width
            mid_x = page_width / 2
            
            left_col = []
            right_col = []
            single_col = []
            
            # Detect column layout: if many blocks fall purely on left or right, we treat it as 2-column
            is_two_column = False
            left_count = 0
            right_count = 0
            for b in blocks:
                x0, y0, x1, y1, text, block_no, block_type = b
                if x1 <= mid_x:
                    left_count += 1
                elif x0 >= mid_x:
                    right_count += 1
            
            if left_count > 2 and right_count > 2:
                is_two_column = True
                
            if is_two_column:
                for b in blocks:
                    x0, y0, x1, y1, text, block_no, block_type = b
                    if x1 <= mid_x + 10:
                        left_col.append(b)
                    elif x0 >= mid_x - 10:
                        right_col.append(b)
                    else:
                        # Spans both columns (e.g. title or wide figure)
                        single_col.append(b)
                
                # Sort each list by y coordinate
                left_col.sort(key=lambda x: x[1])
                right_col.sort(key=lambda x: x[1])
                single_col.sort(key=lambda x: x[1])
                
                # Reconstruct: title/top blocks first, then left col, then right col, then bottom blocks
                sorted_blocks = []
                # Simple rule: if single_col block is at the top of the page, put it first
                for sb in single_col:
                    if sb[1] < page.rect.height * 0.2:
                        sorted_blocks.append(sb)
                sorted_blocks.extend(left_col)
                sorted_blocks.extend(right_col)
                for sb in single_col:
                    if sb[1] >= page.rect.height * 0.2:
                        sorted_blocks.append(sb)
            else:
                # Single column: sort by y0, then x0
                sorted_blocks = sorted(blocks, key=lambda x: (x[1], x[0]))
            
            page_text_blocks = [b[4].strip() for b in sorted_blocks if b[4].strip()]
            page_text = "\n".join(page_text_blocks)
            full_text.append(page_text)
            pages_content.append({"page": page_num + 1, "text": page_text})
        
        complete_text = "\n\n".join(full_text)
        sections = PDFService._split_sections(complete_text)
        references = PDFService._extract_references(complete_text)
        
        return {
            "full_text": complete_text,
            "pages": pages_content,
            "sections": sections,
            "references": references
        }
        
    @staticmethod
    def _split_sections(text: str) -> Dict[str, str]:
        """
        Split the paper text into sections based on keywords.
        """
        section_patterns = {
            "abstract": [r"\babstract\b", r"\bsummary\b"],
            "introduction": [r"\bintroduction\b", r"\bbackground\b"],
            "methodology": [r"\bmethodology\b", r"\bmethods\b", r"\bexperimental\s+setup\b", r"\bproposed\s+approach\b"],
            "results": [r"\bresults\b", r"\bevaluation\b", r"\bexperiments\b", r"\bfindings\b"],
            "conclusion": [r"\bconclusion\b", r"\bconcluding\s+remarks\b", r"\bdiscussion\b"],
            "references": [r"\breferences\b", r"\bbibliography\b", r"\bliterature\s+cited\b"]
        }
        
        sections = {k: "" for k in section_patterns.keys()}
        sections["other"] = text
        
        # Build split regex
        headers = []
        for sec, patterns in section_patterns.items():
            for pat in patterns:
                headers.append((sec, pat))
                
        # Find matches for headers (case-insensitive)
        matches = []
        for sec, pat in headers:
            for match in re.finditer(pat, text, re.IGNORECASE):
                # Ensure the header matches a line/paragraph start or isolated text
                start, end = match.span()
                # Check surrounding text context to reduce false positives
                around = text[max(0, start-10):min(len(text), end+10)]
                # Typically headers are on their own lines or capitalized
                matches.append((start, end, sec))
                
        # Sort matches by start position
        matches.sort(key=lambda x: x[0])
        
        # Remove overlapping or redundant sub-matches
        filtered_matches = []
        last_end = -1
        for start, end, sec in matches:
            if start >= last_end:
                filtered_matches.append((start, end, sec))
                last_end = end
                
        # Slice text into sections
        if not filtered_matches:
            sections["other"] = text
            return sections
            
        for i in range(len(filtered_matches)):
            start, end, sec = filtered_matches[i]
            next_start = filtered_matches[i+1][0] if i + 1 < len(filtered_matches) else len(text)
            sections[sec] = text[end:next_start].strip()
            
        return sections

    @staticmethod
    def _extract_references(text: str) -> List[Dict[str, Any]]:
        """
        Extracts references from the end of the text.
        """
        # Look for references section
        ref_header_matches = list(re.finditer(r"\b(references|bibliography|literature\s+cited)\b", text, re.IGNORECASE))
        if not ref_header_matches:
            return []
            
        # Take the last occurrences of reference headers
        ref_start = ref_header_matches[-1].end()
        ref_section = text[ref_start:].strip()
        
        # Split references (often numbered like [1], [2], or author-year format)
        ref_items = []
        # Try numbering split
        parts = re.split(r"\[(\d+)\]", ref_section)
        if len(parts) > 2:
            for i in range(1, len(parts), 2):
                ref_num = parts[i]
                ref_content = parts[i+1].strip() if i+1 < len(parts) else ""
                ref_content = re.sub(r"\s+", " ", ref_content)
                if ref_content:
                    ref_items.append(PDFService._parse_reference_text(ref_content))
        else:
            # Fallback split on line breaks or bullet points
            lines = ref_section.split("\n")
            current_ref = ""
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # If looks like new reference (e.g. starts with author name or number)
                if re.match(r"^(\d+\.|\w+\,\s+\w\.)", line) and current_ref:
                    ref_items.append(PDFService._parse_reference_text(current_ref))
                    current_ref = line
                else:
                    current_ref += " " + line
            if current_ref:
                ref_items.append(PDFService._parse_reference_text(current_ref))
                
        return [item for item in ref_items if item]

    @staticmethod
    def _parse_reference_text(ref_text: str) -> Dict[str, Any]:
        """
        Heuristically extract title, authors, year from a reference string.
        """
        ref_text = ref_text.strip()
        # Find year
        year_match = re.search(r"\b(19\d{2}|20\d{2})\b", ref_text)
        year = int(year_match.group(0)) if year_match else None
        
        # Find authors (often up to first period or before title)
        authors = []
        title = ref_text
        
        # Simple extraction heuristic
        parts = ref_text.split(".")
        if len(parts) > 1:
            authors_part = parts[0].strip()
            # If it contains commas, likely author names
            if "," in authors_part:
                authors = [a.strip() for a in authors_part.split(",") if a.strip()]
            else:
                authors = [authors_part]
            title = parts[1].strip()
        
        return {
            "raw_text": ref_text,
            "title": title,
            "authors": authors,
            "year": year
        }
