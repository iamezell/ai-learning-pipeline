# OCR Confidence Calibration and Human Review Headcount

> **Why I captured this:** I need to explain to a Director why confidence calibration drives our human-review headcount at 200M pages a year

## Before You Start — Try These First

- If your OCR returns a confidence score of 72% on a extracted invoice total, what information do you need to decide whether that invoice goes to a human reviewer or straight into your accounting system?
- At 200 million pages per year, if lowering your confidence threshold from 95% to 90% cuts human review by 30%, what question must you ask before making that change?
- Why would two documents with identical OCR accuracy (e.g., 95% correct extractions) require different human-review headcounts?

## Learning Objectives

- This source does NOT address confidence calibration or how OCR accuracy drives human-review staffing decisions. The learner needs material on false positive rates, confidence thresholds, precision-recall trade-offs, and cost modeling for review workflows — none of which appear here. What IS here: OCR definition, industry uses, AWS services, and a brief technology overview. Use this only to establish shared vocabulary (OCR vs ICR) before seeking sources on calibration and QA pipeline design.

## Discrimination

- You need to pull handwritten dollar amounts off scanned expense forms and route uncertain extractions to a reviewer. Why is simple pattern-matching OCR insufficient and what does ICR add? >> Pattern-matching OCR requires exact font matches stored in a database — it cannot handle the unlimited variation in handwriting styles. ICR uses neural networks to learn features (curves, line direction, loops) and generalize across handwriting, producing usable extractions with associated confidence scores. *(key difference: Ability to generalize beyond stored font templates to handle varied handwriting and layouts.)*
- You have 50,000 invoices to process. One vendor always uses the same template and prints clearly; another submits photos of handwritten receipts. Both go through the same OCR engine. Why would the second vendor drive most of your review queue even if page counts are equal? >> Handwritten receipts and inconsistent layouts produce lower confidence scores than clean, templated invoices. Lower confidence triggers human review. Equal page counts do not mean equal review workload — document quality and structure determine confidence distributions and thus review volume. *(key difference: Confidence score distribution, which determines what proportion of documents require human verification.)*
- Amazon Textract can extract text from a scanned contract OR identify tables and key-value pairs in a structured form. If you are deciding review headcount for 200M pages, why does document type matter more than total page count? >> Structured forms with tables and key-value pairs have predictable layouts, yielding higher confidence and less review. Contracts with dense paragraphs, footnotes, and varied formatting produce more low-confidence extractions. Headcount is driven by the volume of uncertain extractions, not raw pages. *(key difference: Layout predictability, which affects OCR confidence and the proportion of pages needing human review.)*

## Scenario Cards

- Your finance team scans 200M pages of invoices yearly. Textract flags 18% as low-confidence (below 85%). A Director asks why you cannot just accept all extractions and skip review. What do you tell them? >> Low-confidence extractions have a higher error rate. Accepting them without review means incorrect amounts flow into accounting, causing payment errors, reconciliation failures, and compliance risk. The 18% review rate exists because those extractions are uncertain — skipping review trades headcount savings for financial accuracy and auditability.
- You are piloting two OCR vendors. Vendor A averages 92% confidence; Vendor B averages 88%. Your review threshold is 90%. A Director asks why the 4-point difference matters. What is your answer? >> Vendor B puts far more pages below the 90% threshold, dramatically increasing review volume. If 200M pages × 4% extra low-confidence items = 8M additional pages for human review. At realistic review rates, that is hundreds of FTEs. The confidence distribution, not the average, determines headcount.
- Your team reviews 30M pages annually (15% of 200M total). Leadership wants to cut review headcount by 30%. You can lower the confidence threshold from 92% to 87%, but error rates will rise. What trade-off do you surface? >> Lowering the threshold reduces pages sent to review, cutting headcount. But more errors pass through: incorrect invoice amounts, misread account numbers, wrong vendor names. You need to quantify the cost of those errors (rework, payment disputes, compliance issues) versus salary savings, then let leadership choose the acceptable error rate.
- A new regulation requires 98% accuracy on medical claim forms. Your current OCR + review pipeline delivers 96%. How does this change your review headcount and what is the mechanism? >> You must tighten the confidence threshold to catch more uncertain extractions before they become errors. This increases the percentage of claims routed to human review, directly increasing headcount. The mechanism: higher accuracy requirements mean lower tolerance for OCR uncertainty, so more items cross the review threshold.

## Concept Cards

- You scan 1,000 invoices. What property of the resulting image files prevents your accounting software from totaling the amounts automatically? >> The text is embedded in image pixels, not stored as text data. Software cannot read, search, or process text that exists only as visual patterns in an image file.
- Amazon Textract returns a confidence score with every extraction. What does a confidence score of 68% tell you? >> Textract estimates a 68% probability that the extraction is correct. It is flagging uncertainty — this item is a candidate for human review depending on your accuracy requirements and error tolerance.
- Your preprocessing step deskews a tilted scan and despeckles noise. Why does this matter for downstream costs? >> Cleaner images yield higher OCR confidence scores and fewer extraction errors, which reduces the volume of low-confidence items routed to human reviewers — directly cutting headcount.
- A scanned form has handwritten amounts in one field and printed text elsewhere. Why might you get different confidence scores across fields? >> ICR handles handwriting but with more uncertainty than printed text. Handwritten fields typically return lower confidence scores, even when correctly extracted, because variability in script is inherent.

