from anthropic import Anthropic
import re
from typing import Dict, Tuple, Optional
import json


class AISolver:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"

    async def solve_mcq(
        self,
        question: str,
        options: Dict[str, str],
        context: Optional[str] = None
    ) -> Tuple[str, str, float]:
        """
        Solve MCQ and return (answer, explanation, confidence)

        Args:
            question: The question text
            options: Dict mapping option letters to option text (e.g., {"A": "Option 1", "B": "Option 2"})
            context: Optional additional context or course material

        Returns:
            Tuple of (answer_letter, explanation, confidence_score)
        """
        options_text = "\n".join([f"{k}) {v}" for k, v in options.items()])

        prompt = f"""Question: {question}

Options:
{options_text}

{f'Additional Context:\n{context}\n' if context else ''}
Analyze this question step by step and provide:
1. Your reasoning (brief and clear)
2. The correct answer (ONLY the letter: {', '.join(options.keys())})
3. Your confidence level (0.0 to 1.0)

Format your response exactly as:
Reasoning: <your detailed analysis>
Answer: <letter>
Confidence: <0.0-1.0>
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text

        # Extract answer
        answer_match = re.search(r'Answer:\s*([A-Z])', text, re.IGNORECASE)
        answer = answer_match.group(1).upper() if answer_match else list(options.keys())[0]

        # Validate answer is in options
        if answer not in options:
            answer = list(options.keys())[0]

        # Extract reasoning
        reasoning_match = re.search(r'Reasoning:\s*(.+?)(?=Answer:|Confidence:|$)', text, re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "Unable to extract reasoning"

        # Extract confidence
        confidence_match = re.search(r'Confidence:\s*([0-9.]+)', text)
        confidence = float(confidence_match.group(1)) if confidence_match else 0.7
        confidence = max(0.0, min(1.0, confidence))  # Clamp between 0 and 1

        return answer, reasoning, confidence

    async def solve_coding(
        self,
        problem: str,
        test_cases: Optional[str] = None,
        constraints: Optional[str] = None,
        language: str = "python"
    ) -> str:
        """
        Generate code solution

        Args:
            problem: Problem description
            test_cases: Optional test cases examples
            constraints: Optional constraints and requirements
            language: Programming language (default: python)

        Returns:
            Complete working code solution
        """
        prompt = f"""Problem: {problem}

{f'Test Cases:\n{test_cases}\n' if test_cases else ''}
{f'Constraints:\n{constraints}\n' if constraints else ''}

Write a complete, working solution in {language}.

Requirements:
- Handle all edge cases
- Optimize for time and space complexity
- Use clean, readable code with proper variable names
- Include proper input/output handling
- Add comments for complex logic
- ONLY output the code, no explanations before or after

Code:"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )

        code = response.content[0].text.strip()

        # Remove markdown code blocks if present
        code = re.sub(r'^```[a-z]*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```$', '', code)
        code = code.strip()

        return code

    async def solve_frontend(
        self,
        requirements: str,
        reference_image: Optional[str] = None
    ) -> Tuple[str, str, str]:
        """
        Generate HTML, CSS, JS solution

        Args:
            requirements: Feature requirements and description
            reference_image: Optional base64 encoded reference image

        Returns:
            Tuple of (html, css, javascript)
        """
        prompt = f"""Create a complete front-end solution for:

{requirements}

{f'Reference Image: {reference_image[:100]}...' if reference_image else ''}

Provide three separate code sections:
1. HTML code (semantic, accessible)
2. CSS code (modern, responsive)
3. JavaScript code (vanilla JS, if needed)

Requirements:
- Use modern CSS (flexbox/grid)
- Make it responsive
- Add smooth animations/transitions
- Ensure cross-browser compatibility
- Use semantic HTML

Format your response exactly as:
HTML:
<your complete html>

CSS:
<your complete css>

JAVASCRIPT:
<your complete javascript or leave empty if not needed>
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text

        # Extract HTML
        html_match = re.search(r'HTML:\s*(.+?)(?=CSS:|$)', text, re.DOTALL | re.IGNORECASE)
        html = html_match.group(1).strip() if html_match else ""
        html = re.sub(r'^```html\n|^```\n|```$', '', html, flags=re.MULTILINE).strip()

        # Extract CSS
        css_match = re.search(r'CSS:\s*(.+?)(?=JAVASCRIPT:|$)', text, re.DOTALL | re.IGNORECASE)
        css = css_match.group(1).strip() if css_match else ""
        css = re.sub(r'^```css\n|^```\n|```$', '', css, flags=re.MULTILINE).strip()

        # Extract JS
        js_match = re.search(r'JAVASCRIPT:\s*(.+?)$', text, re.DOTALL | re.IGNORECASE)
        js = js_match.group(1).strip() if js_match else ""
        js = re.sub(r'^```javascript\n|^```js\n|^```\n|```$', '', js, flags=re.MULTILINE).strip()

        return html, css, js

    async def analyze_code_error(self, code: str, error: str, language: str = "python") -> str:
        """
        Analyze code error and suggest fix

        Args:
            code: The code with error
            error: Error message
            language: Programming language

        Returns:
            Fixed code
        """
        prompt = f"""Fix this {language} code that has an error:

Code:
{code}

Error:
{error}

Provide the corrected code. ONLY output the fixed code, no explanations.

Fixed Code:"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        fixed_code = response.content[0].text.strip()
        fixed_code = re.sub(r'^```[a-z]*\n', '', fixed_code, flags=re.MULTILINE)
        fixed_code = re.sub(r'\n```$', '', fixed_code)

        return fixed_code.strip()