## Cloze

- Amazon Textract returns a {{c1::confidence score}} for everything it identifies so that you can make informed decisions about how you want to use the results.
- At 200 million pages per year, even small shifts in {{c1::confidence thresholds}} or document quality can change human-review headcount by thousands of hours.
- OCR converts an image of text into {{c1::machine-readable text data}}, but text embedded in image files cannot be processed by word processing software in the same way as text documents.
- ICR uses {{c1::neural networks}} to analyze text over many levels, processing the image repeatedly and looking for curves, lines, intersections, and loops to get the final result.

## Recall Cards

- What does ICR stand for and how does it differ from simple OCR? >> Intelligent Character Recognition. ICR uses neural networks to recognize text like humans do (analyzing curves, lines, intersections), while simple OCR relies on pattern-matching against stored font templates.

## Multiple Choice

- Your OCR system processes 200M pages yearly with a 90% confidence threshold for review. Improving preprocessing (better deskewing, despeckling) shifts the average confidence from 89% to 91%. What is the primary impact?
    - A. Accuracy improves but review headcount stays the same because the threshold is unchanged
    - B. Fewer pages fall below the 90% threshold, reducing human-review volume
    - C. Processing speed doubles because cleaner images are faster to read
    - D. The system can now handle handwritten forms that were previously rejected
    - >> B. Fewer pages fall below the 90% threshold, reducing human-review volume
        - Shifting average confidence from 89% to 91% moves a significant portion of the distribution above the 90% review threshold. Fewer low-confidence extractions mean fewer pages sent to reviewers, directly cutting headcount. The threshold itself has not changed, but the proportion of pages below it has dropped.
- Amazon Textract extracts text from a scanned invoice and returns a confidence score of 74% on the total amount. What does this score represent?
    - A. Textract processed the image in 74% of the expected time
    - B. There is a 74% probability that the extraction matches the actual text in the image
    - C. 74% of the characters in that field were recognized correctly
    - D. The image quality was rated 74 out of 100
    - >> B. There is a 74% probability that the extraction matches the actual text in the image
        - A confidence score is a probability estimate. 74% means Textract is moderately uncertain — it is flagging this extraction as a candidate for human review. It does NOT mean 74% of characters are correct (you could have 100% wrong at 74% confidence if the model is miscalibrated).
- You are explaining to a Director why 200M pages require different review headcounts depending on document type. Two datasets have identical OCR accuracy (94% correct extractions). Why might one require 3× the review hours?
    - A. One dataset has a narrower confidence distribution, putting more pages near the review threshold
    - B. One dataset includes more pages, so even at the same percentage, absolute volume is higher
    - C. One dataset uses an older OCR engine with slower processing
    - D. One dataset comes from international sources requiring translation
    - >> A. One dataset has a narrower confidence distribution, putting more pages near the review threshold
        - Review headcount is driven by how many extractions fall below the confidence threshold, not by overall accuracy. A dataset with 94% accuracy but many scores clustered near the threshold (e.g., 85–92%) will send more items to review than one with 94% accuracy and scores concentrated at 98%. The shape of the confidence distribution, not the mean, determines review volume.
- Which OCR improvement would most directly reduce human-review headcount in a 200M-page-per-year workflow?
    - A. Support for 30 additional languages
    - B. Higher confidence scores on the same extractions (shifting the distribution upward)
    - C. Faster processing speed (10 pages/sec to 50 pages/sec)
    - D. Ability to extract tables as well as plain text
    - >> B. Higher confidence scores on the same extractions (shifting the distribution upward)
        - Higher confidence scores move more pages above the review threshold, directly reducing the volume sent to human reviewers. Speed, language support, and table extraction are valuable features but do not change what proportion of pages require manual verification.

## Teach Back

- Explain to a non-technical Director how confidence scores from an OCR system determine how many people you need to review 200 million pages a year. Walk through the mechanism step-by-step.
  - OCR extracts text from scanned images and assigns each extraction a confidence score (a probability it is correct)
  - You set a threshold — e.g., anything below 90% confidence goes to a human reviewer
  - The percentage of pages below that threshold × 200M pages = total pages needing review
  - Review capacity (pages per hour per person) converts that volume into headcount
  - Improving OCR quality (better preprocessing, better models) shifts confidence scores upward, fewer pages cross the threshold, headcount drops
  - Tightening accuracy requirements (regulatory compliance) forces a higher threshold, more pages need review, headcount rises

## Apply This Today

- [ ] Pull the last month of OCR confidence scores from your current system (or request sample data from your vendor). Plot the distribution. Pick three candidate review thresholds (e.g., 85%, 90%, 95%) and calculate how many pages per month would go to review at each level. Multiply by your team's average review rate (pages/hour) to estimate FTE impact. Write a one-paragraph summary of the trade-off between headcount and risk for each threshold. Time: 20 minutes.
- [ ] Draft a 3-sentence explanation of why 'OCR accuracy' and 'review headcount' are not the same thing, using a concrete example with two datasets at 94% accuracy but different confidence distributions. Test it on a non-technical colleague. Revise based on their confusion points. This is your opening when the Director asks why vendor A costs less but requires more reviewers. Time: 15 minutes.